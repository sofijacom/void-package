#!/bin/bash
set -e

REPO="Calamares/calamares"
TPL="srcpkgs/calamares/template"
ID="7639303"

echo "### Checking for Calamares updates..."

LATEST_VERSION=$(curl -s "https://codeberg.org/api/v1/repos/Calamares/calamares/releases/${ID}" | jq -r ".tag_name")

VERSION=${LATEST_VERSION#"v"}
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

URL_X86="https://codeberg.org/Calamares/calamares/releases/download/v${LATEST_VERSION}/calamares-${LATEST_VERSION}.tar.gz"

echo "Calculating checksum..."
CHK_X86=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK_X86" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK_X86"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! Calamares updated to $VERSION"
