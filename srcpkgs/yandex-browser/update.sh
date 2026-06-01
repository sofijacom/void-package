#!/usr/bin/env bash

# site="https://repo.yandex.ru/yandex-browser/deb/pool/main/y/yandex-browser-stable/"
# pattern="yandex-browser-stable_\K\d+\.\d+\.\d+\.\d+(?=_amd64\.deb)"


set -e

TPL="srcpkgs/yandex-browser/template"
APP="yandex-browser"
CHANNEL="stable"
URL="https://repo.yandex.ru/yandex-browser/deb/pool/main/y/yandex-browser-stable/"

echo "### Checking for yandex-browser updates..."

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

# Ambil versi terbaru dari Yandex version API
LATEST_VERSION=$(curl -Ls "https://repo.yandex.ru/yandex-browser/deb/pool/main/y/$APP-$CHANNEL/" | tr '">< ' '\n' | grep ".*amd64.deb" | tail -1)" \
    | grep -oP '"version":"\K[^"]+' | head -1)


if [ -z "$LATEST_VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

DEB_URL="${URL}yandex-browser-${CHANNEL}_${LATEST_VERSION}-1_amd64.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$DEB_URL" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$LATEST_VERSION" >> $GITHUB_ENV
echo "### Done! yandex-browser updated to $LATEST_VERSION"
