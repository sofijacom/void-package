#!/bin/bash
set -euo pipefail

# --- Настройки ---
REPO="mullvad/mullvadvpn-app"
TEMPLATE_FILE="./srcpkgs/mullvadvpn/template"
DEB_PATTERN='.*amd64.*\.deb$'  # Ищем MullvadVPN-2026.4_amd64.deb

# --- Вспомогательная функция: безопасная запись в GITHUB_OUTPUT ---
safe_output() {
  local key="$1"
  local value="$2"
  echo "$key=$value" >> "$GITHUB_OUTPUT" 2>/dev/null || true
}

# --- 1. Получаем данные о последнем релизе ---
echo "Fetching latest release from $REPO..."
API_URL="https://api.github.com/repos/$REPO/releases/latest"
RESPONSE=$(curl -s -H "Accept: application/vnd.github.v3+json" "$API_URL")

# --- Отладка: выводим все ассеты ---
echo "Found assets:"
echo "$RESPONSE" | jq -r '.assets[].name'

# --- 2. Ищем URL .deb для amd64 ---
echo "Searching for .deb asset matching pattern: $DEB_PATTERN"

DEB_URL=$(echo "$RESPONSE" | jq -r --arg pattern "$DEB_PATTERN" '
  .assets[] 
  | select(.name | test($pattern)) 
  | .browser_download_url
')

if [[ -z "$DEB_URL" || "$DEB_URL" == "null" ]]; then
  echo "No .deb asset found matching pattern: $DEB_PATTERN" >&2
  exit 1
fi

VERSION=$(echo "$RESPONSE" | jq -r '.tag_name')
if [[ -z "$VERSION" || "$VERSION" == "null" ]]; then
  echo "Failed to extract version from release" >&2
  exit 1
fi

echo "Version: $VERSION"
echo "DEB URL: $DEB_URL"

# --- 3. Сохраняем данные ---
safe_output "version" "$VERSION"
safe_output "deb_url" "$DEB_URL"

# --- 4. Скачиваем и считаем SHA256 ---
echo "Downloading package: $DEB_URL"
curl -Lo mullvad.deb "$DEB_URL"

echo "Calculating SHA256..."
SHA256=$(sha256sum mullvad.deb | awk '{print $1}')

echo "SHA256: $SHA256"
safe_output "sha256" "$SHA256"

# --- 5. Проверяем и обновляем template ---
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Template file not found: $TEMPLATE_FILE" >&2
  exit 1
fi

CURRENT_VERSION=$(grep '^version=' "$TEMPLATE_FILE" | cut -d= -f2)
echo "Current version in template: $CURRENT_VERSION"
echo "New version: $VERSION"

if [[ "$CURRENT_VERSION" == "$VERSION" ]]; then
  echo "Version is already up to date — no changes needed."
  exit 0
fi

echo "Updating template: $TEMPLATE_FILE"
sed -i "s/^version=.*/version=$VERSION/" "$TEMPLATE_FILE"
sed -i "s/^checksum=.*/checksum=$SHA256/" "$TEMPLATE_FILE"

echo "Template successfully updated to version $VERSION"

# --- 6. Экспортируем версию в окружение (для GitHub Actions) ---
echo "NEW_VERSION=$VERSION" >> "$GITHUB_ENV" 2>/dev/null || true

# --- Финал ---
echo "Done MullvadVPN updated from $CURRENT_VERSION to $VERSION"
