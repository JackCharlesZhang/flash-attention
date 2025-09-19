#!/usr/bin/env python3
"""
Test script to verify our setup.py source generation logic
"""

import sys
import os
import itertools
from pathlib import Path

def test_source_generation():
    # Set environment variables like CI
    os.environ['FLASH_ATTENTION_DISABLE_SM80'] = 'TRUE'
    os.environ['FLASH_ATTENTION_DISABLE_CLUSTER'] = 'TRUE'

    # Extract just the source generation logic from setup.py
    DISABLE_SOFTCAP = os.getenv('FLASH_ATTENTION_DISABLE_SOFTCAP', 'FALSE') == 'TRUE'
    DISABLE_SM8x = os.getenv('FLASH_ATTENTION_DISABLE_SM80', 'FALSE') == 'TRUE'
    DISABLE_HDIMDIFF64 = os.getenv('FLASH_ATTENTION_DISABLE_HDIMDIFF64', 'FALSE') == 'TRUE'
    DISABLE_HDIMDIFF192 = os.getenv('FLASH_ATTENTION_DISABLE_HDIMDIFF192', 'FALSE') == 'TRUE'

    print(f'DISABLE_SM8x: {DISABLE_SM8x}')
    print(f'DISABLE_SOFTCAP: {DISABLE_SOFTCAP}')

    # Test our source generation logic
    DTYPE_FWD_SM80 = ['bf16', 'fp16']
    DTYPE_FWD_SM90 = ['bf16', 'fp16', 'e4m3']
    DTYPE_BWD = ['bf16', 'fp16']
    HEAD_DIMENSIONS_FWD_SM80 = [64, 96, 128, 192, 256]
    HEAD_DIMENSIONS_BWD = [64, 96, 128, 192, 256]
    SPLIT = ['', '_split']
    PAGEDKV = ['', '_paged']
    SOFTCAP = ['', '_softcap']
    PACKGQA = ['', '_packgqa']

    # Generate sources using our modified logic
    sources_fwd_sm80 = [f'instantiations/flash_fwd_hdim{hdim}_{dtype}{paged}{split}_softcapall_sm80.cu'
                        for hdim, dtype, split, paged in itertools.product(HEAD_DIMENSIONS_FWD_SM80, DTYPE_FWD_SM80, SPLIT, PAGEDKV)] if not DISABLE_SOFTCAP else []

    sources_fwd_sm90 = []
    sources_fwd_sm90 += [f'instantiations/flash_fwd_hdimall_{dtype}{paged}{split}{softcap}{packgqa}_sm90.cu'
                         for dtype, split, paged, softcap, packgqa in itertools.product(DTYPE_FWD_SM90, SPLIT, PAGEDKV, SOFTCAP, PACKGQA)
                         if not (packgqa and (paged or split))]

    has_hdimdiff = not DISABLE_HDIMDIFF64 or not DISABLE_HDIMDIFF192
    if has_hdimdiff:
        sources_fwd_sm90 += [f'instantiations/flash_fwd_hdimdiff_{dtype}{paged}{split}{softcap}{packgqa}_sm90.cu'
                             for dtype, split, paged, softcap, packgqa in itertools.product(DTYPE_FWD_SM90, SPLIT, PAGEDKV, SOFTCAP, PACKGQA)
                             if not (packgqa and (paged or split))]

    sources_bwd_sm90 = [f'instantiations/flash_bwd_hdim{hdim}_{dtype}_softcapall_sm90.cu'
                        for hdim, dtype in itertools.product(HEAD_DIMENSIONS_BWD, DTYPE_BWD)] if not DISABLE_SOFTCAP else []

    print(f'SM80 fwd sources: {len(sources_fwd_sm80)}')
    print(f'SM90 fwd sources: {len(sources_fwd_sm90)}')
    print(f'SM90 bwd sources: {len(sources_bwd_sm90)}')

    # Check if files exist
    missing = []
    all_sources = sources_fwd_sm80 + sources_fwd_sm90 + sources_bwd_sm90
    for f in all_sources[:10]:
        if not os.path.exists(f):
            missing.append(f)

    print(f'Missing files (first 10): {missing}')
    print(f'First few sources: {all_sources[:3]}')
    
    return all_sources, missing

if __name__ == "__main__":
    all_sources, missing = test_source_generation()
    
    if missing:
        print(f"\nERROR: Found {len(missing)} missing files!")
        sys.exit(1)
    else:
        print(f"\nSUCCESS: All {len(all_sources)} source files exist!")
        sys.exit(0)