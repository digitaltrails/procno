#
# spec file for procno
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Contact:  m i c h a e l   @   a c t r i x   .   g e n   .   n z
#

Name: procno
Version: 1.1.4
Release: 0
License: GPL-3.0-or-later
BuildArch: noarch
URL: https://github.com/digitaltrails/procno
Group: System/GUI/Other
Summary: A process monitor with DBUS Freedesktop-Notifications
Source0:        %{name}-%{version}.tar.gz

%if 0%{?suse_version} || 0%{?fedora_version}
Requires: python38 python38-qt5 python38-dbus-python python38-psutil
%endif

BuildRequires: coreutils

BuildRoot: %{_tmppath}/%{name}-%{version}-build
%description
Procno is a process monitor with DBUS Freedesktop-Notifications.
Like top, but not as we know it.

%prep
%setup -q

%build

exit 0

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/applications
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps
install -m 755 procno.py  %{buildroot}/%{_bindir}/%{name}

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Terminal=false
Exec=%{_bindir}/%{name}
Name=Procno
GenericName=Procno
Comment=A process monitor with DBUS Freedesktop-Notifications. Like top, but not as we know it.
Icon=procno
Categories=Qt;System;Monitor;System;
EOF

install -m644 %{name}.desktop %{buildroot}/%{_datadir}/applications
install -m644 %{name}.png %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps

#gzip -c docs/_build/man/vdu_controls.1 > %{buildroot}/%{_datadir}/man/man1/%{name}.1.gz

%post


%files
%license LICENSE.md
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%changelog

* Fri Dec 17 2021 Michael Hamilton <michael@actrix.gen.nz>
- Wayland compatability tweaks. 1.1.4
* Wed Dec 15 2021 Michael Hamilton <michael@actrix.gen.nz>
- Change minimum match to 2 chars to match 2 char commands. 1.1.3
* Sat Dec 04 2021 Michael Hamilton <michael@actrix.gen.nz>
- Check if system tray is available before applying system_tray_enabled. 1.1.2
* Sun Nov 28 2021 Michael Hamilton <michael@actrix.gen.nz>
- Display process finish time. 1.1.1
- More color options. Single updating message per incident. 1.1.0
* Mon Oct 25 2021 Michael Hamilton <michael@actrix.gen.nz>
- Packaged for rpm procno 1.0.0
