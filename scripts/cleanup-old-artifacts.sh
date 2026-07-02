#!/bin/bash

# gh auth login
# Замените <owner/repo> на ваш репозиторий (например, my-org/my-repo)
REPO=sofijacom/void-package
DAYS_OLD=5  # Удаляем артефакты старше 5 дней

echo "Cleaning up artifacts older than $DAYS_OLD days for repository:$REPO"

# Функция для удаления артефакта по ID
delete_artifact() {
  local artifact_id='[{"id": 1}, {"id": 2}]' | jq '..id'
  gh api -X DELETE /repos/$REPO/actions/artifacts/$artifact_id
}

# Основной цикл: получаем список артефактов и удаляем старые
PAGE=1
while true; do
  RESPONSE=$(gh api -H "Accept: application/vnd.github+json" \
    "/repos/$REPO/actions/artifacts?per_page=100&page=$PAGE")
  ARTIFACTS=$(echo "$RESPONSE" | jq -c '.artifacts | {id: .id, name: .name, created_at: .created_at}')
  if [ "$(echo "$RESPONSE" | jq '.artifacts | length')" -eq 0 ]; then
    break
  fi
  for artifact in $ARTIFACTS; do
    delete_artifact "$($ echo $artifact | jq -r '.id')"
    echo "Deleted artifact: $($ echo $artifact | jq -r '.name')"
  done
  PAGE=$((PAGE + 1))
done
echo "Cleanup completed."
