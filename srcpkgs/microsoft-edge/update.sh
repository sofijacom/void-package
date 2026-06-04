#!/usr/bin/env bash

set -e

TPL="srcpkgs/microsoft-edge/template"
APP="microsoft-edge"
CHANNEL="stable"
URL="https://github.com/NDViet/microsoft-edge-stable/releases/download/"

__dir="$(dirname "${BASH_SOURCE[0]}")"

echo "### Checking for microsoft-edge updates..."

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

#export SHA256=$(curl -sL https://github.com/NDViet/microsoft-edge-stable/releases/download/${VERSION}/microsoft-edge-stable_${VERSION}-1_amd64.deb
#https://github.com/NDViet/microsoft-edge-stable/releases/download/148.0.3967.96-1/microsoft-edge-stable_148.0.3967.96-1_amd64.deb

DEB_URL="${URL}${VERSION}-1/microsoft-edge-${CHANNEL}_${VERSION}-1_amd64.deb"

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
