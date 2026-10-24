#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

# Используем репозиторий Qt-версии
REPO="josejp2424/Rox-Filer2-QT"
TPL="srcpkgs/Rox-Filer2-QT/template" # Путь к вашему файлу

echo "### Checking for Rox-Filer2-QT updates..."

command -v gh >/dev/null 2>&1 || { echo "Error: 'gh' is not installed."; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "Error: 'curl' is not installed."; exit 1; }

# Получаем последний тег. У Qt-проекта свои теги (например, v1.0.7-QT)
if ! LATEST_TAG=$(gh api repos/"$REPO"/releases/latest --jq .tag_name); then
    echo "Error: Failed to fetch latest tag from GitHub API."
    exit 1
fi

# Нормализация версии: убираем 'v' и суффикс '-QT', заменяем дефисы на точки
# Из тега v1.0.7-QT получится версия 1.0.7
LATEST_VERSION=${LATEST_TAG#v}
VERSION="${LATEST_VERSION%-QT}"
VERSION="${VERSION//-/.}"

if [[ ! -f "$TPL" ]]; then
    echo "Error: Template file '$TPL' not found."
    exit 1
fi
mapfile -t CURRENT_LINES < <(grep -E '^(version|checksum)=' "$TPL")
CURRENT_VERSION=$(echo "${CURRENT_LINES[0]}" | cut -d= -f2 | tr -d '"')

printf "Latest version is: %s\nCurrent version is: %s\n" "$VERSION" "$CURRENT_VERSION"

if [[ "$VERSION" == "$CURRENT_VERSION" ]]; then
    echo "No update required."
    exit 0
fi

echo "Update found: $CURRENT_VERSION -> $VERSION"

# URL должен точно соответствовать distfiles в шаблоне
URL="https://github.com/$REPO/archive/refs/tags/${LATEST_TAG}.tar.gz"

echo "Calculating checksum..."
if ! ARCHIVE_CONTENT=$(curl -L --fail-with-body -s "$URL"); then
    echo "Error: Failed to download archive from $URL"
    exit 1
fi
CHK=$(echo "$ARCHIVE_CONTENT" | sha256sum | awk '{print $1}')

if [[ -z "$CHK" ]]; then
    echo "Error: Failed to calculate checksum."
    exit 1
fi

echo "Checksum: $CHK"

# Обновляем шаблон
sed -i "s/^version=.*/version=\"$VERSION\"/" "$TPL"
sed -i "s/^checksum=.*/checksum=\"$CHK\"/" "$TPL"

printf 'NEW_VERSION=%s\nOLD_VERSION=%s\n' "$VERSION" "$CURRENT_VERSION" >> "$GITHUB_ENV"

echo "### Done! Rox-Filer2-QT updated to $VERSION"
