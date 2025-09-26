#!/usr/bin/env python3

import os
import sys
import glob

# Check what's in site-packages
site_packages = '/home/jz4267/miniconda3/envs/test/lib/python3.12/site-packages'
print(f"Checking {site_packages}...")

# Look for flash_attn related packages
flash_dirs = []
for item in os.listdir(site_packages):
    if 'flash' in item.lower():
        flash_dirs.append(item)
        
print(f"Flash-related directories: {flash_dirs}")

# Check each flash directory
for dir_name in flash_dirs:
    full_path = os.path.join(site_packages, dir_name)
    print(f"\n=== Contents of {dir_name} ===")
    if os.path.isdir(full_path):
        try:
            contents = os.listdir(full_path)
            for item in contents:
                item_path = os.path.join(full_path, item)
                if item.endswith('.so'):
                    print(f"  {item} (shared library)")
                elif os.path.isdir(item_path):
                    print(f"  {item}/ (directory)")
                    # Check for .so files in subdirectories
                    try:
                        sub_contents = os.listdir(item_path)
                        so_files = [f for f in sub_contents if f.endswith('.so')]
                        if so_files:
                            print(f"    Contains: {so_files}")
                    except:
                        pass
                else:
                    print(f"  {item}")
        except Exception as e:
            print(f"  Error reading directory: {e}")
    else:
        print(f"  {dir_name} is not a directory")

# Also check for any .so files globally in site-packages
print(f"\n=== All .so files in site-packages ===")
so_files = glob.glob(os.path.join(site_packages, '**/*.so'), recursive=True)
for so_file in so_files:
    if 'flash' in so_file.lower():
        print(f"  {so_file}")