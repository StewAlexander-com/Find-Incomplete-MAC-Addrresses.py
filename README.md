# Find-Incomplete-MAC-Addrresses.py
Finds the list of incomplete MAC addresses from a Cisco sh IP arp, if any, and counts the total

## Why did I create this?
* Looking through an entire sh ip arp from a main switch can be daunting, this expedites the process
* Why bother? Incomplete MAC addresses are indicative of a networking issue

## Usage

### Command-Line Mode (Recommended)
You can pass the ARP file as a command-line argument:

```bash
python3 Find-Incomplete-MAC-Addresses.py arp_output.txt
python3 Find-Incomplete-MAC-Addresses.py /absolute/path/to/arp.txt
python3 Find-Incomplete-MAC-Addresses.py ~/Documents/switch_arp.txt
python3 Find-Incomplete-MAC-Addresses.py ../data/arp.txt
```

The script supports:
- **Absolute paths**: `/path/to/file.txt`
- **Relative paths**: `../data/file.txt` or `subdir/file.txt`
- **Home directory expansion**: `~/Documents/file.txt`
- **Current directory files**: `file.txt`

### Interactive Mode
If no file is provided, the script will prompt you interactively:

```bash
python3 Find-Incomplete-MAC-Addresses.py
```

You'll be shown files in the current directory and can enter any of the path formats listed above.

### Help
View usage information and examples:

```bash
python3 Find-Incomplete-MAC-Addresses.py --help
```

## Output of the program:
![image](https://user-images.githubusercontent.com/48565067/144282674-46847ebd-00cb-4f1b-8641-0693d6ec0d27.png)

## Updates

### December 02, 2025
* **Added command-line argument support**: The script now accepts the input file as a command-line argument, enabling automation and scripting workflows. This makes it easier to integrate into larger automation pipelines and batch processing scripts
* **Enhanced path resolution**: Added support for absolute paths, relative paths (including `..` parent directory navigation), and home directory expansion (`~`). This provides flexibility in how users specify file locations, whether files are in the current directory, subdirectories, or completely different locations
* **Improved user experience**: Interactive mode now provides clearer instructions about supported path formats, making it easier for users to understand their options when selecting files
* **Expanded test coverage**: Added 10 new test cases (24 total) covering path resolution, command-line arguments, and error handling for invalid paths. This ensures the new functionality is reliable and edge cases are properly handled
* **Updated .gitignore**: Added exclusions for additional Python development tools (type checkers, linters, Jupyter notebooks) to keep the repository clean

### December 02, 2025 (Initial Refactoring)
* **Code refactoring for efficiency and best practices**: Restructured the code into modular functions with clear responsibilities, improving maintainability and readability
* **Fixed critical bug**: Resolved variable shadowing issue where the same file handle variable `f` was reused in nested `with` blocks, which could cause unexpected behavior
* **Improved efficiency**: Optimized file operations to read input file once and write output file once, instead of opening/closing files multiple times
* **Added comprehensive test suite**: Created `test_find_incomplete_mac_addresses.py` with 14 test cases covering various scenarios including edge cases, ensuring code reliability
* **Added type hints and documentation**: Implemented Python 3 type hints and comprehensive docstrings for better IDE support and code documentation
* **Enhanced error handling**: Added proper file validation, IndexError protection, and IOError handling for more robust operation
* **Added .gitignore**: Created `.gitignore` file to exclude test outputs, cache files, and other files that shouldn't be committed to GitHub
* **Modernized code**: Updated to use `pathlib.Path` for file operations, f-strings for string formatting, and proper `if __name__ == "__main__"` guard

