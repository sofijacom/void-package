#!/bin/bash

set -euo pipefail

REPO="brave/brave-browser"
TPL="srcpkgs/brave-origin/template"

echo "### Checking for brave-origin updates..."

if [ ! -f "$TPL" ]; then
    echo "Error: Template file not found: $TPL"
    exit 1
fi

# Cari release yang punya aset brave-origin ZIP (exact match, bukan .sha256 dll)
LATEST_VERSION=$(gh api "repos/$REPO/releases?per_page=50" \
    --jq '[.[] | select(any(.assets[]; .name | test("brave-origin.*amd64\\.zip$")))] | first | .tag_name' \
    | sed 's/^v//')

if [ -z "$LATEST_VERSION" ]; then
    echo "Error: Failed to fetch latest version."
    exit 1
fi

CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)
if [ -z "$CURRENT_VERSION" ]; then
    echo "Error: Failed to read current version from template."
    exit 1
fi

echo "Current version : $CURRENT_VERSION"
echo "Latest version  : $LATEST_VERSION"

if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required."
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $LATEST_VERSION"

# Ambil URL langsung dari API, hanya file .zip (bukan .sha256 atau .asc)
URL=$(gh api "repos/$REPO/releases?per_page=50" \
    --jq "[.[] | select(.tag_name == \"v${LATEST_VERSION}\")] | first | .assets[] | select(.name | test(\"brave-origin.*amd64\\\\.zip$\")) | .browser_download_url")

if [ -z "$URL" ]; then
    echo "Error: RPM asset not found in release v${LATEST_VERSION}."
    exit 1
fi

echo "Fetching checksum from: $URL"

CHK=$(curl -fL --retry 3 --retry-delay 2 -s "$URL" | sha256sum | awk '{print $1}')
if [ -z "$CHK" ]; then
    echo "Error: Failed to calculate checksum."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$LATEST_VERSION/" "$TPL"
sed -i "s/^revision=.*/revision=1/" "$TPL"
sed -i "s/^checksum=.*/checksum=\"$CHK\"/" "$TPL"

if [ -n "${GITHUB_ENV:-}" ]; then
    echo "NEW_VERSION=$LATEST_VERSION" >> "$GITHUB_ENV"
fi

echo "### Done! brave-origin updated to $LATEST_VERSION"
