%define beta tp1

Name: qtwebengine
Version: 0.1.0
Release: 0.%beta.1
Source0: http://alfred.qt-project.org/qt/development_releases/qt/qtwebengine-tp/qtwebengine-opensource-src-%{version}-%{beta}.tar.gz
Summary: Qt WebEngine
URL: http://qtwebengine.sf.net/
License: GPL
Group: System/Libraries
BuildRequires: qmake5
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(gtk+-2.0) pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libpulse)
BuildRequires: git-core
BuildRequires: cups-devel
BuildRequires: python
BuildRequires: nasm
BuildRequires: yasm

%libpackage Qt5WebEngineWidgets 5
%libpackage Qt5WebEngine 5

%description
Chromium based web rendering engine for Qt

%package devel
Summary: Development files for Qt WebEngine
Group: Development/KDE and Qt
Requires: %{mklibname Qt5WebEngine 5} = %EVRD
Requires: %{mklibname Qt5WebEngineWidgets 5} = %EVRD
Provides: %{mklibname -d Qt5WebEngine} = %EVRD
Provides: %{mklibname -d Qt5WebEngineWidgets} = %EVRD
%if "%_lib" == "lib64"
Provides: devel(libQt5WebEngineCore(64bit))
%else
Provides: devel(libQt5WebEngineCore())
%endif

%description
Development files for Qt WebEngine

%package demobrowser
Summary: Demo browser utilizing Qt WebEngine
Requires: %{mklibname Qt5WebEngine 5} = %EVRD
Requires: %{mklibname Qt5WebEngineWidgets 5} = %EVRD
Group: Networking/WWW

%description demobrowser
Demo browser utilizing Qt WebEngine

%prep
%setup -q -n %{name}-opensource-src-%{version}-%{beta}
%qmake_qt5 *.pro

%build
%make

%install
%make install INSTALL_ROOT=%buildroot
mkdir -p %buildroot%_bindir %buildroot%_datadir/applications
install -c -m 755 examples/widgets/browser/browser %buildroot%_bindir/
cat >%buildroot%_datadir/applications/%{name}-browser.desktop <<EOF
[Desktop Entry]
Name=QtWebEngine Browser
Type=Application
Icon=qtwebengine
Categories=Network;WebBrowser;
Comment=A fast web browser
GenericName=Web Browser
Exec=%_bindir/browser %%u
MimeType=text/html;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
Terminal=false
EOF
for i in 16 22 32 48 64; do
	mkdir -p %buildroot%_datadir/icons/hicolor/${i}x${i}/apps
	convert examples/widgets/browser/data/defaulticon.png -scale ${i}x${i} %buildroot%_datadir/icons/hicolor/${i}x${i}/apps/qtwebengine.png
done

%files
%_datadir/qt5/translations/qtwebengine_locales
%_datadir/qt5/qtwebengine_resources.pak
%_libdir/qt5/qml/QtWebEngine
%_libdir/qt5/plugins/qtwebengine
%_libdir/libQt5WebEngineCore.so

%files devel
%_libdir/cmake/Qt5WebEngine
%_libdir/cmake/Qt5WebEngineWidgets
%_libdir/libQt5WebEngine.so
%_libdir/libQt5WebEngine.prl
%_libdir/libQt5WebEngineWidgets.so
%_libdir/libQt5WebEngineWidgets.prl
%_libdir/pkgconfig/Qt5WebEngine.pc
%_libdir/pkgconfig/Qt5WebEngineWidgets.pc
%_libdir/qt5/examples/quick/quicknanobrowser
%_libdir/qt5/examples/widgets/browser
%_libdir/qt5/examples/widgets/fancybrowser
%_libdir/qt5/mkspecs/modules/*.pri
%_includedir/qt5/QtWebEngine
%_includedir/qt5/QtWebEngineWidgets
%_libdir/qt5/libexec/QtWebEngineProcess

%files demobrowser
%_bindir/browser
%_datadir/applications/*.desktop
%_datadir/icons/hicolor/*/apps/qtwebengine.png
