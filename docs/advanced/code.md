# Code Highlighting

MaTiSSe.py uses [highlight.js 11](https://highlightjs.org/) for syntax highlighting.

## Fenced code blocks

Use standard Markdown fenced blocks with a language identifier:

````markdown
```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```
````

````markdown
```fortran
program hello
  implicit none
  print *, "Hello, World!"
end program hello
```
````

## Supported languages

highlight.js 11 supports over 190 languages automatically. Some common ones:

`python`, `fortran`, `c`, `cpp`, `bash`, `yaml`, `json`, `markdown`, `latex`, `matlab`, `r`, `julia`

## Choosing a style

List all available highlight.js styles:

```bash
MaTiSSe.py --print-highlight-styles
```

Specify a style in your metadata block:

```yaml
---
title: My Talk
highlight_style: github-dark
---
```

## Inline code

Standard Markdown backtick inline code is rendered without syntax highlighting:

```markdown
Use the `MaTiSSe.py` command to build your presentation.
```
