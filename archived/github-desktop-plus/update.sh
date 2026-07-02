#!/bin/bash

set -euo pipefail

REPO="desktop-plus/desktop-plus"
TPL="srcpkgs/github-desktop-plus/template"

echo "### Checking for helium-browser updates..."

# LATEST_VERSION=$(gh api repos/$REPO/releases/latest --jq .tag_name | sed 's/^v//')
LATEST_VERSION=$(curl -s https://api.github.com/repos/$REPO/releases/latest | jq -r .tag_name)
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

export VERSION=${LATEST_VERSION#"v"}

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

URL_X86="https://github.com/$REPO/releases/download/${LATEST_VERSION}/DesktopPlus-${LATEST_VERSION}-linux-x86_64.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! github-desktop-plus updated to $VERSION"
