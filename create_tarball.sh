#!/bin/bash
CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

git_hash=$(git --git-dir="${CURR_DIR}/.git" rev-parse --short HEAD)
current_date=$(date +%Y%m%d)
filename="pyorbbecsdk_${current_date}_${git_hash}.tar.gz"
exclude_list=(
  .git
  cmake-build-*
  .vscode
  build
  install
  venv
  .idea
  Log
  .vscode
   .DS_Store
  *.pyc
  __pycache__
  *.gz
)
exclude_flags=$(printf -- "--exclude=%s " "${exclude_list[@]}")
tar -czvf "${filename}" ${exclude_flags} .
echo "Created tarball: ${filename}"
