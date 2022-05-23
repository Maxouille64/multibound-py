import tkinter as tk
from tkinter import messagebox
from functools import partial
import os
import json

sb_dir = 'C:\General\Steam\steamapps\common\Starbound\win64'
instances = 'C:\Starbound MultiStorage'

class MyWindow(tk.Frame):

    def __init__(self,):

        super().__init__()
        self.master.title("minimal multibound")
        self.obj = None
        self.init_ui()

    def init_ui(self):

        self.pack(fill=tk.BOTH, expand=1,)

        w = tk.Frame()

        i=0
        for file in os.listdir(instances):
            d = os.path.join(instances, file)
            if os.path.isdir(d):
                button = (tk.Button(self, text=file, width=30, command=partial(self.on_button_clicked, d)))
                button.grid()
            i=+1

        tk.Button(w, text="browse", width=30, command=partial(self.open_dir, instances)).pack()
        tk.Button(w, text="Close", command=self.on_close).pack()
        w.pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)

    def on_close(self,evt=None):
        self.master.destroy()

    def open_dir(self, d):
        os.startfile(d)

    def on_button_clicked(self, data):
        os.chdir(sb_dir)
        with open(sb_dir + '\sbinit.config', 'r+') as f:
            jsn = json.load(f)
            jsn['assetDirectories'][1] = data + "/mods/" # <--- add `mods` value.
            jsn['storageDirectory'] = data + "/storage/" # <--- add `storage` value.
            f.seek(0)	# <--- should reset file position to the beginning.
            json.dump(jsn, f, indent=4)
            f.truncate()	# remove remaining part
        os.startfile('starbound.exe')

if __name__ == '__main__':
    MyWindow().mainloop()
