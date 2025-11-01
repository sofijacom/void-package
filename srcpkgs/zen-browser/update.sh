#!/bin/sh

# Script to update Zen Browser xbps-src template
#
# Required: xbps-src, curl, sed, xtools
#
# You have to set XBPS_DISTDIR
# Example: export XBPS_DISTDIR="$HOME/.void-packages"

if [ -z "$XBPS_DISTDIR" ]; then
  echo "Please set XBPS_DISTDIR to your xbps-src directory."
  exit 1
fi

cd "$XBPS_DISTDIR" || exit 1

release_url=$(curl -Ls -o /dev/null -w '%{url_effective}' https://github.com/zen-browser/desktop/releases/latest)
release_tag=$(basename "$release_url")
release_tag=$(echo "$release_tag" | sed 's/-//g')
echo "Downloading Zen Browser $release_tag"

sed -i 's/version=[a-zA-Z0-9.-]\+/version='"$release_tag"'/' "srcpkgs/zen-browser/template" && echo "Updated version in template to $release_tag"

xgensum -i zen-browser && echo "Generated checksums for Zen Browser"

./xbps-src pkg zen-browser && echo "Built Zen Browser package"

xi zen-browser && echo "Installed Zen Browser package $release_tag"
