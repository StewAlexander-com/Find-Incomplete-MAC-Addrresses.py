# Find-Incomplete-MAC-Addrresses.py
Finds the list of incomplete MAC addresses from a Cisco sh IP arp, if any, and counts the total
## Why did I create this?
* Looking through an entire sh ip arp from a main switch can be daunting, this expedites the process
* Why bother? Incomplete MAC addresses are indicative of a networking issue
## Output of the program:
![image](https://user-images.githubusercontent.com/48565067/144282674-46847ebd-00cb-4f1b-8641-0693d6ec0d27.png)

## Updates

### December 02, 2025
* **Code refactoring for efficiency and best practices**: Restructured the code into modular functions with clear responsibilities, improving maintainability and readability
* **Fixed critical bug**: Resolved variable shadowing issue where the same file handle variable `f` was reused in nested `with` blocks, which could cause unexpected behavior
* **Improved efficiency**: Optimized file operations to read input file once and write output file once, instead of opening/closing files multiple times
* **Added comprehensive test suite**: Created `test_find_incomplete_mac_addresses.py` with 14 test cases covering various scenarios including edge cases, ensuring code reliability
* **Added type hints and documentation**: Implemented Python 3 type hints and comprehensive docstrings for better IDE support and code documentation
* **Enhanced error handling**: Added proper file validation, IndexError protection, and IOError handling for more robust operation
* **Added .gitignore**: Created `.gitignore` file to exclude test outputs, cache files, and other files that shouldn't be committed to GitHub
* **Modernized code**: Updated to use `pathlib.Path` for file operations, f-strings for string formatting, and proper `if __name__ == "__main__"` guard

