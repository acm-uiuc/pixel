import json
import logging
import struct
import os
from config.constants import BMP_PATH

MESSAGE_NO_ERROR = "N/A"
STATUS_SUCCESS = "SUCCESS"


def construct_response(status=STATUS_SUCCESS, message=MESSAGE_NO_ERROR):
    """
    Constructs a JSON response for endpoints with side-effects.
    """
    if message != MESSAGE_NO_ERROR:
        logging.log(logging.DEBUG, message)

    response = {
        "status": status,
        "messsage": message
    }

    return json.dumps(response)


# bmp header for 128x128 24bit image
bmp_header = b'BMz\xc0\x00\x00\x00\x00\x00\x00z\x00\x00\x00l\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\xc0\x00\x00#.\x00\x00#.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00BGRs\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def create_bmp():
    """Create output bmp if it doesn't exist"""

    if not os.path.exists(BMP_PATH):
        f = open(BMP_PATH, 'wb')
        f.write(bmp_header)
        # fill in with white
        f.write(b'\xff' * 128 * 128 * 3)
        f.close()


def write_bmp(x, y, r, g, b):
    """Write RGB value to position x (from left) and y (from top)"""

    f = open(BMP_PATH, 'r+b')

    # flip y coordinate from top to bottom
    y = 127 - y

    f.seek((128 * y + x) * 3 + len(bmp_header))
    for val in (b, g, r):
        f.write(struct.pack('B', val))
    f.close()
