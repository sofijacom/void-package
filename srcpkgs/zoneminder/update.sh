#!/usr/bin/env bash

set -euo pipefail

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

TPL=${__dir}/template
REPO="ZoneMinder/zoneminder"

LATEST_VERSION=$(gh release list --repo ${REPO} --json name,tagName,isLatest --jq '.[] | select(.isLatest)|.tagName')
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' "${TPL}" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

# No preprepped checksum files, need to download the binary and calculate it myself
gh release download -R ${REPO} --archive=tar.gz --output "zoneminder-${VERSION}.tar.gz"
export SHA256=$(sha256sum ./zoneminder-${VERSION}.tar.gz | cut -d ' ' -f1 )
rm ./zoneminder-${VERSION}.tar.gz
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^checksum=.*/checksum=${SHA256}/" "$TPL"

printf "ZoneMinder template updated\n"
