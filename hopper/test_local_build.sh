#!/bin/bash

# Local test script to mimic GitHub Actions build environment
set -e

echo "=== Local Build Test for Flash Attention 3 ==="
echo "This script mimics the GitHub Actions build environment"

# Set the same environment variables as GitHub Actions
export MAX_JOBS=1  # Match GitHub's resource constraints
export NVCC_THREADS=2
export FLASH_ATTENTION_FORCE_BUILD="TRUE"
export FLASH_ATTENTION_FORCE_CXX11_ABI="FALSE"  # Default value

# Disable features for faster testing builds (same as GitHub)
export FLASH_ATTENTION_DISABLE_CLUSTER="TRUE"
export FLASH_ATTENTION_DISABLE_SM80="TRUE"

echo "Environment variables set:"
echo "  MAX_JOBS=$MAX_JOBS"
echo "  NVCC_THREADS=$NVCC_THREADS"
echo "  FLASH_ATTENTION_FORCE_BUILD=$FLASH_ATTENTION_FORCE_BUILD"
echo "  FLASH_ATTENTION_DISABLE_CLUSTER=$FLASH_ATTENTION_DISABLE_CLUSTER"
echo "  FLASH_ATTENTION_DISABLE_SM80=$FLASH_ATTENTION_DISABLE_SM80"

# Check if we're in the hopper directory
if [ ! -f "setup.py" ]; then
    echo "Error: Please run this script from the hopper directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check Python and pip
echo ""
echo "=== Python Environment ==="
python --version
pip --version

# Install required packages (same as GitHub)
echo ""
echo "=== Installing build dependencies ==="
pip install setuptools==75.8.0
pip install ninja packaging wheel

# Check CUDA availability
echo ""
echo "=== CUDA Environment ==="
if command -v nvcc &> /dev/null; then
    nvcc --version
else
    echo "WARNING: nvcc not found in PATH"
fi

echo "CUDA_HOME: ${CUDA_HOME:-not set}"

# Find PyTorch CUDA include paths (same logic as GitHub)
echo ""
echo "=== Looking for CUDA headers ==="
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
echo "Site packages: $SITE_PACKAGES"

# Find all CUDA include directories from nvidia packages
CUDA_INCLUDES=""

# Debug: list all nvidia packages
echo "Available nvidia packages:"
ls -la "$SITE_PACKAGES/nvidia/" 2>/dev/null || echo "No nvidia directory found"

# Look for include directories in nvidia packages
for include_dir in $(find "$SITE_PACKAGES/nvidia" -name "include" -type d 2>/dev/null); do
  if [ -d "$include_dir" ] && [ "$(ls -A "$include_dir")" ]; then
    echo "Found CUDA include directory: $include_dir"
    if [ -z "$CUDA_INCLUDES" ]; then
      CUDA_INCLUDES="$include_dir"
    else
      CUDA_INCLUDES="$CUDA_INCLUDES:$include_dir"
    fi
    # List some headers for debugging
    find "$include_dir" -name "*.h" -type f 2>/dev/null | head -3
  fi
done

# Also search for specific headers we need
echo "Searching for specific CUDA headers..."
for header in cusparse.h cublas_v2.h; do
  HEADER_PATH=$(find "$SITE_PACKAGES" -name "$header" -type f 2>/dev/null | head -1)
  if [ -n "$HEADER_PATH" ]; then
    HEADER_DIR=$(dirname "$HEADER_PATH")
    echo "Found $header at: $HEADER_PATH"
    if [[ ":$CUDA_INCLUDES:" != *":$HEADER_DIR:"* ]]; then
      if [ -z "$CUDA_INCLUDES" ]; then
        CUDA_INCLUDES="$HEADER_DIR"
      else
        CUDA_INCLUDES="$CUDA_INCLUDES:$HEADER_DIR"
      fi
    fi
  else
    echo "WARNING: $header not found in site-packages"
  fi
done

if [ -n "$CUDA_INCLUDES" ]; then
  export CPATH="$CUDA_INCLUDES${CPATH:+:$CPATH}"
  echo "Added to CPATH: $CUDA_INCLUDES"
else
  echo "WARNING: Could not find CUDA include directories"
  # Fallback to system CUDA or create dummy headers
  if [ -d "/usr/local/cuda-12.9/include" ]; then
    export CPATH="/usr/local/cuda-12.9/include${CPATH:+:$CPATH}"
    echo "Using system CUDA headers"
  else
    echo "Creating minimal dummy headers"
    mkdir -p include
    echo "#pragma once" > include/cusparse.h
    echo "#pragma once" > include/cublas_v2.h
    export CPATH="$(pwd)/include${CPATH:+:$CPATH}"
  fi
fi

# Clean any previous builds
echo ""
echo "=== Cleaning previous builds ==="
rm -rf build/ dist/ *.egg-info/ || true

# Run the build (same as GitHub)
echo ""
echo "=== Starting Python setup.py build ==="
EXIT_CODE=0
python setup.py bdist_wheel --dist-dir=dist -v 2>&1 | tee build.log || EXIT_CODE=$?
echo "=== Build finished with exit code: $EXIT_CODE ==="

# Show last 100 lines of build output for debugging
echo "=== Last 100 lines of build output ==="
tail -100 build.log || true

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Built wheels:"
    ls -la dist/
else
    echo ""
    echo "❌ Build failed with exit code: $EXIT_CODE"
    echo "Check build.log for full details"
    
    # Show some key error indicators
    echo ""
    echo "=== Looking for common error patterns ==="
    grep -i "error\|failed\|exception" build.log | tail -20 || echo "No obvious error patterns found"
fi

exit $EXIT_CODE