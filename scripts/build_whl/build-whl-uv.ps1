#!/usr/bin/env pwsh
#Requires -Version 5.1
<#
.SYNOPSIS
    uv-optimized pyorbbecsdk2 build script (Windows)

.DESCRIPTION
    Build pyorbbecsdk wheel packages for specified Python versions using uv.

.PARAMETER Version
    Python version(s) to build (e.g., "3.10", "3.11"). Use "all" for 3.8-3.13.

.PARAMETER Offline
    Offline mode, skip network downloads (requires local pybind11 in venv).

.PARAMETER NoClean
    Don't clean build directories before building.

.PARAMETER Clean
    Clean build directories before building (default).

.PARAMETER CleanOnly
    Only clean, don't build.

.PARAMETER Yes
    Automatically confirm all cleanup prompts (skip interactive mode).

.EXAMPLE
    .\build-whl-uv.ps1 3.10
    # Build for Python 3.10

.EXAMPLE
    .\build-whl-uv.ps1 3.8, 3.9, 3.10
    # Build for multiple Python versions

.EXAMPLE
    .\build-whl-uv.ps1 all
    # Build all supported versions (3.8-3.13)

.EXAMPLE
    .\build-whl-uv.ps1 3.10 -Offline
    # Offline build (requires local venv with pybind11)

.EXAMPLE
    .\build-whl-uv.ps1 -CleanOnly
    # Clean only, don't build

.EXAMPLE
    .\build-whl-uv.ps1 all -Yes
    # Build all versions, auto-confirm all cleanups
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Version = @(),

    [switch]$Offline,

    [switch]$NoClean,

    [switch]$Clean,

    [switch]$CleanOnly,

    [switch]$Yes,

    [switch]$NoSync
)

$ErrorActionPreference = "Stop"

# ============================================================
# Global variables for tracking cleanup failures
# ============================================================

$script:CleanupFailed = @()
$script:CleanupSkipped = @()
$script:AutoConfirm = $Yes.IsPresent

# Per-version venv directories created by THIS run (for final cleanup).
# Only these are removed at the end; pre-existing venv<ver> dirs are left alone.
$script:CreatedVenvs = @()

# ============================================================
# Configuration
# ============================================================

$env:UV_LINK_MODE = "copy"

if ($Offline) {
    $env:UV_OFFLINE = "1"
}

# ROOT_DIR: scripts/build_whl/ -> up 2 levels = repo root
$ROOT_DIR = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Build options
$OFFLINE_MODE = $Offline.IsPresent
$CLEAN_BUILD = if ($NoClean.IsPresent) { $false } else { $true }
$CLEAN_ONLY = $CleanOnly.IsPresent

# Directory paths
$WHEEL_DIR = Join-Path $ROOT_DIR "wheel"
$INSTALL_DIR = Join-Path $ROOT_DIR "install"
$INSTALL_LIB_DIR = Join-Path $INSTALL_DIR "lib\pyorbbecsdk"
$SHARED_DST_DIR = Join-Path $INSTALL_LIB_DIR "shared"
$ENV_SETUP_SRC = Join-Path $ROOT_DIR (Join-Path "scripts" "env_setup")

# Parse Python versions and options
$PYTHON_VERSIONS = @()
foreach ($v in $Version) {
    switch -Wildcard ($v) {
        "all" {
            $PYTHON_VERSIONS = @("3.8", "3.9", "3.10", "3.11", "3.12", "3.13")
        }
        "--clean" {
            $Clean = $true
        }
        "--offline" {
            $Offline = $true
        }
        "--no-clean" {
            $NoClean = $true
        }
        "--clean-only" {
            $CleanOnly = $true
        }
        "--yes" {
            $Yes = $true
        }
        "--no-sync" {
            $NoSync = $true
        }
        "3.*" {
            $PYTHON_VERSIONS += $v
        }
        default {
            if ($v -match '^3\.\d+$') {
                $PYTHON_VERSIONS += $v
            } else {
                Write-Error "Unknown option or version: $v"
                exit 1
            }
        }
    }
}

