#!/usr/bin/python3
"""
Procno: Process monitor and notifications forwarder
===================================================

A GUI procfs stat viewer with Freedesktop-Notifications forwarding.  Kind of like ``top``, but not as we know it.

Usage:
======

        procno [-h]
                     [--about] [--detailed-help]
                     [--install] [--uninstall]

Optional arguments:
-------------------

      -h, --help            show this help message and exit
      --detailed-help       full help in markdown format
      --about               about procno
      --install             installs the procno in the current user's path and desktop application menu.
      --uninstall           uninstalls the procno application menu file and script for the current user.

Description
===========

``Procno`` is a GUI ``procfs`` process stat monitoring tool.  Procno can can warn of processes consuming
excessive CPU or memory by raising *Freedesktop DBUS Notifications* (most linux desktop environments present
DBUS Notifications as popup messages).  Procno's UI functions as follows:

 * All the processes on the system are represented by dots.
 * The static dot coloring is specific to the process owner (all the light grey processes belong to root).
 * If a process consumes a little CPU (<10%) its dot will briefly light up in blue.
 * If a process consumes a lot of CPU its dot will vary from lighter pinkish-red to full-red depending on how much
   CPU it is consuming.
 * If a dot briefly enlarges or decreases in size, the process's resident set size has gone up or down.
 * Each process dot is augmented with a dashed-ring that indicates the processes resident set size as proportion of RAM.
 * If text is entered in the search field (for example nmb), any process with matching text is circled in red
   (this happens dynamically, so new matching processes will be circled when they start).  Text search becomes
   incremental once more than three characters have been entered.
 * Hovering over a dot brings up a tooltip containing process details.
 * Clicking on a dot brings up a small dialog with process details that update dynamically.  The dialog
   includes an arming switch (a checkbox) that arms a signal dropdown which can be used to signal/terminate
   the process.
 * If a process consumes too much CPU or RSS for too long, a desktop notification will be raised. The notification
   will continue to update as long as the process continues to offend.  If the notification is closed, no
   no further notifications will be raised while the process continues to offend.  When a processed ceases
   to offend its notification status is reset, any subsequent offending will result in fresh notifications.
 * Procno can optionally run out of the system tray. Geometry and configuration is preserved
   across restarts. Procno dynamically adjusts to light and dark desktop themes.
 * The mouse wheel zooms the view.

Procno is designed to increase awareness of background activity.  Possibilities for it use include:

 * Detecting runaway processes, either CPU or RAM.
 * Getting a quick overview of where resources are going.
 * Looking for patterns in resource consumption.
 * Identifying unnecessary services that are present and idle.
 * Entertaining the cat.

Optional metrics
----------------
Procno can optionally report some other process metrics:

  * USS: unique set size, this should more accurately reflect memory consumption, but it appears to be
    very expensive to collect, procno's CPU consumption jumps from around 8% to 50% if USS stats
    are enabled. In respect to my own desktop, RSS is pretty similar to USS for the applications
    that consume the bulk of most memory.  Another issue with USS is that access to USS is limited,
    USS will only be shown for your own processes.
  * Shared memory: this is inexpensive to report but is not confined to RSS or USS, so may not be
    a good indicator of pressure on the system.
  * I/O: this is a basic indicator of whether read/write occurred in the last period.  Most processes
    are continually doing some amount of I/O, so perhaps this is not that useful, although a
    continuous-on indicator may be an indication of pressure in some circumstances.  Access to
    I/O read/write counts is restricted, I/O indicators will only be shown for your own processes.

Experimentation notification options
------------------------------------

The follow options excercise facilities defined in the
[Desktop Notifications Specification](https://specifications.freedesktop.org/notification-spec/latest/)
(https://specifications.freedesktop.org/notification-spec/latest/)
Some Linux desktops claim to support many of these features, but quite often the implementations are
buggy or divergent from behaviour specified in the standard.

If the following two options fail to work as expected, it is almost certainly a defect in your
desktop's support of the standard.  Any bugs raised should be directed to the desktop project concerned
and not the procno application.

  * notification_updates_enabled: if a desktop supports updatable notifications, notifications
    will be updated as the incident continues.  On some desktops this can be buggy, for example
    on KDE/Plasma the desktop sometimes loses track of existing notifications leading to multiple
    notifications appearing instead of one (a logout may correct the problem).
  * notification_actions_enabled: an Info button will be added to notifications, when pressed it
    should callback the application to popup info on the incident's subject process.  On some
    desktops this too is buggy, and causes even more problems when combined with notification
    updates.

Despite the results being buggy, I've left the options available, partly as a reference-implementation,
and partly in the hope that desktops support of these features may improve in time.

Config files
------------

All settings made in the *Configuration* panel are saved to a config file.  There is no need to manually
edit the config file, but if it is externally edited the application will automatically reload the changes.


The config file is in INI-format divided into a number of sections as outlined below::
```
        # The options section controls notice timeouts, burst treatment
        [options]
        # Polling interval, how often to wait for journal entries between checking for config changes
        poll_seconds = 2

        # Run out of the system tray
        system_tray_enabled = yes
        # Start the application with notifications enabled (disable notifications from start up).
        start_with_notifications_enabled = yes

        # For debugging the application
        debug_enabled = yes

```

The config file is normally save to a standard desktop location:

        $HOME/.config/procno/procno.conf

In addition to the application config file, window geometry and state is saved to:

        $HOME/.config/procno.qt.state/procno.conf


Prerequisites
=============

All the following runtime dependencies are likely to be available pre-packaged on any modern Linux distribution
(``procno`` was originally developed on OpenSUSE Tumbleweed).

* python 3.8: ``procno`` is written in python and may depend on some features present only in 3.8 onward.
* python 3.8 QtPy: the python GUI library used by ``procno``.
* python 3.8 psutils: the library used to gather the data (often preinstalled in many Linux systems)
* python 3.8 dbus: python module for dbus used for issuing notifications

Dependency installation on ``OpenSUSE``:

        zypper install python38-QtPy python38-dbus

Optional Accessories
====================

A suggested accessory is [KDE Connect](https://kdeconnect.kde.org/).  If you enabled the appropriate permissions on
your phone, KDE Connect can forward desktop notifications to the phone.  Use procno to forward Systemd-Journal
messages to Desktop-Notifications, and use KDE Connect to forward them to your phone.

Debugging Tools
===============

* dbus-monitor --session interface=org.freedesktop.Notifications
* d-feet
* gdbus monitor --session --dest org.freedesktop.Notifications

Procno Copyright (C) 2021 Michael Hamilton
===========================================

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.

**Contact:**  m i c h a e l   @   a c t r i x   .   g e n   .   n z

----------

"""
# TODO IO
# TODO vsize ring?
# TODO random color suggestion button
# TODO make the random color picker pick colors distant from the last pick - maybe feed it an invert of the last pick.
# TODO input validation (more)
# TODO zoom in should do more than just enlarge - annotate?
# TODO Help
# TODO night palette option?
# TODO try a brighter less-pastel palette
#
import argparse
import configparser
import math
import os
import pwd
import random
import re
import signal
import stat
import sys
import textwrap
import time
import traceback
from datetime import timedelta
from html import escape
from io import StringIO
from pathlib import Path
from typing import Mapping, List, Type, Callable, Tuple

import dbus
import psutil
from PyQt5.QtCore import QCoreApplication, QProcess, Qt, pyqtSignal, QThread, QSize, \
    QEvent, QSettings, QObject, QRegExp, QRect
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QIntValidator, \
    QFontDatabase, QCloseEvent, QPalette, QColor, QPen, QMouseEvent, QWheelEvent, QResizeEvent, \
    QRegExpValidator, QGuiApplication
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QLineEdit, QLabel, \
    QPushButton, QSystemTrayIcon, QMenu, QTextEdit, QDialog, QCheckBox, QGridLayout, QMainWindow, QSizePolicy, QToolBar, \
    QHBoxLayout, QStyleFactory, QToolButton, QScrollArea, QLayout, QStatusBar, QToolTip, QComboBox, QTabWidget, \
    QColorDialog
from dbus.mainloop.glib import DBusGMainLoop

PROGRAM_VERSION = '1.2.9'

# On Plasma Wayland the system tray may not be immediately available at login - so keep trying for...
SYSTEM_TRAY_WAIT_SECONDS = 20


def get_program_name() -> str:
    return Path(sys.argv[0]).stem


ABOUT_TEXT = f"""

<b>Procno version {PROGRAM_VERSION}</b>
<p>
A Systemd-process viewer with Freedesktop-Notifications forwarding.
<p>
Visit <a href="https://github.com/digitaltrails/{get_program_name()}">https://github.com/digitaltrails/{get_program_name()}</a> for
more details.
<p><p>

<b>Procno Copyright (C) 2021 Michael Hamilton</b>
<p>
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, version 3.
<p>
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.
<p>
You should have received a copy of the GNU General Public License along
with this program. If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>.

"""

DEFAULT_CONFIG = '''
[options]
poll_seconds = 1
debug_enabled = yes
system_tray_enabled = no
notification_seconds = 30
start_with_notifications_enabled = yes
notify_cpu_use_percent = 100
notify_cpu_use_seconds = 30
notify_rss_exceeded_mbytes = 1000
notify_rss_growing_seconds = 5
io_indicators_enabled = no
uss_enabled = no
shared_enabled = no
tree_enabled = no

[colors]

cpu_activity_color = 0x3491e1
new_process_color = 0xf8b540
search_match_color = 0x00aa00
root_user_color = 0xd2d2d2

'''

ERROR_DBUS_NOTIFICATIONS_UNAVAILABLE = "DBUS notification service unavailable"
ERROR_DBUS_NOTIFICATION_FAILED = "DBUS notification failed"

ICON_HELP_ABOUT = "help-about"
ICON_HELP_CONTENTS = "help-contents"
ICON_APPLICATION_EXIT = "application-exit"
ICON_CONTEXT_MENU_LISTENING_ENABLE = "view-refresh"
ICON_CONTEXT_MENU_LISTENING_DISABLE = "process-stop"
SVG_TRAY_LISTENING_DISABLED = ICON_CONTEXT_MENU_LISTENING_DISABLE
ICON_COPY_TO_CLIPBOARD = "edit-copy"
ICON_UNDOCK = "window-new"
ICON_DOCK = "view-restore"
ICON_GO_NEXT = "go-down"
ICON_GO_PREVIOUS = "go-up"
ICON_CLEAR_RECENTS = "edit-clear-all"
ICON_DEFAULTS = 'edit-reset'
ICON_REVERT = 'edit-undo'
# This might only be KDE/Linux icons - not in Freedesktop Standard.
ICON_APPLY = "dialog-ok-apply"
ICON_VIEW_PROCESS_ENTRY = 'view-fullscreen'
ICON_CLEAR_SELECTION = 'edit-undo'
ICON_COPY_SELECTED = 'edit-copy'
ICON_PLAIN_TEXT_SEARCH = 'insert-text'
ICON_REGEXP_SEARCH = 'list-add'
ICON_SETTINGS_CONFIGURE = 'settings-configure'
ICON_SEARCH_PROCESSES = "system-search"

SVG_LIGHT_THEME_COLOR = b"#232629"
SVG_DARK_THEME_COLOR = b"#f3f3f3"

SVG_PROGRAM_ICON = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">

    <circle cx="5" cy="5" r="2" fill="#3491e1"/>
    <circle cx="10" cy="5" r="2" fill="#3491e1"/>
    <circle cx="15" cy="5" r="2" fill="#da4453"/>
    <circle cx="5" cy="10" r="2" fill="#3491e1"/>
    <circle cx="10" cy="10" r="2" fill="#3491e1"/>
    <circle cx="15" cy="10" r="2" fill="#3491e1"/>
    <circle cx="5" cy="15" r="2" fill="#3491e1"/>
    <circle cx="10" cy="15" r="2" fill="#3491e1"/>
    <circle cx="15" cy="15" r="2" fill="#3491e1"/>

</svg>"""

SVG_PROGRAM_ICON_LIGHT = SVG_PROGRAM_ICON.replace(SVG_LIGHT_THEME_COLOR, b'#bbbbbb')

SVG_TOOLBAR_RUN_DISABLED = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
    <style type="text/css" id="current-color-scheme">
        .ColorScheme-Text {
            color:#232629;
        }
    </style>
    <path d="m3 3v16l16-8z" class="ColorScheme-Text" fill="currentColor"/>
</svg>
"""

SVG_TOOLBAR_RUN_ENABLED = SVG_TOOLBAR_RUN_DISABLED.replace(b"#232629;", b"#3daee9;")
SVG_TOOLBAR_STOP = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
    <style type="text/css" id="current-color-scheme">
        .ColorScheme-Text {
            color:#da4453;
        }
    </style>
    <path d="m3 3h16v16h-16z" class="ColorScheme-Text" fill="currentColor"/>
