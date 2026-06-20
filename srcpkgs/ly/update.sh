#!/usr/bin/env bash

set -euo pipefail

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

REPO="fairyglade/ly"
TEMPLATE=${__dir}/template
ID="9341631"

LATEST_VERSION=$(curl -s "https://codeberg.org/api/v1/repos/${REPO}/releases/${ID}" | jq -r ".tag_name")

VERSION=${LATEST_VERSION#"v"}

CURRENT_VERSION=$(grep -E '^version=' "${TEMPLATE}" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

# No preprepped checksum files, need to download the binary and calculate it myself
gh release download -R ${REPO} --archive=tar.gz --output "v$VERSION.tar.gz"
export SHA256=$(sha256sum ./v$VERSION.tar.gz | cut -d ' ' -f1 )
rm ./v$VERSION.tar.gz
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

sed -i "s/^version=.*/version=$VERSION/" "$TEMPLATE"
sed -i "s/^checksum=.*/checksum=\"$SHA256\"/" "$TEMPLATE"

printf "ly template updated\n"

