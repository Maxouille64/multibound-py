import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from functools import partial
import os
import json
import sys


try:
    with open('config.json', 'r') as config:
        jsn = json.load(config)

except IOError:
    print('File not found, will create a new one.')
    jsn = {"sb_dir":"","instances":""}
    with open("config.json","w") as config:
        json.dump(jsn, config, indent=4)

with open("config.json","r+") as config:
    jsn = json.load(config)
    if not os.path.isdir(jsn['sb_dir']):
        jsn['sb_dir'] = askdirectory(title="Select Starbound's executable folder")
    if not os.path.isdir(jsn['instances']):
        jsn['instances'] = askdirectory(title="Select Instances' Folder")

    config.seek(0)	# <--- should reset file position to the beginning.
    json.dump(jsn, config, indent=4)
    config.truncate()	# remove remaining part
    sb_dir=jsn['sb_dir']
    instances=jsn['instances']


print(sb_dir)
print(instances)

class MyWindow(tk.Frame):

    def __init__(self,):

        super().__init__()
        self.master.title("minimal multibound")
        self.obj = None
        self.init_ui()

    def init_ui(self):

        self.pack(fill=tk.BOTH, expand=1,)

        w = tk.Frame()

        for file in os.listdir(instances):
            d = os.path.join(instances, file)
            if os.path.isdir(d):
                button = (tk.Button(self, text=file, width=30, command=partial(self.on_button_clicked, d)))
                button.grid()

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