# NO_SYNC must be computed after parsing, since --no-sync can be passed as a
# positional arg (handled in the switch above) or as the -NoSync switch.
$NO_SYNC = $NoSync.IsPresent

# Default to 3.10 if no versions specified
if ($PYTHON_VERSIONS.Count -eq 0) {
    $PYTHON_VERSIONS = @("3.10")
}

# ============================================================
# Helper Functions
# ============================================================

function Show-Usage {
    @"
Usage: $(Split-Path -Leaf $PSCommandPath) [OPTIONS] [VERSION...]

Build pyorbbecsdk wheel packages for specified Python versions.

Options:
  -Offline        Offline mode, skip network downloads (requires local pybind11)
  -NoClean        Don't clean build directories before building
  -Clean          Clean build directories before building (default)
  -CleanOnly      Only clean, don't build
  -Yes            Auto-confirm all cleanup prompts (non-interactive)
  -NoSync         Use the currently activated virtual environment instead of
                  recreating venv<ver> and running uv sync. Requires an active
                  venv (VIRTUAL_ENV must be set); pybind11 is used as-is.
  -?, -Help       Show this help message

Arguments:
  VERSION         Python version (e.g., 3.10, 3.11) or 'all' for 3.8-3.13

Examples:
  $(Split-Path -Leaf $PSCommandPath) 3.10              # Build Python 3.10
  $(Split-Path -Leaf $PSCommandPath) 3.8, 3.9, 3.10    # Build multiple versions
  $(Split-Path -Leaf $PSCommandPath) all               # Build all versions (3.8-3.13)
  $(Split-Path -Leaf $PSCommandPath) 3.10 -Offline     # Offline build
  $(Split-Path -Leaf $PSCommandPath) -CleanOnly        # Clean only, don't build
  $(Split-Path -Leaf $PSCommandPath) all -Yes          # Auto-confirm cleanups
"@ | Write-Host
}

# Show help if requested
if ($Version -contains "-?" -or $Version -contains "-Help" -or $Version -contains "--help" -or $Version -contains "-h") {
    Show-Usage
    exit 0
}

# Remove a directory with error handling, returns $true if success or not exists
function Remove-DirectorySafe {
    param(
        [string]$Path,
        [string]$Name
    )

    if (-not (Test-Path $Path)) {
        return $true
    }

    try {
        Remove-Item -Recurse -Force $Path -ErrorAction Stop
        Write-Host "    Deleted: $Name"
        return $true
    }
    catch {
        Write-Warning "    Failed to delete: $Name - $($_.Exception.Message)"
        $script:CleanupFailed += "$Name ($Path)"
        return $false
    }
}

# Confirm deletion interactively
function Confirm-Delete {
    param(
        [string]$Path,
        [string]$Name
    )

    if (-not (Test-Path $Path)) {
        return $true
    }

    Write-Host -NoNewline "  Found: $Name - delete? (y=yes/n=no/a=all/s=skip-all): "
    $response = Read-Host

    switch ($response.ToLower()) {
        "y" {
            return (Remove-DirectorySafe -Path $Path -Name $Name)
        }
        "a" {
            $script:AutoConfirm = $true
            return (Remove-DirectorySafe -Path $Path -Name $Name)
        }
        "s" {
            Write-Host "    Skipped: $Name"
            $script:CleanupSkipped += "$Name ($Path)"
            return $false
        }
        default {
            Write-Host "    Skipped: $Name"
            $script:CleanupSkipped += "$Name ($Path)"
            return $false
        }
    }
}

