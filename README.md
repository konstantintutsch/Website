# Web Apps

![Web Apps logo](data/icons/hicolor/48x48/apps/net.codelogistics.webapps.png)

Install websites as desktop applications.

Made with Gtk4, WebKitGTK, libadwaita and Flatpak.

## Dependencies
org.gnome.Platform 44

This is currently a Flatpak-only application. It needs access to the host's xdg-data dirs to add new apps to the menus.

## Usage

### For end-users

Open 'Web Apps' for the main interface, or the name of the web app for the web app itself, from the menu.

### Command line
`flatpak run net.codelogistics.webapps`

For running a specific Web App,

`flatpak run net.codelogistics.webapps NAME`

where NAME is the name of the Web App (replace spaces with '-' if applicable). This is case-sensitive.

## Todos

* Edit already created web apps
* The different web apps have the same application ID (and therefore the same icon) on X11

## Credits

This program is licensed under the GNU General Public License, version 3.0 or later.
