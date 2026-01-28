#!/usr/bin/env python3
"""
ISO Downloader - Find, verify, and download operating system ISO images
Supports multiple Linux distributions and verification methods
"""

import hashlib
import requests
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import json
from datetime import datetime

class ISODownloader:
    """Main class for downloading and verifying ISO images"""
    
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
    # Operating system sources configuration
    OS_SOURCES = {
        'ubuntu': {
            'name': 'Ubuntu',
            'versions': {
                '24.04': {
                    'url': 'https://releases.ubuntu.com/24.04/ubuntu-24.04.1-desktop-amd64.iso',
                    'checksum_url': 'https://releases.ubuntu.com/24.04/SHA256SUMS',
                    'checksum_type': 'sha256'
                },
                '22.04': {
                    'url': 'https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso',
                    'checksum_url': 'https://releases.ubuntu.com/22.04/SHA256SUMS',
                    'checksum_type': 'sha256'
                }
            }
        },
        'debian': {
            'name': 'Debian',
            'versions': {
                '13': {
                    'url': 'https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/debian-13.3.0-amd64-DVD-1.iso',
                    'checksum_url': 'https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/SHA256SUMS',
                    'checksum_type': 'sha256'
                }
            }
        },
        'fedora': {
            'name': 'Fedora Workstation',
            'versions': {
                '41': {
                    'url': 'https://download.fedoraproject.org/pub/fedora/linux/releases/43/Workstation/x86_64/iso/Fedora-Workstation-Live-43-1.6.x86_64.iso',
                    'checksum_url': 'https://ftp2.osuosl.org/pub/fedora/linux/releases/43/Workstation/x86_64/iso/Fedora-Workstation-43-1.6-x86_64-CHECKSUM',
                    'checksum_type': 'sha256'
                }
            }
        },
        'arch': {
            'name': 'Arch Linux',
            'versions': {
                'latest': {
                    'url': 'https://mirror.rackspace.com/archlinux/iso/latest/archlinux-x86_64.iso',
                    'checksum_url': 'https://mirror.rackspace.com/archlinux/iso/latest/sha256sums.txt',
                    'checksum_type': 'sha256'
                }
            }
        },
        'manjaro': {
            'name': 'Manjaro',
            'versions': {
                'gnome': {
                    'url': 'https://download.manjaro.org/gnome/24.1.2/manjaro-gnome-24.1.2-241204-linux612.iso',
                    'checksum_url': 'https://download.manjaro.org/gnome/24.1.2/manjaro-gnome-24.1.2-241204-linux612.iso.sha256',
                    'checksum_type': 'sha256'
                }
            }
        },
        'mint': {
            'name': 'Linux Mint',
            'versions': {
                '22': {
                    'url': 'https://mirrors.kernel.org/linuxmint/stable/22/linuxmint-22-cinnamon-64bit.iso',
                    'checksum_url': 'https://mirrors.kernel.org/linuxmint/stable/22/sha256sum.txt',
                    'checksum_type': 'sha256'
                }
            }
        }
    }
    
    def list_available_systems(self) -> None:
        """Display all available operating systems and versions"""
        print("\n=== Available Operating Systems ===\n")
        for os_key, os_data in self.OS_SOURCES.items():
            print(f"🖥️  {os_data['name']} ({os_key})")
            for version in os_data['versions'].keys():
                print(f"   └─ Version: {version}")
            print()
    
    def calculate_checksum(self, filepath: Path, hash_type: str = 'sha256') -> str:
        """Calculate checksum of a file"""
        hash_func = getattr(hashlib, hash_type)()
        
        print(f"Calculating {hash_type.upper()} checksum...")
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def fetch_checksum(self, checksum_url: str, filename: str) -> Optional[str]:
        """Fetch and parse checksum from remote file"""
        try:
            print(f"Fetching checksum from: {checksum_url}")
            response = self.session.get(checksum_url, timeout=30)
            response.raise_for_status()
            
            # Parse checksum file
            content = response.text
            for line in content.split('\n'):
                if filename in line or line.strip().endswith('.iso'):
                    # Extract checksum (first part of the line)
                    parts = line.strip().split()
                    if parts:
                        # Handle different formats: "checksum filename" or "checksum *filename"
                        checksum = parts[0]
                        # Validate it looks like a hash
                        if len(checksum) in [32, 40, 64, 128]:  # MD5, SHA1, SHA256, SHA512
                            return checksum.lower()
            
            # If specific filename not found, try to get the first checksum
            for line in content.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 1:
                    checksum = parts[0]
                    if len(checksum) in [32, 40, 64, 128]:
                        print(f"⚠️  Using first checksum found (specific file not matched)")
                        return checksum.lower()
                        
            print("⚠️  Could not parse checksum from file")
            return None
            
        except Exception as e:
            print(f"⚠️  Error fetching checksum: {e}")
            return None
    
    def verify_checksum(self, filepath: Path, expected_checksum: str, 
                       hash_type: str = 'sha256') -> bool:
        """Verify file checksum against expected value"""
        actual_checksum = self.calculate_checksum(filepath, hash_type)
        
        print(f"\nChecksum Verification:")
        print(f"Expected: {expected_checksum}")
        print(f"Actual:   {actual_checksum}")
        
        if actual_checksum == expected_checksum.lower():
            print("✅ Checksum verification PASSED")
            return True
        else:
            print("❌ Checksum verification FAILED")
            return False
    
    def download_file(self, url: str, destination: Path, 
                     show_progress: bool = True) -> bool:
        """Download a file with progress indication"""
        try:
            print(f"\nDownloading from: {url}")
            print(f"Destination: {destination}")
            
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size == 0:
                print("⚠️  Warning: Content length unknown")
            
            downloaded = 0
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if show_progress and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            
                            # Progress bar
                            bar_length = 40
                            filled = int(bar_length * downloaded / total_size)
                            bar = '█' * filled + '░' * (bar_length - filled)
                            
                            print(f"\r[{bar}] {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", 
                                  end='', flush=True)
            
            if show_progress:
                print()  # New line after progress bar
            
            print(f"✅ Download complete: {destination.name}")
            return True
            
        except Exception as e:
            print(f"\n❌ Download failed: {e}")
            if destination.exists():
                destination.unlink()  # Remove partial download
            return False
    
    def download_and_verify(self, os_name: str, version: str) -> bool:
        """Download an ISO and verify its integrity"""
        
        # Validate OS and version
        if os_name not in self.OS_SOURCES:
            print(f"❌ Unknown OS: {os_name}")
            self.list_available_systems()
            return False
        
        os_data = self.OS_SOURCES[os_name]
        
        if version not in os_data['versions']:
            print(f"❌ Unknown version '{version}' for {os_data['name']}")
            print(f"Available versions: {', '.join(os_data['versions'].keys())}")
            return False
        
        version_data = os_data['versions'][version]
        iso_url = version_data['url']
        checksum_url = version_data['checksum_url']
        checksum_type = version_data['checksum_type']
        
        # Extract filename from URL
        filename = os.path.basename(urlparse(iso_url).path)
        destination = self.download_dir / filename
        
        print(f"\n{'='*60}")
        print(f"  Downloading: {os_data['name']} {version}")
        print(f"{'='*60}")
        
        # Check if file already exists
        if destination.exists():
            print(f"\n⚠️  File already exists: {destination}")
            response = input("Do you want to re-download? (y/N): ").strip().lower()
            if response != 'y':
                print("Skipping download, will verify existing file...")
            else:
                destination.unlink()
                # Download the ISO
                if not self.download_file(iso_url, destination):
                    return False
        else:
            # Download the ISO
            if not self.download_file(iso_url, destination):
                return False
        
        # Fetch and verify checksum
        print(f"\n{'='*60}")
        print(f"  Verifying Integrity")
        print(f"{'='*60}")
        
        expected_checksum = self.fetch_checksum(checksum_url, filename)
        
        if expected_checksum:
            if self.verify_checksum(destination, expected_checksum, checksum_type):
                print(f"\n✅ SUCCESS: {filename} is ready to use!")
                print(f"📁 Location: {destination.absolute()}")
                return True
            else:
                print(f"\n❌ FAILED: Checksum mismatch - file may be corrupted")
                print(f"Consider deleting and re-downloading: {destination}")
                return False
        else:
            print(f"\n⚠️  Could not verify checksum automatically")
            print(f"File downloaded to: {destination.absolute()}")
            print(f"Please verify manually using: {checksum_url}")
            return True  # Still consider it a success since file downloaded
    
    def search_iso(self, search_term: str) -> List[Tuple[str, str]]:
        """Search for ISOs matching a term"""
        results = []
        search_lower = search_term.lower()
        
        for os_key, os_data in self.OS_SOURCES.items():
            if search_lower in os_key.lower() or search_lower in os_data['name'].lower():
                for version in os_data['versions'].keys():
                    results.append((os_key, version))
        
        return results


