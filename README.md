# Pixel

A 256x256 crowdsourced display.  Users can collaborate to draw images on the screen.  Only 2 updates allowed per IP per minute.

## Setting pixels with curl

Set pixels using curl.  <0, 0> corresponds to the top left corner.

    curl -H "x: 128" -H "y: 128" -H "color: #FF0000" -X post http://pixel.acm.illinois.edu
