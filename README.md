# ACM@UIUC Pixel

<img src="photo.jpg" width=500>

A 128x128 crowd-sourced display.

# Endpoints

Base API URL: [http://pixel.acm.illinois.edu](http://pixel.acm.illinois.edu).

Rate Limit: 2 requests per minute.

## GET /

Redirects to the GitHub repository.

## POST /

Renders a pixel with specified pixel color, at the given x and y coordinates.

Request body:

```
{
    "x": 25,
    "y": 25,
    "color": "#FF0000"
}
```

Send a POST request to `pixel.acm.illinois.edu` with data

- `x`: 0-127
- `y`: 0-127
- `color`: #FFFFFF or a supported [color string](https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm).

## GET /screenshot/small.png/

Fetches a regular-sized screenshot of the Pixel display.

## GET /screenshot/regular.png/

Fetches a small-sized screenshot of the Pixel display.


## Examples

cURL
```
    curl -d "x=0&y=0&color=red" -X POST pixel.acm.illinois.edu
```

python

```python
import requests
requests.post('http://pixel.acm.illinois.edu', data={'x': '0', 'y': '0', 'color': '#FF0000'})
```
