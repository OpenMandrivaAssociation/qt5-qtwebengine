%define _disable_ld_no_undefined 1
%define beta %{nil}
%define	debug_package %nil
# FIXME build failure w/ 5.11.0beta4, clang 6.0, binutils 2.30
#define _disable_lto 1

# exclude plugins (all architectures) and libv8.so (i686, it's static everywhere else)
%global __provides_exclude ^lib.*plugin\\.so.*|libv8\\.so$
# exclude libv8.so (i686, it's static everywhere else)
%global __requires_exclude ^libv8\\.so$
# and designer plugins
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

Summary:	Qt WebEngine
Name:		qt5-qtwebengine
Version:	5.12.1
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebengine-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%(echo %{beta} |sed -e "s,1$,,")/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtwebengine-everywhere-src-%{version}
#Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}-clean.tar.xz
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
License:	GPLv2
Group:		System/Libraries
Url:		http://qtwebengine.sf.net/
Source1000:	%{name}.rpmlintrc
# some tweaks to linux.pri (system libs, link libpci, run unbundling script,
# do an NSS/BoringSSL "chimera build", see Provides: bundled(boringssl) comment)
#Patch1:		qtwebengine-everywhere-src-5.6.1-linux-pri.patch
# quick hack to avoid checking for the nonexistent icudtl.dat and silence the
# resulting warnings - not upstreamable as is because it removes the fallback
# mechanism for the ICU data directory (which is not used in our builds because
# we use the system ICU, which embeds the data statically) completely
Patch2:		qtwebengine-everywhere-src-5.6.0-no-icudtl-dat.patch
# fix extractCFlag to also look in QMAKE_CFLAGS_RELEASE, needed to detect the
# ARM flags with our %%qmake_qt5 macro, including for the next patch
Patch3:		qtwebengine-everywhere-src-5.6.0-beta-fix-extractcflag.patch
# Define __mulodi4 when building with clang but without compiler-rt
Patch4:		qtwebengine-__mulodi4.patch
# use the system NSPR prtime (based on Debian patch)
# We already depend on NSPR, so it is useless to copy these functions here.
# Debian uses this just fine, and I don't see relevant modifications either.
# FIXME port
Patch5:		qtwebengine-everywhere-src-5.11.0-system-nspr-prtime.patch
# use the system ICU UTF functions
# We already depend on ICU, so it is useless to copy these functions here.
# I checked the history of that directory, and other than the renames I am
# undoing, there were no modifications at all. Must be applied after Patch5.
# FIXME currently disabled because of linkage problems
#Patch6:		qtwebengine-5.8-system-icu.patch
Patch7:		qtwebengine-5.12-no-static-libstdc++.patch
# (tpg) Detect MESA DRI nouveau drivers and disable gpu usage to work around nouveau crashing
Patch9:		disable-gpu-when-using-nouveau-boo-1005323.diff
# Support ffmpeg 3.5
Patch10:	chromium-65-ffmpeg-3.5.patch
Patch11:	ffmpeg-linkage.patch
Patch14:	qtwebengine-everywhere-src-5.11.1-reduce-build-log-size.patch
Patch15:	qtwebengine-5.12.0-armfixes.patch
# Keep in sync with the patch in Chromium...
# NOT YET READY
#Patch16:	enable-vaapi.patch
BuildRequires:	git-core
BuildRequires:	nasm
BuildRequires:	re2-devel
BuildRequires:	re2c
BuildRequires:	python2
BuildRequires:	qmake5
BuildRequires:	yasm
BuildRequires:	cups-devel
BuildRequires:	gperf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ninja
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
# /usr/bin/clang++ -Xassembler --version -x assembler -c /dev/null
# not working, well gcc-cpp need only to detect version
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(atk)
# QT5 part
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5WebChannel)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Positioning)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Sensors)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5Location)
# Designer plugin
BuildRequires:	pkgconfig(Qt5Designer)
# end
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libwebpdemux)
BuildRequires:	pkgconfig(jsoncpp)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	snappy-devel
BuildRequires:	srtp-devel
BuildRequires:	qt5-qtquickcontrols2
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
%dir %{_datadir}/qt5
%dir %{_datadir}/qt5/translations
%{_datadir}/qt5/translations/qtwebengine_locales
%{_datadir}/qt5/resources
%{_libdir}/qt5/qml/QtWebEngine
%{_libdir}/qt5/libexec/QtWebEngineProcess
%{_libdir}/qt5/bin/qwebengine_convert_dict

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
%{_includedir}/qt5/QtWebEngineCore
%{_libdir}/cmake/Qt5WebEngineCore
%{_libdir}/libQt5WebEngineCore.so
%{_libdir}/libQt5WebEngineCore.prl
%{_libdir}/pkgconfig/Qt5WebEngineCore.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginecore.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginecore_private.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_webenginecoreheaders_private.pri

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
%{_libdir}/cmake/Qt5Designer/Qt5Designer_QWebEngineViewPlugin.cmake
%{_libdir}/qt5/plugins/designer/libqwebengineview.so

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
Obsoletes:	%{name}-demobrowser < %{EVRD}

