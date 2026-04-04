# Code Highlighting

MaTiSSe uses [highlight.js 11](https://highlightjs.org/) for syntax highlighting.

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
matisse --print-highlight-styles
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
Use the `matisse` command to build your presentation.
```

## Note on indented code blocks

Original Markdown allows indenting by 4 spaces to create a code block. This form is **not fully supported** in MaTiSSe. Always use fenced code blocks (` ``` `) instead.
