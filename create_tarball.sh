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
  .DS_Store
  *.pyc
  __pycache__
  *.gz
  *.bag
  *.raw
  *.png
  *.ply
)

# 初始化一个空数组
exclude_flags=()

# 循环遍历 exclude_list，将每个元素添加到 exclude_flags 数组中
for item in "${exclude_list[@]}"; do
  exclude_flags+=(--exclude="$item")
done

tar -czvf "${filename}" "${exclude_flags[@]}" .
echo "Created tarball: ${filename}"