</svg>
"""

SVG_TRAY_LISTENING_DISABLED = SVG_PROGRAM_ICON.replace(b'3491e1', b'ff0000')

SVG_TOOLBAR_HAMBURGER_MENU = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#232629;
      }
      </style>
  </defs>
 <path
     style="fill:currentColor;fill-opacity:1;stroke:none"
     d="m3 5v2h16v-2h-16m0 5v2h16v-2h-16m0 5v2h16v-2h-16" class="ColorScheme-Text" />
</svg>
"""

SVG_TOOLBAR_NOTIFIER_ENABLED = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#379fd3;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
       d="M 3 4 L 3 16 L 6 20 L 6 17 L 6 16 L 19 16 L 19 4 L 3 4 z M 4 5 L 18 5 L 18 15 L 4 15 L 4 5 z M 16 6 L 9.5 12.25 L 7 10 L 6 11 L 9.5 14 L 17 7 L 16 6 z "
     class="ColorScheme-Text"
     />
</svg>
"""
SVG_TOOLBAR_NOTIFIER_DISABLED = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#da4453;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
       d="M 3 4 L 3 16 L 6 20 L 6 17 L 6 16 L 19 16 L 19 4 L 3 4 z M 4 5 L 18 5 L 18 15 L 4 15 L 4 5 z M 8 6 L 7 7 L 10 10 L 7 13 L 8 14 L 11 11 L 14 14 L 15 13 L 12 10 L 15 7 L 14 6 L 11 9 L 8 6 z "
     class="ColorScheme-Text"
     />
</svg>
"""

SVG_COLOR_SWATCH = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
    <style type="text/css" id="current-color-scheme">
        .ColorScheme-Text {
            color:#000000;
        }
    </style>
    <path d="m3 3h16v16h-16z" class="ColorScheme-Text" fill="currentColor"/>
</svg>
"""

system_boot_time = psutil.boot_time()
system_vm_bytes = psutil.virtual_memory().total
system_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])


def tr(source_text: str):
    """For future internationalization - recommended way to do this at this time."""
    return QCoreApplication.translate('procno', source_text)


class ConfigOption:

    def __init__(self, option_id: str, tooltip: str, int_range: Tuple[int, int] = None):
        self.option_id = option_id
        self.int_range = int_range
        self._tooltip = tooltip

    def label(self):
        return tr(self.option_id).replace('_', ' ').capitalize()

    def tooltip(self):
        fmt = tr(self._tooltip)
        return fmt.format(self.int_range[0], self.int_range[1]) if self.int_range is not None else fmt


CONFIG_OPTIONS_LIST: List[ConfigOption] = [
    ConfigOption('poll_seconds', tr('How often to poll for new messages ({}..{} seconds).'), (1, 30)),
    ConfigOption('notification_seconds',
                 tr('How long should a desktop notification remain visible, zero for no timeout ({}..{} seconds)'),
                 (0, 60)),
    ConfigOption('notify_cpu_use_percent',
                 tr('Processes CPU consumption threshold ({}..{} percent)'),
                 (0, 900)),
    ConfigOption('notify_cpu_use_seconds',
                 tr('Notify if a process stays above the CPU threshold for this amount of time ({}..{} seconds)'),
                 (0, 300)),
    ConfigOption('notify_rss_exceeded_mbytes',
                 tr('Process rss consumption threshold (1..100000 Mbytes)'),
                 (1, 100_000)),
    ConfigOption('notify_rss_growing_seconds',
                 tr('Notify if a process rss continues to grow above the threshold for this amount of time  ({}..{} '
                    'seconds)'),
                 (0, 60)),
    ConfigOption('system_tray_enabled', tr('procno should start minimised in the system-tray.')),
    ConfigOption('start_with_notifications_enabled', tr('procno should start with desktop notifications enabled.')),
    ConfigOption('io_indicators_enabled',
                 tr("Show read/write indicators\n(not available for other user's processes).")),
    ConfigOption('uss_enabled', tr("Show USS - Unique SS - obtaining USS is expensive CPU wise\n"
                                   "(not available for other user's processes).")),
    ConfigOption('shared_enabled', tr("Show potentially shared.")),
    ConfigOption('notification_updates_enabled',
                 tr("Update existing notifications with new info (if supported by desktop, buggy on some desktops).")),
    ConfigOption('notification_actions_enabled',
                 tr("Info button on notifications (if supported by desktop, buggy on some desktops, buggy on some "
                    "desktops when combined with update notifications).")),
    ConfigOption('tree_enabled', tr("Festive layout.")),
    ConfigOption('debug_enabled', tr('Enable extra debugging output to standard-out.')),
]

io_indicators_enabled = False
uss_enabled = False
shared_enabled = False

debugging = False


def debug(*arg):
    if debugging:
        print('DEBUG:', *arg)


def info(*arg):
    print('INFO:', *arg)


def warning(*arg):
    print('WARNING:', *arg)


def error(*arg):
    print('ERROR:', *arg)


def random_color(mix, seed: int = None):
    if seed:
        random.seed(seed)
    # https://newbedev.com/algorithm-to-randomly-generate-an-aesthetically-pleasing-color-palette
    # Changed 127 to 168 to make the colors lighter
    red = random.randint(168, 256)
    green = random.randint(168, 256)
    blue = random.randint(168, 256)
    # mix the color
    if mix is not None:
        red = (red + mix[0]) // 2
        green = (green + mix[1]) // 2
        blue = (blue + mix[2]) // 2
    return red, green, blue


def exception_handler(e_type, e_value, e_traceback):
    """Overarching error handler in case something unexpected happens."""
    error("\n", ''.join(traceback.format_exception(e_type, e_value, e_traceback)))
    alert = QMessageBox()
    alert.setText(tr('Error: {}').format(''.join(traceback.format_exception_only(e_type, e_value))))
    alert.setInformativeText(tr('Unexpected error'))
    alert.setDetailedText(
        tr('Details: {}').format(''.join(traceback.format_exception(e_type, e_value, e_traceback))))
    alert.setIcon(QMessageBox.Critical)
    alert.exec()
    QApplication.quit()


def install_as_desktop_application(uninstall: bool = False):
    """Self install this script in the current Linux user's bin directory and desktop applications->settings menu."""
    desktop_dir = Path.home().joinpath('.local', 'share', 'applications')
    icon_dir = Path.home().joinpath('.local', 'share', 'icons')

    if not desktop_dir.exists():
        warning("creating:{desktop_dir.as_posix()}")
        os.mkdir(desktop_dir)

    bin_dir = Path.home().joinpath('bin')
    if not bin_dir.is_dir():
        warning("creating:{bin_dir.as_posix()}")
        os.mkdir(bin_dir)

    if not icon_dir.is_dir():
        warning("creating:{icon_dir.as_posix()}")
        os.mkdir(icon_dir)

    installed_script_path = bin_dir.joinpath("procno")
    desktop_definition_path = desktop_dir.joinpath("procno.desktop")
    icon_path = icon_dir.joinpath("procno.png")

    if uninstall:
        os.remove(installed_script_path)
        info(f'removed {installed_script_path.as_posix()}')
        os.remove(desktop_definition_path)
        info(f'removed {desktop_definition_path.as_posix()}')
        os.remove(icon_path)
        info(f'removed {icon_path.as_posix()}')
        return

    if installed_script_path.exists():
        warning(f"skipping installation of {installed_script_path.as_posix()}, it is already present.")
    else:
        source = open(__file__).read()
        source = source.replace("#!/usr/bin/python3", '#!' + sys.executable)
        info(f'creating {installed_script_path.as_posix()}')
        open(installed_script_path, 'w').write(source)
        info(f'chmod u+rwx {installed_script_path.as_posix()}')
        os.chmod(installed_script_path, stat.S_IRWXU)

    if desktop_definition_path.exists():
        warning(f"skipping installation of {desktop_definition_path.as_posix()}, it is already present.")
    else:
        info(f'creating {desktop_definition_path.as_posix()}')
        desktop_definition = textwrap.dedent(f"""
            [Desktop Entry]
            Type=Application
            Exec={installed_script_path.as_posix()}
            Name=procno
            GenericName=procno
            Comment=A process monitor with DBUS Freedesktop-Notifications. Like top, but not as we know it.
            Icon={icon_path.as_posix()}
            Categories=Qt;System;Monitor;System;
            """)
        open(desktop_definition_path, 'w').write(desktop_definition)

    if icon_path.exists():
        warning(f"skipping installation of {icon_path.as_posix()}, it is already present.")
    else:
        info(f'creating {icon_path.as_posix()}')
        create_pixmap_from_svg_bytes(SVG_PROGRAM_ICON).save(icon_path.as_posix())

    info('installation complete. Your desktop->applications->system should now contain procno')


