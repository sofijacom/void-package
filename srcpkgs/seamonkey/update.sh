#!/usr/bin/env bash

set -euo pipefail

TPL="srcpkgs/seamonkey/template"
APP="seamonkey"

echo "### Checking for smartgit updates..."

# Detect the channel
VERSION=$(curl -Ls "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=seamonkey" | grep "^pkgver=" | cut -c 8-)

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0


if [ -z "$VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $VERSION"

DEB_URL="https://archive.seamonkey-project.org/releases/${VERSION}/linux-x86_64/en-US/${APP}-${VERSION}.en-US.linux-x86_64.tar.bz2"

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
echo "### Done! seamonkey updated to $VERSION"
