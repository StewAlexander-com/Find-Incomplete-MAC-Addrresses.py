#!/usr/bin/env python3
"""
Test suite for Find-Incomplete-MAC-Addresses.py

This test file uses mock Cisco switch ARP table output to test
the functionality of finding incomplete MAC addresses.
"""

import pytest
import tempfile
import importlib.util
from pathlib import Path
from typing import List

# Import the functions from the main module (handling hyphenated filename)
import sys
module_path = Path(__file__).parent / "Find-Incomplete-MAC-Addresses.py"
spec = importlib.util.spec_from_file_location("find_incomplete_mac_addresses", module_path)
find_incomplete_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(find_incomplete_module)

# Import functions from the loaded module
find_incomplete_mac_addresses = find_incomplete_module.find_incomplete_mac_addresses
save_results = find_incomplete_module.save_results
display_results = find_incomplete_module.display_results
resolve_file_path = find_incomplete_module.resolve_file_path
get_input_file = find_incomplete_module.get_input_file


class TestResolveFilePath:
    """Test cases for path resolution functionality."""
    
    def test_resolve_absolute_path(self, tmp_path):
        """Test resolving an absolute path."""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        result = resolve_file_path(str(test_file))
        
        assert result.exists()
        assert result.is_file()
        assert result == test_file.resolve()
    
    def test_resolve_relative_path(self, tmp_path, monkeypatch):
        """Test resolving a relative path."""
        # Change to tmp_path directory
        monkeypatch.chdir(tmp_path)
        
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        result = resolve_file_path("test_arp.txt")
        
        assert result.exists()
        assert result.is_file()
        assert result.name == "test_arp.txt"
    
    def test_resolve_relative_path_with_parent(self, tmp_path, monkeypatch):
        """Test resolving a relative path with .. parent directory."""
        # Create a subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        # Change to subdirectory
        monkeypatch.chdir(subdir)
        
        result = resolve_file_path("../test_arp.txt")
        
        assert result.exists()
        assert result.is_file()
        assert result.name == "test_arp.txt"
    
    def test_resolve_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError, match="not found"):
            resolve_file_path("/nonexistent/file.txt")
    
    def test_resolve_directory_not_file(self, tmp_path):
        """Test that error is raised when path is a directory, not a file."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        with pytest.raises(FileNotFoundError, match="is not a file"):
            resolve_file_path(str(test_dir))


class TestGetInputFile:
    """Test cases for getting input file with command-line or interactive mode."""
    
    def test_get_input_file_with_argument(self, tmp_path):
        """Test get_input_file with command-line argument."""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        result = get_input_file(str(test_file))
        
        assert result.exists()
        assert result == test_file.resolve()
    
    def test_get_input_file_with_relative_path(self, tmp_path, monkeypatch):
        """Test get_input_file with relative path argument."""
        monkeypatch.chdir(tmp_path)
        
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        result = get_input_file("test_arp.txt")
        
        assert result.exists()
        assert result.is_file()
    
    def test_get_input_file_interactive_mode(self, tmp_path, monkeypatch):
        """Test get_input_file in interactive mode with mocked input."""
        monkeypatch.chdir(tmp_path)
        
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("test data")
        
        # Mock the input() function
        monkeypatch.setattr('builtins.input', lambda _: "test_arp.txt")
        
        result = get_input_file()
        
        assert result.exists()
        assert result.is_file()
        assert result.name == "test_arp.txt"
    
    def test_get_input_file_interactive_empty_input(self, monkeypatch):
        """Test get_input_file raises error on empty input."""
        # Mock the input() function to return empty string
        monkeypatch.setattr('builtins.input', lambda _: "")
        
        with pytest.raises(FileNotFoundError, match="No file path provided"):
            get_input_file()
    
    def test_get_input_file_nonexistent_file(self):
        """Test get_input_file raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            get_input_file("/nonexistent/file.txt")


