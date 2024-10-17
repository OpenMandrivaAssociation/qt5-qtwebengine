%define _disable_ld_no_undefined 1
#define beta %{nil}
%define snapshot 20240906

# exclude plugins (all architectures) and libv8.so (i686, it's static everywhere else)
%global __provides_exclude ^lib.*plugin\\.so.*|libv8\\.so$
# exclude libv8.so (i686, it's static everywhere else)
%global __requires_exclude ^libv8\\.so$
# and designer plugins
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

# Use this if you get "filename too long" errors:
# Workaround for filenames getting too long for ****ing gn to handle
%define _builddir /tmp/b

# Build with gcc instead of clang
# (tpg) 2023-06-08 Falkon quite often displays "Error when loading page"
# which indicates that qtwebengine process coredumped
%bcond_without gcc

%if ! %{with gcc}
# Workaround for debugsource generator
# not finding anything
%define _debugsource_template %{nil}
%endif

# 2021-02-08 Currently doesn't work because system gn is way ahead of what
# qtwebengine expects
%bcond_with system_gn

Summary:	Qt WebEngine
Name:		qt5-qtwebengine
Version:	5.15.18
%if 0%{?snapshot}
Release:	0.%{?beta:%{beta}.}%{snapshot}.1
%define qttarballdir qtwebengine-everywhere-src-%{version}-%{snapshot}
# Use package-source.sh to create the 2 files below
# git://code.qt.io/qt/qtwebengine.git -- branch 5.15 --prefix qtwebengine-everywhere-src-%{version}-%{snapshot}/
Source0:	qtwebengine-everywhere-src-%{version}-%{snapshot}.tar.zst
# git://code.qt.io/qt/qtwebengine-chromium.git -- branch 87-based (no prefix)
Source1:	qtwebengine-chromium-87-%{snapshot}.tar.zst
Source1001:	package-source.sh
%else
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebengine-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	2
%define qttarballdir qtwebengine-everywhere-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
%endif
License:	GPLv2
Group:		System/Libraries
Url:		https://download.qt.io/official_releases/qt
Source1000:	%{name}.rpmlintrc
# Patches "borrowed" from rpmfusion
# https://github.com/rpmfusion/qt5-qtwebengine-freeworld
# some tweaks to linux.pri (system yasm, link libpci, run unbundling script)
Patch0:		 https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-everywhere-src-5.10.0-linux-pri.patch
# Make it work with the Lima driver, see
# https://www.plasma-mobile.org/2019/12/20/plasma_mobile_as_daily_driver_on_pinephone.html
Patch1:		qtwebengine-5.15.0-lima-driver.patch
# Detect system ninja 1.10+
Patch2:		qtwebengine-detect-system-ninja.patch
# disable NEON vector instructions on ARM where the NEON code FTBFS due to
# GCC bug https://bugzilla.redhat.com/show_bug.cgi?id=1282495
Patch3:		https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-opensource-src-5.9.0-no-neon.patch
# ../../../../src/3rdparty/chromium/third_party/skia/src/opts/SkRasterPipeline_opts.h:734:5: warning: 'memcpy' will always overflow; destination buffer has size 2, but size argument is 8 [-Wfortify-source]
#     memcpy(&fp16, &h, sizeof(U16));
#     ^
# ../../../../src/3rdparty/chromium/third_party/skia/src/opts/SkRasterPipeline_opts.h:755:19: error: functional-style cast from 'neon::F' (aka 'V<float>') to '__fp16' is not allowed
#     __fp16 fp16 = __fp16(f);
#                   ^~~~~~~~
#Patch4:	qt5-qtwebengine-workaround-aarch64-build-failure.patch
Patch5:		qtwebengine-5.15.16-clang16.patch
# re2 needs absl with c++17 or higher for string_view
Patch6:		qtwebengine-5.15.15-c++17.patch
# Try to get ABI compatibility between system absl (used by system re2)
# and internalized absl until we can remove the latter
Patch7:		qtwebengine-system-absl-compat.patch
Patch8:		qtwebengine-icu.patch
# Try to restore a sufficient amount of binary compatibility between the
# internalized copy of absl (which can't be disabled yet) and the system
# version (used, among others, by the system version of re2, which DOES
# get used...
#Patch6:		qtwebengine-re2-absl-compat.patch 
# remove Android dependencies from openmax_dl ARM NEON detection (detect.c)
#Patch10: https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-opensource-src-5.9.0-openmax-dl-neon.patch
# Force verbose output from the GN bootstrap process
# Needs porting
#Patch21: https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-everywhere-src-5.12.0-gn-bootstrap-verbose.patch
# Fix/workaround FTBFS on aarch64 with newer glibc
Patch24:	https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-everywhere-src-5.11.3-aarch64-new-stat.patch
# borrow fix from chromium packaging
Patch26:	https://raw.githubusercontent.com/rpmfusion/qt5-qtwebengine-freeworld/master/qtwebengine-gcc9-drop-rsp-clobber.patch
# Fix build with SIOCGSTAMP missing
Patch27:	qtwebengine-5.13-SIOCGSTAMP-compile.patch
# ====================
# OpenMandriva patches
# ====================
# Define __mulodi4 when building with clang but without compiler-rt
Patch1000:	qtwebengine-__mulodi4.patch
# use the system NSPR prtime (based on Debian patch)
# We already depend on NSPR, so it is useless to copy these functions here.
# Debian uses this just fine, and I don't see relevant modifications either.
# FIXME port
Patch1001:	qtwebengine-everywhere-src-5.11.0-system-nspr-prtime.patch
Patch1002:	qtwebengine-5.12-no-static-libstdc++.patch
# (tpg) Detect MESA DRI nouveau drivers and disable gpu usage to work around nouveau crashing
Patch1003:	disable-gpu-when-using-nouveau-boo-1005323.diff
# https://bugreports.qt.io/browse/QTBUG-59769
Patch1004:	881ef63.diff
#Patch1005:	qtwebengine-87-glibc-2.34-libstdc++-11.patch
# Support ffmpeg 3.5
#Patch1010:	chromium-65-ffmpeg-3.5.patch
#Patch1011:	ffmpeg-linkage.patch
#Patch1014:	qtwebengine-everywhere-src-5.11.1-reduce-build-log-size.patch
#Patch1015:	qtwebengine-QTBUG-75265.patch
# Make it build with clang on i686
Patch1017:	qtwebengine-5.13.0-b4-i686-missing-latomic.patch
Patch1019:	chromium-77-aarch64-buildfix.patch
Patch1020:	qtwebengine-pdf-compile.patch
Patch1023:	qtwebengine-5.15.4-compile.patch
# Fix glibc 2.34
Patch1026:	qtwebengine-5.15.15-compile.patch

