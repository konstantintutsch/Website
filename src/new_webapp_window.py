# new_webapp_window.py
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
import pickle
import gi
import json

gi.require_version("Adw", '1')
from gi.repository import Gtk, Gio, Adw

from .create_desktop_file import desktop_filer

icon_path = __file__.rpartition(os.path.sep)[0] + '/data/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'

class NewWebAppWindow(Gtk.Dialog):

    def __init__(self, parent, application, **kwargs):
        super().__init__(application = application)
        Adw.init()
        self.set_title("Create New Web App")
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(600,400)
        self.set_default_icon_name("net.codelogistics.webapps")

        headerbar = Gtk.HeaderBar()

        cancel_button = Gtk.Button()
        cancel_button.set_label("Cancel")
        cancel_button.connect("clicked", lambda x: self.destroy())
        headerbar.pack_start(cancel_button)

        self.add_button = Gtk.Button()
        self.add_button.add_css_class("suggested-action")
        self.add_button.set_sensitive(False)
        self.add_button.set_label("Install")
        self.add_button.set_tooltip_text("Create a new web app")
        headerbar.pack_end(self.add_button)

        self.set_titlebar(headerbar)

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        prefs_list_clamp = Adw.Clamp()
        prefs_list = Gtk.ListBox()
        prefs_list.add_css_class("boxed-list")
        prefs_list.set_selection_mode(Gtk.SelectionMode.NONE)

        name_row = Adw.EntryRow()
        name_row.set_title("Name")
        name_row.connect("changed", self.enable_install)
        prefs_list.append(name_row)

        url_row = Adw.EntryRow()
        url_row.set_title("URL")
        prefs_list.append(url_row)

        self.icon_row = Adw.ActionRow()
        self.icon_row.set_title("Icon")
        self.icon_row.set_subtitle("Default Favicon")
        select_icon_button = Gtk.Button()
        button_content = Adw.ButtonContent()
        button_content.set_label("Browse")
        button_content.set_icon_name("folder-open-symbolic")
        select_icon_button.set_child(button_content)
        self.icon_row.add_suffix(select_icon_button)
        prefs_list.append(self.icon_row)

        show_navigation_row = Adw.SwitchRow()
        show_navigation_row.set_title("Show Navigation Options")
        show_navigation_row.set_subtitle("Show the buttons for back, forward and reload.")
        prefs_list.append(show_navigation_row)

        strict_domain_row = Adw.SwitchRow()
        strict_domain_row.set_title("Strict Domain Matching")
        strict_domain_row.set_subtitle("Subdomains of the URL will not be opened")
        prefs_list.append(strict_domain_row)

        loading_bar_row = Adw.SwitchRow()
        loading_bar_row.set_title("Show Loading Bars")
        loading_bar_row.set_subtitle("A loading bar will be visible at the top of the web page when it is being loaded.")
        prefs_list.append(loading_bar_row)

        javascript_row = Adw.SwitchRow()
        javascript_row.set_title("Enable JavaScript")
        javascript_row.set_subtitle("Enable web scripting.")
        prefs_list.append(javascript_row)

        incognito_row = Adw.SwitchRow()
        incognito_row.set_title("Incognito Browsing")
        incognito_row.set_subtitle("Cookies and other data will not be stored.")
        prefs_list.append(incognito_row)

        prefs_list_clamp.set_child(prefs_list)
        box.append(prefs_list_clamp)

        self.add_button.connect("clicked", self.install_webapp, [name_row, url_row, self.icon_row, show_navigation_row, strict_domain_row, loading_bar_row, javascript_row, incognito_row], parent)
        select_icon_button.connect("clicked", self.choose_icon)
        self.set_child(box)

    def enable_install(self, entry):
        if entry.get_text().strip() == "" or not entry.get_text().replace(" ","").isalpha() or len(entry.get_text()) > 20:
            self.add_button.set_sensitive(False)
        else:
            self.add_button.set_sensitive(True)

    def choose_icon(self, button):
        def choose_icon_finish(dialog, result):
            file = choose_dialog.open_finish(result)
            self.icon_row.set_subtitle(file.get_path())
        choose_dialog = Gtk.FileDialog()
        pngfilter = Gtk.FileFilter()
        pngfilter.set_name("PNG")
        pngfilter.add_suffix("png")
        choose_dialog.set_default_filter(pngfilter)
        choose_dialog.open(self, None, choose_icon_finish)

    def install_webapp(self, button, widgets, parent):
        self.destroy()
        if widgets[1].get_text() == "":
            url = "about:blank"
        else:
            url = widgets[1].get_text()
        if not url.startswith('http'):
            url = 'https://' + url
        if not url.endswith('/'):
            url += '/'
        state = {
            'name': widgets[0].get_text(),
            'url': url,
            'icon': widgets[2].get_subtitle(),
            'show_navigation': widgets[3].get_active(),
            'strict_domain': widgets[4].get_active(),
            'loading_bar': widgets[5].get_active(),
            'javascript': widgets[6].get_active(),
            'incognito': widgets[7].get_active()
        }

        with open('.var/app/net.codelogistics.webapps/webapps/' + state['name'].replace(' ', '-') + '.json', 'w') as f:
            json.dump(state, f)

        desktop_filer(parent, state['name'], state['url'], state['icon'])

        parent.refresh_rows()
