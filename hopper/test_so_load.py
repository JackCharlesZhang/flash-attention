#!/usr/bin/env python3

import ctypes
import os
import sys

so_path = '/home/jz4267/.local/lib/python3.12/site-packages/flash_attn_3-3.0.0b1-py3.12-linux-x86_64.egg/flash_attn_3/_C.abi3.so'

print(f"Attempting to load: {so_path}")
print(f"File exists: {os.path.exists(so_path)}")
print(f"File size: {os.path.getsize(so_path)} bytes")
print()

# Try to load the shared library directly
try:
    lib = ctypes.CDLL(so_path)
    print("✓ Successfully loaded shared library with ctypes.CDLL")
except OSError as e:
    print(f"✗ Failed to load shared library: {e}")

print()

# Try importing with better error reporting
egg_path = '/home/jz4267/.local/lib/python3.12/site-packages/flash_attn_3-3.0.0b1-py3.12-linux-x86_64.egg'
if egg_path not in sys.path:
    sys.path.insert(0, egg_path)

print("Attempting Python import...")
try:
    import flash_attn_3
    print("✓ Successfully imported flash_attn_3")
except ImportError as e:
    print(f"✗ Failed to import flash_attn_3: {e}")
    print("  This is likely the undefined symbol error we saw before")

print()

# Check what symbols we can find in the .so file
print("Checking symbols in the .so file...")
try:
    import subprocess
    result = subprocess.run(['nm', '-D', so_path], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        # Look for the problematic Li86E symbol
        li86e_lines = [line for line in lines if 'Li86E' in line]
        if li86e_lines:
            print("Found Li86E symbols:")
            for line in li86e_lines[:5]:  # Show first 5
                print(f"  {line}")
        else:
            print("No Li86E symbols found in exported symbols")
            
        # Look for run_mha_bwd symbols
        bwd_lines = [line for line in lines if 'run_mha_bwd' in line]
        print(f"Found {len(bwd_lines)} run_mha_bwd symbols")
        if bwd_lines:
            print("Sample run_mha_bwd symbols:")
            for line in bwd_lines[:3]:
                print(f"  {line}")
    else:
        print("nm command failed")
except Exception as e:
    print(f"Error running nm: {e}")

print()

# Try a more direct approach - check if it's the same undefined symbol issue
print("Checking for undefined symbols...")
try:
    result = subprocess.run(['ldd', so_path], capture_output=True, text=True)
    if "not found" in result.stdout:
        print("Missing dependencies:")
        for line in result.stdout.split('\n'):
            if "not found" in line:
                print(f"  {line.strip()}")
    else:
        print("All dependencies found")
except Exception as e:
    print(f"Error running ldd: {e}")