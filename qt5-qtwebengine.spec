%define _disable_ld_no_undefined 1
%define beta %nil

Summary:	Qt WebEngine
Name:		qt5-qtwebengine
Version:	5.5.1
%if "%{beta}" != ""
Release:	1.%{beta}.1
%define qttarballdir qtwebengine-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	4
%define qttarballdir qtwebengine-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
License:	GPLv2
Group:		System/Libraries
Url:		http://qtwebengine.sf.net/
Source1000:	%{name}.rpmlintrc
Patch0:		add-arm64-arm-support-wo-crosscompile.patch
Patch1:         Add-support-for-Shockwave-Flash-plugin.patch
Patch2:         gyp_conf.patch
Patch3:		0001-allow-build-for-linux-clang-platform.patch
Patch4:         Fix-widgets-plugin-settings.patch
BuildRequires:	git-core
BuildRequires:	nasm
BuildRequires:	python2
BuildRequires:	qmake5
BuildRequires:	yasm
BuildRequires:	cups-devel
BuildRequires:	gperf
BuildRequires:	bison
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5WebChannel)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	snappy-devel
BuildRequires:	srtp-devel
BuildRequires:	re2c
BuildRequires:	qt5-qtquick-private-devel
# FIXME this is evil - the build system should be fixed properly
# instead of making sure there's no previous version floating
# around.
# But as of 5.5.1, QtWebEngine will find system Qt5WebEngine and
# use its headers -- preventing it from accessing new APIs
BuildConflicts:	pkgconfig(Qt5WebEngineCore)

%dependinglibpackage Qt5WebEngineWidgets 5
%dependinglibpackage Qt5WebEngineCore 5
%dependinglibpackage Qt5WebEngine 5

%define engined %{mklibname -d Qt5WebEngine}
%define cored %{mklibname -d Qt5WebEngineCore}
%define widgetsd %{mklibname -d Qt5WebEngineWidgets}

%description
Chromium based web rendering engine for Qt.

%files
%{_datadir}/qt5/icudtl.dat
%{_datadir}/qt5/translations/qtwebengine_locales
%{_datadir}/qt5/qtwebengine_resources*.pak
%{_libdir}/qt5/qml/QtWebEngine
%{_libdir}/qt5/plugins/qtwebengine
%{_libdir}/qt5/libexec/QtWebEngineProcess

%package -n %{engined}
Summary:	Development files for Qt WebEngine
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5WebEngine 5} = %{EVRD}

%description -n %{engined}
Development files for Qt WebEngine.

%files -n %{engined}
%{_libdir}/cmake/Qt5WebEngine
%{_libdir}/libQt5WebEngine.so
%{_libdir}/libQt5WebEngine.prl
%{_libdir}/pkgconfig/Qt5WebEngine.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_webengine.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_webengine_private.pri
%{_includedir}/qt5/QtWebEngine

%package -n %{cored}
Summary:	Development files for Qt WebEngine Core
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5WebEngineCore 5} = %{EVRD}

%description -n %{cored}
Development files for Qt WebEngine Core.

%files -n %{cored}
%{_libdir}/cmake/Qt5WebEngineCore
%{_libdir}/libQt5WebEngineCore.so
%{_libdir}/libQt5WebEngineCore.prl
%{_libdir}/pkgconfig/Qt5WebEngineCore.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginecore.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginecore_private.pri

%package -n %{widgetsd}
Summary:	Development files for Qt WebEngine Widgets
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5WebEngineWidgets 5} = %{EVRD}

%description -n %{widgetsd}
Development files for Qt WebEngine Widgets.

%files -n %{widgetsd}
%{_libdir}/cmake/Qt5WebEngineWidgets
%{_libdir}/libQt5WebEngineWidgets.so
%{_libdir}/libQt5WebEngineWidgets.prl
%{_libdir}/pkgconfig/Qt5WebEngineWidgets.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginewidgets.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginewidgets_private.pri
%{_includedir}/qt5/QtWebEngineWidgets

