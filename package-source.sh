#!/bin/sh
rm -rf qtwebengine qtwebengine-chromium
D="$(date +%Y%m%d)"
git clone -b 5.15 --depth 1 git://code.qt.io/qt/qtwebengine.git
cd qtwebengine
git archive -o ../qtwebengine-everywhere-src-5.15.4-$D.tar --prefix qtwebengine-everywhere-src-5.15.4-$D/ origin/5.15
cd ..
git clone -b 87-based --depth 1 git://code.qt.io/qt/qtwebengine-chromium.git
cd qtwebengine-chromium
git archive -o ../qtwebengine-chromium-87-$D.tar origin/87-based
cd ..
zstd --ultra -22 --rm *.tar
