# Changelog

## 2026-08-19

### New Repository

- Themes moved out of `xfetch-cli/configs` into their own repository (`xfetch-cli/themes`), with independent versioning per theme via `index.json`. The registry URLs now point to this repository.
- All registry themes (`colors/*.jsonc`) dropped the `icons` block — icons are a per-user font choice, not theme identity (the core fills them from defaults; backward compatible).
- Each theme ships `logo_color` (its primary accent) so the ASCII logo is colored to match the palette.
