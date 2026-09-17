#!/bin/bash
set -euo pipefail

# В GitLab адрес репозитория указывается без .git
REPO="mullvad/mullvadvpn-app"
TEMPLATE_FILE="./srcpkgs/mullvadvpn/template"
DEB_PATTERN='.*amd64.*\.deb$'

echo "Fetching latest release from $REPO..."
# Используем публичный API GitLab. 
# Обратите внимание: Mullvad VPN хостится на GitHub, поэтому мы запрашиваем у GitLab зеркало или прокси.
# Если проект перенесут на gitlab.com/mullvad/mullvadvpn-app, путь будет таким:
API_URL="https://gitlab.com/api/v4/projects/${REPO//\//%2F}/releases/permalink/latest"
RESPONSE=$(curl -s "$API_URL")

# Логика поиска DEB-файла остается прежней, так как структура JSON релизов GitLab похожа на GitHub
DEB_URL=$(echo "$RESPONSE" | jq -r --arg pattern "$DEB_PATTERN" '
  .assets.links[]
  | select(.name | test($pattern))
  | .direct_asset_url // .url
')

if [[ -z "$DEB_URL" || "$DEB_URL" == "null" ]]; then
  echo "No .deb asset found matching pattern: $DEB_PATTERN" >&2
  exit 1
fi

VERSION=$(echo "$RESPONSE" | jq -r '.tag_name')
SHA256=""

# В GitLab нет временных файлов вроде GITHUB_OUTPUT. 
# Экспортируем данные через job artifacts, чтобы забрать их в следующих jobs.
cat > build_info.env <<EOF
VERSION=${VERSION}
DEB_URL=${DEB_URL}
EOF

echo "Downloading package: $DEB_URL"
curl -Lo mullvad.deb "$DEB_URL"

echo "Calculating SHA256..."
SHA256=$(sha256sum mullvad.deb | awk '{print $1}')
echo "SHA256: $SHA256"

# Дописываем хеш в тот же файл экспорта
echo "SHA256=${SHA256}" >> build_info.env

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Template file not found: $TEMPLATE_FILE" >&2
  exit 1
fi

CURRENT_VERSION=$(grep '^version=' "$TEMPLATE_FILE" | cut -d= -f2)

if [[ "$CURRENT_VERSION" == "$VERSION" ]]; then
  echo "Version is already up to date."
  exit 0
fi

sed -i "s/^version=.*/version=$VERSION/" "$TEMPLATE_FILE"
sed -i "s/^checksum=.*/checksum=$SHA256/" "$TEMPLATE_FILE"

echo "Template updated to version $VERSION"

# Сохраняем измененный шаблон как артефакт, чтобы его можно было выгрузить или использовать в job'е отправки MR
mkdir -p updated_template
cp "$TEMPLATE_FILE" "updated_template/template"
