#!/usr/bin/env bash

set -e

TPL="srcpkgs/smartgit/template"
APP="smartgit"

echo "### Checking for smartgit updates..."

# Detect the channel
# https://download.smartgit.dev/smartgit/smartgit-26_1_038-linux_amd64.deb
LATEST_VERSION=$(curl -s https://download.smartgit.dev/smartgit/ | grep '"browser_download_url":' | grep 'amd64.deb' | grep -vE '(\.pem|\.sig)' | grep -o 'https://[^"]*')
#wait
if wget --version | head -1 | grep -q ' 1.'; then
    wget -q --no-verbose --show-progress --progress=bar "https://download.smartgit.dev/smartgit/$LATEST_VERSION" || exit 1
else
    wget "https://download.smartgit.dev/smartgit/$LATEST_VERSION" || exit 1
fi

# Extract the archive
ar x ./*.deb
tar xf ./control.tar.gz

# Check the version
VERSION=$(cat control | grep Version | cut -c 10-)

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

# https://download.smartgit.dev/smartgit/smartgit-26_1_038-linux_amd64.deb
DEB_URL="https://download.smartgit.dev/smartgit/${LATEST_VERSION}"

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
echo "### Done! smartgit updated to $VERSION"
