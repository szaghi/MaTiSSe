# Video

The `$video...$endvideo` environment embeds a video into a slide.

## Syntax

```markdown
$video
$style[width:70%;margin:auto]
$content[simulation.mp4]
$endvideo
```

## Options

| Tag | Description |
|---|---|
| `$style[...]` | CSS style applied to the video container |
| `$content[...]` | Path to the video file (relative to the source) or a URL |

## Supported formats

Any format supported by the browser's native `<video>` element: `mp4`, `webm`, `ogg`.

## Example — simulation result

```markdown
#### Flow Visualisation

$video
$style[width:80%;margin:auto;display:block]
$content[videos/cavity_flow.mp4]
$endvideo

Reynolds number $Re = 1000$, $512 \times 512$ grid.
```