class TestFindIncompleteMACAddresses:
    """Test cases for finding incomplete MAC addresses."""
    
    def test_find_single_incomplete_mac(self, tmp_path):
        """Test finding a single incomplete MAC address."""
        # Create mock ARP data with one incomplete entry
        # Format: IP Address Age MAC_Address Type Interface
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    aabb.ccdd.eeff  ARPA   GigabitEthernet0/1
192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2
192.168.1.3           10    1122.3344.5566  ARPA   GigabitEthernet0/3
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 1
        assert "192.168.1.2" in result[0]
        assert "INCOMPLETE" in result[0]
    
    def test_find_multiple_incomplete_macs(self, tmp_path):
        """Test finding multiple incomplete MAC addresses."""
        # Create mock ARP data with multiple incomplete entries
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    aabb.ccdd.eeff  ARPA   GigabitEthernet0/1
192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2
192.168.1.3           10    1122.3344.5566  ARPA   GigabitEthernet0/3
10.0.0.1              15    INCOMPLETE       ARPA   GigabitEthernet0/4
172.16.0.1            20    INCOMPLETE       ARPA   GigabitEthernet0/5
192.168.1.100         25    9988.7766.5544  ARPA   GigabitEthernet0/6
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 3
        assert all("INCOMPLETE" in line for line in result)
        assert "192.168.1.2" in result[0]
        assert "10.0.0.1" in result[1]
        assert "172.16.0.1" in result[2]
    
    def test_no_incomplete_macs(self, tmp_path):
        """Test when no incomplete MAC addresses are present."""
        # Create mock ARP data with no incomplete entries
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    aabb.ccdd.eeff  ARPA   GigabitEthernet0/1
192.168.1.2            5    1122.3344.5566  ARPA   GigabitEthernet0/2
192.168.1.3           10    9988.7766.5544  ARPA   GigabitEthernet0/3
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 0
        assert result == []
    
    def test_all_incomplete_macs(self, tmp_path):
        """Test when all MAC addresses are incomplete."""
        # Create mock ARP data where all entries are incomplete
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    INCOMPLETE       ARPA   GigabitEthernet0/1
192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2
192.168.1.3           10    INCOMPLETE       ARPA   GigabitEthernet0/3
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 3
        assert all("INCOMPLETE" in line for line in result)
    
    def test_empty_file(self, tmp_path):
        """Test handling of an empty file."""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text("")
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 0
        assert result == []
    
    def test_header_only(self, tmp_path):
        """Test file with only header line."""
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        assert len(result) == 0
    
    def test_mixed_case_incomplete(self, tmp_path):
        """Test that only exact 'INCOMPLETE' is matched (case-sensitive)."""
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    INCOMPLETE       ARPA   GigabitEthernet0/1
192.168.1.2            5    incomplete       ARPA   GigabitEthernet0/2
192.168.1.3           10    Incomplete       ARPA   GigabitEthernet0/3
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        # Should only find the exact match
        assert len(result) == 1
        assert "192.168.1.1" in result[0]
    
    def test_short_lines(self, tmp_path):
        """Test handling of lines with fewer than 3 words."""
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1
Short line
192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2
"""
        test_file = tmp_path / "test_arp.txt"
        test_file.write_text(arp_data)
        
        result = find_incomplete_mac_addresses(test_file)
        
        # Should find the incomplete entry and skip short lines
        assert len(result) == 1
        assert "192.168.1.2" in result[0]


class TestSaveResults:
    """Test cases for saving results to file."""
    
    def test_save_single_result(self, tmp_path):
        """Test saving a single incomplete MAC address."""
        incomplete_lines = [
            "192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2\n"
        ]
        output_file = tmp_path / "output.txt"
        
        save_results(incomplete_lines, output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "INCOMPLETE" in content
        assert "192.168.1.2" in content
    
    def test_save_multiple_results(self, tmp_path):
        """Test saving multiple incomplete MAC addresses."""
        incomplete_lines = [
            "192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2\n",
            "10.0.0.1              15    INCOMPLETE       ARPA   GigabitEthernet0/4\n",
            "172.16.0.1            20    INCOMPLETE       ARPA   GigabitEthernet0/5\n"
        ]
        output_file = tmp_path / "output.txt"
        
        save_results(incomplete_lines, output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        lines = content.splitlines()
        assert len(lines) == 3
        assert all("INCOMPLETE" in line for line in lines)
    
    def test_save_empty_results(self, tmp_path):
        """Test saving empty results list."""
        incomplete_lines: List[str] = []
        output_file = tmp_path / "output.txt"
        
        save_results(incomplete_lines, output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert content == ""
    
    def test_overwrite_existing_file(self, tmp_path):
        """Test that save_results overwrites existing file."""
        output_file = tmp_path / "output.txt"
        output_file.write_text("Old content\n")
        
        incomplete_lines = [
            "192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2\n"
        ]
        
        save_results(incomplete_lines, output_file)
        
        content = output_file.read_text()
        assert "Old content" not in content
        assert "INCOMPLETE" in content


class TestIntegration:
    """Integration tests combining find and save operations."""
    
    def test_full_workflow(self, tmp_path, capsys):
        """Test the complete workflow: find and save incomplete MACs."""
        # Create mock ARP data
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    aabb.ccdd.eeff  ARPA   GigabitEthernet0/1
192.168.1.2            5    INCOMPLETE       ARPA   GigabitEthernet0/2
192.168.1.3           10    1122.3344.5566  ARPA   GigabitEthernet0/3
10.0.0.1              15    INCOMPLETE       ARPA   GigabitEthernet0/4
"""
        input_file = tmp_path / "test_arp.txt"
        input_file.write_text(arp_data)
        
        output_file = tmp_path / "Incomplete-MAC-Addresses.txt"
        
        # Find incomplete MACs
        incomplete_lines = find_incomplete_mac_addresses(input_file)
        
        # Save results
        save_results(incomplete_lines, output_file)
        
        # Display results
        display_results(incomplete_lines, output_file)
        
        # Verify output file
        assert output_file.exists()
        content = output_file.read_text()
        assert len(content.splitlines()) == 2
        assert "192.168.1.2" in content
        assert "10.0.0.1" in content
        
        # Verify display output
        captured = capsys.readouterr()
        assert "2 incomplete MAC Addresses" in captured.out
        assert "Incomplete-MAC-Addresses.txt" in captured.out
    
    def test_workflow_no_results(self, tmp_path, capsys):
        """Test workflow when no incomplete MACs are found."""
        # Create mock ARP data with no incomplete entries
        arp_data = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
192.168.1.1            0    aabb.ccdd.eeff  ARPA   GigabitEthernet0/1
192.168.1.2            5    1122.3344.5566  ARPA   GigabitEthernet0/2
"""
        input_file = tmp_path / "test_arp.txt"
        input_file.write_text(arp_data)
        
        output_file = tmp_path / "Incomplete-MAC-Addresses.txt"
        
        # Find incomplete MACs
        incomplete_lines = find_incomplete_mac_addresses(input_file)
        
        # Save results
        save_results(incomplete_lines, output_file)
        
        # Display results
        display_results(incomplete_lines, output_file)
        
        # Verify output file exists but is empty
        assert output_file.exists()
        content = output_file.read_text()
        assert content == ""
        
        # Verify display output
        captured = capsys.readouterr()
        assert "No incomplete MAC addresses found" in captured.out


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])

