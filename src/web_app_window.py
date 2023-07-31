# web_app_window.py
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
from urllib import parse
import gi
gi.require_version("Adw", '1')
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, Gdk, Gio, Adw, WebKit

class WebAppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'WebAppWindow'

    def __init__(self, application, state, **kwargs):
        super().__init__(application = application)
        Adw.init()
        self.set_title(state[0])
        self.set_default_size(800,600)
        if os.path.exists(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/' + state[0] + '.window')):
            restore_window = open(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/' + state[0] + '.window'), 'r').read()
            if restore_window == "True":
                self.maximize()
        self.set_default_icon_name("net.codelogistics.webapps")
        self.connect("close-request", self.on_close, state)

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        context = WebKit.WebContext.get_default()
        network_session = WebKit.NetworkSession.get_default()
        cookies = network_session.get_cookie_manager()
        self.webview = WebKit.WebView()
        user_content_manager = self.webview.get_user_content_manager()

        storage = WebKit.CookiePersistentStorage.TEXT
        policy = WebKit.CookieAcceptPolicy.ALWAYS
        cookies.set_accept_policy(policy)
        cookies.set_persistent_storage(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/' + state[0] + '.cookies.txt'), storage)

        self.webview.set_vexpand(True)
        if state[1] == "":
            state[1] = "https://codelogistics.net/"
        self.webview.load_uri(state[1])
        overlay = Gtk.Overlay()
        overlay.set_child(self.webview)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.add_css_class("osd")
        self.progressbar.set_valign(Gtk.Align.START)
        if state[5]:
            overlay.add_overlay(self.progressbar)
        box.append(overlay)
        self.set_child(box)

        headerbar = Gtk.HeaderBar()
        self.back_button = Gtk.Button()
        self.back_button.set_tooltip_text("Back")
        self.back_button.set_label("←")
        self.back_button.set_sensitive(False)
        self.back_button.connect("clicked", lambda button: self.webview.go_back())
        headerbar.pack_start(self.back_button)

        self.forward_button = Gtk.Button()
        self.forward_button.set_tooltip_text("Forward")
        self.forward_button.set_label("→")
        self.forward_button.set_sensitive(False)
        self.forward_button.connect("clicked", lambda button: self.webview.go_forward())
        headerbar.pack_start(self.forward_button)

        self.reload_button = Gtk.Button()
        self.reload_button.set_tooltip_text("Reload")
        self.reload_button.set_label("⟳")
        self.reload_button.connect("clicked", self.on_reload_clicked)
        headerbar.pack_start(self.reload_button)

        if state[3]:
            self.set_titlebar(headerbar)

        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.connect('notify::estimated-load-progress', self.on_load_progress)
        self.webview.connect("context-menu", self.on_context_menu)
        self.webview.connect("decide-policy", self.on_decide_policy, state)

        reload_cb_action = Gtk.CallbackAction.new(lambda x, y: self.webview.reload())
        reload_trigger = Gtk.ShortcutTrigger.parse_string("<Control>r")
        reload_shortcut = Gtk.Shortcut.new(reload_trigger, reload_cb_action)
        self.add_shortcut(reload_shortcut)

    def on_reload_clicked(self, button):
        if button.get_label() == '⨯':
            self.webview.stop_loading()
            button.set_label('⟳')
            button.set_tooltip_text('Reload')
            self.progressbar.set_visible(False)
        else:
            self.webview.reload()
            button.set_label('⨯')
            button.set_tooltip_text('Stop')

    def on_load_progress(self, webview, progress):
        self.progressbar.set_fraction(webview.get_estimated_load_progress())

    def on_context_menu(self, webview, context_menu, hit_test_result):
        if hit_test_result.context_is_editable() and not (hit_test_result.context_is_image() or hit_test_result.context_is_link() or hit_test_result.context_is_media()):
            return
        return True

    def on_load_changed(self, webview, event):
        if event == WebKit.LoadEvent.STARTED:
            self.progressbar.set_visible(True)
            self.reload_button.set_label('⨯')
            self.reload_button.set_tooltip_text('Stop')
        elif event == WebKit.LoadEvent.FINISHED:
            self.progressbar.set_visible(False)
            self.reload_button.set_label('⟳')
            self.reload_button.set_tooltip_text('Reload')
        if self.webview.can_go_back():
            self.back_button.set_sensitive(True)
        else:
            self.back_button.set_sensitive(False)
        if self.webview.can_go_forward():
            self.forward_button.set_sensitive(True)
        else:
            self.forward_button.set_sensitive(False)

    def on_decide_policy(self, webview, decision, decision_type, state):
        if decision_type == WebKit.PolicyDecisionType.RESPONSE:
            uri = decision.get_response().get_uri()

            if self.get_domain_name(uri, state[4]) != self.get_domain_name(state[1], state[4]):
                os.system("xdg-open {}".format(uri))
                decision.ignore()

    def on_close(self, window, state):
        with open(os.path.expanduser('~/.local/share/net.codelogistics.webapps/webapps/' + state[0] + '.window'), 'w') as restore_file:
            restore_file.write(str(self.is_maximized()))
        self.webview.terminate_web_process()

    def get_domain_name(self, url, strict=True) -> str:
        parsed_url = parse.urlparse(url)
        domain_name = parsed_url.netloc
        if not strict:
            domain_name = domain_name.split('.')[-2] + '.' + domain_name.split('.')[-1]
        return domain_name

