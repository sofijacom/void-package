#!/usr/bin/env bash

set -euo pipefail

REPO="thuutien/Conky-Manager-3"
TPL="srcpkgs/conky-manager3/template"

echo "### Checking for conky-manager3 updates..."

# Detect the channel with error handling
if ! LATEST_TAG=$(gh api repos/"$REPO"/releases/latest --jq .tag_name 2>/dev/null); then
    echo "Error: Failed to fetch latest tag from GitHub API."
    exit 1
fi

VERSION=${LATEST_TAG#v}

# Read current version safely
if [[ ! -f "$TPL" ]]; then
    echo "Error: Template file '$TPL' not found."
    exit 1
fi
CURRENT_VERSION=$(grep '^version=' "$TPL" | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "$VERSION" "$CURRENT_VERSION"

# Основной контроль версий (дублирующая однострочная проверка выше удалена)
if [ "$VERSION" = "$CURRENT_VERSION" ]; then
    echo "No update required. Current version: $CURRENT_VERSION"
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $VERSION"

URL="https://github.com/$REPO/archive/refs/tags/v${VERSION}.tar.gz"

echo "Calculating checksum..."
CHK=$(curl -L -s "$URL" | sha256sum | awk '{print $1}')

if [ -z "$CHK" ]; then
    echo "Error: Failed to fetch or hash archive."
    exit 1
fi

echo "Checksum: $CHK"

sed -i "s/^version=.*/version=$VERSION/" "$TPL"
sed -i "s/^checksum=.*/checksum=$CHK/" "$TPL"

# Передача в следующие шаги GitHub Actions
printf 'NEW_VERSION=%s\n' "$VERSION" >> "$GITHUB_ENV"

echo "### Done! conky-manager3 updated to $VERSION"