BuildRequires:	atomic-devel
BuildRequires:	git-core
BuildRequires:	nasm
BuildRequires:	pkgconfig(re2)
BuildRequires:	re2c
BuildRequires:	python2
BuildRequires:	qmake5
BuildRequires:	yasm
BuildRequires:	cups-devel
BuildRequires:	gperf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ninja
BuildRequires:	nodejs
%if %{with system_gn}
BuildRequires:	gn
%endif
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(libjpeg)
# /usr/bin/clang++ -Xassembler --version -x assembler -c /dev/null
# not working, well gcc-cpp need only to detect version
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(atk)
BuildRequires:	cmake(absl)
# QT5 part
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5WebChannel)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Positioning)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Sensors)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5Location)
BuildRequires:	cmake(Qt5XcbQpa)
BuildRequires:	cmake(Qt5QmlModels)
BuildRequires:	qt5-qtqmlmodels-private-devel
# Designer plugin
BuildRequires:	pkgconfig(Qt5Designer)
# end
BuildRequires:	pkgconfig(libdrm)
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
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(absl_config)
BuildRequires:	snappy-devel
BuildRequires:	srtp-devel
BuildRequires:	qt5-qtquickcontrols2
BuildRequires:	qt5-qtquick-private-devel
BuildRequires:	qt5-qtqmlmodels-private-devel
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libva-drm)
BuildRequires:	pkgconfig(libva-glx)
BuildRequires:	pkgconfig(libva-x11)
BuildRequires:	pkgconfig(dri)
BuildRequires:	%{_lib}GL-devel
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(poppler-cpp)
# FIXME this is evil - the build system should be fixed properly
# instead of making sure there's no previous version floating
# around.
# But as of 5.5.1, QtWebEngine will find system Qt5WebEngine and
# use its headers -- preventing it from accessing new APIs
BuildConflicts:	pkgconfig(Qt5WebEngineCore)
# dlopened
Requires:	%mklibname freebl 3
Requires:	nss-shlibsign

