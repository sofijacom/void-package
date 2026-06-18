#!/usr/bin/env bash

set -euo pipefail

TPL="srcpkgs/github-desktop/template"
APP="github-desktop"

__dir="$(dirname "${BASH_SOURCE[0]}")"

echo "### Checking for smartgit updates..."

# Detect the channel
LATEST_VERSION=$(curl -Ls "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=github-desktop-bin" | grep "^pkgver=" | cut -c 8-)
LATEST_VER="${LATEST_VERSION//_/-}"

VERSION=${LATEST_VER#"v"}
CUR_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)
CUR_TIMESTAMP=$(grep -E '^timestamp=' ${__dir}/template | cut -d= -f2)
CURRENT_VERSION=$(printf "%s-%s" "${CUR_VERSION}" "${CUR_TIMESTAMP}")

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

export TIMESTAMP=${VERSION##*-}
export VERSION=${VERSION%-*}

if [ -z "$VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $VERSION"

URL_X86="https://github.com/shiftkey/desktop/releases/latest/download/GitHubDesktop-linux-amd64-${LATEST_VER}.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^timestamp=.*/timestamp=$TIMESTAMP/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! github-desktop updated to $VERSION"
