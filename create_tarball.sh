#!/bin/bash
CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SUBDIR_NAME="pyorbbecsdk"

git_hash=$(git --git-dir="${CURR_DIR}/.git" rev-parse --short HEAD)
current_date=$(date +%Y%m%d)
filename="${SUBDIR_NAME}_${current_date}_${git_hash}.tar.gz"
exclude_list=(
  .git
  cmake-build-*
  .vscode
  build
  install
  venv
  .idea
  Log
  .DS_Store
  *.pyc
  __pycache__
  *.gz
  *.bag
  *.raw
  *.png
  *.ply
)

exclude_flags=()

for item in "${exclude_list[@]}"; do
  exclude_flags+=(--exclude="$SUBDIR_NAME/$item")
done

mkdir -p "${SUBDIR_NAME}"
rsync -av --progress . "${SUBDIR_NAME}" --exclude "${SUBDIR_NAME}"

tar -czvf "${filename}" "${exclude_flags[@]}" "${SUBDIR_NAME}"
rm -rf "${SUBDIR_NAME}"
echo "Created tarball: ${filename}"
