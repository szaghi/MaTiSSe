# Metadata

Presentation metadata is defined in the first YAML block of the source file.

## Supported keys

```yaml
---
title:              My Talk
subtitle:           A Subtitle
authors:            ['Stefano Zaghi', 'John Doe']
authors_short:      ['S. Zaghi', 'J. Doe']
emails:             ['stefano.zaghi@cnr.it', 'jdoe@example.com']
affiliations:       ['CNR-INSEAN, Rome', 'Example University']
affiliations_short: ['CNR-INSEAN', 'Example U.']
location:           Rome, Italy
location_short:     Rome
date:               April 2026
conference:         My Conference 2026
conference_short:   MC2026
session:            Invited Talk
session_short:      Invited
logo:               images/logo.png
max_time:           25
dirs_to_copy:       ['images', 'data']
---
```

All keys are optional. String keys are plain values; keys marked with `[]` accept lists.

### Key descriptions

| Key | Type | Description |
|---|---|---|
| `title` | string | Presentation title |
| `subtitle` | string | Presentation subtitle |
| `authors` | list | Full author names |
| `authors_short` | list | Abbreviated author names (for headers/footers) |
| `emails` | list | Author email addresses |
| `affiliations` | list | Full affiliation names |
| `affiliations_short` | list | Abbreviated affiliation names |
| `location` | string | Venue location |
| `location_short` | string | Abbreviated location |
| `date` | string | Presentation date |
| `conference` | string | Conference name |
| `conference_short` | string | Abbreviated conference name |
| `session` | string | Session name |
| `session_short` | string | Abbreviated session name |
| `logo` | string | Path to a logo image (relative to source file) |
| `max_time` | integer | Presentation duration in minutes — drives the countdown timer |
| `dirs_to_copy` | list | Directories copied into the output directory (use for images, videos, etc.) |
| `css_overtheme` | list | Custom CSS files appended to the generated stylesheet |

### `max_time` and `dirs_to_copy`

`max_time` sets the countdown timer duration. If you include a timer widget in your theme it will count down from this value.

`dirs_to_copy` is essential when your presentation references files in subdirectories. MaTiSSe uses relative paths, so any directory containing images, videos, or data files must be listed here so it is copied alongside `index.html`:

```yaml
---
dirs_to_copy: ['images', 'videos', 'data']
---
```

### `css_overtheme` — custom CSS files

`css_overtheme` accepts a list of CSS file paths (relative to the source file).
Each file is copied into the output `css/` directory and linked from `index.html`.
Use it to override generated styles, style callouts and theorems, or add
presentation-specific CSS that would be awkward to express in the YAML theme:

```yaml
---
css_overtheme: ['custom.css']
---
```

Example `custom.css`:

```css
/* Style all theorem blocks with a subtle tint */
.theorem-thm  { background: rgba(74, 144, 217, 0.06); }
.theorem-def  { background: rgba(46, 139,  87, 0.06); }

/* Increase callout body font size */
.callout-body { font-size: 105%; }

/* Override Pygments code block border radius */
.highlight pre { border-radius: 6px; }
```

## Auto-generated metadata

These keys are computed automatically — you cannot set them, but you can use them anywhere:

| Key | Description |
|---|---|
| `toc` | Full table of contents (HTML) |
| `sectiontitle` | Title of the current section |
| `sectionnumber` | Number of the current section |
| `subsectiontitle` | Title of the current subsection |
| `subsectionnumber` | Number of the current subsection |
| `slidetitle` | Title of the current slide |
| `slidenumber` | Number of the current slide |
| `total_slides_number` | Total number of slides in the presentation |

## Interpolation in theme strings

Any metadata key becomes a `$key` placeholder in theme `content` strings:

```yaml
---
theme_slide_header_1:
  active:  True
  height:  10%
  content: "$title — $authors"

theme_slide_footer_1:
  active:  True
  height:  6%
  content: "$conference | $location | $date"
---
```

## Interpolation in slide content

Metadata can also be placed directly inside slide content using the `$key[style]` notation, where `[style]` is optional CSS:

```markdown
#### Title Slide

Welcome! My name is $authors[font-size:150%;color:#003366]

This talk runs for $max_time minutes.
```

## Multi-line values

Long list values can be broken across lines using the `&&` line-break marker:

```
authors = ['NERD Laboratory, The World Most Uncool Research Center', &&
            'LOST Institute, Missed People Research Institute']
```

## Title page

The `$titlepage` token generates a slide populated from metadata. A common pattern is to compose the title page with `$box` environments:

```markdown
$titlepage

$box
$style[width:100%;height:35%;background:#4788B3;]
$content[color:white;text-align:center;]{
$title[font-size:200%;padding-top:2%;]
$subtitle[font-size:120%;padding-top:2%;]
$logo[height:50px;]
}
$endbox

$box
$style[width:100%;]
$content[text-align:center;]{
a presentation by $authors[font-size:150%]
$emails[font-size:90%;]
$affiliations
}
$endbox

$box
$style[width:100%;padding-top:2%;]
$content[text-align:center;color:#4788B3;]{
$conference[font-size:150%;]
$session[font-size:120%;]
$location[font-size:90%;text-align:right;]
$date[font-size:90%;text-align:right;]
}
$endbox
```