%package devel
Summary:	Metapackage pulling in all QtWebEngine development files
Group:		Development/KDE and Qt
Requires:	%{engined} = %{EVRD}
Requires:	%{cored} = %{EVRD}
Requires:	%{widgetsd} = %{EVRD}

%description devel
Development files for Qt WebEngine.

%files devel

%package examples
Summary:	Examples for QtWebEngine
Group:		Development/KDE and Qt
Requires:	%{name}-devel = %{EVRD}

%description examples
Examples for QtWebEngine.

%files examples
%{_libdir}/qt5/examples/webengine
%{_libdir}/qt5/examples/webenginewidgets

%package demobrowser
Summary:	Demo browser utilizing Qt WebEngine
Group:		Networking/WWW
Requires:	%{mklibname Qt5WebEngine 5} = %{EVRD}
Requires:	%{mklibname Qt5WebEngineCore 5} = %{EVRD}
Requires:	%{mklibname Qt5WebEngineWidgets 5} = %{EVRD}

%description demobrowser
Demo browser utilizing Qt WebEngine.

%files demobrowser
%{_bindir}/browser
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/qtwebengine.png

%prep
%setup -qn %{qttarballdir}
%apply_patches
mkdir -p bin
ln -s %{_bindir}/python2 bin/python
export PATH=$PWD/bin:$PATH

%if "%{__cc}" == "/usr/bin/clang"
sed -i 's!host_clang=0!host_clang=1!g' src/core/config/desktop_linux.pri
%endif

# basic configuration
myconf+=" -Duse_system_expat=1
          -Duse_system_flac=1
          -Duse_system_jsoncpp=1
          -Duse_system_libevent=1
          -Duse_system_libjpeg=1
          -Duse_system_libpng=1
          -Duse_system_libusb=1
          -Duse_system_libxml=1
          -Duse_system_libxslt=1
          -Duse_system_opus=1
          -Duse_system_libevent=1
	  -Duse_system_snappy=1
          -Duse_system_zlib=1
          -Duse_system_speex=1"

pushd src/3rdparty/chromium/
build/linux/unbundle/replace_gyp_files.py $myconf
popd

# reduce memory on linking
export LDFLAGS="%{ldflags} -Wl,--as-needed"
export PYTHON=%{__python2}

# Yuuucccckkk... gyp
ln -s %{_bindir}/python2 python
export PATH=`pwd`:$PATH
# chromium is a huge bogosity -- references to hidden SQLite symbols, has
# asm files forcing an executable stack etc., but still tries to force ld
# into --fatal-warnings mode...
sed -i -e 's|--fatal-warnings|-O2|' src/3rdparty/chromium/build/config/compiler/BUILD.gn src/3rdparty/chromium/build/common.gypi src/3rdparty/chromium/android_webview/android_webview.gyp
sed -i 's/c++/g++/g' src/3rdparty/chromium/build/compiler_version.py
%ifarch armv7hl
export target_arch="arm"
export GYP_DEFINES="target_arch=arm arm_float_abi=hard"
%endif
%qmake_qt5 qtwebengine.pro WEBENGINE_CONFIG="proprietary_codecs"

%build
export STRIP=strip
export PATH=`pwd`:$PATH
%make

%install
export STRIP=strip
export PATH=`pwd`:$PATH
%make install INSTALL_ROOT=%{buildroot}
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}/applications
install -c -m 755 examples/webenginewidgets/browser/browser %{buildroot}%{_bindir}/
cat >%{buildroot}%{_datadir}/applications/%{name}-browser.desktop <<EOF
[Desktop Entry]
Name=QtWebEngine Browser
Type=Application
Icon=qtwebengine
Categories=Network;WebBrowser;
Comment=A fast web browser
GenericName=Web Browser
Exec=%{_bindir}/browser %%u
MimeType=text/html;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
Terminal=false
EOF
for i in 16 22 32 48 64; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	convert examples/webenginewidgets/browser/data/defaulticon.png -scale ${i}x${i} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/qtwebengine.png
done
