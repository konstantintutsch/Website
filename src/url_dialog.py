# url_dialog.py
#
# Copyright 2024 Satvik Patwardhan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi
import json
import requests
import shutil

gi.require_version("Adw", '1')

from gi.repository import Gtk, Adw, GLib

from .parse_manifest import get_website_data_from_manifest
from .parse_webpage import get_website_data_from_webpage

class URLDialog(Adw.Dialog):
    def __init__(self, parent_window, app):
        super().__init__()

        self.app = app
        self.parent_window = parent_window

        self.set_title("Enter URL")

        self.set_title(_("Add Web App"))
        self.set_content_width(500)
        self.set_content_height(300)

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        self.stack = Gtk.Stack()

        clamp = Adw.Clamp()
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.set_valign(Gtk.Align.CENTER)

        label = Gtk.Label()
        label.set_markup(_("Enter URL"))
        label.add_css_class("title-1")
        box.append(label)
        box.append(Gtk.Label())

        self.url_entry = Gtk.Entry()
        self.url_entry.set_hexpand(True)
        self.url_entry.set_placeholder_text(_("Enter URL"))
        self.url_entry.connect("changed", self.enable_add_button)
        box.append(self.url_entry)
        box.append(Gtk.Label())

        self.add_button = Gtk.Button()
        self.add_button.set_sensitive(False)
        self.add_button.set_vexpand(False)
        self.add_button.set_label(_("Add"))
        self.add_button.connect("clicked", self.add_webapp)
        self.add_button.set_tooltip_text(_("Add"))
        self.add_button.add_css_class("suggested-action")
        self.add_button.add_css_class("pill")
        app.create_action('add_webapp', self.add_webapp, ['Return'])
        box.append(self.add_button)

        box.append(Gtk.Label())
        clamp.set_child(box)

        self.stack.add_named(clamp, "clamp")

        loading_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        loading_label = Gtk.Label()
        loading_label.set_markup(_("Loading..."))
        loading_label.add_css_class("title-1")
        loading_box.append(loading_label)

        self.stack.add_named(loading_box, "loading")
        toolbar.set_content(self.stack)

        toolbar.add_top_bar(headerbar)
        self.set_child(toolbar)

    def enable_add_button(self, entry):
        if entry.get_text().strip() != "" and entry.get_text().find(" ") == -1 and entry.get_text().find(".") != -1 and len(entry.get_text().rpartition(".")[-1]) >= 2:
            self.add_button.set_sensitive(True)
        else:
            self.add_button.set_sensitive(False)

    def add_webapp(self, button, data = None):
        if not self.add_button.get_sensitive(): # for the shortcut
            return

        self.stack.set_visible_child_name("loading")

        GLib.idle_add(self.get_data)

    def get_data(self):
        url = self.url_entry.get_text()
        manifest_data = get_website_data_from_manifest(url)
        if manifest_data and manifest_data[0] is not None and manifest_data[1] is not None:
            # manifest found and name and favicon found
            name = manifest_data[1]
            favicon = manifest_data[0]

        else:
            # manifest not found
            website_data = get_website_data_from_webpage(url)

            if website_data[1] is not None:
                name = website_data[1]
            else:
                # title not found by html parser
                name = _("New Web App")
            
            if website_data[0] is not None:
                favicon = website_data[0]
            else:
                favicon = '/tmp/tmp_webapps_icon.png'

        # By now, we are sure that name and favicon are there: whether actual or default
        state = {'name': name, 'url': url, 'icon': favicon}
        self.parent_window.show_edit_window(self, state)
        