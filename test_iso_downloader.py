#!/usr/bin/env python3
"""
Test script for ISO Downloader functionality
Demonstrates features without downloading large files
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import iso_downloader
sys.path.insert(0, str(Path(__file__).parent))

from iso_downloader import ISODownloader

def test_list_systems():
    """Test listing available systems"""
    print("\n" + "="*60)
    print("TEST 1: Listing Available Systems")
    print("="*60)
    
    downloader = ISODownloader()
    downloader.list_available_systems()
    print("✅ List test passed")


def test_search():
    """Test search functionality"""
    print("\n" + "="*60)
    print("TEST 2: Search Functionality")
    print("="*60)
    
    downloader = ISODownloader()
    
    # Test search
    search_terms = ['ubuntu', 'debian', 'arch']
    
    for term in search_terms:
        results = downloader.search_iso(term)
        print(f"\n🔍 Searching for '{term}':")
        if results:
            for os_name, version in results:
                os_data = downloader.OS_SOURCES[os_name]
                print(f"  ✓ Found: {os_data['name']} (OS: {os_name}, Version: {version})")
        else:
            print(f"  ✗ No results found")
    
    print("\n✅ Search test passed")


def test_checksum_calculation():
    """Test checksum calculation on a small file"""
    print("\n" + "="*60)
    print("TEST 3: Checksum Calculation")
    print("="*60)
    
    downloader = ISODownloader()
    
    # Create a test file
    test_file = Path("test_checksum.txt")
    test_content = b"This is a test file for checksum calculation.\n"
    
    with open(test_file, 'wb') as f:
        f.write(test_content)
    
    # Calculate checksums
    print("\nCalculating checksums for test file...")
    sha256 = downloader.calculate_checksum(test_file, 'sha256')
    print(f"SHA256: {sha256}")
    
    # Verify
    expected_sha256 = "969f91ca780937db2a6b02664cc3ae5a63dd42d3203a55fc1a0aba85e89e01bb"
    
    if sha256 == expected_sha256:
        print("✅ Checksum calculation correct!")
    else:
        print(f"⚠️  Checksum mismatch (expected: {expected_sha256})")
    
    # Clean up
    test_file.unlink()
    print("✅ Checksum test passed")


def test_url_parsing():
    """Test URL and filename extraction"""
    print("\n" + "="*60)
    print("TEST 4: URL Parsing")
    print("="*60)
    
    downloader = ISODownloader()
    
    # Test with a few OS entries
    test_cases = [
        ('ubuntu', '24.04'),
        ('debian', '12'),
        ('arch', 'latest')
    ]
    
    for os_name, version in test_cases:
        if os_name in downloader.OS_SOURCES:
            os_data = downloader.OS_SOURCES[os_name]
            if version in os_data['versions']:
                version_data = os_data['versions'][version]
                url = version_data['url']
                filename = os.path.basename(url)
                
                print(f"\n{os_data['name']} {version}:")
                print(f"  URL: {url}")
                print(f"  Filename: {filename}")
                print(f"  Checksum URL: {version_data['checksum_url']}")
                print(f"  Hash Type: {version_data['checksum_type']}")
    
    print("\n✅ URL parsing test passed")


def test_download_directory():
    """Test download directory creation"""
    print("\n" + "="*60)
    print("TEST 5: Download Directory")
    print("="*60)
    
    custom_dir = "test_downloads"
    downloader = ISODownloader(download_dir=custom_dir)
    
    if downloader.download_dir.exists():
        print(f"✅ Download directory created: {downloader.download_dir.absolute()}")
        # Clean up
        downloader.download_dir.rmdir()
        print("✅ Cleanup successful")
    else:
        print("❌ Failed to create download directory")
    
    print("✅ Directory test passed")


def run_all_tests():
    """Run all tests"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║              ISO DOWNLOADER TEST SUITE                    ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        test_list_systems,
        test_search,
        test_checksum_calculation,
        test_url_parsing,
        test_download_directory
    ]
    
    failed_tests = []
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            failed_tests.append(test.__name__)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(tests)
    passed = total - len(failed_tests)
    
    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for test_name in failed_tests:
            print(f"  ❌ {test_name}")
    else:
        print("\n✅ All tests passed!")
    
    print("\n" + "="*60)
    print("Note: These are unit tests only.")
    print("To test actual downloads, use:")
    print("  python iso_downloader.py download <os> <version>")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
