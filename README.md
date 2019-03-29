# Pixel

<img src="photo.jpg" width=500>

A 128x128 crowdsourced display.

Send a POST request to `pixel.acm.illinois.edu` with data
- `x`: 0-127
- `y`: 0-127
- `color`: #FFFFFF or a supported [color string](https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm)

## Examples

curl

    curl -d "x=0&y=0&color=red" -X POST pixel.acm.illinois.edu
    
python

``` python
import requests
requests.post('http://pixel.acm.illinois.edu', data={'x': '0', 'y': '0', 'color': '#FF0000'})
```

    
