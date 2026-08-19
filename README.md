<div align="center">
  <img src="https://raw.githubusercontent.com/xfetch-cli/assets/main/logo/banner/xfetch.svg" width="30%" alt="XFetch banner" />
  <h1>Themes</h1>
  <p>The official theme registry for <strong>xfetch</strong>.</p>
</div>

Themes are partial JSONC configs: they declare only what they want to change
(colors, logo color, layout, palette style), and the core merges them over
your config. Icons are not part of themes — they are a per-user font choice.

<h2>Structure</h2>

<pre><code>themes/
├── index.json        # Registry index: metadata + source for every theme
├── schema.json       # JSON schema for the index
├── colors/           # The theme files themselves (*.jsonc)
├── README.md
└── CHANGELOG.md</code></pre>

<h2>How it works</h2>

<ol>
  <li>xfetch loads <code>"theme": "&lt;name&gt;"</code> from your config and merges the theme over the defaults.</li>
  <li><code>xfetch theme list|set|remove|export</code> manage installed themes locally.</li>
  <li>The <code>theme-manager</code> plugin (see <a href="https://github.com/xfetch-cli/plugins">xfetch-cli/plugins</a>) lists, searches, inspects and installs themes from this registry.</li>
</ol>

<h2>Registry index format</h2>

<pre><code class="language-jsonc">{
    "themes": [
        {
            "name": "dracula",
            "author": "xscriptor",
            "version": "1.0.0",
            "description": "Dark magenta, red, and cyan palette ...",
            "layout": "section",
            "palette_style": "circles",
            "tags": ["dark", "dracula", "popular"],
            "source": "https://raw.githubusercontent.com/xfetch-cli/themes/main/colors/dracula.jsonc"
        }
    ]
}</code></pre>

<h2>Adding a theme</h2>

<ol>
  <li>Create <code>colors/&lt;name&gt;.jsonc</code> with only the fields you want to change (<code>colors</code>, <code>logo_color</code>, <code>layout</code>, <code>palette_style</code>, <code>show_colors</code>, ...).</li>
  <li>Add an entry to <code>index.json</code> with the metadata above; tag it <code>dark</code> or <code>light</code> so users can pick for their terminal.</li>
  <li>Add a note in <code>CHANGELOG.md</code> and open a PR.</li>
</ol>

<h2>Theme file example</h2>

<pre><code class="language-jsonc">{
    "layout": "section",
    "show_colors": true,
    "palette_style": "circles",
    "logo_color": "Magenta",
    "colors": {
        "os": "Magenta",
        "cpu": "Red",
        "memory": "Yellow",
        "shell": "Green"
    }
}</code></pre>


<div id="about-the-developer" align="center">
<h2>X</h2>

<a href="https://dev.xscriptor.com">
  <img src="https://xscriptor.github.io/icons/icons/code/product-design/xsvg/verified-filled.svg" width="24" alt="X Web" />
</a>
 & 
<a href="https://github.com/xscriptor">
  <img src="https://xscriptor.github.io/icons/icons/code/product-design/xsvg/github.svg" width="24" alt="X Github Profile" />
</a>
 & 
<a href="https://www.xscriptor.com">
  <img src="https://xscriptor.github.io/icons/icons/code/product-design/xsvg/quotes.svg" width="24" alt="Xscriptor web" />
</a>

</div>