function Invoke-InteractiveCleanup {
    Write-Host ">>> Checking for existing build artifacts to clean"
    Write-Host ""

    # Collect paths to check
    $pathsToCheck = @(
        @{ Path = (Join-Path $ROOT_DIR "build"); Name = "build directory" },
        @{ Path = (Join-Path $ROOT_DIR "dist"); Name = "dist directory" },
        @{ Path = (Join-Path $ROOT_DIR "install"); Name = "install directory" },
        @{ Path = $WHEEL_DIR; Name = "wheel directory" }
    )

    # Check for build_* directories
    Get-ChildItem -Path $ROOT_DIR -Directory -Filter "build_*" -ErrorAction SilentlyContinue | ForEach-Object {
        $pathsToCheck += @{ Path = $_.FullName; Name = "$($_.Name) directory" }
    }

    # Check if anything exists
    $hasItems = $false
    foreach ($item in $pathsToCheck) {
        if (Test-Path $item.Path) {
            $hasItems = $true
            break
        }
    }

    if (-not $hasItems) {
        Write-Host "  No build artifacts found, nothing to clean."
        Write-Host ""
        New-Item -ItemType Directory -Force $WHEEL_DIR | Out-Null
        return
    }

    # Process each path
    $skipAll = $false
    foreach ($item in $pathsToCheck) {
        $path = $item.Path
        $name = $item.Name

        if ($skipAll) {
            Write-Host "  Skipped: $name"
            $script:CleanupSkipped += "$name ($path)"
            continue
        }

        if ($script:AutoConfirm) {
            Remove-DirectorySafe -Path $path -Name $name | Out-Null
        }
        else {
            $result = Confirm-Delete -Path $path -Name $name
            if (-not $result -and -not $script:AutoConfirm) {
                # User chose skip-all
                $skipAll = $true
            }
        }
    }

    Write-Host ""
    New-Item -ItemType Directory -Force $WHEEL_DIR | Out-Null
}

function Invoke-PerVersionCleanup {
    param([string]$PyVer)

    $buildDir = Join-Path $ROOT_DIR "build_$PyVer"
    $distDir = Join-Path $ROOT_DIR "dist"

    Write-Host "  Cleaning build artifacts for Python $PyVer..."

    Remove-DirectorySafe -Path $buildDir -Name "build_$PyVer directory" | Out-Null
    Remove-DirectorySafe -Path $INSTALL_DIR -Name "install directory" | Out-Null
    Remove-DirectorySafe -Path $distDir -Name "dist directory" | Out-Null

    # Recreate required directories
    New-Item -ItemType Directory -Force $buildDir | Out-Null
    New-Item -ItemType Directory -Force $SHARED_DST_DIR | Out-Null
}

function Install-PythonVersion {
    <#
    .SYNOPSIS
        Ensures the specified Python version is installed via uv.
    .DESCRIPTION
        Checks if the Python version is available via 'uv python list'.
        If not installed, automatically installs it using 'uv python install'.
    .PARAMETER PyVer
        Python version to ensure (e.g., "3.10", "3.11")
    .EXAMPLE
        $pythonExe = Install-PythonVersion -PyVer "3.10"
    #>
    param(
        [string]$PyVer
    )

    # Check if Python version is already installed using uv python list
    $isInstalled = $false
    $installedVersions = $null
    try {
        $installedVersions = uv python list 2>$null
    }
    catch {
        $installedVersions = $null
    }

    if ($installedVersions) {
        foreach ($line in $installedVersions) {
            if ($line -match "\b$([regex]::Escape($PyVer))\b") {
                $isInstalled = $true
                break
            }
        }
    }

    # If already installed, just find and return the executable
    if ($isInstalled) {
        try {
            # Use Push-Location to avoid project .venv interfering with uv python find
            Push-Location $env:TEMP
            $pythonExe = uv python find $PyVer 2>$null
            Pop-Location
            if ($pythonExe -and (Test-Path $pythonExe)) {
                return $pythonExe
            }
        }
        catch {
            # uv python find may fail even if list shows it, continue to install
            $pythonExe = $null
        }
    }

    # Not found - auto-install
    Write-Host ""
    Write-Host "Python ${PyVer} not found. Installing via uv..."
    Write-Host "  (This may take a few minutes depending on network speed)"

    # Execute installation - show progress by not suppressing output
    uv python install ${PyVer}
    $installExitCode = $LASTEXITCODE

    if ($installExitCode -ne 0) {
        Write-Error @"
Failed to install Python ${PyVer} via uv.

Possible causes:
- Network connectivity issues
- Invalid Python version: ${PyVer}
- uv tool not properly installed

To manually install, run:
  uv python install ${PyVer}
"@
        exit 1
    }

    Write-Host "Python ${PyVer} installed successfully."

    # Verify installation and return executable path
    try {
        # Use Push-Location to avoid project .venv interfering with uv python find
        Push-Location $env:TEMP
        $pythonExe = uv python find ${PyVer} 2>$null
        Pop-Location
    }
    catch {
        $pythonExe = $null
    }
    if (-not $pythonExe -or -not (Test-Path $pythonExe)) {
        Write-Error "Python ${PyVer} was reported as installed but cannot be found."
        exit 1
    }

    return $pythonExe
}

