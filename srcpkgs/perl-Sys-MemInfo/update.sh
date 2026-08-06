#!/bin/bash

set -euo pipefail

TPL="srcpkgs/perl-Sys-MemInfo/template"

echo "### Checking for perl-Sys-MemInfo updates..."

LATEST_VERSION=$(curl -s https://api.metacpan.org/v1/release/Sys-MemInfo | jq -r .version | sed 's/^v//')
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${LATEST_VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${LATEST_VERSION}" ] && printf "No new version to release\n" && exit 0

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

# URL="${CPAN_SITE}/Sys/Sys-MemInfo-${LATEST_VERSION}.tar.gz"
URL_X86="https://cpan.metacpan.org/authors/id/S/SC/SCRESTO/Sys-MemInfo-${LATEST_VERSION}.tar.gz"

echo "Calculating checksum..."
CHK=$(curl -L -s "$URL_X86" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^checksum=.*/checksum=\"$CHK\"/" "$TPL"

echo "NEW_VERSION=$LATEST_VERSION" >> $GITHUB_ENV
echo "### Done! perl-Sys-MemInfo updated to $LATEST_VERSION"