%dependinglibpackage Qt5WebEngineWidgets 5
%dependinglibpackage Qt5WebEngineCore 5
%dependinglibpackage Qt5WebEngine 5
%dependinglibpackage Qt5Pdf 5
%{_libdir}/qt5/plugins/imageformats/libqpdf.so
%{_libdir}/qt5/qml/QtQuick/Pdf
%dependinglibpackage Qt5PdfWidgets 5

%define engined %{mklibname -d Qt5WebEngine}
%define cored %{mklibname -d Qt5WebEngineCore}
%define widgetsd %{mklibname -d Qt5WebEngineWidgets}
%define pdfd %{mklibname -d Qt5Pdf}
%define pdfwidgetsd %{mklibname -d Qt5PdfWidgets}

%description
Chromium based web rendering engine for Qt5.

%files
%dir %{_datadir}/qt5
%dir %{_datadir}/qt5/translations
%{_datadir}/qt5/translations/qtwebengine_locales
%dir %{_datadir}/qt5/qtwebengine_dictionaries
%{_datadir}/qt5/resources
%{_libdir}/qt5/qml/QtWebEngine
%{_libdir}/qt5/libexec/QtWebEngineProcess
%{_libdir}/qt5/bin/qwebengine_convert_dict

%package -n %{engined}
Summary:	Development files for Qt WebEngine
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5WebEngine} = %{EVRD}

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
Requires:	%{mklibname Qt5WebEngineCore} = %{EVRD}

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
Requires:	%{mklibname Qt5WebEngineWidgets} = %{EVRD}

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
%optional %{_libdir}/cmake/Qt5Designer/Qt5Designer_QWebEngineViewPlugin.cmake
%optional %{_libdir}/qt5/plugins/designer/libqwebengineview.so

%package -n %{pdfd}
Summary:	Development files for Qt Pdf
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5Pdf} = %{EVRD}

%description -n %{pdfd}
Development files for Qt Pdf

%files -n %{pdfd}
%{_includedir}/qt5/QtPdf
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QPdfPlugin.cmake
%{_libdir}/cmake/Qt5Pdf
%{_libdir}/libQt5Pdf.prl
%{_libdir}/libQt5Pdf.so
%{_libdir}/pkgconfig/Qt5Pdf.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_pdf.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_pdf_private.pri

%package -n %{pdfwidgetsd}
Summary:	Development files for Qt Pdf Widgets
Group:		Development/KDE and Qt
Requires:	%{mklibname Qt5PdfWidgets} = %{EVRD}

%description -n %{pdfwidgetsd}
Development files for Qt Pdf Widgets.

%files -n %{pdfwidgetsd}
%{_includedir}/qt5/QtPdfWidgets
%{_libdir}/cmake/Qt5PdfWidgets
%{_libdir}/libQt5PdfWidgets.prl
%{_libdir}/libQt5PdfWidgets.so
%{_libdir}/pkgconfig/Qt5PdfWidgets.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_pdfwidgets.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_pdfwidgets_private.pri

%package devel
Summary:	Metapackage pulling in all QtWebEngine development files
Group:		Development/KDE and Qt
Requires:	%{engined} = %{EVRD}
Requires:	%{cored} = %{EVRD}
Requires:	%{widgetsd} = %{EVRD}
Requires:	%{pdfd} = %{EVRD}
Requires:	%{pdfwidgetsd} = %{EVRD}

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
%{_libdir}/qt5/examples/pdf
%{_libdir}/qt5/examples/pdfwidgets
%{_libdir}/qt5/examples/webengine
%{_libdir}/qt5/examples/webenginewidgets

