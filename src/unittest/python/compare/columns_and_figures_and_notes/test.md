---metadata
dirs_to_copy = ['images']
---endmetadata

---theme_slide_global
border = 2px solid black
---endtheme_slide_global

### Test Columns and Figures

Just a two columns for testing purpose

$columns

$column[width:45%;background:rgb(200,200,200);]
#### First column

$figure
$content[width:100%]{images/matisse-universe-no_bg.png}
$caption(Fig.)[font-style:oblique;]{A first figure}
$endfigure

$note
$style[font-size:110%]
$content[font-style:oblique;]{A first note}
$endnote

$column[width:55%;background:rgb(180,180,180);]
#### Second column

$figure
$content[width:100%]{images/matisse-universe-no_bg.png}
$caption(Fig.){A Second figure}
$endfigure

$note
$style[font-size:110%]
$content[font-style:oblique;]{A second note}
$endnote

$endcolumns
