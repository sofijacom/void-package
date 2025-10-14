#!/usr/bin/env bash

# yandex-browser-stable_25.8.1.890-1_amd64.deb
pattern="yandex-browser-stable_\K\d+\.\d+\.\d+\.\d+(?=_amd64\.deb)"

#printf "Checking latest version\n"

#__dir="$(dirname "${BASH_SOURCE[0]}")"

#LATEST_VERSION=$(curl -Ss --request GET "https://repo.yandex.ru/yandex-browser/deb/pool/main/y/yandex-browser-stable/" | jq -r '.[0] | .name')
#export VERSION=${LATEST_VERSION#"v"}
#CURRENT_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)

#printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
#[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

#export SHA256=$(curl -L https://repo.yandex.ru/yandex-browser/deb/pool/main/y/yandex-browser-stable/${LATEST_VERSION}/yandex-browser-stable_${VERSION}_amd64.deb.sha256 | cut -d ' ' -f1 )
#[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

#envsubst '${SHA256} ${VERSION}' < ${__dir}/.template > ${__dir}/template

#printf "Yandex template updated\n"
