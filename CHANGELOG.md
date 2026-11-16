# Changelog

## 2026-11-16

### Registry fixes

- Corrected dark/light tags: the six `-light` palettes (`one-light`,
  `gruvbox-light`, `solarized-light`, `ayu-light`, `everforest-light`,
  `papercolor-light`) are no longer tagged `dark`; `night-owl-light`,
  `catppuccin-latte`, `tokyo-night-day`, `kanagawa-lotus` and `rose-pine-dawn`
  are now tagged `light`; `nord` is tagged `dark`.
- Removed duplicate tags from the dark variants.
- Aligned `schema.json` with the layouts and palette styles accepted by the
  core: added `section-box`, `custom-x` and `right`, and dropped the
  unsupported `dots` palette style.
- Normalized the two themes that requested `palette_style: "dots"`
  (`catppuccin-mocha`, `paris`) to `squares`, which was already the effective
  rendering.
- `scripts/validate.py` now checks the registry index against `schema.json`,
  requires unique names and tags, rejects themes tagged both `dark` and
  `light`, validates layouts and palette styles, and verifies that every
  `colors/*.jsonc` file is listed and exists.

## 2026-08-19

### New Repository

- Themes moved out of `xfetch-cli/configs` into their own repository (`xfetch-cli/themes`), with independent versioning per theme via `index.json`. The registry URLs now point to this repository.
- All registry themes (`colors/*.jsonc`) dropped the `icons` block — icons are a per-user font choice, not theme identity (the core fills them from defaults; backward compatible).
- Each theme ships `logo_color` (its primary accent) so the ASCII logo is colored to match the palette.
