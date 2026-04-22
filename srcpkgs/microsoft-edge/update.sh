#!/usr/bin/env bash

printf "Checking latest version\n"

__dir="$(dirname "${BASH_SOURCE[0]}")"

LATEST_VERSION=$(git ls-remote --tags --refs https://github.com/NDViet/microsoft-edge-stable | grep -o 'microsoft-edge-stable-\(v\)\?[0-9]\+\.[0-9]\+\.[0-9]\+-[0-9]\{8,14\}$' \
  | awk -F- '
      {
        ts = $NF
        while (length(ts) < 14) ts = ts "0"
        print ts, $0
      }
    ' \
  | sort -nr | head -n1 | cut -d' ' -f2-
)
VERSION=${LATEST_VERSION#"v"}
CUR_VERSION=$(grep -E '^version=' ${__dir}/template | cut -d= -f2)
CUR_TIMESTAMP=$(grep -E '^timestamp=' ${__dir}/template | cut -d= -f2)
CURRENT_VERSION=$(printf "%s-%s" "${CUR_VERSION}" "${CUR_TIMESTAMP}")

printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

export TIMESTAMP=${VERSION##*-}
export VERSION=${VERSION%-*}


printf "Latest version is: %s\nLatest built version is: %s\n" "${VERSION}" "${CURRENT_VERSION}"
[ "${CURRENT_VERSION}" = "${VERSION}" ] && printf "No new version to release\n" && exit 0

export SHA256=$(curl -sL https://github.com/NDViet/microsoft-edge-stable/releases/download/${VERSION}/microsoft-edge-stable_${VERSION}_amd64.deb | shasum -a 256 | cut -d " " -f 1 )
## | cut -d ' ' -f1 )
[[ ! ${SHA256} =~ ^[a-z0-9]+$ ]] && printf "got junk instead of sha256\n" && exit 1

envsubst '${SHA256} ${VERSION} ${TIMESTAMP}' < ${__dir}/.template > ${__dir}/template

printf "microsoft-edge-stable template updated\n"