%description examples
Examples for QtWebEngine.

%files examples
%{_libdir}/qt5/examples/webengine
%{_libdir}/qt5/examples/webenginewidgets

%prep
%autosetup -n %{qttarballdir} -p1

# chromium is a huge bogosity -- references to hidden SQLite symbols, has
# asm files forcing an executable stack etc., but still tries to force ld
# into --fatal-warnings mode...
sed -i -e 's|--fatal-warnings|-O2|' src/3rdparty/chromium/build/config/compiler/BUILD.gn src/3rdparty/chromium/build/common.gypi

# fix missing (bogus but required) file duplication
cp src/3rdparty/chromium/base/numerics/*_arm_impl.h src/3rdparty/gn/base/numerics/

# remove ./ from #line commands in ANGLE to avoid debugedit failure (?)
sed -i -e 's!\./!!g' \
  src/3rdparty/chromium/third_party/angle/src/compiler/preprocessor/Tokenizer.cpp \
  src/3rdparty/chromium/third_party/angle/src/compiler/translator/glslang_lex.cpp

# FIXME need to do/fix: Make sure we don't get an executable stack
#find . -type f -name "*.asm" |while read r; do
#	if ! grep -q GNU-stack $r; then
#		echo '.section .note.GNU-stack noalloc noexec nowrite progbits' >>$r
#	fi
#done

# adapt internal ffmpeg to system headers
#sed -i 's!PixelFormat !AVPixelFormat !g;s!VideoAVPixelFormat!VideoPixelFormat!g' src/3rdparty/chromium/media/ffmpeg/ffmpeg_common.{h,cc}
#sed -i 's!PIX_FMT_!AV_PIX_FMT_!g' src/3rdparty/chromium/media/ffmpeg/ffmpeg_common.cc
#sed -i 's!max_analyze_duration2!max_analyze_duration!g' src/3rdparty/chromium/media/filters/ffmpeg_demuxer.cc
#sed -i 's!CODEC_ID_!AV_CODEC_ID_!g' src/3rdparty/chromium/media/filters/ffmpeg_aac_bitstream_converter.cc

# most arches run out of memory with full debuginfo
sed -i 's|$(STRIP)|strip|g' src/core/core_module.pro

%build
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}
export CXXFLAGS="%{optflags} -std=gnu++14 -fno-delete-null-pointer-checks -Wno-class-memaccess -Wno-packed-not-aligned"

# most arches run out of memory with full debuginfo, so use -g1 on non-x86_64
export CXXFLAGS=`echo "$CXXFLAGS" | sed -e 's/ -g / -g0 /g' -e 's/-gdwarf-4//'`
# Use of vfp instructions is hardcoded in SkBlurMaskFilter.cpp
export CXXFLAGS=`echo "$CXXFLAGS" | sed -e 's/-mfpu=neon /-mfpu=neon-vfpv4 /;s/-mfpu=neon$/-mfpu=neon-vfpv4/'`

# reduce memory on linking
export LDFLAGS="%{ldflags} -Wl,--as-needed"

%ifarch %{arm} %{aarch64} %{ix86}
# As of Qt 5.12.0, clang 7.0.1, falkon freezes if qtwebengine is built
# with clang on aarch64
# On i686, we get a build time error (undefined reference to
# __atomic_load_8) with Qt 5.12.1, clang 7.0.1
# On armv7hnl, gn gets miscompiled and throws an Illegal Instruction error
# when generating the ninja files.
export CC=gcc
export CXX=g++
export QMAKE_CC=gcc
export QMAKE_CXX=g++
%endif

mkdir %{_target_platform}
pushd %{_target_platform}
mkdir bin
ln -s /usr/bin/python2 bin/python
export PATH="$(pwd)/bin:$PATH"

export NINJAFLAGS="-v %{_smp_mflags}"
# use_system_icu <--- should be put back, currently disabled because of undefined reference
# to base::i18n::GetRawIcuMemory()
%qmake_qt5 QMAKE_EXTRA_ARGS="-proprietary-codecs -pulseaudio -alsa -webp -printing-and-pdf -spellchecker -system-ffmpeg -system-opus -system-webengine-icu" LFLAGS="${LDFLAGS}" ..

%make_build NINJA_PATH=ninja
popd

%install
export STRIP=strip
export PATH="$(pwd)/bin:$PATH"
%make_install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd
