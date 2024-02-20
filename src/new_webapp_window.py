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

        icon_row = Adw.ActionRow()
        icon_row.set_title("Icon")
        icon_row.set_subtitle("Default Favicon")
        select_icon_button = Gtk.Button()
        button_content = Adw.ButtonContent()
        button_content.set_label("Browse")
        button_content.set_icon_name("folder-open-symbolic")
        select_icon_button.set_child(button_content)
        icon_row.add_suffix(select_icon_button)
        prefs_list.append(icon_row)

        show_navigation_row = Adw.ActionRow()
        show_navigation_row.set_title("Show Navigation Options")
        show_navigation_row.set_subtitle("Show the buttons for back, forward and reload.")
        show_navs_switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        show_navs_switch_box.append(Gtk.Label()) # Padding, otherwise the switch looks stretched. I don't have Adw 1.4 yet so I can't use switchrow.
        show_navs_switch = Gtk.Switch()
        show_navs_switch_box.append(show_navs_switch)
        show_navs_switch_box.append(Gtk.Label())
        show_navigation_row.add_suffix(show_navs_switch_box)
        prefs_list.append(show_navigation_row)

        strict_domain_row = Adw.ActionRow()
        strict_domain_row.set_title("Strict Domain Matching")
        strict_domain_row.set_subtitle("Subdomains of the URL will not be opened")
        strict_domain_switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        strict_domain_switch_box.append(Gtk.Label())
        strict_domain_switch = Gtk.Switch()
        strict_domain_switch_box.append(strict_domain_switch)
        strict_domain_switch_box.append(Gtk.Label())
        strict_domain_row.add_suffix(strict_domain_switch_box)
        prefs_list.append(strict_domain_row)

        loading_bar_row = Adw.ActionRow()
        loading_bar_row.set_title("Show Loading Bars")
        loading_bar_row.set_subtitle("A loading bar will be visible at the top of the web page when it is being loaded.")
        loading_bar_switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        loading_bar_switch_box.append(Gtk.Label())
        loading_bar_switch = Gtk.Switch()
        loading_bar_switch.set_active(True)
        loading_bar_switch_box.append(loading_bar_switch)
        loading_bar_switch_box.append(Gtk.Label())
        loading_bar_row.add_suffix(loading_bar_switch_box)
        prefs_list.append(loading_bar_row)

        javascript_row = Adw.ActionRow()
        javascript_row.set_title("Enable JavaScript")
        javascript_row.set_subtitle("Enable web scripting.")
        javascript_switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        javascript_switch_box.append(Gtk.Label())
        javascript_switch = Gtk.Switch()
        javascript_switch.set_active(True)
        javascript_switch_box.append(javascript_switch)
        javascript_switch_box.append(Gtk.Label())
        javascript_row.add_suffix(javascript_switch_box)
        prefs_list.append(javascript_row)

        incognito_row = Adw.ActionRow()
        incognito_row.set_title("Incognito Browsing")
        incognito_row.set_subtitle("Cookies and other data will not be stored.")
        incognito_switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        incognito_switch_box.append(Gtk.Label())
        incognito_switch = Gtk.Switch()
        incognito_switch_box.append(incognito_switch)
        incognito_switch_box.append(Gtk.Label())
        incognito_row.add_suffix(incognito_switch_box)
        prefs_list.append(incognito_row)

        prefs_list_clamp.set_child(prefs_list)
        box.append(prefs_list_clamp)

        self.add_button.connect("clicked", self.install_webapp, [name_row, url_row, icon_row, show_navs_switch, strict_domain_switch, loading_bar_switch, javascript_switch, incognito_switch], parent)
        self.set_child(box)

    def enable_install(self, entry):
        if entry.get_text().strip() == "" or not entry.get_text().replace(" ","").isalpha() or len(entry.get_text()) > 20:
            self.add_button.set_sensitive(False)
        else:
            self.add_button.set_sensitive(True)

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
        state = [widgets[0].get_text(), url, widgets[2].get_subtitle(), widgets[3].get_active(), widgets[4].get_active(), widgets[5].get_active(), widgets[6].get_active(), widgets[7].get_active()]
        with open('.var/app/net.codelogistics.webapps/webapps/' + state[0].replace(' ', '-'), 'wb') as f:
            pickle.dump(state, f)

        desktop_filer(parent, state[0], state[1], state[2])

        parent.refresh_rows()
