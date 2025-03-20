#!/usr/bin/env bash

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

PROJECT_ID="48070925"
LATEST_VERSION=$(curl -Ss --request GET "https://gitlab.com/api/v4/projects/${PROJECT_ID}/repository/tags" | jq -r '.[0] | .name')
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

curl --output rebos.tar.gz https://gitlab.com/Oglo12/rebos/-/archive/${LATEST_VERSION}/rebos-${LATEST_VERSION}.tar.gz
[ ! -f rebos.tar.gz ] && printf "got junk instead of rebos archive\n" && exit 1
export SHA256=$(sha256sum rebos.tar.gz | cut -d ' ' -f1)
rm rebos.tar.gz

[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

envsubst '${SHA256} ${VERSION}' < ${__dir}/.template > ${__dir}/template

printf "Rebos template updated\n"