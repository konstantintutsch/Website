# window.py
#
# Copyright 2023 Satvik Patwardhan
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

import os
import gi
import json

gi.require_version("Adw", '1')

from gi.repository import Gtk, Gio, Adw, Xdp
from .edit_webapp_window import EditWebAppWindow

icon_path = __file__.rpartition(os.path.sep)[0] + '/data/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'

class WebAppsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WebAppsWindow'

    def __init__(self, application, **kwargs):
        super().__init__(application = application)
        self.set_title("Web Apps")
        self.set_default_size(800,600)
        self.set_default_icon_name("net.codelogistics.webapps")

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        window_title = Adw.WindowTitle()
        window_title.set_title("Web Apps")
        window_title.set_subtitle("Install websites as desktop applications")
        headerbar.set_title_widget(window_title)

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.connect("clicked", self.on_add_button_clicked)
        add_button.set_tooltip_text("Add Web App")
        headerbar.pack_start(add_button)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button_menu = Gio.Menu()
        menu_button.set_menu_model(menu_button_menu)
        about_item = Gio.MenuItem.new("About", "app.about")
        menu_button_menu.append_item(about_item)
        headerbar.pack_end(menu_button)

        toolbar.add_top_bar(headerbar)

        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.clamp = Adw.Clamp()

        rowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        rowbox.append(Gtk.Label())

        heading = Gtk.Label(label = "Your Web Apps")
        heading.add_css_class("heading")
        heading.set_halign(Gtk.Align.START)
        rowbox.append(heading)

        rowbox.append(Gtk.Label())

        self.apps_list = Gtk.ListBox()
        self.apps_list.add_css_class("boxed-list")
        self.apps_list.set_selection_mode(Gtk.SelectionMode.NONE)

        self.rows = self.add_rows(self.apps_list, application)

        rowbox.append(self.apps_list)
        self.clamp.set_child(rowbox)

        self.no_webapps_page = Adw.StatusPage()
        self.no_webapps_page.set_vexpand(True)
        self.no_webapps_page.set_title("No Web Apps installed")
        self.no_webapps_page.set_description("Press the Add Web App button to create one")
        self.no_webapps_page.set_icon_name("web-browser-symbolic")

        if len(os.listdir('.var/app/net.codelogistics.webapps/webapps/')) > 0:
            self.box.append(self.clamp)

        else:
            self.box.append(self.no_webapps_page)

        toolbar.set_content(self.box)

        self.set_content(toolbar)

    def on_add_button_clicked(self, button):
        new_app_win = EditWebAppWindow(self, edit = False)
        new_app_win.present(parent = self)

    def add_rows(self, apps_list, application = None):
        rows = {}
        for i in os.listdir('.var/app/net.codelogistics.webapps/webapps/'):
            if i.endswith('.json'):
                rows[i] = [Adw.ActionRow(), Gtk.Button(), Gtk.Button()]

                with open('.var/app/net.codelogistics.webapps/webapps/' + i.replace(' ', '-'), 'r') as f:
                    tmpstate = json.load(f)

                rows[i][0].set_title(tmpstate['name'])
                rows[i][1].add_css_class('destructive-action')
                rows[i][1].set_icon_name('user-trash-symbolic')
                rows[i][1].connect("clicked", self.delete_row, i)

                rows[i][2].add_css_class('suggested-action')
                rows[i][2].set_icon_name('document-edit-symbolic')
                rows[i][2].connect("clicked", self.edit_row, tmpstate['name'].replace(' ', '-'))
                
                box1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
                box1.append(Gtk.Label()) # We add the box instead of the button directly to give padding as otherwise the button looks stretched.
                box1.append(rows[i][1])
                box1.append(Gtk.Label())

                box2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
                box2.append(Gtk.Label())
                box2.append(rows[i][2])
                box2.append(Gtk.Label())

                box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
                box.append(box2)
                box.append(Gtk.Label(label = ' '))
                box.append(box1)

                rows[i][0].add_suffix(box)
                apps_list.append(rows[i][0])

        return rows

    def refresh_rows(self):
        try:
            self.box.remove(self.no_webapps_page)
            self.box.append(self.clamp)

        except:
            pass

        for i in self.rows:
            self.apps_list.remove(self.rows[i][0])
        self.rows = self.add_rows(self.apps_list)
        if self.rows == {}:
            self.box.remove(self.clamp)
            self.box.append(self.no_webapps_page)


    def delete_row(self, button, app):
        app = app[:-5]
        os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.json')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.window'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.window')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.cookies.txt'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.cookies.txt')
        if os.path.exists('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app + '.png'):
            os.remove('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app + '.png')
        portal = Xdp.Portal()
        try:
            portal.dynamic_launcher_uninstall("net.codelogistics.webapps." + app.replace(' ', '-') + ".desktop")
        except:
            print('Portal error')
        self.refresh_rows()

    def edit_row(self, button, name):
        with open('.var/app/net.codelogistics.webapps/webapps/' + name + '.json', 'r') as f:
            tmpstate = json.load(f)
        edit_app_win = EditWebAppWindow(self, edit = True, state = tmpstate)
        edit_app_win.present(parent=self)