# ACM@UIUC Pixel

<img src="photo.jpg" width=500>

A 128x128 crowd-sourced display.

## Examples

curl
```
    curl -d "x=0&y=0&color=red" -X POST pixel.acm.illinois.edu
```

python

```python
import requests
requests.post('http://pixel.acm.illinois.edu', data={'x': '0', 'y': '0', 'color': '#FF0000'})
```

## Endpoints

#### POST /

Renders a pixel with specified pixel color, at the given x and y coordinates.

Request body:

- `x`: 0-127
- `y`: 0-127
- `color`: #FFFFFF or a supported [color string](https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm).

#### GET /small.bmp

Fetches a 128x128 screenshot of the Pixel display.

<!-- #### GET /screenshot/regular.png/ -->

<!-- Fetches a small-sized screenshot of the Pixel display. -->

