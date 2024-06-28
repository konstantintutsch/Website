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
import sys
import uuid
import shutil

from urllib import parse

gi.require_version("Adw", '1')

from gi.repository import Gtk, Gio, Adw, Xdp, Gdk, GLib
from .create_web_app_dialog import CreateWebAppDialog
from .edit_web_app_dialog import EditWebAppDialog
from .url_dialog import URLDialog
from .create_desktop_file import desktop_filer

class WebAppsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WebAppsWindow'

    def __init__(self, application, **kwargs):
        super().__init__(application = application)
        self.app = application
        self.set_default_size(800,600)
        self.set_size_request(296,360)
        self.set_default_icon_name("net.codelogistics.webapps")

        application.create_action('close_mainwindow', lambda *_: self.close(), ['<primary>w'])

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        window_title = Adw.WindowTitle()
        window_title.set_title(_("Web Apps"))
        window_title.set_subtitle(_("Install websites as desktop applications"))
        headerbar.set_title_widget(window_title)

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.connect("clicked", self.on_add_button_clicked, application)
        add_button.set_tooltip_text(_("Add Web App"))
        headerbar.pack_start(add_button)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button_menu = Gio.Menu()
        menu_button.set_menu_model(menu_button_menu)
        about_item = Gio.MenuItem.new(_("About"), "app.about")
        menu_button_menu.append_item(about_item)
        application.create_action('report', lambda *_: self.on_report_broken(app=application))
        report_button = Gio.MenuItem.new(_("Report Broken Website"), "app.report")
        menu_button_menu.append_item(report_button)
        headerbar.pack_end(menu_button)

        toolbar.add_top_bar(headerbar)

        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.clamp = Adw.Clamp()

        rowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        rowbox.append(Gtk.Label())

        heading = Gtk.Label(label = _("Your Web Apps"))
        heading.add_css_class("heading")
        heading.set_halign(Gtk.Align.START)
        rowbox.append(heading)

        rowbox.append(Gtk.Label())

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_vexpand(True)
        self.scrolled.set_valign(Gtk.Align.FILL)
        self.apps_list = Gtk.ListBox()
        self.apps_list.add_css_class("boxed-list")
        self.apps_list.set_selection_mode(Gtk.SelectionMode.NONE)
        rowbox.append(self.apps_list)
        self.clamp.set_child(rowbox)
        self.scrolled.set_child(self.clamp)

        self.no_webapps_page = Adw.StatusPage()
        self.no_webapps_page.set_vexpand(True)
        self.no_webapps_page.set_title(_("No Web Apps installed"))
        self.no_webapps_page.set_description(_("Press the Add Web App button to create one"))
        self.no_webapps_page.set_icon_name("web-browser-symbolic")

        if len(os.listdir('.var/app/net.codelogistics.webapps/webapps/')) > 1: # uuid_verified is always there.
            self.box.append(self.scrolled)

        else:
            self.box.append(self.no_webapps_page)

        toolbar.set_content(self.box)

        self.set_content(toolbar)

        self.rows = self.add_rows(self.apps_list, application)

    def on_add_button_clicked(self, button, app):
        url_dialog = URLDialog(self, app)
        url_dialog.present(parent=self)

    def show_edit_window(self, urldialog, state):
        urldialog.close()
        
        create_app_dialog = CreateWebAppDialog(parent_window = self, state = state)
        create_app_dialog.present(self)            
                
    def add_rows(self, apps_list, application = None):
        rows = {}
        for i in os.listdir('.var/app/net.codelogistics.webapps/webapps/'):
            if i.endswith('.json') and not i.endswith('.permissions.json'):
                rows[i] = [Adw.ActionRow(), Gtk.Button(), Gtk.Button()]

                with open('.var/app/net.codelogistics.webapps/webapps/' + i, 'r') as f:
                    try:
                        tmpstate = json.load(f)
                    except:
                        # Translators: Keep the {} as it is
                        print(_('File {} broken! Maybe it was modified locally?').format(i))
                        continue

                rows[i][0].set_title(tmpstate['name'])
                rows[i][1].add_css_class('destructive-action')
                rows[i][1].set_icon_name('user-trash-symbolic')
                rows[i][1].set_tooltip_text(_("Delete"))
                rows[i][1].connect("clicked", self.delete_row, i[:-5])

                rows[i][2].add_css_class('suggested-action')
                rows[i][2].set_icon_name('document-edit-symbolic')
                rows[i][2].set_tooltip_text(_("Edit"))
                rows[i][2].connect("clicked", self.edit_row, i[:-5])
                
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
                box.append(Gtk.Label(label = '   '))
                box.append(box1)

                rows[i][0].add_suffix(box)
                apps_list.append(rows[i][0])

        return rows

    def refresh_rows(self):
        try:
            self.box.remove(self.no_webapps_page)
            self.box.append(self.scrolled)

        except:
            pass

        for i in self.rows:
            self.apps_list.remove(self.rows[i][0])
        self.rows = self.add_rows(self.apps_list)
        if self.rows == {}:
            self.box.remove(self.scrolled)
            self.box.append(self.no_webapps_page)


    def delete_row(self, button, app_id):
        os.remove('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.json')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.window'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.window')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.cookies.txt'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.cookies.txt')
        if os.path.exists('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app_id + '.png'):
            os.remove('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app_id + '.png')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.permissions.json'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.permissions.json')
        if os.path.exists(os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.' + app_id + '.desktop')):
            os.remove(os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.' + app_id + '.desktop'))
        self.refresh_rows()

    def edit_row(self, button, app_id):
        with open('.var/app/net.codelogistics.webapps/webapps/' + app_id + '.json', 'r') as f:
            tmpstate = json.load(f)
        edit_app_win = EditWebAppDialog(self, state = tmpstate, app = self.app)
        edit_app_win.present(parent=self)

    def on_report_broken(self, app):
        def submit(button):
            if url_entry.get_text() == '' or len(details_text.get_text()) < 200:
                message = Adw.AlertDialog()
                message.set_heading(_("Incomplete report"))
                message.set_body(_("Please enter the URL and a detailed description (atleast 200 characters) of the issue in English to help resolve it faster. Please make sure to mention your desktop environment and distro."))
                message.add_response('ok', 'OK')
                message.present(broken_dialog)
            
            else:
                title = '[Bug][Auto-generated]+' +  url_entry.get_text() + '+broken'
                body = ''
                if app_creation_radio.get_active():
                    body += 'Cannot install the website ' + url_entry.get_text()
                elif website_broken_radio.get_active():
                    body += 'Website+' + url_entry.get_text() + '+broken'

                body += '%0A%0A**Details:**%0A%0A' + details_text.get_text().replace(' ', '+').replace('"','\'')
                os.system("xdg-open \"https://codeberg.org/eyekay/webapps/issues/new?title=" + title + "&body=" + body + "\"")

                broken_dialog.close()

        broken_dialog = Adw.Dialog()
        broken_dialog.set_title(_("Report Broken Website"))
        broken_dialog.set_content_width(500)
        broken_dialog.set_content_height(300)

        toolbar = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        clamp = Adw.Clamp()
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.set_valign(Gtk.Align.CENTER)

        label = Gtk.Label()
        label.set_markup(_("Website broken?"))
        label.add_css_class("title-1")
        box.append(label)
        box.append(Gtk.Label())

        url_entry = Gtk.Entry()
        url_entry.set_hexpand(True)
        url_entry.set_placeholder_text(_("Enter URL"))
        box.append(url_entry)
        box.append(Gtk.Label())

        app_creation_radio = Gtk.CheckButton()
        app_creation_radio.set_active(True)
        app_creation_radio.set_label(_("I can't install the website"))
        box.append(app_creation_radio)

        website_broken_radio = Gtk.CheckButton()
        website_broken_radio.set_group(app_creation_radio)
        website_broken_radio.set_label(_("The website is not opening/ working"))
        box.append(website_broken_radio)

        box.append(Gtk.Label())
        details_text = Gtk.Entry()
        details_text.set_hexpand(True)
        details_text.set_placeholder_text(_("Enter details"))
        box.append(details_text)
        box.append(Gtk.Label())

        submit_button = Gtk.Button()
        submit_button.set_vexpand(False)
        submit_button.set_label(_("Submit"))
        submit_button.connect("clicked", submit)
        submit_button.set_tooltip_text(_("Submit"))
        submit_button.add_css_class("suggested-action")
        submit_button.add_css_class("pill")
        box.append(submit_button)
        box.append(Gtk.Label())

        clamp.set_child(box)

        toolbar.set_content(clamp)

        toolbar.add_top_bar(headerbar)
        broken_dialog.set_child(toolbar)
        broken_dialog.present(self)