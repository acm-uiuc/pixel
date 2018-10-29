# Pixel

A 128x128 crowdsourced display.

## Examples

curl

    curl -H "x: 0" -H "y: 0" -H "color: #FF0000" -X post pixel.acm.illinois.edu
    
python

``` python
import requests
requests.post('http://pixel.acm.illinois.edu', headers={'x': '0', 'y': '0', 'color': '#FF0000'})
```

    
