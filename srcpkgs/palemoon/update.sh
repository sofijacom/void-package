#!/bin/bash
set -e

TPL="srcpkgs/palemoon/template"
APP="palemoon"
TOOLKIT="gtk3"

echo "### Checking for helium-browser updates..."

# TEMPORARY DIRECTORY
#mkdir -p tmp
#cd ./tmp || exit 1

# Detect the channel
DOWNLOAD_URL="https://www.palemoon.org/download.php?mirror=us&bits=64&type=linux${TOOLKIT}"

# Download with wget or wget2
if wget --version | head -1 | grep -q ' 1.'; then
  wget -q --no-verbose --show-progress --progress=bar "$DOWNLOAD_URL" --trust-server-names || exit 1
else
  wget "$DOWNLOAD_URL" --trust-server-names || exit 1
fi

# Extract the archiv
[ -e ./*tar.* ] && tar fx ./*tar.* && rm -f ./*tar.* || exit 1

LATEST_VERSION=$(cat ./${APP}/application.ini | grep "^Version=" | head -1 | cut -c 9-)
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

URL_X86="https://rm-eu.palemoon.org/release/palemoon-${LATEST_VERSION}.linux-x86_64-gtk3.tar.xz"

echo "Calculating checksum..."
CHK=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=\"$CHK\"/" "$TPL"

echo "NEW_VERSION=$LATEST_VERSION" >> $GITHUB_ENV
echo "### Done! palemoon updated to $LATEST_VERSION"
