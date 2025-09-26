#!/usr/bin/env python3

import os
import glob

egg_path = '/home/jz4267/.local/lib/python3.12/site-packages/flash_attn_3-3.0.0b1-py3.12-linux-x86_64.egg'

print(f"Examining flash_attn_3 egg: {egg_path}")
print()

def explore_directory(path, prefix=""):
    try:
        items = os.listdir(path)
        for item in sorted(items):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"{prefix}{item}/")
                if not item.startswith('.'):  # Skip hidden dirs
                    explore_directory(item_path, prefix + "  ")
            else:
                size = os.path.getsize(item_path)
                if item.endswith('.so'):
                    print(f"{prefix}{item} ({size} bytes) *** SHARED LIBRARY ***")
                elif item.endswith('.py'):
                    print(f"{prefix}{item} ({size} bytes)")
                else:
                    print(f"{prefix}{item} ({size} bytes)")
    except Exception as e:
        print(f"{prefix}Error reading directory: {e}")

if os.path.exists(egg_path):
    explore_directory(egg_path)
    
    print()
    print("Looking specifically for .so files...")
    so_files = glob.glob(os.path.join(egg_path, '**/*.so'), recursive=True)
    for so_file in so_files:
        print(f"  {so_file}")
        
    print()
    print("Looking for _C module...")
    c_files = glob.glob(os.path.join(egg_path, '**/*_C*'), recursive=True)
    for c_file in c_files:
        print(f"  {c_file}")
        
else:
    print(f"Egg path does not exist: {egg_path}")

# Also check if we can import from the egg
print()
print("Testing import from egg...")
import sys
if egg_path not in sys.path:
    sys.path.insert(0, egg_path)

try:
    import flash_attn_3
    print("✓ Successfully imported flash_attn_3")
    print(f"  Location: {flash_attn_3.__file__}")
    
    # Try to access the _C module
    try:
        from flash_attn_3 import _C
        print("✓ Successfully imported _C from flash_attn_3")
    except ImportError as e:
        print(f"✗ Failed to import _C from flash_attn_3: {e}")
        
except ImportError as e:
    print(f"✗ Failed to import flash_attn_3: {e}")