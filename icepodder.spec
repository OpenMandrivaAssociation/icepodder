%define name	icepodder
%define fname	IcePodder
%define version	5.4
%define release	%mkrel 1

Name:		%{name}
Summary:	Graphical podcast catcher and player
Version:	%{version}
Release:	%{release}

Source0:	http://www.icepodder.com/wp-content/uploads/2007/02/%{fname}-%{version}.tar.bz2
URL:		http://www.icepodder.com/
License:	GPLv2+
Group:		Networking/News
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	wxpython2.6
Requires:	pyxmms
Requires:	python
Requires:	python-libxml2
Requires:	id3
BuildRequires:	ImageMagick

BuildArch:	noarch

Provides:	iPodder
Provides:	ipodder
Provides:	castpodder
Obsoletes:	iPodder
Obsoletes:	ipodder
Obsoletes:	castpodder

%description
IcePodder is technically a Media Aggregator - a program that allows
you to select and download audio files from anywhere on the Internet
to your desktop.

IcePodder is a podcatcher (RSS client) for Linux conceived as a
replacement for CastPodder.  IcePodder is written in Python. The goal
of this project is to provide Linux users with a dedicated client to
download podcasts, with an emphasis on reliability and stability.

%prep
%setup -q -n %name

chmod 755 `find -name '*.py'`
perl -pi -e 's/\#\!\/bin\/python/\#\!\/usr\/bin\/python/' `find -name '*.py'`
perl -pi -e 's,#! python,#!/usr/bin/python,g' `find -name '*.py'`
perl -pi -e 's,#!/usr/bin/env python,#!/usr/bin/python,g' `find -name '*.py'`

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot/%_bindir
mkdir -p %buildroot/%_datadir/%{name}
install -m755 CastPodder.sh -D %buildroot/%_bindir/%{name}
cp -r * %buildroot/%_datadir/%{name}
chmod 755 %buildroot/%_datadir/%{name}/*/*.py
rm -f %buildroot/%_datadir/%{name}/{Changelog,gpl.txt,INSTALL,install.sh,castpodder.desktop,CastPodder.sh,CastPodder.spec,KNOWN-ISSUES,make-distribution.sh,NOTES,LICENSE,README,TODO}
rm -fr %buildroot/%_datadir/%{name}/build
rm -rf %buildroot/%_datadir/%name/tools/id3-tool/*
rm -rf %buildroot/%_datadir/%name/tools/id3-*.tar.gz
ln -s %_bindir/id3 %buildroot/%_datadir/%name/tools/id3-tool/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=IcePodder
Comment=Podcast catcher
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Network;News;
StartupNotify=true
EOF

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -transparent white CastPodder-48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -transparent white CastPodder-32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -transparent white CastPodder-16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
%{update_icon_cache hicolor}
		
%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%files
%defattr(-,root,root)
%doc KNOWN-ISSUES NOTES README TODO
%{_bindir}/%name
%{_datadir}/%name
%_datadir/applications/mandriva*
%{_iconsdir}/hicolor/*/apps/%{name}.png

