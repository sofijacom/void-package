#!/bin/bash
set -euo pipefail

# --- Настройки ---
REPO="mullvad/mullvadvpn-app"
ASSET_PATTERN=".*amd64.*\\.deb$"
TEMPLATE_FILE="./srcpkgs/mullvadvpn/template"

# --- Функция: запись в GITHUB_OUTPUT, если доступно ---
safe_output() {
  local key="$1"
  local value="$2"
  echo "$key=$value" >> "$GITHUB_OUTPUT" 2>/dev/null || true
  # Также экспортируем в переменные окружения для использования в том же сценарии
  export "GH_${key^^}=$value"
}

# --- 1. Получаем данные с GitHub API ---
echo "Fetching latest release from $REPO..."
API_URL="https://api.github.com/repos/$REPO/releases/latest"
RESPONSE=$(curl -s "$API_URL")

echo "Found assets:"
echo "$RESPONSE" | jq -r '.assets[].name'

VERSION=$(echo "$RESPONSE" | jq -r '.tag_name')
DEB_URL=$(echo "$RESPONSE" | jq -r ".assets[] | select(.name | test(\"$ASSET_PATTERN\")) | .browser_download_url")

if [[ -z "$DEB_URL" ]]; then
  echo "❌ No matching .deb asset found for pattern: $ASSET_PATTERN" >&2
  exit 1
fi

echo "✅ Version: $VERSION"
echo "✅ DEB URL: $DEB_URL"

# --- Сохраняем в outputs и окружение ---
safe_output "version" "$VERSION"
safe_output "deb_url" "$DEB_URL"

# --- 2. Скачиваем и считаем хеш ---
echo "📥 Downloading package..."
curl -Lo mullvad.deb "$DEB_URL"

SHA256=$(sha256sum mullvad.deb | awk '{print $1}')
echo "✅ SHA256: $SHA256"
safe_output "sha256" "$SHA256"

# --- 3. Обновляем шаблон ---
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "❌ Template file not found: $TEMPLATE_FILE" >&2
  exit 1
fi

echo "🔧 Updating template: $TEMPLATE_FILE"
sed -i "s/^version=.*/version=$VERSION/" "$TEMPLATE_FILE"
sed -i "s/^checksum=.*/checksum=$SHA256/" "$TEMPLATE_FILE"

echo "✅ Template updated successfully!"

# --- Дополнительно: экспорт в GITHUB_ENV, если нужно в последующих шагах ---
echo "NEW_VERSION=$VERSION" >> "$GITHUB_ENV" 2>/dev/null || true

echo "🎉 Done MullvadVPN updated to version $VERSION"