%prep
%setup -qn %{qttarballdir}
%if 0%{?snapshot}
cd src/3rdparty
tar xf %{S:1}
cd ../..
%endif
%autopatch -p1 -M 1999

# Until we can figure out how to kill the internal absl, let's at least
# try to make it ABI compatible with the system copy (as used by re2...)
cp -f %{_includedir}/absl/base/options.h src/3rdparty/chromium/third_party/abseil-cpp/absl/base/options.h
# Chromium isn't compatible with std::optional though
sed -i -e 's,#define ABSL_OPTION_USE_STD_OPTIONAL 1,#define ABSL_OPTION_USE_STD_OPTIONAL 0,' src/3rdparty/chromium/third_party/abseil-cpp/absl/base/options.h

# chromium is a huge bogosity -- references to hidden SQLite symbols, has
# asm files forcing an executable stack etc., but still tries to force ld
# into --fatal-warnings mode...
sed -i -e 's|fatal_linker_warnings = true|fatal_linker_warnings = false|' src/3rdparty/chromium/build/config/compiler/BUILD.gn

# fix missing (bogus but required) file duplication
cp src/3rdparty/chromium/base/numerics/*_arm_impl.h src/3rdparty/gn/base/numerics/

# Prevent the code from using internal ICU headers even if told to use system icu
cp -f %{_includedir}/unicode/* src/3rdparty/chromium/third_party/icu/source/common/unicode/

# remove ./ from #line commands in ANGLE to avoid debugedit failure (?)
#sed -i -e 's!\./!!g' \
#  src/3rdparty/chromium/third_party/angle/src/compiler/preprocessor/Tokenizer.cpp \
#  src/3rdparty/chromium/third_party/angle/src/compiler/translator/glslang_lex.cpp

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

%ifarch %{arm}
# As of clang 10.0.0-20200207, qt5-qtwebengine 20191213 (chromium-77),
# on armv7hnl, gn gets miscompiled and throws an Illegal Instruction error
# when generating the ninja files.
# The rest of qtwebengine can be built with clang -- so let's do an ugly
# hack and force a different compiler for gn
sed -i -e 's,\$\$QMAKE_CC,gcc,g;s,\$\$QMAKE_CXX,g++,g' src/buildtools/gn.pro
%endif

# Let's trust our kernel and libc, not files copied in
# from some horribly outdated distro
for i in src/3rdparty/chromium/sandbox/linux/system_headers/*_linux_syscalls.h; do
    echo '#include <asm/unistd.h>' >$i
done

# webengine really really likes forcing C++14 on us...
# but we need C++17 for compatibility with system absl
find . -name "*.pro" -o -name "*.pri" |while read r; do
	echo 'QMAKE_CXXFLAGS_GNUCXX14 = -std=gnu++17' >>$r
done

%{_libdir}/qt5/bin/syncqt.pl -version %{version}

%build
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}
export CXXFLAGS="%{optflags} -std=gnu++17 -fno-delete-null-pointer-checks -Wno-class-memaccess -Wno-packed-not-aligned"

# most arches run out of memory with full debuginfo, so use -g1 on non-x86_64
export CXXFLAGS=$(echo "$CXXFLAGS" | sed -e 's/ -g / -g0 /g' -e 's/-gdwarf-4//')
# Use of vfp instructions is hardcoded in SkBlurMaskFilter.cpp
export CXXFLAGS=$(echo "$CXXFLAGS" | sed -e 's/-mfpu=neon /-mfpu=neon-vfpv4 /;s/-mfpu=neon$/-mfpu=neon-vfpv4/')

# (tpg) ld.lld does not understand some GNU ld options
QMAKE_LFLAGS="%{build_ldflags} -Wl,--as-needed"

# (tpg) default QtWebEngine feature set
QMAKE_EXTRA_ARGS=" -feature-webengine-system-re2 -feature-webengine-system-icu -feature-webengine-system-libwebp -feature-webengine-system-opus -no-feature-webengine-system-ffmpeg \
    -feature-webengine-system-libvpx -feature-webengine-system-glib -feature-webengine-system-minizip -feature-webengine-system-libxml2 -feature-webengine-system-lcms2 \
    -feature-webengine-system-freetype -feature-webengine-system-harfbuzz -feature-webengine-system-png -feature-webengine-system-jpeg -feature-webengine-system-zlib \
    -feature-webengine-system-ninja -feature-webengine-alsa -feature-webengine-kerberos -feature-webengine-geolocation -feature-webengine-proprietary-codecs -feature-webengine-pulseaudio \
    -feature-webengine-spellchecker  -feature-webengine-printing-and-pdf -feature-webengine-qtpdf-support \
    -no-feature-webengine-embedded-build -feature-pdf-v8 -feature-pdf-xfa -verbose"

%if %{with gcc}
export CC=gcc
export CXX=g++
export QMAKE_CC=gcc
export QMAKE_CXX=g++
export QMAKE_XSPEC=linux-g++
export QMAKESPEC=%{_libdir}/qt5/mkspecs/${QMAKE_XSPEC}
%else
export CC=clang
export CXX=clang++
export QMAKE_CC=clang
export QMAKE_CXX=clang++
export QMAKE_XSPEC=linux-clang
export QMAKESPEC=%{_libdir}/qt5/mkspecs/${QMAKE_XSPEC}
%global optflags %{optflags} -flto=thin
# (tpg) 2023-06-05 fix for clang-16
# error: integer value 7 is outside the valid range of values [0, 3] for this enumeration type [-Wenum-constexpr-conversion]
sed -i -e 's|"-Wno-unknown-attributes",|"-Wno-enum-constexpr-conversion",\n      &|' src/3rdparty/chromium/build/config/compiler/BUILD.gn
%endif

mkdir %{_target_platform}
cd %{_target_platform}
mkdir bin
ln -s /usr/bin/python2 bin/python
export PATH="$(pwd)/bin:$PATH"

if [ $(getconf _NPROCESSORS_ONLN) -le 32 ]; then
    export NINJAFLAGS="-v %{_smp_mflags}"
else
# 160 parallel build processes on altra
# always run out of memory
    export NINJAFLAGS="-v -j 32"
fi

%if %{with system_gn}
QMAKE_EXTRA_ARGS+=" -webengine-system-gn"
%endif

%qmake_qt5 \
%if %{with gcc}
%ifnarch %{arm} %{ix86}
	-spec linux-g++ \
%else
	-spec linux-g++-32 \
%endif
%endif
	QMAKE_LFLAGS="${QMAKE_LFLAGS}" \
	QMAKE_EXTRA_ARGS="${QMAKE_EXTRA_ARGS}" ..

# Intentionally not using %%make_build because there seem to be
# problems at -j32
make NINJA_PATH=ninja
cd -

%install
export STRIP=strip
export PATH="$(pwd)/bin:$PATH"
%make_install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
cd %{buildroot}%{_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
cd -

# Allow QtWebEngine > 5.15.2 to coexist with other Qt modules from 5.15.x
# In general, we want stable Qt, but QtWebEngine git is significantly better
# than 5.15.2 due to the Chromium 87 sync...
sed -i -e 's,%{version} \${_Qt5WebEngineCore_FIND_VERSION_EXACT},5.15.2 ${_Qt5WebEngineCore_FIND_VERSION},g' %{buildroot}%{_libdir}/cmake/Qt5WebEngineCore/Qt5WebEngineCoreConfig.cmake
sed -i -e 's,%{version} \${_Qt5WebEngineWidgets_FIND_VERSION_EXACT},5.15.2 ${_Qt5WebEngineWidgets_FIND_VERSION},g' %{buildroot}%{_libdir}/cmake/Qt5WebEngineWidgets/Qt5WebEngineWidgetsConfig.cmake

mkdir -p %{buildroot}%{_datadir}/qt5/qtwebengine_dictionaries
