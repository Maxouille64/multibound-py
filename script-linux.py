#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import os
import json

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import Notify

print("Libs successfully imported !")

sb_dir = \
    '/home/gigad/.steam/debian-installation/steamapps/common/Starbound/linux'
#sb_dir = '/home/gigad/Documents/Starbound-master/dist'
instances = '/home/gigad/Documents/instances'


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='minimal multibound')
        Gtk.Window.set_default_size(self, 640, 480)
        Notify.init('Simple GTK3 Application')

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)
        self.button = []
        i = 0
        for file in os.listdir(instances):
            d = os.path.join(instances, file)
            if os.path.isdir(d):
                self.button.append(Gtk.Button(label=file))
                #self.button[i].set_halign(Gtk.Align.CENTER)
                #self.button[i].set_valign(Gtk.Align.CENTER)
                self.button[i].connect('clicked', self.on_button_clicked, d, file)
                self.box.pack_start(self.button[i], True, True, 0)
                print(d)
                i = i +1

        self.browse = Gtk.Button(label='browse')
        self.browse.set_halign(Gtk.Align.CENTER)
        self.browse.set_valign(Gtk.Align.CENTER)
        self.browse.connect('clicked', self.open_dir, sb_dir)

        self.box.pack_start(self.browse, True, True, 0)



    def open_dir(self, widget, *data):
        os.system('xdg-open ' + data[0])

    def on_button_clicked(self, widget, *data):
        n = Notify.Notification.new('Starbound', data[1])
        n.show()

        os.chdir(sb_dir)
        with open(sb_dir + '/sbinit.config', 'r+') as f:
        	jsn = json.load(f)
        	jsn['assetDirectories'][1] = data[0] + "/mods/" # <--- add `mods` value.
        	jsn['storageDirectory'] = data[0] + "/storage/" # <--- add `storage` value.
        	f.seek(0)	# <--- should reset file position to the beginning.
        	json.dump(jsn, f, indent=4)
        	f.truncate()	# remove remaining part
        #os.system('gnome-terminal -x ./starbound')
        os.system('gnome-terminal -x steam steam://rungameid/starbound')



win = MyWindow()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
