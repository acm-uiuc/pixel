# Pixel

A 128x128 crowdsourced display.

Send a POST request to `pixel.acm.illinois.edu` with headers
- `x`: 0-127
- `y`: 0-127
- `color`: #FFFFFF or a supported [color string](https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm)

## Examples

curl

    curl -H "x: 0" -H "y: 0" -H "color: red" -X post pixel.acm.illinois.edu
    
python

``` python
import requests
requests.post('http://pixel.acm.illinois.edu', headers={'x': '0', 'y': '0', 'color': '#FF0000'})
```

    