# Get the venv path for a Python version (e.g. "3.10" -> venv310)
function Get-VenvPath {
    param([string]$PyVer)
    $venvSuffix = $PyVer.Replace(".", "")
    return Join-Path $ROOT_DIR "venv$venvSuffix"
}

# Get the python executable inside the per-version venv
function Get-VenvPython {
    param([string]$PyVer)
    return Join-Path (Get-VenvPath $PyVer) "Scripts\python.exe"
}

# Recreate the per-version venv (delete + uv venv) for reproducible automated builds
function New-PerVersionVenv {
    param([string]$PyVer)

    $venvDir = Get-VenvPath $PyVer
    $venvPython = Get-VenvPython $PyVer

    Write-Host "  Recreating venv for Python $PyVer..."
    Remove-DirectorySafe -Path $venvDir -Name "venv for $PyVer" | Out-Null
    New-Item -ItemType Directory -Force (Split-Path -Parent $venvDir) | Out-Null

    uv venv $venvDir --python $PyVer
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create venv for Python $PyVer"
        exit 1
    }

    if (-not (Test-Path $venvPython)) {
        Write-Error "venv for Python $PyVer created but python not found at $venvPython"
        exit 1
    }

    # Track this venv so final cleanup removes only what this run created.
    $script:CreatedVenvs += $venvDir

    return $venvDir
}

# Validate that a virtual environment is activated (for --no-sync mode).
# Returns the python executable path of the active venv, or exits on error.
function Get-ActiveVenvPython {
    if (-not $env:VIRTUAL_ENV) {
        Write-Error @"
--no-sync requires an activated virtual environment.
Please activate a venv first, e.g.:
  . .\venv310\Scripts\Activate.ps1
then re-run.
"@
        exit 1
    }

    $candidates = @(
        (Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"),
        (Join-Path $env:VIRTUAL_ENV "bin\python")
    )
    foreach ($py in $candidates) {
        if (Test-Path $py) {
            return $py
        }
    }

    Write-Error "No python executable found in activated venv '$($env:VIRTUAL_ENV)'."
    exit 1
}

# Get pybind11 CMake dir from the currently activated venv (--no-sync mode).
# Uses the active venv's pybind11 as-is; does not install or pin a version.
function Get-ActivePybind11Dir {
    $py = Get-ActiveVenvPython
    $output = & $py -c "import pybind11; print(pybind11.get_cmake_dir())"
    if ($LASTEXITCODE -ne 0 -or -not $output) {
        Write-Error "Failed to resolve pybind11 CMake directory from active venv (is pybind11 installed there?)"
        exit 1
    }
    return $output.Trim()
}

function Get-Pybind11Dir {
    param([string]$PyVer)

    # pybind11 is installed into the per-version venv with a pinned version
    # (matches pyproject.toml [build-system].requires). This keeps the CMake
    # compile environment identical to the packaging environment.
    $venvPython = Get-VenvPython $PyVer

    Write-Host "  Installing pybind11==2.12.0 into venv for Python $PyVer..."
    uv pip install pybind11==2.12.0 --python $venvPython
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install pybind11 into venv for Python $PyVer"
        exit 1
    }

    $output = & $venvPython -c "import pybind11; print(pybind11.get_cmake_dir())"
    if ($LASTEXITCODE -ne 0 -or -not $output) {
        Write-Error "Failed to resolve pybind11 CMake directory from venv python"
        exit 1
    }

    return $output.Trim()
}

