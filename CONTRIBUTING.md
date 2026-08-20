<h1>Contributing Themes</h1>

<p>
  Thanks for contributing to the <strong>xfetch</strong> theme registry.
  Themes are partial JSONC configs: they declare only what they want to change
  (colors, logo color, layout, palette style) and the core merges them over the
  user's config.
</p>

<h2>Workflow</h2>

<ol>
  <li>Fork the repository and create a feature branch.</li>
  <li>Create the theme file at <code>colors/&lt;name&gt;.jsonc</code>.</li>
  <li>Add the matching entry to <code>index.json</code> (and extend <code>schema.json</code> only if you add a new field).</li>
  <li>
    Run the validation CI locally before opening the PR:
    <code>bash scripts/ci.sh</code> (Linux/macOS) or <code>./scripts/ci.ps1</code>
    (Windows). It parses <code>index.json</code> and every theme file.
  </li>
  <li>Test end-to-end: <code>xfetch theme set &lt;name&gt;</code> or install it with the <code>theme-manager</code> plugin.</li>
  <li>Add an entry to <a href="./CHANGELOG.md">CHANGELOG.md</a>.</li>
  <li>Open a pull request. PRs that fail validation are rejected.</li>
</ol>

<h2>Theme Rules</h2>

<ul>
  <li><strong>No <code>icons</code> block.</strong> Icons are a per-user font choice; the core fills them from defaults. A theme with <code>icons</code> is rejected.</li>
  <li>Only visual fields are allowed: <code>colors</code>, <code>logo_color</code>, <code>logo_colors</code>, <code>layout</code>, <code>palette_style</code>, <code>show_colors</code>, <code>header_icons</code>, <code>footer_text</code>, <code>logo_path</code>.</li>
  <li>Declare only what the theme changes — themes are merged over the user's config and must not set module lists or other non-visual keys.</li>
  <li>Color values use the supported names (<code>Black</code>–<code>White</code>, <code>Grey</code>/<code>Gray</code>, dark variants) — any module key works, including <code>plugin:&lt;name&gt;</code> entries.</li>
  <li><code>logo_color</code> is the theme's primary accent for the ASCII logo; <code>logo_colors</code> optionally colors the logo per row (array of colors, cycled by row).</li>
  <li>Use <code>tags</code> consistently (e.g. <code>dark</code>, <code>light</code>, <code>minimal</code>, <code>popular</code>) so <code>theme-manager</code> search keeps working.</li>
</ul>

<h2>The index entry (<code>index.json</code>)</h2>

<pre><code class="language-jsonc">{
    "name": "my-theme",
    "author": "you",
    "version": "1.0.0",
    "description": "One-line description for listings.",
    "layout": "section",           // optional; must be a valid layout name
    "palette_style": "circles",    // optional; squares | circles | triangles | lines
    "tags": ["dark", "minimal"],
    "source": "https://raw.githubusercontent.com/xfetch-cli/themes/main/colors/my-theme.jsonc"
}
</code></pre>

<p>
  The <code>source</code> URL must point at the theme file in this repository
  (<code>colors/&lt;name&gt;.jsonc</code>), and every index entry must have a
  matching file on disk.
</p>

<h2>Code of Conduct</h2>

<p>
  Be respectful, constructive, and collaborative. Harassment, trolling, and
  personal attacks are not tolerated.
</p>
