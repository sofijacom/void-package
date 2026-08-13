#!/bin/bash

set -euo pipefail

API_URL="https://api.github.com/repos/mullvad/mullvadvpn-app/releases/latest"
RESPONSE=$(curl -s "$API_URL")

echo "Full release asset list for debugging:"
echo "$RESPONSE" | jq '.assets[].name'

VERSION=$(echo "$RESPONSE" | jq -r '.tag_name')
DEB_URL=$(echo "$RESPONSE" | jq -r '.assets[] | select(.name | test(".*amd64.*\\.deb$")) | .browser_download_url')

echo "Parsed version: $VERSION"
echo "Detected .deb URL: $DEB_URL"

if [[ -z "$DEB_URL" ]]; then
  echo "::notice title=No .deb found::The latest release does not contain a .deb asset. Exiting gracefully."
  echo "skip_update=true" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "version=${VERSION}" >> "$GITHUB_OUTPUT"
echo "deb_url=${DEB_URL}" >> "$GITHUB_OUTPUT"

CURRENT_VERSION=$(grep '^version=' ./srcpkgs/mullvadvpn/template | cut -d= -f2)
echo "current_version=${CURRENT_VERSION}" >> "$GITHUB_OUTPUT"

curl -Lo mullvad.deb "${{ steps.get_release.outputs.deb_url }}"
SHA256=$(sha256sum mullvad.deb | awk '{print $1}')
echo "sha256=${SHA256}" >> "$GITHUB_OUTPUT"

sed -i "s/^version=.*/version=${{ steps.get_release.outputs.version }}/" ./srcpkgs/mullvadvpn/template
sed -i "s/^checksum=.*/checksum=${{ steps.download_and_verify.outputs.sha256 }}/" ./srcpkgs/mullvadvpn/template

echo "NEW_VERSION=$VERSION" >> $GITHUB_ENV
echo "### Done! mullvadvpn updated to $VERSION"

# echo "Update Mullvad VPN to v${{ steps.get_release.outputs.version }} [automated update]"
