#!/usr/bin/env bash
# =============================================================================
# 02-lint.sh - Code Linting Stage
# =============================================================================

set -euo pipefail

run_lint() {
    log_info "Starting lint checks..."
    start_timer

    local status="success"

    # Install lint tools
    log_info "Installing lint tools..."
    pip install black isort flake8 --quiet

    # Run black check
    log_info "Running black format check..."
    if black --check . 2>&1 | tee "${REPO_ROOT}/logs/black.log"; then
        log_success "Black format check passed"
    else
        log_warning "Black format check failed (run 'black .' to fix)"
        status="warning"
    fi

    # Run isort check
    log_info "Running isort check..."
    if isort --check . 2>&1 | tee "${REPO_ROOT}/logs/isort.log"; then
        log_success "isort check passed"
    else
        log_warning "isort check failed (run 'isort .' to fix)"
        status="warning"
    fi

    # Run flake8
    log_info "Running flake8..."
    if flake8 src/ --max-line-length=120 --ignore=E203,W503 2>&1 | tee "${REPO_ROOT}/logs/flake8.log"; then
        log_success "flake8 check passed"
    else
        log_error "flake8 check failed"
        status="failure"
    fi

    # Generate report
    local duration
    duration=$(end_timer)
    generate_report_summary "lint" "${status}" "${duration}"

    if [[ "${status}" == "failure" ]]; then
        exit 1
    fi

    log_success "Lint checks completed"
}
