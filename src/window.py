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
import requests
from urllib import parse

gi.require_version("Adw", '1')

from html.parser import HTMLParser

from gi.repository import Gtk, Gio, Adw, Xdp, Gdk, GLib
from .edit_webapp_window import EditWebAppWindow

icon_path = __file__.rpartition(os.path.sep)[0] + '/data/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.manifest_url = ''
        self.title = ''
        self.starttag = ''

    def handle_starttag(self, tag, attrs):
        self.starttag = tag
        if tag == 'link' and attrs[0] == ('rel', 'manifest'):
            manifest_url = ''
            for attr in attrs:
                if attr[0] == 'href':
                    manifest_url = attr[1]
            self.manifest_url = manifest_url

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if data.strip() != "":
            if self.starttag == "title":
                self.title = data

class WebAppsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WebAppsWindow'

    def __init__(self, application, **kwargs):
        super().__init__(application = application)
        self.app = application
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
        add_button.connect("clicked", self.on_add_button_clicked, application)
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

    def on_add_button_clicked(self, button, app):
        def url_chosen(url):
            def get_data(url, dialog):

                state = {'url': url}
                if not url.startswith('http'):
                    url = 'https://' + url
                if not url.endswith('/'):
                    url += '/'

                try:
                    html = requests.get(url).text
                except:
                    html = ""
                
                parser = MyHTMLParser()
                parser.feed(html)
                manifest_url = parser.manifest_url
                
                if manifest_url != '':
                    parsed_uri = parse.urlparse(url)
                    domain_name = parsed_uri.netloc
                    manifest_url = 'https://' + domain_name + '/' + manifest_url.lstrip('/')

                    try:
                        manifest = requests.get(manifest_url).text # This is a json file
                    except:
                        manifest = ""

                    if manifest != '':
                        manifest = json.loads(manifest)

                        state['name'] = manifest['name']

                        if 'icons' in manifest:
                            max_size = [0, '']
                            for i in manifest['icons']:
                                if 'purpose' in i and i['purpose'] == 'monochrome':
                                    continue
                                size = int(i['sizes'].split('x')[0])
                                if size > max_size[0] and size <= 512:
                                    max_size = [size, i['src']]
                                if i['type'] == 'image/svg' or i['type'] == 'image/svg+xml':
                                    max_size = [512, i['src']]
                            
                            icon = requests.get(max_size[1]).content
                            
                            with open('/tmp/webapps_icon.png', 'wb') as f:
                                f.write(icon)

                            state['icon'] = '/tmp/webapps_icon.png'

                if not 'name' in state:
                    if parser.title.strip() != '':
                        state['name'] = parser.title
                    else:
                        state['name'] = ''

                if not 'icon' in state:
                    state['icon'] = ''
                    
                dialog.close()
                new_app_win = EditWebAppWindow(self, edit = False, state = state, app = app)       
                new_app_win.present(parent = self)

                return False

            stack.set_visible_child_name('loading')

            GLib.idle_add(get_data, url, url_dialog)

        def enable_add_button(entry):
            if entry.get_text().strip() != "" and str(entry.get_text()).find(" ") == -1:
                add_button.set_sensitive(True)
            else:
                add_button.set_sensitive(False)
        
        url_dialog = Adw.Dialog()
        url_dialog.set_title("Add Web App")
        url_dialog.set_content_width(500)
        url_dialog.set_content_height(300)
        app.create_action('close', lambda *_: url_dialog.close(), ['Escape'])

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        stack = Gtk.Stack()

        clamp = Adw.Clamp()
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.set_valign(Gtk.Align.CENTER)

        label = Gtk.Label()
        label.set_markup("Enter URL")
        label.add_css_class("title-1")
        box.append(label)
        box.append(Gtk.Label())

        url_entry = Gtk.Entry()
        url_entry.set_hexpand(True)
        url_entry.set_placeholder_text("Enter URL")
        url_entry.connect("changed", enable_add_button)
        box.append(url_entry)
        box.append(Gtk.Label())

        add_button = Gtk.Button()
        add_button.set_sensitive(False)
        add_button.set_vexpand(False)
        add_button.set_label("Add")
        add_button.connect("clicked", lambda *_: url_chosen(url_entry.get_text()))
        add_button.set_tooltip_text("Add")
        add_button.add_css_class("suggested-action")
        add_button.add_css_class("pill")
        app.create_action('add_webapp', lambda *_: url_chosen(url_entry.get_text()), ['Return'])
        box.append(add_button)

        clamp.set_child(box)

        stack.add_named(clamp, "clamp")

        loading_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        loading_label = Gtk.Label()
        loading_label.set_markup("Loading...")
        loading_label.add_css_class("title-1")
        loading_box.append(loading_label)

        stack.add_named(loading_box, "loading")
        toolbar.set_content(stack)

        toolbar.add_top_bar(headerbar)
        url_dialog.set_child(toolbar)
        url_dialog.present(self)

    def add_rows(self, apps_list, application = None):
        rows = {}
        for i in os.listdir('.var/app/net.codelogistics.webapps/webapps/'):
            if i.endswith('.json') and not i.endswith('.permissions.json'):
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
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.permissions.json'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.permissions.json')
        portal = Xdp.Portal()
        try:
            portal.dynamic_launcher_uninstall("net.codelogistics.webapps." + app.replace(' ', '-') + ".desktop")
        except:
            print('Portal error')
        self.refresh_rows()

    def edit_row(self, button, name):
        with open('.var/app/net.codelogistics.webapps/webapps/' + name + '.json', 'r') as f:
            tmpstate = json.load(f)
        edit_app_win = EditWebAppWindow(self, edit = True, state = tmpstate, app = self.app)
        edit_app_win.present(parent=self)