#!/bin/bash
set -e

REPO="librewolf/source"
TPL="srcpkgs/librewolf/template"

__dir="$(dirname "${BASH_SOURCE[0]}")"

echo "### Checking for librewolf updates..."
# https://codeberg.org/api/packages/librewolf/generic/librewolf-source/151.0.4-1/librewolf-151.0.4-1.source.tar.gz

# curl -sL https://codeberg.org/api/repos/ваш_пользователь/ваш_репозиторий/releases/latest | jq -r ".tag_name"

# LATEST_VERSION=$(curl -sL https://codeberg.org/repos/librewolf/source/releases | jq -r ".tag_name")

LATEST_VERSION=$(curl -sL https://codeberg.org/librewolf/source/releases/tag | jq -r ".*tar.gz" | sed 's/^v//')

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

URL_X86="https://codeberg.org/api/packages/librewolf/generic/librewolf-source/${LATEST_VERSION}/librewolf-${LATEST_VERSION}.source.tar.gz"

echo "Calculating checksum..."
CHK_X86=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK_X86" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK_X86"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^timestamp=.*/timestamp=$TIMESTAMP/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! librewolf updated to $VERSION"
