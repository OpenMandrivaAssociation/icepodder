%define fname	IcePodder

%define svn	68
%define rel	3

%if %svn
%define release		%mkrel 0.%{svn}.%{rel}
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{fname}-%{version}.tar.bz2
%define dirname		%{name}
%endif

Name:		icepodder
Summary:	Graphical podcast catcher and player
Version:	5.5
Release:	%{release}
# Note: SVN is on sourceforge - AdamW 2008/12
Source0:	http://www.icepodder.com/wp-content/uploads/2007/02/%{distname}
URL:		http://www.icepodder.com/
License:	GPLv2+
Group:		Networking/News
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
Requires:	python
Requires:	python-libxml2
Requires:	id3
Requires:	wxPythonGTK
BuildRequires:	imagemagick
BuildRequires:	dos2unix
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
%setup -q -n %{dirname}

chmod 755 `find -name '*.py'`
sed -i -e 's/\#\!\/bin\/python/\#\!\/usr\/bin\/python/' `find -name '*.py'`

# This file being in Mac encoding screws up find-requires.
dos2unix --m2u localization/catalog/et.py

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}
install -m755 CastPodder.sh -D %{buildroot}/%{_bindir}/%{name}
cp -r * %{buildroot}/%{_datadir}/%{name}
chmod 755 %{buildroot}/%{_datadir}/%{name}/*/*.py
rm -f %{buildroot}/%{_datadir}/%{name}/{Changelog,gpl.txt,INSTALL,install.sh,castpodder.desktop,CastPodder.sh,CastPodder.spec,KNOWN-ISSUES,make-distribution.sh,NOTES,LICENSE,README,TODO}
rm -fr %{buildroot}/%{_datadir}/%{name}/build
rm -rf %{buildroot}/%{_datadir}/%{name}/tools/id3-tool/*
rm -rf %{buildroot}/%{_datadir}/%{name}/tools/id3-*.tar.gz
ln -s %{_bindir}/id3 %{buildroot}/%{_datadir}/%{name}/tools/id3-tool/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif
		
%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr(-,root,root)
%doc AUTHORS CREDITS NOTES README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/mandriva*
%{_iconsdir}/hicolor/*/apps/%{name}.png

