#!/bin/bash
set -e

REPO="imputnet/helium-linux"
TPL="srcpkgs/helium-browser/template"

echo "### Checking for helium-browser updates..."

LATEST_VERSION=$(gh api repos/$REPO/releases/latest --jq .tag_name | sed 's/^v//')
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

URL_X86="https://github.com/$REPO/releases/download/${LATEST_VERSION}/helium-${LATEST_VERSION}-x86_64_linux.tar.xz"

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
echo "### Done! helium-browser updated to $LATEST_VERSION"