function Get-VSGenerator {
    <#
    .SYNOPSIS
        Detects installed Visual Studio version and returns CMake generator.
    .DESCRIPTION
        Uses vswhere.exe to find installed VS versions (2017, 2019, 2022, 2026).
        Falls back to cmake --help if vswhere is not available.
    .OUTPUTS
        String - CMake generator name (e.g., "Visual Studio 17 2022")
    #>
    $VSGenerator = $null
    $VSInstallPath = $null

    # vswhere is included with VS2017+ and located at fixed path
    $vswherePath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

    if (Test-Path $vswherePath) {
        # Check for VS2022 (v17)
        $VSInstallPath = & $vswherePath -version "[17.0,18.0)" -products "*" -property installationPath 2>$null | Select-Object -First 1
        if ($VSInstallPath) {
            $VSGenerator = "Visual Studio 17 2022"
        } else {
            # Check for VS2019 (v16)
            $VSInstallPath = & $vswherePath -version "[16.0,17.0)" -products "*" -property installationPath 2>$null | Select-Object -First 1
            if ($VSInstallPath) {
                $VSGenerator = "Visual Studio 16 2019"
            } else {
                # Check for VS2017 (v15)
                $VSInstallPath = & $vswherePath -version "[15.0,16.0)" -products "*" -property installationPath 2>$null | Select-Object -First 1
                if ($VSInstallPath) {
                    $VSGenerator = "Visual Studio 15 2017"
                } else {
                    # Check for VS2026 (v18) - future version
                    $VSInstallPath = & $vswherePath -version "[18.0,19.0)" -products "*" -property installationPath 2>$null | Select-Object -First 1
                    if ($VSInstallPath) {
                        $VSGenerator = "Visual Studio 18 2026"
                    }
                }
            }
        }
    }

    # If vswhere not available or no VS found, try cmake --help as fallback
    if (-not $VSGenerator) {
        $VSGenerators = @(
            "Visual Studio 17 2022",
            "Visual Studio 16 2019",
            "Visual Studio 15 2017",
            "Visual Studio 18 2026"
        )

        foreach ($gen in $VSGenerators) {
            $result = cmake --help 2>&1 | Select-String $gen
            if ($result) {
                $VSGenerator = $gen
                break
            }
        }
    }

    return $VSGenerator
}

