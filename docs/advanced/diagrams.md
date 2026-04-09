# Diagrams

MaTiSSe supports two diagram engines rendered directly in the browser:

- **Mermaid** — flowcharts, sequence diagrams, Gantt charts, ER diagrams, and more
- **Graphviz / dot** — directed and undirected graphs via the `dot` language

Both use fenced code blocks with a special info string.  The required CDN scripts
are injected automatically into `index.html` — no extra configuration needed.

---

## Mermaid diagrams

### Syntax

````markdown
```{mermaid}
%%| fig-cap: "Optional caption"
flowchart LR
  A[Source] --> B{Parser} --> C[HTML]
```
````

The `%%| fig-cap:` line is optional.  It must be the **first** line of the block
if present, and is stripped before the diagram is rendered.

### Example: flowchart

````markdown
```{mermaid}
%%| fig-cap: "MaTiSSe build pipeline"
flowchart LR
  MD[Markdown source] --> P[Parser]
  P --> TH[Theme]
  P --> SL[Slides]
  TH --> R[Renderer]
  SL --> R
  R --> HTML[index.html]
```
````

### Example: sequence diagram

````markdown
```{mermaid}
%%| fig-cap: "Request / response sequence"
sequenceDiagram
  participant C as Client
  participant S as Server
  C->>S: GET /data
  S-->>C: 200 OK + JSON
```
````

### Example: Gantt chart

````markdown
```{mermaid}
gantt
  title Project schedule
  dateFormat YYYY-MM-DD
  section Phase 1
    Design :done, 2026-01-01, 2026-01-15
    Implementation :active, 2026-01-16, 2026-02-28
  section Phase 2
    Testing : 2026-03-01, 2026-03-20
```
````

Mermaid supports many diagram types — see the
[Mermaid documentation](https://mermaid.js.org/intro/) for the full syntax
reference.

---

## Graphviz / dot diagrams

### Syntax

````markdown
```{dot}
%%| fig-cap: "Optional caption"
digraph G {
  rankdir=LR;
  matisse -> parser;
  matisse -> theme;
  parser  -> slide;
  theme   -> slide;
}
```
````

The `%%| fig-cap:` line works the same way as for Mermaid.

### Example: dependency graph

````markdown
```{dot}
%%| fig-cap: "Module dependencies"
digraph modules {
  rankdir=TB;
  node [shape=box, style=filled, fillcolor="#e8f4fd"];
  presentation -> parser;
  presentation -> theme;
  presentation -> slide;
  slide        -> figure;
  slide        -> box;
  slide        -> table;
}
```
````

### Example: undirected graph

````markdown
```{dot}
graph network {
  node [shape=circle];
  A -- B;
  A -- C;
  B -- D;
  C -- D;
  D -- E;
}
```
````

Graphviz supports a rich attribute language — see the
[Graphviz documentation](https://graphviz.org/documentation/) for details.

---

## CDN scripts

MaTiSSe detects which engines are used and injects the required scripts at the
bottom of `index.html`.

### Mermaid

```html
<script type="module">
  import mermaid from
    'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>
```

Injected only when at least one ` ```{mermaid} ` block is present.

### Graphviz

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@hpcc-js/wasm-graphviz/dist/graphviz.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-graphviz@5/build/d3-graphviz.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.graphviz').forEach(function(el) {
      d3.select(el).graphviz().renderDot(el.textContent.trim());
    });
  });
</script>
```

Injected only when at least one ` ```{dot} ` block is present.

---

## HTML output

```html
<!-- Mermaid -->
<figure class="diagram diagram-mermaid" id="diagram-1">
  <pre class="mermaid">
flowchart LR
  A[Source] --> B{Parser} --> C[HTML]
  </pre>
  <figcaption>Build pipeline</figcaption>
</figure>

<!-- Graphviz -->
<figure class="diagram diagram-graphviz" id="diagram-2">
  <div class="graphviz">
digraph G { … }
  </div>
  <figcaption>Module dependencies</figcaption>
</figure>
```

### Styling via CSS

```css
/* custom.css */
.diagram        { margin: 1em auto; text-align: center; }
.diagram figcaption { font-size: 80%; font-style: italic; color: #666; }
.diagram-mermaid pre { background: transparent; border: none; }
```

Apply via `css_overtheme` in your metadata block:

```yaml
---
css_overtheme: ['custom.css']
---
```

---

## Offline mode

Mermaid and Graphviz CDN scripts are **not** bundled by `--offline`.  If you
need to present without internet access, download the scripts manually and
reference them via `css_overtheme` or a custom HTML snippet.

> **Syntax highlighting** (Pygments) is always local regardless of offline mode.
> Only diagram engines require a network connection.

---

## Cross-referencing diagrams

Use the `dia` prefix to cross-reference a diagram.  Add an id with
`{#dia-my-diagram}` after the caption line, or embed the id in a nearby label.

Diagrams are auto-numbered — `@dia-pipeline` resolves to **Diagram 1**, etc.
See [Theorems & Proofs](/advanced/theorems#cross-references) for the full
cross-reference syntax.

---

## See also

- [Math & LaTeX](/advanced/math) — MathJax-powered equations
- [Code Highlighting](/advanced/code) — Pygments-highlighted code blocks
- [Theorems & Proofs](/advanced/theorems) — numbered theorem environments
- [Offline Mode](/advanced/offline) — bundling assets for air-gapped venues
