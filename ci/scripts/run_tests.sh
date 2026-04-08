#!/usr/bin/env bash
# =============================================================================
# run_tests.sh - Unified Test Runner Script
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LOG_DIR="${REPO_ROOT}/logs"
REPORT_DIR="${REPO_ROOT}/reports"

mkdir -p "${LOG_DIR}" "${REPORT_DIR}"

HARDWARE_AVAILABLE="${HARDWARE_AVAILABLE:-false}"
PYTHON_VERSION="${PYTHON_VERSION:-3.10}"
TEST_MARKERS="${TEST_MARKERS:-""}"

show_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Run pyorbbecsdk test suite.

Options:
  --hardware          Enable hardware tests (requires device)
  --markers MARKERS   pytest markers to select (e.g., "g300_series")
  --python VERSION    Python version (default: 3.10)
  -h, --help          Show this help message

Examples:
  $(basename "$0")                          # Run no-hardware tests
  $(basename "$0") --hardware               # Run all tests with device
  $(basename "$0") --markers "g300_series"  # Run G300 series tests
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --hardware)
                HARDWARE_AVAILABLE="true"
                shift
                ;;
            --markers)
                TEST_MARKERS="$2"
                shift 2
                ;;
            --python)
                PYTHON_VERSION="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

run_tests() {
    local pytest_args=(
        "${REPO_ROOT}/test"
        "-v"
        "--timeout=60"
        "--junit-xml=${REPORT_DIR}/pytest.xml"
        "-o" "log_cli=true"
        "--tb=short"
    )

    if [[ "${HARDWARE_AVAILABLE}" != "true" ]]; then
        pytest_args+=("-m" "not hardware")
    elif [[ -n "${TEST_MARKERS}" ]]; then
        pytest_args+=("-m" "${TEST_MARKERS}")
    fi

    echo "=========================================="
    echo " Running Tests"
    echo " HARDWARE: ${HARDWARE_AVAILABLE}"
    echo " MARKERS: ${TEST_MARKERS:-(none)}"
    echo "=========================================="

    pytest "${pytest_args[@]}" 2>&1 | tee "${LOG_DIR}/pytest.log"
}

main() {
    parse_args "$@"

    # Check if pyorbbecsdk is installed
    if ! python -c "import pyorbbecsdk" 2>/dev/null; then
        echo "Error: pyorbbecsdk not installed. Please build and install first."
        exit 1
    fi

    # Install test dependencies
    pip install pytest pytest-timeout --quiet

    run_tests

    echo "[SUCCESS] Tests completed."
}

main "$@"