function Invoke-BuildVersion {
    param([string]$PyVer)

    Write-Host ""
    Write-Host "==========================================="
    Write-Host " Building pyorbbecsdk for Python $PyVer"
    Write-Host "==========================================="

    $BUILD_DIR = Join-Path $ROOT_DIR "build_$PyVer"

    # Per-version cleanup
    if ($CLEAN_BUILD) {
        Invoke-PerVersionCleanup $PyVer
    } else {
        New-Item -ItemType Directory -Force $BUILD_DIR | Out-Null
        New-Item -ItemType Directory -Force $SHARED_DST_DIR | Out-Null
    }

    # In --no-sync mode, use the currently activated venv as-is (no recreate,
    # no pinned pybind11, no uv sync). Otherwise recreate the per-version venv
    # for reproducible automated builds.
    if ($NO_SYNC) {
        Write-Host "  --no-sync: using activated venv (no venv recreation, no uv sync)"
        $VENV_PYTHON = Get-ActiveVenvPython
        $VENV_DIR = Split-Path -Parent (Split-Path -Parent $VENV_PYTHON)
        Write-Host "  Using active venv Python: $VENV_PYTHON"

        # Resolve pybind11 from the active venv (use as-is, not pinned)
        Write-Host "Resolving pybind11 CMake directory from active venv..."
        $PYBIND11_DIR = Get-ActivePybind11Dir
        Write-Host "pybind11_DIR=$PYBIND11_DIR"
    } else {
        # Recreate the per-version venv (delete + uv venv) for reproducible builds.
        # Ensures no stale packages from previous runs leak into the build.
        $VENV_DIR = New-PerVersionVenv -PyVer $PyVer

        # Resolve Python interpreter (auto-install if needed)
        Write-Host "Resolving Python interpreter..."
        $PYTHON_EXE = Install-PythonVersion -PyVer $PyVer
        Write-Host "Using Python: $PYTHON_EXE"

        # Use the per-version venv python for CMake, so pybind11 (installed into the
        # venv) and the Python headers/libs are from the same interpreter.
        $VENV_PYTHON = Get-VenvPython $PyVer
        Write-Host "Using venv Python for build: $VENV_PYTHON"

        # Resolve pybind11 CMake directory (installs pinned pybind11 into the venv)
        Write-Host "Resolving pybind11 CMake directory..."
        $PYBIND11_DIR = Get-Pybind11Dir $PyVer
        Write-Host "pybind11_DIR=$PYBIND11_DIR"
    }

    # CMake configure & build
    Push-Location $BUILD_DIR

    try {
        # Get Python root directory for CMake (force specific Python version)
        $pythonRoot = Split-Path -Parent (Split-Path -Parent $VENV_PYTHON)

        # Detect installed Visual Studio
        $VSGenerator = Get-VSGenerator

        if (-not $VSGenerator) {
            Write-Warning "Visual Studio 2017/2019/2022/2026 not found, trying default generator"
            cmake `
                -DCMAKE_BUILD_TYPE=Release `
                -DCMAKE_PREFIX_PATH="$pythonRoot" `
                -DPython3_EXECUTABLE="$VENV_PYTHON" `
                -DPython3_ROOT_DIR="$pythonRoot" `
                -DPython3_FIND_STRATEGY=LOCATION `
                -Dpybind11_DIR="$PYBIND11_DIR" `
                -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" `
                "$ROOT_DIR"
        } else {
            Write-Host "Using generator: $VSGenerator"
            cmake -G $VSGenerator -A x64 `
                -DCMAKE_BUILD_TYPE=Release `
                -DCMAKE_PREFIX_PATH="$pythonRoot" `
                -DPython3_EXECUTABLE="$VENV_PYTHON" `
                -DPython3_ROOT_DIR="$pythonRoot" `
                -DPython3_FIND_STRATEGY=LOCATION `
                -Dpybind11_DIR="$PYBIND11_DIR" `
                -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" `
                "$ROOT_DIR"
        }

        if ($LASTEXITCODE -ne 0) {
            throw "CMake configuration failed (Python $PyVer)"
        }

        cmake --build . --config Release --target install --parallel

        if ($LASTEXITCODE -ne 0) {
            throw "CMake build failed (Python $PyVer)"
        }
    }
    finally {
        Pop-Location
    }

    # Copy extra runtime files
    Write-Host "Copying extra runtime files..."

    $examplesDir = Join-Path $ROOT_DIR "examples"
    $configDir = Join-Path $ROOT_DIR "config"
    $requirementsFile = Join-Path $ROOT_DIR "requirements.txt"

    if (Test-Path $examplesDir) {
        Copy-Item -Recurse -Force $examplesDir $INSTALL_LIB_DIR
    }

    if (Test-Path $configDir) {
        Copy-Item -Recurse -Force $configDir $INSTALL_LIB_DIR
    }

    if (Test-Path $requirementsFile) {
        $examplesDest = Join-Path $INSTALL_LIB_DIR "examples"
        New-Item -ItemType Directory -Force $examplesDest | Out-Null
        Copy-Item -Force $requirementsFile $examplesDest
    }

    if (Test-Path $ENV_SETUP_SRC) {
        Get-ChildItem -Path $ENV_SETUP_SRC -Filter "*.ps1" -ErrorAction SilentlyContinue |
            Copy-Item -Destination $SHARED_DST_DIR -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path $ENV_SETUP_SRC -Filter "*.md" -ErrorAction SilentlyContinue |
            Copy-Item -Destination $SHARED_DST_DIR -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path $ENV_SETUP_SRC -Filter "setup_env.py" -ErrorAction SilentlyContinue |
            Copy-Item -Destination $SHARED_DST_DIR -Force -ErrorAction SilentlyContinue
    }

    # Copy pyi stub files
    Write-Host "Copying pyi stub files..."
    $STUBS_DIR = Join-Path $ROOT_DIR "stubs"
    if (Test-Path $STUBS_DIR) {
        $pyiFiles = @("__init__.pyi", "pyorbbecsdk.pyi")
        foreach ($pyiFile in $pyiFiles) {
            $srcPath = Join-Path $STUBS_DIR $pyiFile
            if (Test-Path $srcPath) {
                Copy-Item -Force $srcPath $INSTALL_LIB_DIR
                Write-Host "  Copied $pyiFile"
            } else {
                Write-Host "  Warning: $pyiFile not found in $STUBS_DIR"
            }
        }
    } else {
        Write-Host "  Warning: stubs directory not found at $STUBS_DIR"
    }

    # Sync runtime dependencies + project into the per-version venv.
    # CMake has already produced install/lib, so the editable install of
    # pyorbbecsdk2 (which copies install/lib) will succeed.
    # In --no-sync mode this step is skipped; the active venv is used as-is.
    if ($NO_SYNC) {
        Write-Host "  --no-sync: skipping uv sync (using active venv as-is)"
    } else {
        Write-Host "Syncing dependencies via uv sync into $VENV_DIR..."
        Push-Location $ROOT_DIR
        try {
            $env:UV_PROJECT_ENVIRONMENT = $VENV_DIR
            # --no-install-project: install dependencies only. Installing the
            # project editable would run setup.py build_ext, whose output dir
            # resolves to src/pyorbbecsdk/ and pollutes the source tree.
            uv sync --no-install-project --python $PyVer
            if ($LASTEXITCODE -ne 0) {
                throw "uv sync failed (Python $PyVer)"
            }
            Remove-Item Env:UV_PROJECT_ENVIRONMENT -ErrorAction SilentlyContinue
        }
        finally {
            Pop-Location
        }
    }

    # Build wheel via uv. Point --python at the venv's python executable so
    # the wheel is tagged for the correct CPython version. Using a bare version
    # number would re-resolve a system interpreter, and omitting it lets the
    # build backend pick the project .venv (which may be a different Python).
    Write-Host "Building wheel..."
    Push-Location $ROOT_DIR
    try {
        $env:UV_PROJECT_ENVIRONMENT = $VENV_DIR
        uv build --wheel --python "$VENV_PYTHON" --link-mode copy
        if ($LASTEXITCODE -ne 0) {
            throw "uv build failed (Python $PyVer)"
        }
        Remove-Item Env:UV_PROJECT_ENVIRONMENT -ErrorAction SilentlyContinue
    }
    finally {
        Pop-Location
    }

    $distDir = Join-Path $ROOT_DIR "dist"
    if (Test-Path $distDir) {
        Get-ChildItem (Join-Path $distDir "*.whl") | Copy-Item -Destination $WHEEL_DIR -Force
        Remove-DirectorySafe -Path $distDir -Name "dist directory" | Out-Null
    }

    Write-Host "Finished Python $PyVer"
}

