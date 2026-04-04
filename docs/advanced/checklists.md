# Checklists

MaTiSSe supports GitHub-flavored checklist lists, mirroring the syntax used on GitHub issues and pull requests.

## Requirement

Checklists require the optional Python package [`markdown-checklist`](https://pypi.org/project/markdown-checklist/):

```bash
pip install markdown-checklist
```

If the package is not installed the items are rendered as ordinary bullet lists without checkboxes.

## Syntax

Use `[ ]` for an unchecked item and `[x]` for a checked item:

```markdown
* [ ] Unchecked item
* [x] Checked item
* [ ] Another unchecked item
```

Rendered output:

* ☐ Unchecked item
* ☑ Checked item
* ☐ Another unchecked item

## Example in a slide

```markdown
#### Pre-flight checklist

* [x] Install matisse
* [x] Write source file
* [ ] Build presentation
* [ ] Review slides
* [ ] Deploy to GitHub Pages
```
