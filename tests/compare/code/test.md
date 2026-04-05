---
theme:
  layout:
    slide:
      border: '2px solid black'
  code:
    style: 'monokai'
    font-size: '85%'
---

#### Test Code Highlighting

##### Python code block

```python
def hello(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"

print(hello("world"))
```

##### Bash code block

```bash
#!/usr/bin/env bash
for f in *.md; do
    echo "Processing $f"
done
```

##### Plain (unannotated) code block

```
plain text, no language
no highlighting expected
```
