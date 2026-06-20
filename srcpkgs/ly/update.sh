#!/usr/bin/env bash

set -euo pipefail

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

REPO="fairyglade/ly"
TEMPLATE=${__dir}/template
ID="9341631"

LATEST_VERSION=$(curl -s "https://codeberg.org/api/v1/repos/${REPO}/releases/${ID}" | jq -r ".tag_name")
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' "${TEMPLATE}" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

URL_X86="https://codeberg.org/${REPO}/v${VERSION}.tar.gz"

echo "Calculating checksum..."
CHK_X86=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK_X86" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK_X86"

sed -i "s/^version=.*/version=$VERSION/" "$TEMPLATE"
sed -i "s/^checksum=.*/checksum=$CHK_X86/" "$TEMPLATE"

printf "ly template updated\n"

