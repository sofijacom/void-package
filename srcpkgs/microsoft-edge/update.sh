#!/usr/bin/env bash

printf "Checking latest version\n"

LATEST_VERSION=$(gh release list --repo NDViet/microsoft-edge --json name,tagName,isLatest --jq '.[] | select(.isLatest)|.tagName')
export VERSION=${LATEST_VERSION#"v"}
CURRENT_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

export SHA256=$(curl -sL https://github.com/NDViet/microsoft-edge-stable/releases/download/${VERSION}/microsoft-edge-stable_${VERSION}_amd64.deb | shasum -a 256 | cut -d " " -f 1 )
## | cut -d ' ' -f1 )
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

envsubst '${SHA256} ${VERSION}' < ${__dir}/.template > ${__dir}/template

printf "microsoft-edge-stable template updated\n"

