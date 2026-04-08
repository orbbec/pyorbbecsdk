#!/usr/bin/env bash
# =============================================================================
# 06-nightly.sh - Nightly Regression Test Stage
# =============================================================================

set -euo pipefail

run_nightly() {
    log_info "Running nightly regression tests..."
    start_timer

    export HARDWARE_AVAILABLE="true"

    # Device health check
    log_info "Checking device health..."
    if ! check_device_connected; then
        log_error "No Orbbec device connected"
        exit 1
    fi

    get_device_info

    # Build wheel
    log_info "Building wheel..."
    source "${SCRIPT_DIR}/stages/03-build.sh"
    build_wheel "linux" "${PYTHON_VERSION}"

    # Install wheel
    log_info "Installing wheel..."
    pip install "${REPO_ROOT}/wheel"/*.whl pytest pytest-timeout --quiet

    local status="success"

    # Run all hardware tests
    log_info "Running all hardware tests..."
    if pytest "${REPO_ROOT}/test" \
        -v \
        -m "hardware" \
        --timeout=300 \
        --junit-xml="${REPO_ROOT}/reports/nightly-hardware.xml" \
        2>&1 | tee "${REPO_ROOT}/logs/nightly.log"; then
        log_success "Hardware tests completed"
    else
        log_warning "Some hardware tests failed"
    fi

    # Run G300 series tests
    log_info "Running G300 series tests..."
    if pytest "${REPO_ROOT}/test" \
        -v \
        -m "g300_series" \
        --timeout=300 \
        --junit-xml="${REPO_ROOT}/reports/nightly-g300.xml" \
        2>&1 | tee -a "${REPO_ROOT}/logs/nightly.log"; then
        log_success "G300 series tests completed"
    else
        log_warning "Some G300 series tests failed"
    fi

    # Run performance tests
    log_info "Running performance tests..."
    if pytest "${REPO_ROOT}/test/test_g300_series_performance.py" \
        -v \
        -m "performance" \
        --timeout=600 \
        --junit-xml="${REPO_ROOT}/reports/nightly-performance.xml" \
        2>&1 | tee -a "${REPO_ROOT}/logs/nightly.log"; then
        log_success "Performance tests completed"
    else
        log_warning "Some performance tests failed"
    fi

    # Generate report
    local duration
    duration=$(end_timer)
    generate_report_summary "nightly" "${status}" "${duration}"

    log_success "Nightly regression tests completed"
}
