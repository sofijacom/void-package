#!/bin/bash

# Call Google's version history API to get stable linux desktop releases
# that are still being served (endtime=none). Look for the 'version' in
# the JSON response.
# site="https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions/all/releases?filter=endtime=none"
# pattern="\"version\": *\"\K[\d.]+(?=\")"

set -euo pipefail

TPL="srcpkgs/google-chrome/template"
CHANNEL="stable"
URL="https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/"

echo "### Checking for google-chrome updates..."

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

# Ambil versi terbaru dari Chrome version API
LATEST_VERSION=$(curl -s "https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Linux&num=1" \
    | grep -oP '"version":"\K[^"]+' | head -1)

printf "Latest version is: %s\nLatest built version is: %s\n" "${LATEST_VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${LATEST_VERSION}" ] && printf "No new version to release\n" && exit 0

if [ -z "$LATEST_VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

DEB_URL="${URL}google-chrome-${CHANNEL}_${LATEST_VERSION}-1_amd64.deb"

echo "Calculating checksum..."
CHK=$(curl -L -s "$DEB_URL" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

echo "NEW_VERSION=$LATEST_VERSION" >> $GITHUB_ENV
echo "### Done! google-chrome updated to $LATEST_VERSION"
