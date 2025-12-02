#!/usr/bin/env python3
"""
Script to find incomplete MAC addresses in Cisco switch ARP table output.

This program searches a text file created from the "#sh ip arp" command
from a Cisco switch for any incomplete MAC addresses. If found, it lists
the lines and saves the results to "Incomplete-MAC-Addresses.txt".
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional


def display_banner() -> None:
    """Display the program banner."""
    print("""
 ┌─────────────────────────────────────────┐
 │  This program searches a text file      │
 │  created from the "#sh ip arp" command  │
 │  from a Cisco switch for any incomplete │
 │  MAC Addresses; if there are any it     │
 │  lists the line in which it was found,  │
 │  and saves the results to a text file   │
 │  called "Incomplete-MAC-Addresses.txt"  │
 └─────────────────────────────────────────┘ \n\n""")


def resolve_file_path(file_path: str) -> Path:
    """
    Resolve a file path, handling absolute paths, relative paths, and ~ expansion.
    
    Args:
        file_path: File path string (can be absolute, relative, or start with ~).
        
    Returns:
        Resolved Path object.
        
    Raises:
        FileNotFoundError: If the file doesn't exist after resolution.
    """
    # Expand ~ to home directory
    expanded_path = os.path.expanduser(file_path)
    
    # Convert to Path and resolve (handles relative paths and ..)
    resolved_path = Path(expanded_path).resolve()
    
    if not resolved_path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    if not resolved_path.is_file():
        raise FileNotFoundError(f"'{file_path}' is not a file.")
    
    return resolved_path


def get_input_file(file_path: Optional[str] = None) -> Path:
    """
    Get input file path from command-line argument or prompt user.
    
    Args:
        file_path: Optional file path from command-line argument.
        
    Returns:
        Path object for the selected file.
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
    """
    if file_path:
        # Use command-line argument
        return resolve_file_path(file_path)
    
    # Interactive mode: prompt user to select file
    print("Please select the #SH IP ARP Data text file\n")
    print("You can enter:")
    print("  - A filename in the current directory")
    print("  - A relative path (e.g., ../data/arp.txt)")
    print("  - An absolute path (e.g., /path/to/arp.txt)")
    print("  - A path with ~ (e.g., ~/Documents/arp.txt)\n")
    
    # List only files (not directories) in the current directory
    current_dir = Path.cwd()
    files = [f.name for f in current_dir.iterdir() if f.is_file()]
    if files:
        print(f"Files in current directory: {files}\n")
    
    file_input = input("Please enter the file path: ").strip()
    
    if not file_input:
        raise FileNotFoundError("No file path provided.")
    
    return resolve_file_path(file_input)


def find_incomplete_mac_addresses(input_file: Path) -> List[str]:
    """
    Search for lines containing "INCOMPLETE" MAC addresses.
    
    Args:
        input_file: Path to the input file to search.
        
    Returns:
        List of lines containing incomplete MAC addresses.
    """
    incomplete_lines: List[str] = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.split()
                # Check if line has at least 3 words and the third word is "INCOMPLETE"
                if len(words) >= 3 and words[2] == "INCOMPLETE":
                    incomplete_lines.append(line)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    return incomplete_lines


def save_results(incomplete_lines: List[str], output_file: Path) -> None:
    """
    Save incomplete MAC address lines to the output file.
    
    Args:
        incomplete_lines: List of lines to save.
        output_file: Path to the output file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(incomplete_lines)
    except IOError as e:
        print(f"Error writing to output file: {e}", file=sys.stderr)
        sys.exit(1)


def display_results(incomplete_lines: List[str], output_file: Path) -> None:
    """
    Display the results to the user.
    
    Args:
        incomplete_lines: List of incomplete MAC address lines.
        output_file: Path to the output file.
    """
    if incomplete_lines:
        print("\n=======================================\n")
        count = len(incomplete_lines)
        print(f"There are {count} incomplete MAC Addresses\n")
        
        for line in incomplete_lines:
            print(line, end='')
        
        print(f"\n-- Saved to \"{output_file.name}\" --\n")
    else:
        print("\nNo incomplete MAC addresses found.\n")


def main() -> None:
    """Main program entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Find incomplete MAC addresses in Cisco switch ARP table output.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s arp_output.txt
  %(prog)s /path/to/arp_output.txt
  %(prog)s ~/Documents/switch_arp.txt
  %(prog)s ../data/arp.txt
  
If no file is provided, the program will prompt you interactively.
        """
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Path to the ARP table output file (optional - will prompt if not provided)'
    )
    
    args = parser.parse_args()
    
    display_banner()
    
    try:
        input_file = get_input_file(args.input_file)
        print(f"Processing file: {input_file}\n")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    output_file = Path("Incomplete-MAC-Addresses.txt")
    
    # Find incomplete MAC addresses
    incomplete_lines = find_incomplete_mac_addresses(input_file)
    
    # Save results to file
    save_results(incomplete_lines, output_file)
    
    # Display results
    display_results(incomplete_lines, output_file)
    
    # Wait for user to exit
    input("\nPress enter to exit the program ")


if __name__ == "__main__":
    main()



            






