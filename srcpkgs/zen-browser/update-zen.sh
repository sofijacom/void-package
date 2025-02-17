#!/usr/bin/env bash

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

LATEST_VERSION=$(gh release list --repo zen-browser/desktop --json name,isLatest --jq '.[] | select(.isLatest)|.name' | awk '{ print $2 }')
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

# No preprepped checksum files, need to download the binary and calculate it myself
gh release download -R zen-browser/desktop -p "zen.linux-x86_64.tar.xz" --output "zen.linux-x86_64.tar.xz"
export SHA256=$(sha256sum ./zen.linux-x86_64.tar.xz | cut -d ' ' -f1 )
rm ./zen.linux-x86_64.tar.xz
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

envsubst '${SHA256} ${VERSION}' < ${__dir}/.template > ${__dir}/template

printf "Zen template updated\n"