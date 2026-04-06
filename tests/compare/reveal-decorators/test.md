---
metadata:
  - title: Decorator Test
  - subtitle: Header/Footer/Sidebar for reveal
  - authors:
    - Test Author
  - conference: Test Conference 2026
---
---
reveal:
  theme: moon
  transition: slide
  plugins:
    - notes
---
---
theme:
  layout:
    header-1:
      height: 8%
      background: "#1a1a2e"
      color: white
      metadata:
        slidetitle:
          float: left
          font-size: 0.9em
        slidenumber:
          float: right
    footer-1:
      height: 4%
      background: "#1a1a2e"
      color: white
      metadata:
        conference:
          float: left
          font-size: 0.75em
---

# Chapter One

## Section One

### Sub One

#### First Slide

This slide has a header and footer.

#### Second Slide

---
overtheme:
  reveal:
    background_color: "#2c3e50"
  layout:
    header-1:
      height: 6%
      background: "#e74c3c"
      color: white
      metadata:
        slidetitle:
          float: left
---

This slide has a per-slide decorator override.

# Chapter Two

## Section Two

### Sub Two

#### Sidebar Slide

This is rendered with a sidebar layout.
