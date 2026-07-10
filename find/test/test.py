import os
from modes.scanner import runScanner

print(os.getcwd())
print(os.path.expanduser("~\\AppData\\Roaming"))


runScanner("default")
print("worked correctly")

