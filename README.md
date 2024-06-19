# Web Apps

![Web Apps logo](data/icons/hicolor/96x96/apps/net.codelogistics.webapps.png)

Install websites as desktop applications.

Made with Gtk4, WebKitGTK, libadwaita and Flatpak.

## Installation

Web Apps is available on Flathub [here](https://flathub.org/apps/net.codelogistics.webapps).

You can install it from GNOME Software, Discover or by using the following command:

`flatpak install flathub net.codelogistics.webapps`

This is application is made for Flatpak only.

## Note for non-GNOME users

Web Apps may or may not function properly on desktop environments other that modern versions of GNOME because of the varying levels of support for the Dynamic Launcher portal provided by the various XDG Desktop Portal backends.

## Building

You can build Web Apps by cloning this repository into GNOME Builder (either the Flatpak or the version shipped with your distro), which will handle all dependencies and build the Flatpak.

## Usage

### For end-users

Open 'Web Apps' for the main interface, or the name of the web app for the web app itself, from the menu.

### Command line

`flatpak run net.codelogistics.webapps`

For running a specific Web App,

`flatpak run net.codelogistics.webapps NAME`

where NAME is the name of the Web App (replace spaces with '-' if applicable). This is case-sensitive.

## Credits

This program is licensed under the GNU General Public License, version 3.0 or later.
