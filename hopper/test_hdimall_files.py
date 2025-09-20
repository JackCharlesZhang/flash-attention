#!/usr/bin/env python3
"""
Test script to check if all hdimall files exist
"""

import os
import itertools

# Set environment variables like the actual setup
os.environ['FLASH_ATTENTION_DISABLE_SM80'] = 'TRUE'
os.environ['FLASH_ATTENTION_DISABLE_CLUSTER'] = 'TRUE'

# Copy the relevant variables from setup.py
DISABLE_SOFTCAP = os.getenv("FLASH_ATTENTION_DISABLE_SOFTCAP", "FALSE") == "TRUE"
DISABLE_SPLIT = os.getenv("FLASH_ATTENTION_DISABLE_SPLIT", "FALSE") == "TRUE"
DISABLE_PAGEDKV = os.getenv("FLASH_ATTENTION_DISABLE_PAGEDKV", "FALSE") == "TRUE"
DISABLE_PACKGQA = os.getenv("FLASH_ATTENTION_DISABLE_PACKGQA", "FALSE") == "TRUE"
DISABLE_FP16 = os.getenv("FLASH_ATTENTION_DISABLE_FP16", "FALSE") == "TRUE"
DISABLE_FP8 = os.getenv("FLASH_ATTENTION_DISABLE_FP8", "FALSE") == "TRUE"

DTYPE_FWD_SM90 = ["bf16"] + (["fp16"] if not DISABLE_FP16 else []) + (["e4m3"] if not DISABLE_FP8 else [])
SPLIT = [""] + (["_split"] if not DISABLE_SPLIT else [])
PAGEDKV = [""] + (["_paged"] if not DISABLE_PAGEDKV else [])
SOFTCAP = [""] + (["_softcap"] if not DISABLE_SOFTCAP else [])
PACKGQA = [""] + (["_packgqa"] if not DISABLE_PACKGQA else [])

print(f'DTYPE_FWD_SM90: {DTYPE_FWD_SM90}')
print(f'SPLIT: {SPLIT}')
print(f'PAGEDKV: {PAGEDKV}')
print(f'SOFTCAP: {SOFTCAP}')
print(f'PACKGQA: {PACKGQA}')

# Generate the same file list as setup.py
sources_fwd_sm90 = [f"instantiations/flash_fwd_hdimall_{dtype}{paged}{split}{softcap}{packgqa}_sm90.cu"
                    for dtype, split, paged, softcap, packgqa in itertools.product(DTYPE_FWD_SM90, SPLIT, PAGEDKV, SOFTCAP, PACKGQA)
                    if not (packgqa and (paged or split))]

print(f'\nTotal hdimall files expected: {len(sources_fwd_sm90)}')
print('First 5 files:')
for f in sources_fwd_sm90[:5]:
    print(f'  {f}')

# Check if files exist
missing_files = []
for file_path in sources_fwd_sm90:
    if not os.path.exists(file_path):
        missing_files.append(file_path)

print(f'\nFiles checked: {len(sources_fwd_sm90)}')
print(f'Missing files: {len(missing_files)}')

if missing_files:
    print('\nMissing files:')
    for f in missing_files[:10]:  # Show first 10 missing
        print(f'  {f}')
    if len(missing_files) > 10:
        print(f'  ... and {len(missing_files) - 10} more')
else:
    print('✅ All hdimall files exist!')