#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '/home/jz4267/miniconda3/envs/test/lib/python3.12/site-packages')

print("Testing flash-attn import...")
try:
    import flash_attn_3
    print("✓ Successfully imported flash_attn_3")
    print(f"flash_attn_3 location: {flash_attn_3.__file__}")
except ImportError as e:
    print(f"✗ Failed to import flash_attn_3: {e}")

print("\nTesting Python import...")
try:
    import _C
    print("✓ Successfully imported _C module")
except ImportError as e:
    print(f"✗ Failed to import _C module: {e}")

print("\nTesting torch import...")
try:
    import torch
    print(f"✓ PyTorch version: {torch.__version__}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✓ CUDA version: {torch.version.cuda}")
        print(f"✓ Device capability: {torch.cuda.get_device_capability()}")
except Exception as e:
    print(f"✗ Torch error: {e}")