#!/usr/bin/env python3
"""
Test script to check what sources setup.py actually generates
"""

import os

def test_setup_sources():
    # Set environment variables like CI
    os.environ['FLASH_ATTENTION_DISABLE_SM80'] = 'TRUE'
    os.environ['FLASH_ATTENTION_DISABLE_CLUSTER'] = 'TRUE'

    # Read setup.py and extract the source generation part
    with open('setup.py', 'r') as f:
        setup_content = f.read()

    # Execute just the part before setup() call to get the sources
    setup_globals = {
        '__file__': 'setup.py',  # Add missing __file__
        '__name__': '__main__'
    }
    exec(setup_content.split('setup(')[0], setup_globals)
    
    # Extract variables from the executed setup code
    PACKAGE_NAME = setup_globals['PACKAGE_NAME']
    sources = setup_globals['sources']
    
    print(f'Package name: {PACKAGE_NAME}')
    print(f'Total sources: {len(sources)}')
    print(f'SM80 sources: {len([s for s in sources if "sm80" in s])}')
    print(f'SM90 sources: {len([s for s in sources if "sm90" in s])}')
    print('First few sources:', sources[:3])
    
    # Check for batch files vs individual files
    batch_files = [s for s in sources if 'hdimall' in s or 'hdimdiff' in s or 'softcapall' in s]
    individual_files = [s for s in sources if 'hdim64' in s or 'hdim96' in s or 'hdim128' in s or 'hdim192' in s or 'hdim256' in s]
    individual_files = [s for s in individual_files if s not in batch_files]  # Remove overlaps
    
    print(f'Batch files: {len(batch_files)}')
    print(f'Individual files: {len(individual_files)}')
    
    if batch_files:
        print('Sample batch files:', batch_files[:3])
    if individual_files:
        print('Sample individual files:', individual_files[:3])
    
    return sources

if __name__ == "__main__":
    sources = test_setup_sources()