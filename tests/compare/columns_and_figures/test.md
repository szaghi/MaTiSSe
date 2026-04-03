---
theme:
  - slide:
    - border: '2px solid black'
---

---
metadata:
  - dirs_to_copy:
    - images
---

#### Test Columns and Figures

Just a two columns for testing purpose

$columns

$column[width:45%;background:rgb(200,200,200);]
##### First column

$figure
$content[width:100%]{images/matisse-universe-no_bg.png}
$caption(Fig.){A first figure}
$endfigure

$column[width:55%;background:rgb(180,180,180);]
##### Second column

$figure
$content[width:100%]{images/matisse-universe-no_bg.png}
$caption(Fig.){A Second figure}
$endfigure

$endcolumns