function Invoke-FinalCleanup {
    Write-Host ""
    Write-Host ">>> Final cleanup..."

    # Remove build_* directories
    Get-ChildItem -Path $ROOT_DIR -Directory -Filter "build_*" -ErrorAction SilentlyContinue |
        ForEach-Object {
            Remove-DirectorySafe -Path $_.FullName -Name "$($_.Name) directory" | Out-Null
        }

    $dirsToRemove = @(
        @{ Path = (Join-Path $ROOT_DIR "build"); Name = "build directory" },
        @{ Path = (Join-Path $ROOT_DIR "dist"); Name = "dist directory" }
    )

    # In --no-sync mode we use the user's activated venv, so keep install/
    # (the compiled C++ artifacts) for them to inspect/use. Otherwise remove it.
    if ($NO_SYNC) {
        Write-Host "  --no-sync: keeping install directory for the active venv build"
    } else {
        $dirsToRemove += @{ Path = (Join-Path $ROOT_DIR "install"); Name = "install directory" }
    }

    foreach ($dir in $dirsToRemove) {
        Remove-DirectorySafe -Path $dir.Path -Name $dir.Name | Out-Null
    }

    # Remove egg-info directories
    $srcDir = Join-Path $ROOT_DIR "src"
    if (Test-Path $srcDir) {
        Get-ChildItem -Path $srcDir -Directory -Filter "*.egg-info" -ErrorAction SilentlyContinue |
            ForEach-Object {
                Remove-DirectorySafe -Path $_.FullName -Name "$($_.Name)" | Out-Null
            }

        # Remove __pycache__ dirs left under src/ by the build
        Get-ChildItem -Path $srcDir -Directory -Filter "__pycache__" -Recurse -ErrorAction SilentlyContinue |
            ForEach-Object {
                Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
            }
    }

    # Remove only the per-version venv dirs THIS run created. Pre-existing
    # venv<ver> dirs (e.g. from an earlier manual setup) are left untouched.
    foreach ($venvDir in $script:CreatedVenvs) {
        Remove-DirectorySafe -Path $venvDir -Name (Split-Path -Leaf $venvDir) | Out-Null
    }
}