def main():
    """Main entry point for the ISO downloader"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║          ISO DOWNLOADER & VERIFICATION TOOL               ║
║      Download and verify operating system images          ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    downloader = ISODownloader()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            downloader.list_available_systems()
            
        elif command == 'download' and len(sys.argv) >= 4:
            os_name = sys.argv[2]
            version = sys.argv[3]
            success = downloader.download_and_verify(os_name, version)
            sys.exit(0 if success else 1)
            
        elif command == 'search' and len(sys.argv) >= 3:
            search_term = sys.argv[2]
            results = downloader.search_iso(search_term)
            
            if results:
                print(f"\n🔍 Found {len(results)} result(s) for '{search_term}':\n")
                for os_name, version in results:
                    os_data = downloader.OS_SOURCES[os_name]
                    print(f"  • {os_data['name']} (OS: {os_name}, Version: {version})")
                print(f"\nTo download, use: python iso_downloader.py download <os> <version>")
            else:
                print(f"\n❌ No results found for '{search_term}'")
                
        else:
            print("❌ Invalid command\n")
            print_usage()
    else:
        # Interactive mode
        downloader.list_available_systems()
        
        print("Enter the OS key (e.g., 'ubuntu', 'debian', 'fedora'):")
        os_name = input("OS: ").strip().lower()
        
        if os_name in downloader.OS_SOURCES:
            versions = list(downloader.OS_SOURCES[os_name]['versions'].keys())
            print(f"\nAvailable versions: {', '.join(versions)}")
            version = input("Version: ").strip()
            
            downloader.download_and_verify(os_name, version)
        else:
            print(f"❌ Unknown OS: {os_name}")


def print_usage():
    """Print usage information"""
    print("""
Usage:
  python iso_downloader.py                    # Interactive mode
  python iso_downloader.py list               # List all available ISOs
  python iso_downloader.py download <os> <version>  # Download specific ISO
  python iso_downloader.py search <term>      # Search for ISOs

Examples:
  python iso_downloader.py list
  python iso_downloader.py download ubuntu 24.04
  python iso_downloader.py download debian 12
  python iso_downloader.py search ubuntu
    """)


if __name__ == "__main__":
    main()
