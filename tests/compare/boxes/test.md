---
theme:
  - slide:
    - border: '2px solid black'
---

#### Test Box Class

##### Testing boxes

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".

$box
$style[background:rgb(200,200,200)]
$caption(GBox)[font-style:oblique;position:TOP;]{First box instance with caption in TOP}
$content[font-size:110%;]{This the first instance of Box class used for testing purpose

+ 1, lorem ipsum **cazzo**;
+ 2  sdfwe _ciao_;
+ 3

##### Test

**test**

```
test
```

*test*

}
$endbox

$box
$style[background:rgb(220,220,220);]
$caption(GBox)[font-style:oblique;position:BOTTOM;]{Second box instance with caption in BOTTOM}
$content[font-size:110%;]{This the second instance of Box class used for testing purpose}
$endbox