def parse_args():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="A process monitor.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.epilog = textwrap.dedent(f"""
            """)
    parser.add_argument('--detailed-help', default=False, action='store_true',
                        help='Detailed help (in markdown format).')
    parser.add_argument('--debug', default=False, action='store_true', help='enable debug output to stdout')
    parser.add_argument('--install', action='store_true',
                        help="installs the procno application in the current user's path and desktop application menu.")
    parser.add_argument('--uninstall', action='store_true',
                        help='uninstalls the procno application menu file and script for the current user.')
    parsed_args = parser.parse_args(args=args)
    if parsed_args.install:
        install_as_desktop_application()
        sys.exit()
    if parsed_args.uninstall:
        install_as_desktop_application(uninstall=True)
        sys.exit()
    if parsed_args.detailed_help:
        print(__doc__)
        sys.exit()


def get_config_path() -> Path:
    program_name = get_program_name()
    config_dir_path = Path.home().joinpath('.config').joinpath(program_name)
    if not config_dir_path.parent.is_dir() or not config_dir_path.is_dir():
        os.makedirs(config_dir_path)
    path = config_dir_path.joinpath(program_name + '.conf')
    return path


class Config(configparser.ConfigParser):

    def __init__(self):
        super().__init__()
        self.path = get_config_path()
        debug("config=", self.path) if debugging else None
        self.modified_time = 0.0
        self.read_string(DEFAULT_CONFIG)

    def save(self):
        if self.path.exists():
            self.path.rename(self.path.with_suffix('.bak'))
        with self.path.open('w') as config_file:
            self.write(config_file)

    def refresh(self) -> bool:
        if self.path.is_file():
            modified_time = self.path.lstat().st_mtime
            if self.modified_time == modified_time:
                return False
            self.modified_time = modified_time
            info(f"Config: reading {self.path}")
            config_text = self.path.read_text()
            for section in ['colors', ]:
                self.remove_section(section)
            self.read_string(config_text)
            for section in ['options', 'colors', ]:
                if section not in self:
                    self[section] = {}
            global_colors.copy_from_config(self['colors'])
            return True
        if self.modified_time > 0.0:
            info(f"Config file has been deleted: {self.path}")
            self.modified_time = 0.0
        return False

    def is_different(self, other: 'Config'):
        try:
            io1 = StringIO()
            self.write(io1)
            io2 = StringIO()
            other.write(io2)
            return io1.getvalue() != io2.getvalue()
        finally:
            io1.close()
            io2.close()


def is_dark_theme():
    # Heuristic for checking for a dark theme.
    # Is the sample text lighter than the background?
    label = QLabel("am I in the dark?")
    text_hsv_value = label.palette().color(QPalette.WindowText).value()
    bg_hsv_value = label.palette().color(QPalette.Background).value()
    dark_theme_found = text_hsv_value > bg_hsv_value
    # debug(f"is_dark_them text={text_hsv_value} bg={bg_hsv_value} is_dark={dark_theme_found}") if debugging else None
    return dark_theme_found


def create_image_from_svg_bytes(svg_str: bytes) -> QImage:
    """There is no QIcon option for loading QImage from a string, only from a SVG file, so roll our own."""
    if is_dark_theme():
        svg_str = svg_str.replace(SVG_LIGHT_THEME_COLOR, SVG_DARK_THEME_COLOR)
    renderer = QSvgRenderer(svg_str)
    image = QImage(64, 64, QImage.Format_ARGB32)
    image.fill(0x0)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    return image


def create_pixmap_from_svg_bytes(svg_str: bytes) -> QPixmap:
    """There is no QIcon option for loading SVG from a string, only from a SVG file, so roll our own."""
    image = create_image_from_svg_bytes(svg_str)
    return QPixmap.fromImage(image)


def create_icon_from_svg_bytes(default_svg: bytes = None,
                               on_svg: bytes = None, off_svg: bytes = None,
                               disabled_svg: bytes = None) -> QIcon:
    """There is no QIcon option for loading SVG from a string, only from a SVG file, so roll our own."""
    if default_svg is not None:
        icon = QIcon(create_pixmap_from_svg_bytes(default_svg))
    else:
        icon = QIcon()
    if on_svg is not None:
        icon.addPixmap(create_pixmap_from_svg_bytes(on_svg), state=QIcon.On)
    if off_svg is not None:
        icon.addPixmap(create_pixmap_from_svg_bytes(off_svg), state=QIcon.Off)
    if disabled_svg:
        icon = QIcon(create_pixmap_from_svg_bytes(on_svg), mode=QIcon.Disabled)
    return icon


def get_icon(source) -> QIcon:
    # Consider caching icon loading - but icons are mutable and subject to theme changes,
    # so perhaps that's asking for trouble.
    if isinstance(source, str):
        return QIcon.fromTheme(source)
    if isinstance(source, bytes):
        return create_icon_from_svg_bytes(source)
    raise ValueError(f"get_icon parameter has unsupported type {type(source)} = {str(source)}")


class NotifyFreeDesktop:
    NO_MORE_NOTIFICATIONS = -1

    def __init__(self, action_request_handler: callable):
        self.notify_interface = dbus.Interface(
            object=dbus.SessionBus(mainloop=DBusGMainLoop(set_as_default=True)).get_object(
                "org.freedesktop.Notifications",
                "/org/freedesktop/Notifications"),
            dbus_interface="org.freedesktop.Notifications")

        self.message_id_map: Mapping[int, object] = {}
        self.capabilities = [str(cap) for cap in self.notify_interface.GetCapabilities()]
        self.supports_persistence = 'persistence' in self.capabilities
        # Persistence and actions together don't seem to always play well - can corrupt the DBUS notifications service.
        self.supports_actions = not self.supports_persistence and 'actions' in self.capabilities
        self.supports_actions = 'actions' in self.capabilities
        debug('notify_interface.GetCapabilities', self.capabilities)

        def notification_closed_handler(*args, **kwargs):
            message_id = args[0]
            debug('notification_closed_handler', message_id)
            if message_id in self.message_id_map:
                debug("close for message_id", message_id)
                del self.message_id_map[message_id]

        def notification_action_invoked_handler(*args, **kwargs):
            message_id = args[0]
            debug('notification_action_invoked_handler', message_id)
            if message_id in self.message_id_map:
                action_id = args[1]
                debug("action for message_id", message_id, action_id)
                action_request_handler(action_id, self.message_id_map[message_id])

        self.notify_interface.connect_to_signal("NotificationClosed", notification_closed_handler)
        self.notify_interface.connect_to_signal("ActionInvoked", notification_action_invoked_handler)

    def notify_desktop(self, app_name: str, summary: str, message: str,
                       timeout: int, replace_id: int = 0, action_requests=[], context: object = None) -> int:
        if self.notify_interface is None:
            return -1
        # https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html
        notification_icon = 'dialog-error'
        # extra_hints = {"urgency": 1, "sound-name": "dialog-warning", }
        # Urgency of 2 cannot time out.
        extra_hints = {"urgency": '2'}
        if replace_id != 0:
            if not self.supports_persistence:
                # No persistence, do not update the existing message (it will probably just generate a duplicate)
                return NotifyFreeDesktop.NO_MORE_NOTIFICATIONS
            if replace_id not in self.message_id_map:
                # user has dismissed this message, do not update a message which no longer exists
                return NotifyFreeDesktop.NO_MORE_NOTIFICATIONS
        if len(action_requests) > 0 and not self.supports_actions:
            action_requests = []
        message_id = self.notify_interface.Notify(app_name,
                                                  replace_id,
                                                  notification_icon,
                                                  escape(summary).encode('UTF-8'),
                                                  escape(message).encode('UTF-8'),
                                                  action_requests,
                                                  extra_hints,
                                                  timeout)
        debug("notification_id ", message_id, "replace_id", replace_id)
        self.message_id_map[message_id] = context
        return message_id


class ProcessInfo:
    def __init__(self, process: psutil.Process, new_process: bool):
        self.last_update = time.time()
        self.pid = process.pid
        self.real_uid, self.effective_uid, _ = process.uids()
        try:
            self.cmdline = process.cmdline()
        except psutil.ZombieProcess:
            self.cmdline = "(zombie)"
        self.comm = process.name()
        cpu_times = process.cpu_times()
        self.utime = cpu_times.user
        self.stime = cpu_times.system
        self.rss = process.memory_info().rss
        self.start_time = time.localtime(process.create_time())
        self.start_time_text = time.strftime("%Y-%m-%d %H:%M:%S", self.start_time)
        self.end_time_text = None
        self.cpu_diff = 0
        self.rss_diff = 0
        self.current_cpu_percent = 0.0
        self.read_count = 0
        self.write_count = 0
        self.read_diff = 0
        self.write_diff = 0
        self.uss = 0
        self.shared = 0
        self.io_accessible = True
        if io_indicators_enabled:
            self.read_count, self.write_count = self.access_io_counters(process)
        self.uss_accessible = True
        if uss_enabled:
            self.uss = self.access_uss(process)
        self.new_process = new_process
        self.cpu_burn_seconds = 0
        self.rss_growing_seconds = 0
        self.incidents = {}
        self.rss_current_percent_of_system_vm = 100.0 * self.rss / system_vm_bytes
        try:
            self.username = pwd.getpwuid(int(self.real_uid)).pw_name
            if self.effective_uid != self.real_uid:
                self.effective_username = pwd.getpwuid(int(self.effective_uid)).pw_name
            else:
                self.effective_username = None
        except KeyError:
            self.username = '<no name>'
            self.effective_username = None
        self.user_color = None
        self.alive = True
        self.psutil_process = process

    def updated(self, process: psutil.Process, cpu_burn_ratio, rss_exceeded_mbytes):
        # Trying to be frugal, not copying to a new ProcInfo, might mean the GUI sees the object as it's
        # being updated - no great sin?
        self.new_process = False
        now = time.time()
        elapsed_seconds = now - self.last_update
        self.last_update = now
        cpu_times = process.cpu_times()
        utime = cpu_times.user
        stime = cpu_times.system
        cpu_diff = (utime + stime) - (self.utime + self.stime)
        rss = process.memory_info().rss
        rss_diff = rss - self.rss
        self.utime = utime
        self.stime = stime
        self.rss = rss
        self.cpu_diff = cpu_diff
        self.read_diff = 0
        self.write_diff = 0
        if shared_enabled:
            self.shared = process.memory_info().shared
        if uss_enabled and self.uss_accessible:
            self.uss = self.access_uss(process)
        if io_indicators_enabled and self.io_accessible:
            read_count, write_count = self.access_io_counters(process)
            self.read_diff = read_count - self.read_count
            self.write_diff = write_count - self.write_count
            self.read_count = read_count
            self.write_count = write_count

        # Don't do unnecessary expensive math - this is called a lot.
        self.current_cpu_percent = 0.0 if cpu_diff == 0 else math.ceil(100.0 * cpu_diff / elapsed_seconds)
        # if self.current_cpu_percent > 95:
        #    print(self.pid, self.current_cpu_percent, cpu_diff / system_ticks_per_second, elapsed_seconds)
        if self.current_cpu_percent >= cpu_burn_ratio:
            self.cpu_burn_seconds += elapsed_seconds
        else:
            self.cpu_burn_seconds = 0

        self.rss_diff = rss_diff
        # Don't do unnecessary expensive math - this is called a lot.
        if self.rss_diff != 0:
            self.rss_current_percent_of_system_vm = 100.0 * self.rss / system_vm_bytes
        if rss_diff > 0 and rss > rss_exceeded_mbytes * 1_000_000:
            self.rss_growing_seconds += elapsed_seconds
        else:
            self.rss_growing_seconds = 0
        return self

    def access_io_counters(self, process):
        try:
            io_counters = process.io_counters()
            return io_counters.read_count, io_counters.write_count
        except psutil.AccessDenied:
            self.io_accessible = False
        return 0, 0

    def access_uss(self, process):
        try:
            return process.memory_full_info().uss
        except psutil.AccessDenied:
            self.uss_accessible = False
        return 0

    def text(self, compact: bool = False):
        cmdline_text = str(self.cmdline)
        if compact and len(cmdline_text) > 30:
            cmdline_text = cmdline_text[0:30] + '..'
        report_io = io_indicators_enabled and (self.read_count > 0 or self.write_count > 0)
        finished = ' \u25b7Finished\u25c1' if not self.alive else ''
        return \
            f"PID: {self.pid}{finished}\ncomm: {self.comm}\n" \
            f"cmdline: {cmdline_text}\n" + \
            f"CPU: {self.current_cpu_percent:2.0f}% utime: {self.utime} stime: {self.stime}\n" + \
            f"RSS/MEM: {self.rss_current_percent_of_system_vm:5.2f}% rss: {self.rss / 1_000_000:.3f} Mbytes\n" + \
            (f"USS: {self.uss}\n" if uss_enabled else '') + \
            (f"Shared: {self.shared}\n" if shared_enabled else '') + \
            (f"Reads: {self.read_count} Writes: {self.write_count}\n" if report_io else '') + \
            f"Started: {self.start_time_text}\n" + \
            (f"Finished {self.end_time_text}\n" if not self.alive else '') + \
            f"Real_UID: {self.real_uid} User={self.username}" + \
            ('' if self.effective_uid == self.real_uid else f"\nEffective_UID: {self.effective_uid}") + \
            ('' if self.effective_username is None else f" Effective_User={self.effective_username}")

    def __str__(self):
        return self.text()


class GenericIncident:
    def __init__(self, watcher: "ProcessWatcher", proc_info: ProcessInfo):
        self.proc_info = proc_info
        self.short_name = self.proc_info.comm if self.proc_info.comm != '' else self.proc_info.cmdline
        if len(self.short_name) > 20:
            self.short_name = self.short_name[0:18] + '..'
        self.duration_seconds = 0.0
        self.watcher = watcher
        self.incident_notification_suppressed = False
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.ceased = False
        self.notify_id = 0
        self.title_cause = None
        self.summary_cause = None
        self.message_cause = None

    def incident_type(self):
        pass

    def format_state(self):
        return tr("finished") if not self.proc_info.alive else (tr("ongoing") if not self.ceased else tr("ceased"))

    def format_notification(self) -> (str, str, str):
        pass

    def update(self, duration_seconds: int):
        self.duration_seconds = duration_seconds


class CpuBurnIncident(GenericIncident):
    def __init__(self, watcher: "ProcessWatcher", proc_info: ProcessInfo):
        super().__init__(watcher, proc_info)

    def format_notification(self) -> (str, str, str):
        app_name = "\u25b3 CPU consumption [{}]".format(self.short_name)
        summary = tr("\u25b6PID={} [{}] High CPU consumption.").format(self.proc_info.pid, self.short_name)
        message = tr(
            "CPU > {:.0f}% for {:.0f} seconds ({}).\npid={}\ncomm={}\ncmdline={}\nIncident started at {}").format(
            self.watcher.notify_cpu_use_percent,
            self.duration_seconds,
            self.format_state(),
            self.proc_info.pid,
            self.proc_info.comm,
            ' '.join(self.proc_info.cmdline),
            self.start_time)
        return app_name, summary, message


class RssGrowingIncident(GenericIncident):
    def __init__(self, watcher: "ProcessWatcher", proc_info: ProcessInfo):
        super().__init__(watcher, proc_info)

    def format_notification(self) -> (str, str, str):
        app_name = "\u25b3 rss growth [{}]".format(self.short_name)
        # \U0001F4C8
        summary = tr("\u25b6PID={} [{}] High rss growth.").format(self.proc_info.pid, self.short_name)
        message = tr(
            "rss has been growing for {:.0f} seconds ({})\nRSS={:.0f} Mbytes. {:0.1f}% of memory\n"
            "pid={}\ncomm={}\ncmdline={}\nIncident started at  {}").format(
            self.duration_seconds,
            self.format_state(),
            self.proc_info.rss / 1_000_000.0,
            self.proc_info.rss_current_percent_of_system_vm,
            self.proc_info.pid,
            self.proc_info.comm,
            ' '.join(self.proc_info.cmdline),
            self.start_time)
        return app_name, summary, message


class ProcessWatcher:

    def __init__(self, supervisor: 'ProcessWatcherTask', action_request_handler: callable):
        self.config = Config()
        self.polling_millis: int = 2_000
        self._stop = False
        self.supervisor = supervisor
        self.notifications_enabled = True
        self.notification_timeout_millis = 30_000
        self.notify_cpu_use_percent = 1.0
        self.notify_cpu_use_seconds = 30
        self.notify_rss_exceeded_mbytes = 1000
        self.notify_rss_growing_seconds = 10
        self.notification_updates_enabled = False
        self.notification_actions_enabled = False
        self.config.refresh()
        self.past_data: Mapping[int, ProcessInfo] = {}
        self.update_settings_from_config()
        self.action_request_handler = action_request_handler
        self.notifier = None
        self.notifier = self.get_notifier()
        if self.notifier is None:
            alert = QMessageBox()
            alert.setText(tr("Notifier initialisation failed"))
            alert.setInformativeText("Could not initialise a DBUS notifier.")
            alert.setDetailedText("Maybe this desktop is not properly initialised, maybe try restarting procno.")
            alert.setIcon(QMessageBox.Critical)
            alert.exec()
        else:
            if self.notification_updates_enabled and not self.notifier.supports_persistence:
                alert = QMessageBox()
                alert.setText(tr("Ignoring notification_updates_enabled"))
                alert.setInformativeText("This desktop does not support notification persistence.")
                alert.setDetailedText("Supported notification capabilities: {}".format(self.notifier.capabilities))
                alert.setIcon(QMessageBox.Critical)
                alert.exec()
            if self.notification_actions_enabled and not self.notifier.supports_actions:
                alert = QMessageBox()
                alert.setText(tr("Ignoring notification_actions_enabled"))
                alert.setInformativeText("This desktop does not support notification actions.")
                alert.setDetailedText("Supported notification capabilities: {}".format(self.notifier.capabilities))
                alert.setIcon(QMessageBox.Critical)
                alert.exec()

    def is_notifying(self) -> bool:
        return self.notifications_enabled

    def enable_notifications(self, enable: bool):
        self.notifications_enabled = enable

    def update_settings_from_config(self):
        info('ProcessWatcher reading config.')
        self.notifications_enabled = self.config.getboolean(
            'options', 'start_with_notifications_enabled', fallback=False)
        if 'poll_seconds' in self.config['options']:
            self.polling_millis = 1_000 * self.config.getfloat('options', 'poll_seconds')
        if 'notification_seconds' in self.config['options']:
            self.notification_timeout_millis = 1_000 * self.config.getint('options', 'notification_seconds')
        if 'notify_cpu_use_percent' in self.config['options']:
            self.notify_cpu_use_percent = self.config.getint('options', 'notify_cpu_use_percent')
        if 'notify_cpu_use_seconds' in self.config['options']:
            self.notify_cpu_use_seconds = self.config.getint('options', 'notify_cpu_use_seconds')
        if 'notify_rss_exceeded_mbytes' in self.config['options']:
            self.notify_rss_exceeded_mbytes = self.config.getint('options', 'notify_rss_exceeded_mbytes')
        if 'notify_rss_growing_seconds' in self.config['options']:
            self.notify_rss_growing_seconds = self.config.getint('options', 'notify_rss_growing_seconds')
        global io_indicators_enabled
        io_indicators_enabled = self.config.getboolean(
            'options', 'io_indicators_enabled', fallback=False)
        global uss_enabled
        uss_enabled = self.config.getboolean(
            'options', 'uss_enabled', fallback=False)
        global shared_enabled
        shared_enabled = self.config.getboolean(
            'options', 'shared_enabled', fallback=False)
        self.notification_updates_enabled = self.config.getboolean(
            'options', 'notification_updates_enabled', fallback=False)
        self.notification_actions_enabled = self.config.getboolean(
            'options', 'notification_actions_enabled', fallback=False)
        if 'debug' in self.config['options']:
            global debugging
            debugging = self.config.getboolean('options', 'debug')
            info("Debugging output is disabled.") if not debugging else None

    def is_stop_requested(self) -> bool:
        return self.supervisor.isInterruptionRequested()

    def watch_processes(self):
        self._stop = False
        initialised = len(self.past_data) != 0
        while True:
            if self.is_stop_requested():
                return
            try:
                if self.config.refresh():
                    self.update_settings_from_config()
                    initialised = False
                data = self.process_psutil_info(initialised)
                initialised = True
                self.supervisor.new_data(data)
            except Exception as e:
                error("watch process handled exception:", e)
                pass
            time.sleep(self.polling_millis / 1000)

    def process_psutil_info(self, initialised):
        data = []
        dead_set = set(self.past_data.keys())
        for process in psutil.process_iter():
            with process.oneshot():
                pid = process.pid
                if pid in self.past_data:
                    dead_set.remove(pid)
                    proc_info = self.past_data[pid].updated(
                        process,
                        self.notify_cpu_use_percent, self.notify_rss_exceeded_mbytes)
                else:
                    proc_info = ProcessInfo(process, initialised)
                    self.past_data[pid] = proc_info

                if proc_info.cpu_burn_seconds >= self.notify_cpu_use_seconds:
                    self.handle_incident(proc_info, CpuBurnIncident, proc_info.cpu_burn_seconds)
                elif CpuBurnIncident in proc_info.incidents:
                    self.finish_incident(proc_info, CpuBurnIncident)

                if proc_info.rss_growing_seconds >= self.notify_rss_growing_seconds:
                    self.handle_incident(proc_info, RssGrowingIncident, proc_info.rss_growing_seconds)
                elif RssGrowingIncident in proc_info.incidents:
                    self.finish_incident(proc_info, RssGrowingIncident)

                data.append(proc_info)
        self.cleanup_dead_processes(dead_set)
        return data

    def cleanup_dead_processes(self, dead_set):
        for pid in dead_set:
            dead_process = self.past_data[pid]
            dead_process.alive = False
            dead_process.end_time_text = time.strftime("%Y-%m-%d %H:%M:%S")
            if CpuBurnIncident in dead_process.incidents:
                debug("dead process", dead_process.pid, dead_process.incidents)
                self.finish_incident(dead_process, CpuBurnIncident)
            if RssGrowingIncident in dead_process.incidents:
                debug("dead process", dead_process.pid, dead_process.incidents)
                self.finish_incident(dead_process, RssGrowingIncident)
            del (self.past_data[pid])

    def handle_incident(self, proc_info: ProcessInfo, incident_type, duration_seconds: int):
        incident = proc_info.incidents[incident_type] if incident_type in proc_info.incidents else None
        if incident is None:
            incident = incident_type(self, proc_info)
            proc_info.incidents[incident_type] = incident
        incident.update(duration_seconds)
        self.notify(incident)

    def finish_incident(self, proc_info: ProcessInfo, incident_type: str):
        debug("Incident finished")
        incident = proc_info.incidents[incident_type] if incident_type in proc_info.incidents else None
        if incident is not None:
            incident.ceased = True
            self.notify(incident)
            del proc_info.incidents[incident_type]

    def notify(self, incident: CpuBurnIncident):
        if self.notifications_enabled:
            if not incident.incident_notification_suppressed:
                if incident.notify_id > 0 and not self.notification_updates_enabled:
                    return
                notifier = self.get_notifier()
                if notifier is None:
                    return
                try:
                    app_name, summary, message = incident.format_notification()
                    debug("replace_id", incident.notify_id, message)
                    notify_id = notifier.notify_desktop(
                        app_name=app_name,
                        summary=summary,
                        message=message,
                        timeout=self.notification_timeout_millis,
                        replace_id=incident.notify_id,
                        action_requests=['info', tr('More Info')] if self.notification_actions_enabled else [],
                        context=incident)
                    if incident.notify_id == NotifyFreeDesktop.NO_MORE_NOTIFICATIONS:
                        debug("Incident suppressed", notify_id)
                        incident.incident_notification_suppressed = True
                    else:
                        incident.notify_id = notify_id
                except dbus.exceptions.DBusException as e:
                    self.notifier = None
                    self.supervisor.signal_error.emit(ERROR_DBUS_NOTIFICATION_FAILED, e)

    def get_notifier(self) -> NotifyFreeDesktop:
        if self.notifier is None:
            try:
                def incident_notification_action_handler(action_id: int, incident: GenericIncident):
                    self.action_request_handler(action_id, incident.proc_info)
                self.notifier = NotifyFreeDesktop(incident_notification_action_handler)
            except dbus.exceptions.DBusException as e:
                self.supervisor.signal_error.emit(ERROR_DBUS_NOTIFICATIONS_UNAVAILABLE, e)
                self.notifications_enabled = False
        return self.notifier

    def state_of_activity(self, ongoing: bool):
        if self.notification_updates_enabled:
            return tr(" (continues)") if ongoing else " (ceased)"
        return ''


class ProcessWatcherTask(QThread):
    signal_new_data = pyqtSignal(list)
    signal_error = pyqtSignal(str, Exception)
    signal_action_request = pyqtSignal(str, object)

    def __init__(self) -> None:
        super().__init__()

        def action_request_handler(action_id: str, process_info: ProcessInfo):
            self.signal_action_request.emit(action_id, process_info)

        self.watcher = ProcessWatcher(self, action_request_handler=action_request_handler)

    def run(self) -> None:
        self.watcher.watch_processes()

    def new_data(self, data: Mapping):
        self.signal_new_data.emit(data)

    def is_notifying(self) -> bool:
        return self.watcher.is_notifying()

    def enable_notifications(self, enable: bool):
        self.watcher.enable_notifications(enable)


def big_label(label: QLabel) -> QLabel:
    # Setting the style breaks theme changes, use HTML instead
    # widget.setStyleSheet("QLabel { font-weight: normal;font-size: 12pt; }")
    label.setTextFormat(Qt.TextFormat.AutoText)
    label.setText(f"<b>{label.text()}</b>")
    return label


class DialogSingletonMixin:
    """
    A mixin that can augment a QDialog or QMessageBox with code to enforce a singleton UI.
    For example, it is used so that only ones settings editor can be active at a time.
    """
    _dialogs_map = {}
    debug = False

    def __init__(self) -> None:
        """Registers the concrete class as a singleton so it can be reused later."""
        super().__init__()
        class_name = self.__class__.__name__
        if class_name in DialogSingletonMixin._dialogs_map:
            raise TypeError(f"ERROR: More than one instance of {class_name} cannot exist.")
        if DialogSingletonMixin.debug:
            debug(f'SingletonDialog created for {class_name}') if debugging else None
        DialogSingletonMixin._dialogs_map[class_name] = self

    def closeEvent(self, event) -> None:
        """Subclasses that implement their own closeEvent must call this closeEvent to deregister the singleton"""
        class_name = self.__class__.__name__
        if DialogSingletonMixin.debug:
            debug(f'SingletonDialog remove {class_name}') if debugging else None
        del DialogSingletonMixin._dialogs_map[class_name]
        event.accept()

    def make_visible(self):
        """
        If the dialog exists(), call this to make it visible by raising it.
        Internal, used by the class method show_existing_dialog()
        """
        self.show()
        self.raise_()
        self.activateWindow()

    @classmethod
    def show_existing_dialog(cls: Type):
        """If the dialog exists(), call this to make it visible by raising it."""
        class_name = cls.__name__
        if DialogSingletonMixin.debug:
            debug(f'SingletonDialog show existing {class_name}') if debugging else None
        instance = DialogSingletonMixin._dialogs_map[class_name]
        instance.make_visible()

    @classmethod
    def exists(cls: Type) -> bool:
        """Returns true if the dialog has already been created."""
        class_name = cls.__name__
        if DialogSingletonMixin.debug:
            debug(
                f'SingletonDialog exists {class_name} {class_name in DialogSingletonMixin._dialogs_map}') if debugging else None
        return class_name in DialogSingletonMixin._dialogs_map


class AboutDialog(QMessageBox, DialogSingletonMixin):

    @staticmethod
    def invoke():
        if AboutDialog.exists():
            AboutDialog.show_existing_dialog()
        else:
            AboutDialog()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('About'))
        self.setTextFormat(Qt.AutoText)
        self.setText(tr('About procno'))
        self.setInformativeText(tr(ABOUT_TEXT))
        self.setIcon(QMessageBox.Information)
        self.exec()


class HelpDialog(QDialog, DialogSingletonMixin):

    @staticmethod
    def invoke():
        if HelpDialog.exists():
            HelpDialog.show_existing_dialog()
        else:
            HelpDialog()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('Help'))
        layout = QVBoxLayout()
        markdown_view = QTextEdit()
        markdown_view.setReadOnly(True)
        markdown_view.setMarkdown(__doc__)
        layout.addWidget(markdown_view)
        self.setLayout(layout)
        # TODO maybe compute a minimum from the actual screen size or use geometry
        self.setMinimumWidth(1400)
        self.setMinimumHeight(1000)
        # .show() is non-modal, .exec() is modal
        self.make_visible()


class OptionsPanel(QWidget):

    def __init__(self, config_section: Mapping[str, str], parent: QWidget = None):
        super().__init__(parent=parent)
        self.option_map: Mapping[str, QWidget] = {}
        grid_layout = QGridLayout(self)
        bool_count = 0
        text_count = 0
        for i, option_spec in enumerate(CONFIG_OPTIONS_LIST):
            option_id = option_spec.option_id
            value = config_section[option_id] if option_id in config_section else ''
            label_widget = QLabel(option_spec.label())
            label_widget.setToolTip(option_spec.tooltip())
            if option_id.endswith("_enabled"):
                input_widget = QCheckBox()
                input_widget.setChecked(value == 'yes')
                input_widget.setToolTip(option_spec.tooltip())
                column_number = 3
                row_number = bool_count
                bool_count += 1
            else:
                input_widget = QLineEdit()
                input_widget.setMaximumWidth(100)
                input_widget.setText(value)
                if option_spec.int_range is not None:
                    input_widget.setValidator(QIntValidator(option_spec.int_range[0], option_spec.int_range[1]))
                else:
                    input_widget.setValidator(QIntValidator(1, 100000))
                input_widget.setToolTip(option_spec.tooltip())
                column_number = 0
                row_number = text_count
                text_count += 1
            grid_layout.addWidget(label_widget, row_number, column_number)
            grid_layout.addWidget(input_widget, row_number, column_number + 1, 1, 1, alignment=Qt.AlignLeft)
            self.option_map[option_id] = input_widget
            if column_number == 0:
                spacer = QLabel("\u2003\u2003")
                grid_layout.addWidget(spacer, row_number, 2)
        scroll_area = QScrollArea(self)
        container = QWidget(scroll_area)
        container.setLayout(grid_layout)
        scroll_area.setWidget(container)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        grid_layout.setHorizontalSpacing(20)
        self.setLayout(layout)

    def copy_from_config(self, config_section: Mapping[str, str]):
        for option_id, widget in self.option_map.items():
            if option_id in config_section:
                if option_id.endswith("_enabled"):
                    widget.setChecked(config_section[option_id].lower() == "yes")
                else:
                    widget.setText(config_section[option_id])

    def copy_to_config(self, config_section: Mapping[str, str]):
        for option_id, widget in self.option_map.items():
            if option_id.endswith("_enabled"):
                config_section[option_id] = "yes" if widget.isChecked() else "no"
            else:
                if widget.text().strip() != "":
                    config_section[option_id] = widget.text()


class ColorPalette:
    def __init__(self):
        self.user_color_map: Mapping[int, QColor] = {}
        self.cpu_activity_color = QColor(0x3491e1)
        self.rss_color = QColor(0x000000)
        self.uss_color = QColor(0xff0000)
        self.shared_color = QColor(0xffc800)
        self.read_indicator_color = QColor(0x00aa00)
        self.write_indicator_color = QColor(0xff0000)
        self.new_process_color = QColor(0xf8b540)
        self.search_match_color = QColor(0x00aa00)
        self.root_user_color = QColor(0xe2e2e2)

        # Starting colors, when they run out we use a random selection
        self.default_user_colors_hex = [QColor(c) for c in
                                        [0xb4beee, 0x67dcb9, 0xb2eae2, 0xb2d7c7, 0xd7d3b9, 0xd9c1d9, 0xdad1c4, 0xa4e805,
                                         0xf0c6a1, 0xc0d3ee, 0xb5c3f0, 0xa7dbee, 0xb5c3f0, 0xffaaff]]

    def to_hex(self, color: QColor) -> str:
        return color.name()

    def set_color(self, name: str, hex_str: str):
        if name.startswith('user_'):
            self.user_color_map[name[len('user_'):]] = QColor(hex_str)
        else:
            self.__setattr__(name, QColor(hex_str))

    def get_color_map(self) -> Mapping[str, str]:
        return {
            **{n: self.to_hex(v) for n, v in self.__dict__.items() if n.endswith('_color')},
            **{'user_' + n: self.to_hex(v) for n, v in self.user_color_map.items()}
        }

    def choose_user_color(self, real_uid) -> QColor:
        username = pwd.getpwuid(int(real_uid)).pw_name
        if real_uid == 0:
            return self.root_user_color

        if username in self.user_color_map:
            return self.user_color_map[username]

        used_colors = self.user_color_map.values()
        while len(self.default_user_colors_hex) != 0:
            color = QColor(self.default_user_colors_hex[0])
            self.default_user_colors_hex = self.default_user_colors_hex[1:]
            if color not in used_colors:
                self.user_color_map[username] = color
                return color

        r, g, b = random_color((0xc0, 0xd3, 0xee), seed=real_uid)
        color = QColor(r, g, b)
        self.user_color_map[username] = color
        return color

    def copy_from_config(self, config_section: Mapping[str, str]):
        for name, value in config_section.items():
            self.set_color(name, value.replace("0x", "#"))

    def copy_to_config(self, config_section: Mapping[str, str]):
        for name, value in self.get_color_map():
            config_section[name] = value.repace("#", "0x")


global_colors = ColorPalette()


def add_color_swatch(color_label: QPushButton, value: str):
    color_label.setPPixmap(create_pixmap_from_svg_bytes(
        SVG_COLOR_SWATCH.replace(b'#000000', value.encode('UTF-8'))))
    return color_label


class ColorEditor:
    def __init__(self, parent: QWidget, color_name: str, hex_str: str):
        tip = tr("Click on a color swatch to bing up the color selection dialog.")
        self.color = QColor(hex_str)
        self.color_name_label = QLabel(color_name)
        self.color_name_label.setToolTip(tip)

        def dialog_color_selected(color: QColor):
            self.color = color
            self.set_swatch_color(color)
            self.input_widget.setText(color.name())

        dialog = QColorDialog(parent)
        dialog.colorSelected.connect(dialog_color_selected)

        def show_color_chooser():
            dialog.setCurrentColor(self.color)
            dialog.show()

        self.color_swatch = QPushButton()
        self.set_swatch_color(self.color)
        self.color_swatch.clicked.connect(show_color_chooser)
        self.color_swatch.setToolTip(tip)

        def editor_color_changed():
            self.color = QColor(self.input_widget.text())
            self.set_swatch_color(self.color)

        self.input_widget = QLineEdit()
        self.input_widget.setValidator(QRegExpValidator(QRegExp("#[A-Fa-f0-9]{6}")))
        self.input_widget.setText(hex_str)
        self.input_widget.textChanged.connect(editor_color_changed)
        self.input_widget.setToolTip(tip)

    def set_swatch_color(self, color: QColor):
        self.color_swatch.setAutoFillBackground(True)
        palette = self.color_swatch.palette()
        palette.setColor(QPalette.Button, color)
        self.color_swatch.setPalette(palette)
        self.color_swatch.update()


class ColorPalettePanel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.editor_map: Mapping[str, ColorEditor] = {}
        scroll_area = QScrollArea(self)
        container = QWidget(scroll_area)
        self.grid_layout = QGridLayout()
        self.layout_ui(global_colors)
        container.setLayout(self.grid_layout)
        scroll_area.setWidget(container)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def layout_ui(self, color_palette: ColorPalette):
        self.editor_map = {}
        grid_layout = self.grid_layout
        for widget in grid_layout.children():
            self.grid_layout.removeWidget(widget)
        col_sequence = (1, 3, 6)
        row_number = 0
        for i, (color_name, value) in enumerate(color_palette.get_color_map().items()):
            row_number += 2 if i % len(col_sequence) == 0 else 0
            column_number = col_sequence[i % len(col_sequence)]
            color_editor = ColorEditor(self, color_name, value)
            self.editor_map[color_name] = color_editor
            grid_layout.addWidget(color_editor.color_name_label, row_number, column_number, 1, 2,
                                  alignment=Qt.AlignLeft)
            grid_layout.addWidget(color_editor.color_swatch, row_number + 1, column_number)
            grid_layout.addWidget(color_editor.input_widget, row_number + 1, column_number + 1, 1, 1,
                                  alignment=Qt.AlignLeft)
        grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        grid_layout.setHorizontalSpacing(20)

    def copy_from_config(self, config_section: Mapping[str, str]):
        global_colors.copy_from_config(config_section)
        self.layout_ui(global_colors)

    def copy_to_config(self, config_section: Mapping[str, str]):
        for option_id, editor in self.editor_map.items():
            global_colors.set_color(option_id, editor.input_widget.text())
            config_section[option_id] = editor.input_widget.text()


class ConfigWatcherTask(QThread):
    signal_config_change = pyqtSignal()

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    def run(self) -> None:
        while True:
            if self.config.refresh():
                debug("ConfigWatcherTask - Config Changed") if debugging else None
                self.signal_config_change.emit()
            time.sleep(5.0)


class ConfigPanel(QDialog):
    signal_editing_filter_pattern = pyqtSignal(str, bool)

    def __init__(self, config_change_func: Callable):
        super().__init__(parent=None, flags=Qt.WindowFlags(Qt.WindowStaysOnTopHint))
        self.setObjectName('config-panel')

        self.setMinimumHeight(500)
        self.setMinimumWidth(900)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_container = QWidget(self)
        title_layout = QHBoxLayout()
        self.title_layout = title_layout
        title_container.setLayout(title_layout)
        title_label = big_label(QLabel(tr("Configuration")))
        title_layout.addWidget(title_label)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_layout.addWidget(spacer)

        tabs = QTabWidget()
        self.tabs = tabs

        self.config = Config()
        self.config.refresh()

        options_panel = OptionsPanel(self.config['options'], parent=self)
        color_palette_panel = ColorPalettePanel(parent=self)

        button_box = QWidget()
        button_box_layout = QHBoxLayout()
        button_box.setLayout(button_box_layout)
        defaults_button = QPushButton(tr("Defaults"))
        defaults_button.setIcon(get_icon(ICON_DEFAULTS))
        button_box_layout.addWidget(defaults_button)
        spacer = QLabel('          ')
        button_box_layout.addWidget(spacer)
        revert_button = QPushButton(tr("Revert"))
        revert_button.setIcon(get_icon(ICON_REVERT))
        button_box_layout.addWidget(revert_button)
        spacer = QLabel('    ')
        button_box_layout.addWidget(spacer)
        apply_button = QPushButton(tr("Apply"))
        apply_button.setIcon(get_icon(ICON_APPLY))
        button_box_layout.addWidget(apply_button)

        self.status_bar = QStatusBar()
        self.status_bar.addPermanentWidget(button_box)

        def save_action():
            debug("save action") if debugging else None
            tmp = Config()
            options_panel.copy_to_config(tmp['options'])
            color_palette_panel.copy_to_config(tmp['colors'])
            if not self.config.is_different(tmp):
                apply_message = QMessageBox(self)
                apply_message.setText(tr('There are no changes to apply. Apply and save anyway?'))
                apply_message.setIcon(QMessageBox.Question)
                apply_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                if apply_message.exec() == QMessageBox.Cancel:
                    return
            options_panel.copy_to_config(self.config['options'])
            color_palette_panel.copy_to_config(self.config['colors'])
            self.config.save()
            self.status_bar.showMessage(tr("All changes have been saved."), 5000)
            debug(f'config saved ok') if debugging else None
            config_change()

        apply_button.clicked.connect(save_action)

        def revert_action():
            debug("revert") if debugging else None
            tmp = Config()
            options_panel.copy_to_config(tmp['options'])
            color_palette_panel.copy_to_config(tmp['colors'])
            if not self.config.is_different(tmp):
                revert_message = QMessageBox(self)
                revert_message.setText(tr('There are no unapplied changes. There is nothing to revert.'))
                revert_message.setIcon(QMessageBox.Warning)
                revert_message.setStandardButtons(QMessageBox.Ok)
                revert_message.exec()
                return
            else:
                revert_message = QMessageBox(self)
                revert_message.setText(
                    tr("There are changes that haven't been applied. Revert and loose those changes?"))
                revert_message.setIcon(QMessageBox.Question)
                revert_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                if revert_message.exec() == QMessageBox.Cancel:
                    return
            info("Reverting unsaved changes.")
            self.status_bar.showMessage(tr("Unapplied changes have been reverted."), 5000)
            reload_from_config()

        def reload_from_config():
            info("UI reloading config from file.") if debugging else None
            options_panel.copy_from_config(self.config['options'])
            color_palette_panel.copy_from_config(self.config['colors'])

        def defaults_action():
            defaults_message = QMessageBox(self)
            defaults_message.setText(tr("Reset which tabs to defaults?"))
            defaults_message.setIcon(QMessageBox.Question)
            defaults_message.addButton(tr("Options"), QMessageBox.AcceptRole)
            defaults_message.addButton(tr("Colors"), QMessageBox.AcceptRole)
            defaults_message.addButton(tr("Both"), QMessageBox.AcceptRole)
            defaults_message.addButton(QMessageBox.Cancel)
            choice = defaults_message.exec()
            if choice == QMessageBox.Cancel:
                return
            if choice == 0 or choice == 2:
                options_panel.copy_from_config(Config()['options'])
            if choice == 1 or choice == 2:
                tmp_default_palette = ColorPalette()
                color_palette_panel.layout_ui(tmp_default_palette)

        defaults_button.clicked.connect(defaults_action)

        revert_button.clicked.connect(revert_action)

        tabs.addTab(options_panel, tr("Options"))
        tabs.setTabToolTip(0, tr("Application configuration options."))
        tabs.setCurrentIndex(0)

        tabs.addTab(color_palette_panel, tr("Colors"))
        tabs.setTabToolTip(1, tr("Color options."))

        layout.addWidget(title_container)

        layout.addWidget(tabs)
        layout.addWidget(self.status_bar)

        self.setWindowTitle(tr("Configuration"))
        self.adjustSize()

        reload_from_config()

        self.config_watcher = ConfigWatcherTask(self.config)

        def config_change():
            reload_from_config()
            config_change_func()

        self.config_watcher.signal_config_change.connect(config_change)
        self.config_watcher.start()

    def get_config(self) -> Config:
        return self.config


class MainToolBar(QToolBar):

    def __init__(self,
                 run_func: Callable,
                 notify_func: Callable,
                 search_func: Callable,
                 menu: QMenu,
                 parent: 'MainWindow'):
        super().__init__(parent=parent)

        # TODO figure out why this toolbar no longer has an undocking handle.
        debug("Toolbar floatable", self.isFloatable(), "movable", self.isMovable()) if debugging else None

        self.setObjectName("main-tool-bar")
        self.setIconSize(QSize(32, 32))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.icon_run_enabled = get_icon(SVG_TOOLBAR_RUN_ENABLED)
        self.icon_run_disabled = get_icon(SVG_TOOLBAR_RUN_DISABLED)
        self.icon_notifier_enabled = get_icon(SVG_TOOLBAR_NOTIFIER_ENABLED)
        self.icon_notifier_disabled = get_icon(SVG_TOOLBAR_NOTIFIER_DISABLED)
        self.icon_run_stop = get_icon(SVG_TOOLBAR_STOP)

        self.icon_menu = get_icon(SVG_TOOLBAR_HAMBURGER_MENU)

        self.run_action = self.addAction(self.icon_run_enabled, "run", run_func)
        self.run_action.setObjectName("run_button")
        self.run_action.setToolTip(tr("Start/stop monitoring processes."))
        # Stylesheets prevent theme changes for the widget - cannot be used.
        # self.widgetForAction(self.run_action).setStyleSheet("QToolButton { width: 130px; }")

        self.stop_action = self.addAction(self.icon_run_stop, tr("Stop"), run_func)
        self.stop_action.setToolTip(tr("Stop monitoring processes."))

        self.addSeparator()

        self.notifier_action = self.addAction(self.icon_notifier_enabled, "notify", notify_func)
        self.notifier_action.setToolTip(tr("Enable/disable desktop-notification forwarding."))
        self.addSeparator()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        def search_entries(text: str) -> None:
            if self.re_search_enabled:
                try:
                    re.compile(text)
                    parent.statusBar().showMessage('')
                except re.error as e:
                    parent.statusBar().showMessage(str(e))
                    return
            search_func(text, self.re_search_enabled)
            # TODO self.search_select_journal(text, regexp_search=self.re_search_enabled)

        self.re_search_enabled = False
        search_input = QLineEdit()
        search_input.setFixedWidth(350)
        search_input.addAction(get_icon(ICON_SEARCH_PROCESSES), QLineEdit.LeadingPosition)
        re_action = search_input.addAction(get_icon(ICON_PLAIN_TEXT_SEARCH), QLineEdit.TrailingPosition)
        re_action.setCheckable(True)
        search_tip = tr(
            "Incrementally search process com and cmdline.\n"
            "Click the icon in the right margin\nto toggle regexp/plain-text matching.")

        def re_search_toggle(enable: bool):
            self.re_search_enabled = enable
            re_action.setIcon(get_icon(ICON_REGEXP_SEARCH if enable else ICON_PLAIN_TEXT_SEARCH))
            tip = tr("Regular expression matching enabled.") if enable else tr("Plain-text matching enabled.")
            parent.statusBar().showMessage(tip, 5000)
            search_input.setToolTip(search_tip + "\n" + tip)

        re_action.toggled.connect(re_search_toggle)
        search_input.setToolTip(search_tip)
        search_input.textEdited.connect(search_entries)
        search_input.setClearButtonEnabled(True)
        self.addWidget(search_input)

        self.addWidget(spacer)
        self.addAction(get_icon(ICON_HELP_CONTENTS), tr('Help'), HelpDialog.invoke)
        self.addAction(get_icon(ICON_HELP_ABOUT), tr('About'), AboutDialog.invoke)
        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(self.icon_menu)
        self.menu_button.setMenu(menu)
        self.menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.addWidget(self.menu_button)
        self.installEventFilter(self)
        self.setMovable(True)

    def reload_icons(self):
        self.icon_run_enabled = get_icon(SVG_TOOLBAR_RUN_ENABLED)
        self.icon_run_disabled = get_icon(SVG_TOOLBAR_RUN_DISABLED)
        self.icon_run_stop = get_icon(SVG_TOOLBAR_STOP)
        self.icon_notifier_enabled = get_icon(SVG_TOOLBAR_NOTIFIER_ENABLED)
        self.icon_notifier_disabled = get_icon(SVG_TOOLBAR_NOTIFIER_DISABLED)
        self.icon_menu = get_icon(SVG_TOOLBAR_HAMBURGER_MENU)

    def eventFilter(self, target: QObject, event: QEvent) -> bool:
        super().eventFilter(target, event)
        # PalletChange happens after the new style sheet is in use.
        if event.type() == QEvent.PaletteChange:
            debug(f"PaletteChange is_dark_theme()={is_dark_theme()} {str(target)}") if debugging else None
            self.reload_icons()
            self.stop_action.setIcon(self.icon_run_stop)
            self.menu_button.setIcon(self.icon_menu)
        event.accept()
        return True

    def configure_run_action(self, running: bool) -> None:
        debug("Run Style is dark", is_dark_theme()) if debugging else None
        if running:
            self.run_action.setIcon(self.icon_run_enabled)
            self.run_action.setIconText(tr("Running"))
            self.stop_action.setEnabled(True)
        else:
            self.run_action.setIcon(self.icon_run_disabled)
            self.run_action.setIconText(tr("Stopped"))
            self.stop_action.setEnabled(False)

    def configure_notifier_action(self, notifying: bool) -> None:
        padded = pad_text([tr('Notifying'), tr('Mute')])
        if notifying:
            self.notifier_action.setIcon(self.icon_notifier_enabled)
            # self.notifier_action.setIconText(tr("Notifying"))
            self.notifier_action.setIconText(padded[0])
        else:
            self.notifier_action.setIcon(self.icon_notifier_disabled)
            # Don't do this with a style sheet - style sheets will break dark/light theme loading.
            # self.notifier_action.setIconText(tr("Mute   \u2002"))
            self.notifier_action.setIconText(padded[1])

    def configure_filter_actions(self, enable: bool) -> None:
        self.add_filter_action.setEnabled(enable)
        self.del_filter_action.setEnabled(enable)


def pad_text(text_list: List[str]):
    max_width = 0
    width_list = []
    output_list = []
    for text in text_list:
        tmp = QLabel(text)
        tmp.adjustSize()
        width = tmp.fontMetrics().boundingRect(tmp.text()).width()
        if width > max_width:
            # debug(f"text='{text}' New max='{width}'")
            max_width = width
        width_list.append(width)
    for text, width in zip(text_list, width_list):
        if width < max_width:
            space = '\u2002'
            while True:
                spaced = text + space
                tmp2 = QLabel(spaced)
                spaced_width = tmp2.fontMetrics().boundingRect(tmp2.text()).width()
                if spaced_width > max_width:
                    break
                # debug(f"text='{text}' w={spaced_width} max={max_width}")
                text = spaced
        output_list.append(text)
    return output_list


class MainContextMenu(QMenu):

    def __init__(self, run_func: Callable, quit_func: Callable, notify_func: Callable, settings_func: Callable,
                 parent: QWidget):
        super().__init__(parent=parent)
        self.icon_notifier_enabled = get_icon(SVG_TOOLBAR_NOTIFIER_ENABLED)
        self.icon_notifier_disabled = get_icon(SVG_TOOLBAR_NOTIFIER_DISABLED)
        self.icon_edit_config = get_icon(ICON_SETTINGS_CONFIGURE)
        self.listen_action = self.addAction(get_icon(ICON_CONTEXT_MENU_LISTENING_DISABLE),
                                            tr("Stop process monitoring"),
                                            run_func)
        self.notifier_action = self.addAction(self.icon_notifier_disabled,
                                              tr("Disable notifications"),
                                              notify_func)
        self.addSeparator()
        self.edit_config_action = self.addAction(self.icon_edit_config,
                                                 tr("Settings"),
                                                 settings_func)
        self.addSeparator()
        self.addAction(get_icon(ICON_HELP_ABOUT),
                       tr('About'),
                       AboutDialog.invoke)
        self.addAction(get_icon(ICON_HELP_CONTENTS),
                       tr('Help'),
                       HelpDialog.invoke)
        self.addSeparator()
        self.addAction(get_icon(ICON_APPLICATION_EXIT),
                       tr('Quit'),
                       quit_func)

    def configure_run_action(self, running: bool) -> None:
        if running:
            self.listen_action.setText(tr("Stop process monitoring"))
            self.listen_action.setIcon(get_icon(ICON_CONTEXT_MENU_LISTENING_DISABLE))
        else:
            self.listen_action.setText(tr("Resume process monitoring"))
            self.listen_action.setIcon(get_icon(ICON_CONTEXT_MENU_LISTENING_ENABLE))

    def configure_notifier_action(self, notifying: bool) -> None:
        if notifying:
            self.notifier_action.setText(tr("Disable notifications"))
            self.notifier_action.setIcon(self.icon_notifier_disabled)
        else:
            self.notifier_action.setText(tr("Enable notifications"))
            self.notifier_action.setIcon(self.icon_notifier_enabled)


class ProcessControlWidget(QDialog):
    instance_map: Mapping[int, 'ProcessControlWidget'] = {}

    def __init__(self, process_info: ProcessInfo, parent: QWidget):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.Window, True)

        self.process_info = process_info

        layout = QVBoxLayout()
        self.setLayout(layout)

        short_name = process_info.comm if process_info.comm != '' else process_info.cmdline
        if len(short_name) > 20:
            short_name = short_name[0:18] + '..'

        self.setWindowTitle(f"{process_info.pid} {short_name}")

        title = big_label(QLabel("PID {}: {}".format(process_info.pid, short_name)))
        layout.addWidget(title)

        text_view = QTextEdit()
        text_view.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        text_view.setReadOnly(True)
        text_view.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        text_view.setMinimumWidth(800)
        text_view.setMinimumHeight(350)
        text = str(process_info)
        self.text_view = text_view
        self.update_data()
        layout.addWidget(text_view)

        button_box = QWidget()
        button_box_layout = QHBoxLayout()
        button_box.setLayout(button_box_layout)

        def signal_process(sig: int):
            try:
                os.kill(process_info.pid, sig)
            except Exception as e:
                alert = QMessageBox(parent=self)
                alert.setText(tr("Failed to signal PID {}").format(process_info.pid))
                alert.setInformativeText(str(e))
                alert.setIcon(QMessageBox.Critical)
                alert.exec()

        pause_button = QPushButton(tr("Pause"))
        pause_button.setEnabled(False)

        def pause_process():
            signal_process(signal.SIGSTOP)

        pause_button.pressed.connect(pause_process)

        continue_button = QPushButton(tr("Continue"))
        continue_button.setEnabled(False)

        def continue_process():
            signal_process(signal.SIGCONT)

        continue_button.pressed.connect(continue_process)

        signal_label = QLabel(tr("Signal:"))
        signal_label.setEnabled(False)

        allowed_signals = [
            (signal.SIGHUP, tr('SIGHUP (hangup)')),
            (signal.SIGTERM, tr('SIGTERM (terminate)')),
            (signal.SIGINT, tr('SIGINT (interrupt)')),
            (signal.SIGQUIT, tr('SIGQUIT (quit')),
            (signal.SIGKILL, tr('SIGKILL (kill)')),
        ]
        signal_combo_box = QComboBox()
        signal_combo_box.setEnabled(False)
        # signal_combo_box.setCurrentIndex(-1)
        for sig, desc in allowed_signals:
            signal_combo_box.addItem(desc, sig)

        def combo_signal_process(index: int):
            signal_process(signal_combo_box.itemData(index))

        signal_combo_box.activated.connect(combo_signal_process)

        self.safety_default_color = signal_combo_box.palette().color(QPalette.Base)
        self.safety_text_pair = pad_text([tr('Safe'), tr('Armed')])

        def arm_signal_button(enable: bool):
            pause_button.setEnabled(not enable)
            continue_button.setEnabled(not enable)
            signal_combo_box.setEnabled(not enable)
            signal_label.setEnabled(not enable)
            # signal_combo_box.setCurrentIndex(-1)
            safety_catch.setText(self.safety_text_pair[0] if enable else self.safety_text_pair[1])
            palette_copy = safety_catch.palette()
            palette_copy.setColor(QPalette.Base, self.safety_default_color if enable else QColor(255, 0, 0))
            safety_catch.setPalette(palette_copy)

        safety_catch = QCheckBox(tr("Safe     "))
        safety_catch.setChecked(True)
        safety_catch.toggled.connect(arm_signal_button)
        # spacer = QLabel('          ')
        # button_box_layout.addWidget(spacer)

        button_box_layout.addWidget(pause_button)
        button_box_layout.addWidget(continue_button)
        button_box_layout.addWidget(signal_label)
        button_box_layout.addWidget(signal_combo_box)
        button_box_layout.addWidget(safety_catch)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_box_layout.addWidget(spacer)

        close_button = QPushButton(tr("Dismiss"))
        close_button.pressed.connect(self.close)
        button_box_layout.addWidget(close_button)

        layout.addWidget(button_box)
        ProcessControlWidget.instance_map[process_info.pid] = self
        self.pick_geometry(parent)

    def pick_geometry(self, parent: QWidget) -> QRect:
        self.adjustSize()
        pg = parent.geometry()
        g = self.geometry()
        h = g.height() + 70
        # Allow a few instances above or below the main window
        if len(ProcessControlWidget.instance_map) <= pg.width() / g.width():
            if h < pg.y():
                g.setY(pg.y() - h)
                g.setX(pg.x() + (len(ProcessControlWidget.instance_map) - 1) * (g.width() + 10))
                self.setGeometry(g)
                self.adjustSize()
                return
            else:
                sh = QGuiApplication.primaryScreen().geometry().height()
                if h < sh - pg.height():
                    g.setY(pg.y() + pg.height() + 70)
                    g.setX(pg.x() + (len(ProcessControlWidget.instance_map) - 1) * (g.width() + 10))
                    self.setGeometry(g)
                    self.adjustSize()
                    return
        # Fall back to a small offset for each instance.
        offset = 20 * (len(ProcessControlWidget.instance_map) - 1)
        g.setX(pg.x() + (pg.width() - g.width()) // 2 + offset)
        g.setY(pg.y() + (pg.height() - g.height()) // 2 + offset)
        self.setGeometry(g)
        self.adjustSize()
        return

    def update_data(self):
        text = str(self.process_info)
        psutil_process = self.process_info.psutil_process
        try:
            extra_text = "\nOpen Files:"
            for fd_info in psutil_process.open_files():
                extra_text += '\n  ' + str(fd_info)[15:-1]
            extra_text += "\nConnections:"
            for conn_info in psutil_process.connections():
                extra_text += '\n  ' + str(conn_info)[6:-1]
            text += extra_text
        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            pass
        preserve_vscroll = self.text_view.verticalScrollBar().value()
        preserve_hscroll = self.text_view.horizontalScrollBar().value()
        self.text_view.setText(text)
        self.text_view.verticalScrollBar().setValue(preserve_vscroll)
        self.text_view.horizontalScrollBar().setValue(preserve_hscroll)

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            del (ProcessControlWidget.instance_map[self.process_info.pid])
        except KeyError:
            pass
        event.accept()


class ProcessDotsWidget(QLabel):
    signal_new_data = pyqtSignal()

    def __init__(self, config: Config, parent: 'MainWindow'):
        super().__init__(parent=parent)
        self.main_window = parent
        self.setObjectName("process_grid_window")
        self.dot_diameter_key = self.objectName() + ".dot_size"
        self.allocated_position = {}
        self.available_positions = []
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        self.data: List[ProcessInfo] = []
        self.past_data: List[ProcessInfo] = []
        self.dot_diameter = 0
        self.spacing = 0
        self.io_dot_diameter = 0
        self.set_dot_diameter(24)
        self.config = config
        self.show_tips = True
        self.color_of_user_map = {}
        self.row_length = 0
        self.rss_max = 100
        self.pi_over_4 = math.pi / 4
        self.gig_rss = 1_000_000_000  # bytes
        self.gig_ring_diameter = self.spacing * 4
        self.re_target = self.last_re_target = None
        self.setAlignment(Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(False)
        # Minimum sizes are needed to persuade the QScrollArea to provide scrollbars.
        # But minimum sizes break auto-relayout of the dots, so stuff that!
        # self.setMinimumWidth(500)
        # self.setMinimumHeight(500)
        self.setLayout(QVBoxLayout())
        self.rgb = (200, 255, 255)
        self.tree_map = {}
        self.tree_enabled = False
        self.rss_color = global_colors.rss_color
        self.background_color = QColor(0xffffff)
        self.update_settings_from_config(config)
        parent.signal_theme_change.connect(self.apply_theme_change)

    def apply_theme_change(self):
        # print('rssl', self.rss_color.lightness(), self.rss_color.value())
        if is_dark_theme():
            self.background_color = QColor(0x41474d)  # 41474d 1b1e20
            if self.rss_color.lightness() < 128:
                self.rss_color = QColor(0xffffff)
        else:
            self.background_color = QColor(0xffffff)
            if self.rss_color.lightness() > 128:
                self.rss_color = QColor(0x000000)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(palette)

    def set_dot_diameter(self, diameter: int):
        self.dot_diameter = diameter
        self.io_dot_diameter = diameter // 6
        self.spacing = self.spacing = 4 * self.dot_diameter // 3

    def app_save_state(self, settings):
        settings.setValue(self.dot_diameter_key, str(self.dot_diameter))

    def app_restore_state(self, settings):
        debug("app_restore_state") if debugging else None
        value = settings.value(self.dot_diameter_key, None)
        if value is not None:
            debug(f"Restore {self.dot_diameter_key}") if debugging else None
            self.set_dot_diameter(int(settings.value(self.dot_diameter_key, None)))

    def update_settings_from_config(self, config: Config):
        self.config = config
        info('Dot widget clearing cached user colors.')
        for process_info in self.data:
            process_info.user_color = None
        self.tree_enabled = self.config.getboolean('options', 'tree_enabled', fallback=False)
        self.rss_color = global_colors.rss_color
        self.apply_theme_change()

    def update_data(self, data: Mapping):
        self.past_data = self.data
        self.data = data
        if self.isVisible():
            self.update_pixmap()
            self.repaint()
        else:
            pass
            # debug("not visible") if debugging else None
        self.signal_new_data.emit()

    def set_re_match(self, text: str, re_enabled: bool):
        if text is None or len(text) < 2:
            self.re_target = None
        else:
            self.re_target = re.compile(text if re_enabled else re.escape(text))

    def choose_user_color(self, process_info: ProcessInfo) -> QColor:
        if process_info.user_color is not None:
            color = process_info.user_color
        else:
            color = global_colors.choose_user_color(process_info.real_uid)
        # Cache it for quick access
        process_info.user_color = color
        return color

    def tree_coordinates(self, number_of_leaves: int):
        coordinates = []
        leaf_count = 0
        for row_num in range(0, number_of_leaves):
            tree_width = row_num * 2 + 1
            for col_num in range(-tree_width // 2 + 1, tree_width // 2 + 1):
                coordinates.append((row_num + 1, col_num,))
                leaf_count += 1
                if leaf_count >= number_of_leaves:
                    # print(coordinates)
                    coordinates.reverse()
                    return row_num, coordinates
        return 0, coordinates

    def update_pixmap(self):
        if self.data is None or len(self.data) == 0:
            return
        self.row_length = self.width() // self.spacing - 1
        wobble_size = self.dot_diameter // 3

        # rss_ring_area_unit = Area of the Gig ring divided by gig_rss (Kbytes quantity)
        rss_ring_area_unit = self.pi_over_4 * (self.gig_ring_diameter ** 2) / self.gig_rss
        rss_ring_pen = QPen(self.rss_color)
        rss_ring_growing_pen = QPen()
        rss_ring_growing_pen.setWidth(4)
        rss_ring_growing_pen.setColor(QColor(0xff0000))
        rss_ring_pen.setStyle(Qt.DashLine)
        rss_ring_pen.setWidth(2 if self.rss_color.lightness() > 128 else 1)

        match_ring_diameter = self.dot_diameter + 4
        match_highlight_pen = QPen(global_colors.search_match_color)
        match_highlight_pen.setWidth(self.dot_diameter // 6)

        if self.tree_enabled:
            self.tree_map = {}
            row_count, tree_coords = self.tree_coordinates(len(self.data))
            # print(tree_coords)
            pixmap = QPixmap((self.row_length + 1) * self.spacing, self.spacing * (row_count + 3))
        else:
            pixmap = QPixmap((self.row_length + 1) * self.spacing,
                             self.spacing * ((len(self.data) // self.row_length) + 3))
        pixmap.fill(self.background_color)

        dot_painter = QPainter(pixmap)
        match_count = 0

        for i, process_info in enumerate(self.data):
            if self.rss_max < process_info.rss:
                self.rss_max = process_info.rss
            cpu_pp = process_info.current_cpu_percent
            if cpu_pp > 10.0:
                red_intensity = 180 - (int(cpu_pp) if cpu_pp < 100.0 else 100)
                dot_color = QColor(255, red_intensity, red_intensity)
            elif cpu_pp > 0.0:
                dot_color = global_colors.cpu_activity_color
            elif process_info.new_process:
                dot_color = global_colors.new_process_color
            else:
                dot_color = self.choose_user_color(process_info)

            if self.tree_enabled:
                tree_row_num, tree_col_num = tree_coords.pop(0)
                col_num = self.row_length // 2 + tree_col_num
                x = col_num * self.spacing + self.spacing
                y = tree_row_num * self.spacing + self.spacing
                self.tree_map[tree_row_num, col_num] = process_info
            else:
                x = (i % self.row_length) * self.spacing + self.spacing
                y = (i // self.row_length) * self.spacing + self.spacing

            if self.re_target is not None:
                text = str(process_info)
                if self.re_target.search(text) is not None:
                    match_count += 1
                    dot_painter.setPen(match_highlight_pen)
                    dot_painter.setOpacity(1.0)
                    dot_painter.drawEllipse(x - match_ring_diameter // 2, y - match_ring_diameter // 2,
                                            match_ring_diameter, match_ring_diameter)

            # Show a wobble if the rss grew or shrunk.
            if process_info.rss_diff > 0:
                adjust_size = wobble_size
            elif process_info.rss_diff < 0:
                adjust_size = -wobble_size
            else:
                adjust_size = 0

            dot_diameter = self.dot_diameter + adjust_size

            rss_ring_diameter = int(math.sqrt((rss_ring_area_unit * process_info.rss) / self.pi_over_4))

            # if process_info.previous_paint_values != paint_values:
            # Need to paint everything in case the canvas has been cleared for some reason
            dot_painter.setPen(QPen(dot_color))
            dot_painter.setOpacity(1.0)
            dot_painter.setBrush(dot_color)
            dot_painter.drawEllipse(x - dot_diameter // 2, y - dot_diameter // 2, dot_diameter, dot_diameter)

            dot_painter.setPen(rss_ring_pen if process_info.rss_growing_seconds == 0 else rss_ring_growing_pen)
            dot_painter.setBrush(Qt.NoBrush)
            dot_painter.setOpacity(0.4)
            dot_painter.drawEllipse(x - rss_ring_diameter // 2, y - rss_ring_diameter // 2, rss_ring_diameter,
                                    rss_ring_diameter)

            if uss_enabled and process_info.uss != 0:
                uss_ring_diameter = int(math.sqrt((rss_ring_area_unit * process_info.uss) / self.pi_over_4))
                dot_painter.setPen(QPen(global_colors.uss_color))
                dot_painter.setBrush(Qt.NoBrush)
                dot_painter.setOpacity(1.0)
                dot_painter.drawEllipse(x - uss_ring_diameter // 2, y - uss_ring_diameter // 2, uss_ring_diameter,
                                        uss_ring_diameter)

            if shared_enabled:
                shared_ring_diameter = int(math.sqrt((rss_ring_area_unit * process_info.shared) / self.pi_over_4))
                dot_painter.setPen(QPen(global_colors.shared_color))
                dot_painter.setBrush(Qt.NoBrush)
                dot_painter.setOpacity(1.0)
                dot_painter.drawEllipse(x - shared_ring_diameter // 2, y - shared_ring_diameter // 2,
                                        shared_ring_diameter, shared_ring_diameter)

            if io_indicators_enabled:
                if process_info.read_diff != 0:
                    dot_painter.setPen(QPen(global_colors.read_indicator_color))
                    dot_painter.setBrush(global_colors.read_indicator_color)
                    dot_painter.setOpacity(1.0)
                    dot_painter.drawEllipse(x - self.spacing // 2 + self.io_dot_diameter, y - self.spacing // 2,
                                            self.io_dot_diameter, self.io_dot_diameter)
                if process_info.write_diff != 0:
                    dot_painter.setPen(QPen(global_colors.write_indicator_color))
                    dot_painter.setBrush(global_colors.write_indicator_color)
                    dot_painter.setOpacity(1.0)
                    dot_painter.drawEllipse(x + self.spacing // 2 - self.io_dot_diameter * 2, y - self.spacing // 2,
                                            self.io_dot_diameter, self.io_dot_diameter)

            # process_info.previous_paint_values = paint_values
        dot_painter.end()
        self.setPixmap(pixmap)
        if self.re_target is None:
            self.last_re_target = None
        elif self.re_target != self.last_re_target:
            self.main_window.status_bar.showMessage(
                tr("Matched {} processes.").format(match_count) if match_count != 0 else tr("No processes matched."),
                5000)
            self.last_re_target = self.re_target

    def get_process_info(self, event: QMouseEvent):
        local_pos = self.mapFromGlobal(event.globalPos())
        row = (local_pos.y() - self.spacing // 2) // self.spacing
        col = (local_pos.x() - self.spacing // 2) // self.spacing
        if self.tree_enabled:
            # print(row,col)
            coordinates = (row, col)
            if coordinates in self.tree_map:
                return self.tree_map[coordinates]
            return None
        if 0 <= col < self.row_length:
            list_index = row * self.row_length + col
            if 0 <= list_index < len(self.data):
                return self.data[list_index]
        return None

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update_pixmap()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.show_tips:
            process_info = self.get_process_info(event)
            if process_info is None:
                QToolTip.hideText()
            else:
                # if QToolTip.isVisible():
                #    QToolTip.hideText()
                # Works on X11
                # QToolTip.showText(event.globalPos(), str(process_info.text(compact=True)), widget=self)
                # Works on X11 and Wayland?
                QToolTip.showText(self.mapToGlobal(event.pos()), str(process_info.text(compact=True)), widget=self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        process_info = self.get_process_info(event)
        if process_info is not None:
            self.show_process_info(process_info)
        event.ignore()

    def show_process_info(self, process_info: ProcessInfo):
        if process_info.pid in ProcessControlWidget.instance_map:
            info_widget = ProcessControlWidget.instance_map[process_info.pid]
        else:
            info_widget = ProcessControlWidget(process_info, self.parent())
            self.signal_new_data.connect(info_widget.update_data)
        info_widget.show()
        info_widget.raise_()
        info_widget.activateWindow()

    def wheelEvent(self, event: QWheelEvent) -> None:
        num_pixels = event.pixelDelta()
        num_degrees = event.angleDelta()
        if num_pixels is not None:
            new_dot_diameter = self.dot_diameter + (2 if num_pixels.y() > 0 else -2)
            if 12 <= new_dot_diameter <= 64:
                self.set_dot_diameter(new_dot_diameter)
        elif num_degrees is not None:
            new_dot_diameter = self.dot_diameter + (1 if num_degrees.y() > 0 else -1)
            if 12 <= new_dot_diameter <= 64:
                self.set_dot_diameter(new_dot_diameter)
        self.parent().statusBar().showMessage(tr("Dot diameter {}").format(self.dot_diameter), 500)
        event.accept()


wait_for_system_tray = True


def is_system_tray_available():
    # Only wait the first time called
    global wait_for_system_tray
    if wait_for_system_tray:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("WARNING: no system tray, waiting to see if one becomes available.")
            for i in range(0, SYSTEM_TRAY_WAIT_SECONDS):
                if QSystemTrayIcon.isSystemTrayAvailable():
                    break
                time.sleep(1)
    wait_for_system_tray = False
    return QSystemTrayIcon.isSystemTrayAvailable()


class MainWindow(QMainWindow):
    signal_theme_change = pyqtSignal()

    def __init__(self, app: QApplication):
        super().__init__()

        global debugging
        self.setObjectName('main_window')
        self.geometry_key = self.objectName() + "_geometry"
        self.state_key = self.objectName() + "_window_state"

        self.config = Config()
        self.config.refresh()
        global debugging
        debugging = self.config.getboolean('options', 'debug_enabled')

        process_dots_widget = ProcessDotsWidget(self.config, self)
        self.setCentralWidget(process_dots_widget)

        hostname = os.uname()[1]

        def new_data(data):
            # debug("New Data", data) if debugging else None
            if self.isVisible():
                self.normal_status_label.setText(
                    tr("\u25B3 Host: {h} \u25F4 Uptime: {u} \u25CB {c} processes \u25B7 loadavg 1m:{a[0]} \u25B9 5m:{"
                       "a[1]} \u25B9 15m:{a[2]}").format(
                        h=hostname, c=len(data), a=os.getloadavg(),
                        u=str(timedelta(seconds=int(time.clock_gettime(time.CLOCK_BOOTTIME))))[0:-3]))
            process_dots_widget.update_data(data)

        def handle_watcher_error(error_str: str, e: Exception):
            msg = QMessageBox(self)
            msg.setWindowTitle(tr("Error"))
            msg.setText(tr(error_str))
            msg.setDetailedText(str(e))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            if error_str == ERROR_DBUS_NOTIFICATIONS_UNAVAILABLE:
                enable_notifier(False)

        def handle_action_request(action_id: str, process_info: ProcessInfo):
            process_dots_widget.show_process_info(process_info)

        info('QStyleFactory.keys()=', QStyleFactory.keys())
        info(f"Icon theme path={QIcon.themeSearchPaths()}")
        info(f"Icon theme '{QIcon.themeName()}' >> is_dark_theme()={is_dark_theme()}")

        QGuiApplication.setDesktopFileName(f"procno")
        app_name = tr(f"procno {hostname}")
        app.setWindowIcon(get_icon(SVG_PROGRAM_ICON_LIGHT))
        app.setApplicationDisplayName(app_name)
        app.setApplicationVersion(PROGRAM_VERSION)
        # Make sure all icons use HiDPI - toolbars don't by default, so force it.
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)

        global is_wayland
        is_wayland = QGuiApplication.platformName() == "wayland"
        debug("is_wayland", is_wayland) if debugging else None

        self.status_bar = QStatusBar()
        self.normal_status_label = QLabel()
        self.status_bar.addWidget(self.normal_status_label)
        self.setStatusBar(self.status_bar)

        self.settings = QSettings('procno.qt.state', 'procno')

        def update_title_and_tray_indicators() -> None:
            if process_watcher_task.isRunning():
                title_text = tr("Running")
                self.setWindowTitle(title_text)
                tray.setToolTip(f"{title_text} \u2014 {app_name}")
                tray.setIcon(get_icon(SVG_PROGRAM_ICON))
            else:
                title_text = tr("Stopped")
                self.setWindowTitle(title_text)
                tray.setToolTip(f"{title_text} \u2014 {app_name}")
                tray.setIcon(get_icon(SVG_TRAY_LISTENING_DISABLED))

        def enable_listener(enable: bool) -> None:
            if enable:
                process_watcher_task.start()
                while not process_watcher_task.isRunning():
                    time.sleep(0.2)
            else:
                process_watcher_task.requestInterruption()
                while process_watcher_task.isRunning():
                    time.sleep(0.2)

            tool_bar.configure_run_action(enable)
            app_context_menu.configure_run_action(enable)
            update_title_and_tray_indicators()

        def toggle_listener() -> None:
            enable_listener(not process_watcher_task.isRunning())

        def enable_notifier(enable: bool) -> None:
            process_watcher_task.enable_notifications(enable)
            tool_bar.configure_notifier_action(enable)
            app_context_menu.configure_notifier_action(enable)
            update_title_and_tray_indicators()

        def toggle_notifier() -> None:
            enable_notifier(not process_watcher_task.is_notifying())

        def quit_app() -> None:
            process_watcher_task.requestInterruption()
            self.app_save_state()
            app.quit()

        def config_change() -> None:
            self.config.refresh()
            global debugging
            debugging = self.config.getboolean('options', 'debug_enabled')
            if self.use_system_tray():
                if not tray.isVisible():
                    tray.setVisible(True)
            else:
                if tray.isVisible():
                    tray.setVisible(False)
            process_dots_widget.update_settings_from_config(self.config)
            update_title_and_tray_indicators()

        def settings() -> None:
            config_editor = ConfigPanel(config_change_func=config_change)
            config_editor.show()

        app_context_menu = MainContextMenu(
            run_func=toggle_listener, notify_func=toggle_notifier, quit_func=quit_app, settings_func=settings,
            parent=self)

        def search(text: str, re_enabled: bool):
            process_dots_widget.set_re_match(text, re_enabled)

        tool_bar = MainToolBar(
            run_func=toggle_listener,
            notify_func=toggle_notifier,
            search_func=search,
            menu=app_context_menu,
            parent=self)
        self.addToolBar(tool_bar)

        tray = QSystemTrayIcon()
        tray.setIcon(get_icon(SVG_PROGRAM_ICON))
        tray.setContextMenu(app_context_menu)
        self.signal_theme_change.connect(update_title_and_tray_indicators)

        process_watcher_task = ProcessWatcherTask()
        process_watcher_task.signal_new_data.connect(new_data)
        process_watcher_task.signal_error.connect(handle_watcher_error)
        process_watcher_task.signal_action_request.connect(handle_action_request)

        enable_listener(True)
        enable_notifier(self.config.getboolean('options', 'start_with_notifications_enabled'))

        if len(self.settings.allKeys()) == 0:
            # First run or qt settings have been erased - guess at sizes and locations
            # rec = QApplication.desktop().screenGeometry()
            # x = int(rec.width())
            # y = int(rec.height())
            # self.setGeometry(x // 2 - 100, y // 3, x // 3, y // 2)
            # self.process_dock_container.setGeometry(x // 2 - 150 - x // 3, y // 3, x // 3, y // 2)
            # self.config_dock_container.setGeometry(x // 2 - 150 - 2 * x // 3, y // 3, x // 3, y // 2)
            self.setGeometry(0, 0, 1000, 900)
            pass

        self.app_restore_state()

        tray.activated.connect(self.tray_activate_window)
        if self.use_system_tray():
            tray.setVisible(True)
        else:
            self.show()
        rc = app.exec_()
        if rc == 999:  # EXIT_CODE_FOR_RESTART:
            QProcess.startDetached(app.arguments()[0], app.arguments()[1:])
        sys.exit(rc)

    def event(self, event: 'QEvent') -> bool:
        try:
            return super().event(event)
        finally:
            # ApplicationPaletteChange happens after the new style theme is in use.
            if event.type() == QEvent.ApplicationPaletteChange:
                debug(f"ApplicationPaletteChange is_dark_theme() {is_dark_theme()}") if debugging else None
                self.signal_theme_change.emit()


    def closeEvent(self, event: QCloseEvent) -> None:
        debug("closeEvent") if debugging else None
        if self.use_system_tray():
            self.tray_activate_window()
        else:
            self.app_save_state()
        super().closeEvent(event)

    def use_system_tray(self):
        return QSystemTrayIcon.isSystemTrayAvailable() and self.config.getboolean('options', 'system_tray_enabled')

    def tray_activate_window(self):
        if self.isVisible():
            debug("tray_activate_window hide") if debugging else None
            self.hide()
        else:
            debug("tray_activate_window show") if debugging else None
            self.show()
            # Attempt to force it to the top with raise and activate
            self.raise_()
            self.activateWindow()

    def app_save_state(self):
        debug(f"app_save_state {self.geometry_key} {self.state_key}") if debugging else None
        self.settings.setValue(self.geometry_key, self.saveGeometry())
        self.settings.setValue(self.state_key, self.saveState())
        self.centralWidget().app_save_state(self.settings)

    def app_restore_state(self):
        debug("app_restore_state") if debugging else None
        geometry = self.settings.value(self.geometry_key, None)
        if geometry is not None:
            debug(f"Restore {self.geometry_key} {self.state_key}") if debugging else None
            self.restoreGeometry(geometry)
            window_state = self.settings.value(self.state_key, None)
            self.restoreState(window_state)
            self.centralWidget().app_restore_state(self.settings)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.excepthook = exception_handler
    # Call QApplication before parsing arguments, it will parse and remove Qt session restoration arguments.
    app = QApplication(sys.argv)
    parse_args()
    MainWindow(app)


if __name__ == '__main__':
    main()
