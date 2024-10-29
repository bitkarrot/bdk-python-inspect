from ffi_explorer import FFIExplorer
import bdkpython

explorer = FFIExplorer(bdkpython)
findings = explorer.explore_module()

# Look for specific functionality
for name, details in findings.items():
    if 'wallet' in name.lower():
        print(f"Found wallet-related component: {name}")
        print(details)
