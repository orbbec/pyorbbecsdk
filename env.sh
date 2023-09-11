#!/bin/bash

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

# shellcheck disable=SC2155
export PYTHONPATH=${CURR_DIR}/install/lib:$PYTHONPATH
