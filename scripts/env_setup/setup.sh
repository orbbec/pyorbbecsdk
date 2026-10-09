#!/bin/bash

# Copyright (c) Orbbec Inc. All Rights Reserved.
# Licensed under the MIT License.

# restore current directory
current_dir=$(pwd)

# cd to the directory where this script is located
cd "$(dirname "$0")"
project_dir=$(pwd)

# set up environment variables
shared_dir=$project_dir/shared
examples_dir=$project_dir/examples

# clear quarantine bit for macOS
os_name=$(uname)
if [[ "$os_name" == "Darwin" ]]; then
    find . -type f \( -name '*ob_*' -o -name '*.dylib' \) -exec sh -c '
        for file; do
            xattr -d com.apple.quarantine "$file" 2>/dev/null || true
        done
        ' _ {} +
fi

# build the examples
if [ -d "$examples_dir" ] && [ -f "$project_dir/build_examples.sh" ]; then
    "$project_dir/build_examples.sh"
fi

# install udev rules
if [ -d "$shared_dir" ] && [ -f "$shared_dir/install_udev_rules.sh" ]; then
    echo ""
    echo "Install udev rules file now..."
    sudo "$shared_dir/install_udev_rules.sh"
fi

cd "$current_dir"

