#!/usr/bin/env python3

import site
import sys
import os
import glob

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print()

print("Site-packages locations:")
for path in site.getsitepackages():
    print(f"  {path}")

print()
print("User site-packages:")
print(f"  {site.getusersitepackages()}")

print()
print("sys.path entries:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

print()
print("Searching for flash-related packages...")

# Check all possible site-packages locations
all_paths = site.getsitepackages() + [site.getusersitepackages()]
for path in all_paths:
    if os.path.exists(path):
        print(f"\nChecking {path}:")
        try:
            items = os.listdir(path)
            flash_items = [item for item in items if 'flash' in item.lower()]
            if flash_items:
                print(f"  Flash-related items: {flash_items}")
                # Check contents of flash directories
                for item in flash_items:
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        print(f"    Contents of {item}:")
                        try:
                            contents = os.listdir(item_path)
                            so_files = [f for f in contents if f.endswith('.so')]
                            if so_files:
                                print(f"      .so files: {so_files}")
                            else:
                                print(f"      Files: {contents[:10]}...")  # Limit output
                        except:
                            print(f"      (could not read)")
            else:
                print(f"  No flash-related items found")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"\n{path} does not exist")

print()
print("Looking for any .so files with 'flash' in the name...")
for path in all_paths:
    if os.path.exists(path):
        try:
            so_files = glob.glob(os.path.join(path, '**/*flash*.so'), recursive=True)
            if so_files:
                print(f"Found in {path}:")
                for so_file in so_files:
                    print(f"  {so_file}")
        except:
            pass