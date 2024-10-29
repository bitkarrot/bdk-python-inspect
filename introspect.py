import bdkpython
import inspect

# Print all available attributes and methods
print(dir(bdkpython))

# For a specific class (if you know one), you can inspect it more deeply
# For example, if you know there's a Wallet class:
print(inspect.getmembers(bdkpython.Wallet))
