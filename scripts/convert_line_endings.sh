#!/bin/bash

# This script will recursively find all text files in the current directory
# and its subdirectories and convert them from Windows line endings to Linux line endings.

# Using find to recursively locate all files
find . -type f | while read -r file; do
    # Check if the file is a text file
    if file "$file" | grep -q text; then
        # Convert the file's line endings using dos2unix
        dos2unix "$file"
        echo "Converted: $file"
    fi
done

echo "Conversion completed!"
