#!/bin/sh
if [ -n "$1" ]; then
	CHROMIUM="$1"
else
	CHROMIUM=87
fi
rm -rf qtwebengine qtwebengine-chromium
D="$(date +%Y%m%d)"
git clone -b 5.15 --depth 1 git://code.qt.io/qt/qtwebengine.git
cd qtwebengine
V="$(cat .qmake.conf |grep ^MODULE_VERSION |cut -d= -f2 |xargs echo)"
git archive -o ../qtwebengine-everywhere-src-$V-$D.tar --prefix qtwebengine-everywhere-src-$V-$D/ origin/5.15
cd ..
git clone -b ${CHROMIUM}-based --depth 1 git://code.qt.io/qt/qtwebengine-chromium.git
cd qtwebengine-chromium
git archive -o ../qtwebengine-chromium-${CHROMIUM}-$D.tar origin/${CHROMIUM}-based
cd ..
zstd --ultra -22 --rm *.tar
