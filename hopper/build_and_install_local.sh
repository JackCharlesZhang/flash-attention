#!/bin/bash

# Local build and install script for Flash Attention 3
set -e

echo "=== Building and Installing Flash Attention 3 Locally ==="

# Check if we're in the hopper directory
if [ ! -f "setup.py" ]; then
    echo "Error: Please run this script from the hopper directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Set build environment variables for local development
export FLASH_ATTENTION_FORCE_BUILD="TRUE"
export FLASH_ATTENTION_DISABLE_SM80="TRUE"  # Faster builds

# Optional: Set for faster local builds (comment out for full build)
# export FLASH_ATTENTION_DISABLE_SPLIT="TRUE"
# export FLASH_ATTENTION_DISABLE_PAGEDKV="TRUE"

echo "Environment variables:"
echo "  FLASH_ATTENTION_FORCE_BUILD=$FLASH_ATTENTION_FORCE_BUILD"
echo "  FLASH_ATTENTION_DISABLE_SM80=$FLASH_ATTENTION_DISABLE_SM80"
echo "  FLASH_ATTENTION_DISABLE_CLUSTER=$FLASH_ATTENTION_DISABLE_CLUSTER"

# Clean previous builds
echo ""
echo "=== Cleaning previous builds ==="
rm -rf build/ dist/ *.egg-info/ || true

# Uninstall any existing flash-attn-3 installation
echo ""
echo "=== Uninstalling existing flash-attn-3 ==="
pip uninstall flash-attn-3 -y || echo "No existing installation found"

# Build and install in development mode
echo ""
echo "=== Building and installing in development mode ==="
echo "This will install the package so you can import it as 'import flash_attn_3'"

# Option 1: Development install (editable, faster for testing changes)
pip install -e . -v

# Option 2: Full wheel build and install (uncomment if you prefer this)
# python setup.py bdist_wheel
# pip install dist/*.whl --force-reinstall

echo ""
echo "=== Installation complete! ==="
echo ""
echo "You can now use Flash Attention 3 in Python:"
echo "  import flash_attn_3"
echo "  from flash_attn_3 import flash_attn_func"
echo ""
echo "To run tests:"
echo "  python -c \"import flash_attn_3; print('Import successful!')\" "
echo "  python test_single_fa3.py  # If this test file exists"
echo ""
echo "To uninstall later:"
echo "  pip uninstall flash-attn-3"