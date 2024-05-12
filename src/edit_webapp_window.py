# edit_webapp_window.py
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

from .create_desktop_file import desktop_filer

icon_path = __file__.rpartition(os.path.sep)[0] + '/data/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'

class EditWebAppWindow(Adw.Dialog):

    def __init__(self, parent, edit = False, state = False, **kwargs):
        super().__init__()
        if edit:
            self.set_title("Edit Web App")
        else:
            self.set_title("Create New Web App")

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        cancel_button = Gtk.Button()
        cancel_button.set_label("Cancel")
        cancel_button.connect("clicked", lambda x: self.close())
        headerbar.pack_start(cancel_button)

        self.add_button = Gtk.Button()
        self.add_button.add_css_class("suggested-action")
        self.add_button.set_sensitive(False)
        if edit:
            self.add_button.set_label("Save")
            self.add_button.set_tooltip_text("Save changes to the web app")
        else:
            self.add_button.set_label("Install")
            self.add_button.set_tooltip_text("Create a new web app")
        headerbar.pack_end(self.add_button)

        toolbar.add_top_bar(headerbar)

        prefs_list_clamp = Adw.Clamp()
        prefs_list = Gtk.ListBox()
        prefs_list.add_css_class("boxed-list")
        prefs_list.set_selection_mode(Gtk.SelectionMode.NONE)

        name_row = Adw.EntryRow()
        name_row.set_title("Name")
        name_row.connect("changed", self.enable_install)
        if edit:
            name_row.set_sensitive(False)
            name_row.set_text(state['name'])
        prefs_list.append(name_row)

        url_row = Adw.EntryRow()
        url_row.set_title("URL")
        if edit:
            url_row.set_text(state['url'])
        prefs_list.append(url_row)

        self.icon_row = Adw.ActionRow()
        self.icon_row.set_title("Icon")
        self.icon_row.set_subtitle("Set the icon for the web app (must be a PNG less than 512x512)")
        select_icon_button = Gtk.Button()
        button_content = Adw.ButtonContent()
        button_content.set_label("Browse")
        button_content.set_icon_name("folder-open-symbolic")
        select_icon_button.set_child(button_content)
        self.icon_row.add_suffix(select_icon_button)
        if edit:
            self.icon_row.set_subtitle(state['icon'])
        prefs_list.append(self.icon_row)

        show_navigation_row = Adw.SwitchRow()
        show_navigation_row.set_title("Show Navigation Options")
        show_navigation_row.set_subtitle("Show the buttons for back, forward and reload.")
        if edit:
            show_navigation_row.set_active(state['show_navigation'])
        prefs_list.append(show_navigation_row)

        domain_matching_row = Adw.ComboRow()
        domain_matching_row.set_title("Domain Matching")
        domain_matching_row.set_subtitle("Set which websites will be allowed to load in the web app.")
        domain_options = Gtk.StringList()
        domain_options.append("Domain and subdomains")
        domain_options.append("Domain only")
        domain_options.append("Allow all")
        domain_matching_row.set_model(domain_options)
        if edit:
            domain_matching_row.set_selected(state['domain_matching'])
        prefs_list.append(domain_matching_row)

        loading_bar_row = Adw.SwitchRow()
        loading_bar_row.set_title("Show Loading Bars")
        loading_bar_row.set_subtitle("A loading bar will be visible at the top of the web page when it is being loaded.")
        loading_bar_row.set_active(True)
        if edit:
            loading_bar_row.set_active(state['loading_bar'])
        prefs_list.append(loading_bar_row)

        javascript_row = Adw.SwitchRow()
        javascript_row.set_title("Enable JavaScript")
        javascript_row.set_subtitle("Enable web scripting.")
        javascript_row.set_active(True)
        if edit:
            javascript_row.set_active(state['javascript'])
        prefs_list.append(javascript_row)

        incognito_row = Adw.SwitchRow()
        incognito_row.set_title("Incognito Browsing")
        incognito_row.set_subtitle("Cookies and other data will not be stored.")
        if edit:
            incognito_row.set_active(state['incognito'])
        prefs_list.append(incognito_row)

        prefs_list_clamp.set_child(prefs_list)

        self.add_button.connect("clicked", self.install_webapp, [name_row, url_row, self.icon_row, show_navigation_row, domain_matching_row, loading_bar_row, javascript_row, incognito_row], parent, edit)
        select_icon_button.connect("clicked", self.choose_icon)
        toolbar.set_content(prefs_list_clamp)
        self.set_child(toolbar)
        self.icon = False
        if edit:
            if self.icon_row.get_subtitle() != '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name_row.get_text().replace(' ', '-') + '.png':
                self.icon = Gio.File.new_for_path(state['icon'])

    def enable_install(self, entry):
        if entry.get_text().strip() == "" or not entry.get_text().replace(" ","").isalpha() or len(entry.get_text()) > 20:
            self.add_button.set_sensitive(False)
        else:
            self.add_button.set_sensitive(True)

    def choose_icon(self, button):
        def choose_icon_finish(dialog, result):
            self.icon = choose_dialog.open_finish(result)
            self.icon_row.set_subtitle(self.icon.get_path())

        choose_dialog = Gtk.FileDialog()
        pngfilter = Gtk.FileFilter()
        pngfilter.set_name("PNG")
        pngfilter.add_suffix("png")
        choose_dialog.set_default_filter(pngfilter)
        choose_dialog.open(self, None, choose_icon_finish)

    def install_webapp(self, button, widgets, parent, edit = False):
        self.close()
        portal = Xdp.Portal()
        if edit:
            try:
                portal.dynamic_launcher_uninstall("net.codelogistics.webapps." + widgets[0].get_text().replace(' ', '-') + ".desktop")
            except:
                print('Portal error')
        if self.icon:
            icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + widgets[0].get_text().replace(' ', '-') + '.png'
            with open(icon_path, 'wb') as f:
                f.write(self.icon.load_bytes()[0].get_data()) #load_bytes() returns a tuple with the bytes and something else
        else:
            icon_path = "Default Favicon"
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
            'icon': icon_path,
            'show_navigation': widgets[3].get_active(),
            'domain_matching': widgets[4].get_selected(),
            'loading_bar': widgets[5].get_active(),
            'javascript': widgets[6].get_active(),
            'incognito': widgets[7].get_active()
        }

        with open('.var/app/net.codelogistics.webapps/webapps/' + state['name'].replace(' ', '-') + '.json', 'w') as f:
            json.dump(state, f)

        desktop_filer(parent, state['name'], state['url'], state['icon'])

        parent.refresh_rows()