function Show-CleanupReport {
    Write-Host ""
    Write-Host "==========================================="

    if ($script:CleanupFailed.Count -eq 0 -and $script:CleanupSkipped.Count -eq 0) {
        Write-Host " Cleanup completed successfully"
        Write-Host " All temporary files were removed"
    }
    else {
        if ($script:CleanupFailed.Count -gt 0) {
            Write-Host " Cleanup completed with FAILURES:"
            Write-Host ""
            Write-Host "  Failed to delete the following items:"
            foreach ($item in $script:CleanupFailed) {
                Write-Host "    - $item" -ForegroundColor Red
            }
        }

        if ($script:CleanupSkipped.Count -gt 0) {
            Write-Host ""
            Write-Host "  Skipped the following items (user requested):"
            foreach ($item in $script:CleanupSkipped) {
                Write-Host "    - $item" -ForegroundColor Yellow
            }
        }

        Write-Host ""
        Write-Host "  You may need to manually remove these files/directories"
        Write-Host "  or run the script with -CleanOnly to try again."
    }

    Write-Host ""
    Write-Host " Wheels are located in: $WHEEL_DIR"
    Write-Host "==========================================="
}

# ============================================================
# Main Entry Point
# ============================================================

# Global cleanup (always run first)
if ($CLEAN_BUILD) {
    Invoke-InteractiveCleanup
} else {
    New-Item -ItemType Directory -Force $WHEEL_DIR | Out-Null
}

# Clean only mode
if ($CLEAN_ONLY) {
    Show-CleanupReport
    Write-Host ""
    Write-Host ">>> Clean completed (no build requested)"
    exit 0
}

# Build each version
foreach ($PyVer in $PYTHON_VERSIONS) {
    Invoke-BuildVersion $PyVer
}

# Final cleanup
Invoke-FinalCleanup

# Show final report
Show-CleanupReport
