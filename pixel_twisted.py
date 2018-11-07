from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import logging
import tkinter as tk
import threading
from tkinter import *
import signal
master = Tk()

screen_width = 1280
screen_height = 1024

display_width = 128
display_height = 128

pixel_width = screen_width / display_width
pixel_height = screen_height / display_height

logging.basicConfig(level=logging.INFO, format='%(message)s')

class TkApp(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.w = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.w.pack()

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.mainloop()

class Page(Resource):
    isLeaf = True
    def render_POST(self, request):
        try:
            x = int(request.args[b'x'][0])
            y = int(request.args[b'y'][0])
            color = request.args[b'color'][0]

            tkapp.w.create_rectangle(
                x * pixel_width,
                y * pixel_height,
                x * pixel_width + pixel_width,
                y * pixel_height + pixel_height,
                fill=color,
                width=0
            )
        except Exception:
            return b"you suck\n"

        return b"success\n"

    def render_GET(self, request):
        print(request.getHeader('x'))
        return b'success\n'


tkapp = TkApp()

signal.signal(signal.SIGINT, signal.default_int_handler)
site = Site(Page())
reactor.listenTCP(8888, site)
reactor.run()
