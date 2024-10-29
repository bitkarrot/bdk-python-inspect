import inspect
from typing import Any, List, Dict
import textwrap

class FFIExplorer:
    def __init__(self, module):
        self.module = module
        
    def explore_object(self, obj: Any, indent: int = 0) -> str:
        """Explore an object and return its structure as a string."""
        result = []
        
        # Get object type
        obj_type = type(obj)
        result.append(f"Type: {obj_type}")
        
        # Get docstring if available
        if obj.__doc__:
            doc = textwrap.dedent(obj.__doc__).strip()
            result.append(f"Documentation:\n{textwrap.indent(doc, '  ')}")
            
        # Get methods
        methods = inspect.getmembers(obj, predicate=inspect.ismethod)
        if methods:
            result.append("\nMethods:")
            for name, method in methods:
                if not name.startswith('_'):  # Skip private methods
                    sig = inspect.signature(method)
                    result.append(f"  {name}{sig}")
                    if method.__doc__:
                        doc = textwrap.dedent(method.__doc__).strip()
                        result.append(f"    {doc.split('.')[0]}.")  # First sentence only
                        
        # Get attributes
        try:
            attrs = {name: getattr(obj, name) for name in dir(obj)
                    if not name.startswith('_')}
            if attrs:
                result.append("\nAttributes:")
                for name, value in attrs.items():
                    if not inspect.ismethod(value):
                        result.append(f"  {name}: {type(value).__name__}")
        except Exception:
            pass
            
        return '\n'.join(result)
    
    def explore_module(self) -> Dict[str, str]:
        """Explore the entire module and return a dictionary of findings."""
        results = {}
        
        for name, obj in inspect.getmembers(self.module):
            if not name.startswith('_'):  # Skip private attributes
                if inspect.isclass(obj):
                    results[name] = self.explore_object(obj)
                elif inspect.isfunction(obj):
                    sig = inspect.signature(obj)
                    results[name] = f"Function: {name}{sig}\n"
                    if obj.__doc__:
                        results[name] += f"Documentation:\n{textwrap.indent(obj.__doc__, '  ')}"
                        
        return results

# Usage example
import bdkpython

explorer = FFIExplorer(bdkpython)
findings = explorer.explore_module()

# Print findings in a readable format
for name, details in findings.items():
    print(f"\n{'=' * 50}")
    print(f"Component: {name}")
    print(f"{'=' * 50}")
    print(details)
    print()
