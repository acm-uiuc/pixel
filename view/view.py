import tkinter as tk
import threading
from tkinter import *

from config import constants


class TkApp(threading.Thread):
    """
    Separate thread for tkinter canvas
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.w = tk.Canvas(
            self.root, width=constants.screen_width, height=constants.screen_height)
        self.w.pack()

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.mainloop()


tkapp = TkApp()
