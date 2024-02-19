import threading
import time
import os
import shutil
import sys
import gi
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, WebKit

def desktop_filer(name, url, icon):
    if icon != "Default Favicon":
        icon_path = icon
        write_desktop_file(name, icon_path)
        return
    else:
        window = Gtk.Window()
        webview = WebKit.WebView()
        network_session = webview.get_network_session()
        data_manager = network_session.get_website_data_manager()
        data_manager.set_favicons_enabled(True)

        window.set_child(webview)
        webview.load_uri(url)
        webview.connect("notify::favicon", favicon_loaded, name)
        end_time = time.time() + 10
        check_if_favicon_thread = threading.Thread(target = check_if_favicon, args = (end_time, name,))
        check_if_favicon_thread.start()

def favicon_loaded(webview, favicon, name):
    favicon = webview.get_favicon()
    if favicon:
        icon_path = os.path.expanduser('~/.local/share/xdg-desktop-portal/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')
        with open(icon_path, 'wb') as f:
            f.write(favicon.save_to_png_bytes().get_data())
    else:
        favicon = '/app/share/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'
        icon_path = os.path.expanduser('~/.local/share/xdg-desktop-portal/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')
        shutil.copyfile(favicon, icon_path)

def check_if_favicon(end_time, name):
    while time.time() < end_time:
        if os.path.exists(os.path.expanduser('~/.local/share/xdg-desktop-portal/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')):
            icon_path = os.path.expanduser('~/.local/share/xdg-desktop-portal/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')
            write_desktop_file(name, icon_path)
            break
    else:
        favicon = '/app/share/icons/hicolor/48x48/apps/net.codelogistics.webapps.png'
        icon_path = os.path.expanduser('~/.local/share/xdg-desktop-portal/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')
        shutil.copyfile(favicon, icon_path)
        write_desktop_file(name, icon_path)

def write_desktop_file(name, icon_path):
    with open(os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.' + name.replace(' ', '-') + '.desktop'), 'w') as desktop_file:
        desktop_file.write('[Desktop Entry]\n')

        desktop_file.write('Name={}\n'.format(name))
        desktop_file.write('Icon=' + icon_path.replace(' ', '-') + '\n')
        desktop_file.write('Exec=flatpak run net.codelogistics.webapps ' + name.replace(' ', '-') + '\n')
        desktop_file.write('Terminal=false\n')
        desktop_file.write('Type=Application\n')
        desktop_file.write('Categories=Network;\n')
    os.system('chmod +x "' + os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.' + name.replace(' ', '-') + '.desktop"'))
    
