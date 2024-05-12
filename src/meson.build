pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'webapps')
gnome = import('gnome')

gnome.compile_resources('webapps',
  'webapps.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'webapps.in',
  output: 'webapps',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

webapps_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'edit_webapp_window.py',
  'web_app_window.py',
  'create_desktop_file.py',
]

install_data(webapps_sources, install_dir: moduledir)
