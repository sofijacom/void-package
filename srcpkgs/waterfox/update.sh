#!/bin/bash

set -euo pipefail

REPO="BrowserWorks/waterfox"
TPL="srcpkgs/waterfox/template"

#export ARCH=$(uname -m)

echo "### Checking for waterfox updates..."

# LATEST_VERSION=$(gh api repos/$REPO/releases/latest --jq .tag_name | sed 's/^v//')
VERSION="$(wget https://www.waterfox.com/download/ -O - | sed 's/[()",{} ]/\n/g' | grep -o "https.*Linux.*bz2")"
LATEST_VERSION=$(echo "$VERSION" | sed -n '1p' | awk '{print $2}')

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${LATEST_VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${LATEST_VERSION}" ] && printf "No new version to release\n" && exit 0

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

URL_X86="https://cdn.waterfox.com/waterfox/releases/${LATEST_VERSION}/Linux_x86_64/waterfox-${LATEST_VERSION}.tar.bz2"

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
echo "### Done! waterfox updated to $LATEST_VERSION"
