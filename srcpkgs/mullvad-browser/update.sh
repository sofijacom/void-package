#!/bin/bash

set -euo pipefail

REPO="mullvad/mullvad-browser"
TPL="srcpkgs/mullvad-browser/template"

echo "### Checking for mullvad-browser updates..."

LATEST_VERSION=$(gh api repos/$REPO/releases/latest --jq .tag_name | sed 's/^v//')
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${LATEST_VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${LATEST_VERSION}" ] && printf "No new version to release\n" && exit 0

if [ -z "$LATEST_VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

URL_X86="https://github.com/$REPO/releases/download/${LATEST_VERSION}/mullvad-browser-linux-x86_64-${LATEST_VERSION}.tar.xz"

echo "Calculating checksum..."
CHK_X86=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK_X86" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK_X86"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=\"$CHK_X86\"/" "$TPL"

echo "NEW_VERSION=$LATEST_VERSION" >> $GITHUB_ENV
echo "### Done! mullvad-browser updated to $LATEST_VERSION"
