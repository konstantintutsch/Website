# main.py
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
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version("Adw", '1')

from gi.repository import Gtk, Gio, Adw
from .window import WebAppsWindow
from .web_app_window import WebAppWindow

class WebappsApplication(Gtk.Application):
    """The main application singleton class."""

    def __init__(self, args):
        if len(args) > 1 and args[1] in os.listdir(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/')):
            super().__init__(application_id='net.codelogistics.webapps.' + args[1],
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        else:
            super().__init__(application_id='net.codelogistics.webapps.Webapps',
                             flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.args = args

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        if len(self.args) == 2 and self.args[1] in os.listdir(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/')):
            with open(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/' + self.args[1]), 'rb') as f:
                state = pickle.load(f)
            win = WebAppWindow(application=self, state = state)
            win.present()
        else:
            win = WebAppsWindow(application=self)
            win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window, modal=True,)
        about.set_application_name("Web Apps")
        about.set_developer_name("Satvik Patwardhan")
        about.set_application_icon('net.codelogistics.webapps')
        about.set_version('0.1.0')
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_developers(['Satvik Patwardhan'])
        about.set_copyright('© 2023 Satvik Patwardhan')

        about.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""

    if os.path.exists(os.path.expanduser('~/.local/share/net.codelogistics.webapps/')):
        pass
    else:
        os.mkdir(os.path.expanduser('~/.local/share/net.codelogistics.webapps/'))
        os.mkdir(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/'))

    app = WebappsApplication(args = sys.argv)
    return app.run()

