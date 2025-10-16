#!/usr/bin/env bash

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

LATEST_VERSION=$(gh release list --repo alex-courtis/wideriver --json name,tagName,isLatest --jq '.[] | select(.isLatest)|.tagName')
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

# No preprepped checksum files, need to download the binary and calculate it myself
gh release download -R alex-courtis/wideriver --archive=tar.gz --output "wideriver.tar.gz"
export SHA256=$(sha256sum ./wideriver.tar.gz | cut -d ' ' -f1 )
rm ./wideriver.tar.gz
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

envsubst '${SHA256} ${VERSION}' < ${__dir}/.template > ${__dir}/template

printf "wideriver template updated\n"
