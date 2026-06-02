#!/usr/bin/env bash

set -e

TPL="srcpkgs/yandex-browser/template"
APP="yandex-browser"
CHANNEL="stable"
PACKAGES_URL="http://repo.yandex.ru/yandex-browser/deb/dists/stable/main/binary-amd64/Packages"
URL="https://repo.yandex.ru/yandex-browser/deb/pool/main/y/yandex-browser-stable/"

echo "### Checking for yandex-browser updates..."

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

# Fetch latest version from the Yandex apt repository
echo "Fetching package index from $PACKAGES_URL ..."
LATEST_VERSION=$(curl -sL "$PACKAGES_URL" \
  | awk '/^Package: yandex-browser-stable$/,/^$/,/$-1/' \
  | awk '/^Version:/ { print $2; exit }')

export VERSION=${LATEST_VERSION#"v"}

# Yandex version
# LATEST_VERSION=$(curl -Ls "https://repo.yandex.ru/yandex-browser/deb/pool/main/y/$APP-$CHANNEL/" | tr '">< ' '\n' | grep ".*amd64.deb" | tail -1)
# export VERSION=${LATEST_VERSION#"yandex-browser-stable_"}

# LATEST_VERSION=$(curl -Ls "https://" \
#    | grep -oP '"version":"\K[^"]+' | head -1)


if [ -z "$VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $VERSION"

DEB_URL="${URL}yandex-browser-${CHANNEL}_${VERSION}-1_amd64.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$DEB_URL" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! yandex-browser updated to $VERSION"
