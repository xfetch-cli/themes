#!/usr/bin/env python3
"""Validate JSONC/JSON files, the theme registry index and schema.

Strips // and /* */ comments and trailing commas, then parses. Exits
non-zero on the first broken file or registry inconsistency."""
import json
import re
import sys
from pathlib import Path

ALLOWED_THEME_KEYS = {
    "colors",
    "logo_color",
    "logo_colors",
    "layout",
    "palette_style",
    "show_colors",
    "header_icons",
    "footer_text",
    "logo_path",
}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def strip_jsonc(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    in_string = False
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def strip_trailing_commas(text: str) -> str:
    return re.sub(r",(\s*[}\]])", r"\1", text)


def load_jsonc(path: Path):
    return json.loads(strip_trailing_commas(strip_jsonc(path.read_text(encoding="utf-8"))))


def validate_registry(root: Path) -> list[str]:
    issues: list[str] = []
    index_path = root / "index.json"
    schema_path = root / "schema.json"
    colors_dir = root / "colors"

    if not index_path.exists():
        return [f"{index_path}: missing"]
    if not schema_path.exists():
        return [f"{schema_path}: missing"]

    try:
        index = load_jsonc(index_path)
        schema = load_jsonc(schema_path)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(index, dict):
        return [f"{index_path}: must contain a JSON object"]
    registry = index.get("registry")
    themes = index.get("themes")
    if not isinstance(registry, str) or not registry:
        issues.append("index.json: missing string 'registry'")
        registry = ""
    if not isinstance(themes, list):
        return issues + ["index.json: missing array 'themes'"]

    try:
        item = schema["properties"]["themes"]["items"]
        required = set(item["required"])
        props = item["properties"]
        layouts = set(props["layout"]["enum"])
        styles = set(props["palette_style"]["enum"])
    except (KeyError, TypeError):
        return issues + ["schema.json: unexpected structure"]

    registry_prefix = registry.rstrip("/") + "/" if registry else ""
    names: set[str] = set()
    for i, theme in enumerate(themes):
        where = f"index.json: themes[{i}]"
        if not isinstance(theme, dict):
            issues.append(f"{where}: must be an object")
            continue
        missing = sorted(required - set(theme))
        if missing:
            issues.append(f"{where}: missing keys {missing}")
            continue
        name = theme["name"]
        if not isinstance(name, str) or not name:
            issues.append(f"{where}: invalid name")
            continue
        if name in names:
            issues.append(f"{where}: duplicate name '{name}'")
            continue
        names.add(name)

        if not isinstance(theme["version"], str) or not VERSION_RE.match(theme["version"]):
            issues.append(f"{where}: version '{theme['version']}' is not semver")

        layout = theme.get("layout")
        if layout is not None and layout not in layouts:
            issues.append(f"{where}: unknown layout '{layout}'")
        style = theme.get("palette_style")
        if style is not None and style not in styles:
            issues.append(f"{where}: unknown palette_style '{style}'")

        tags = theme.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            issues.append(f"{where}: tags must be an array of strings")
        else:
            if len(tags) != len(set(tags)):
                issues.append(f"{where}: duplicate tags")
            if "dark" in tags and "light" in tags:
                issues.append(f"{where}: cannot be both dark and light")

        source = theme.get("source")
        expected = f"colors/{name}.jsonc"
        if not isinstance(source, str) or not source.endswith("/" + expected):
            issues.append(f"{where}: source must point at {expected}")
        elif registry_prefix and not source.startswith(registry_prefix):
            issues.append(f"{where}: source is outside the registry")
        if not (root / expected).exists():
            issues.append(f"{where}: missing file {expected}")

    actual = {p.stem for p in colors_dir.glob("*.jsonc")}
    if names != actual:
        for name in sorted(names - actual):
            issues.append(f"index.json: '{name}' has no colors/{name}.jsonc")
        for name in sorted(actual - names):
            issues.append(f"colors/{name}.jsonc is not listed in index.json")

    for path in sorted(colors_dir.glob("*.jsonc")):
        try:
            theme = load_jsonc(path)
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(theme, dict):
            issues.append(f"{path}: must contain a JSON object")
            continue
        extra = sorted(set(theme) - ALLOWED_THEME_KEYS)
        if extra:
            issues.append(f"{path}: unsupported keys {extra}")
        layout = theme.get("layout")
        if layout is not None and layout not in layouts:
            issues.append(f"{path}: unknown layout '{layout}'")
        style = theme.get("palette_style")
        if style is not None and style not in styles:
            issues.append(f"{path}: unknown palette_style '{style}'")

    return issues


def main() -> int:
    roots = [Path(p) for p in sys.argv[1:]] or [Path(".")]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        else:
            files.extend(root.rglob("*.jsonc"))
            files.extend(root.rglob("*.json"))
    files = sorted(f for f in files if ".git" not in f.parts)
    if not files:
        print("No JSON/JSONC files found.")
        return 1

    ok = True
    for f in files:
        try:
            load_jsonc(f)
        except json.JSONDecodeError as e:
            ok = False
            print(f"INVALID {f}: {e}")

    root = roots[0]
    if root.is_file():
        root = root.parent
    issues = validate_registry(root)
    for issue in issues:
        ok = False
        print(f"INVALID registry: {issue}")

    if ok:
        print(f"OK: {len(files)} JSON/JSONC files valid.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
