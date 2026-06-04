#!/usr/bin/env bash

set -e

TPL="srcpkgs/microsoft-edge/template"
APP="microsoft-edge"
CHANNEL="stable"
#PACKAGES_URL="https://github.com/NDViet/microsoft-edge-stable/releases/tags"
URL="https://github.com/NDViet/microsoft-edge-stable/releases/download/${VERSION}/"

__dir="$(dirname "${BASH_SOURCE[0]}")"

echo "### Checking for microsoft-edge updates..."

# CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

# Fetch latest version from the Yandex apt repository
#echo "Fetching package index from $PACKAGES_URL ..."
#LATEST_VERSION=$(curl -sL "$PACKAGES_URL" \
#  | awk '/^Package: microsoft-edge-stable$/,/^$/' \
#  | awk '/^Version:/ { print $2; exit }')

LATEST_VERSION=$(gh release list --repo NDViet/microsoft-edge-stable --json name,tagName,isLatest --jq '.[] | select(.isLatest)|.tagName')

VERSION=${LATEST_VERSION#"v"}
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

DEB_URL="${URL}microsoft-edge-${CHANNEL}_${VERSION}-1_amd64.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$DEB_URL" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^timestamp=.*/timestamp=$TIMESTAMP/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! microsoft-edge updated to $VERSION"
