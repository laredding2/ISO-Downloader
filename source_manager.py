#!/usr/bin/env python3
"""
ISO Source Manager - Add and manage custom ISO sources
"""

import json
from pathlib import Path
from typing import Dict

class ISOSourceManager:
    """Manage custom ISO sources configuration"""
    
    def __init__(self, config_file: str = "custom_sources.json"):
        self.config_file = Path(config_file)
        self.sources = self.load_sources()
    
    def load_sources(self) -> Dict:
        """Load custom sources from config file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_sources(self) -> None:
        """Save sources to config file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.sources, f, indent=2)
        print(f"✅ Sources saved to {self.config_file}")
    
    def add_source(self, os_key: str, os_name: str, version: str, 
                   iso_url: str, checksum_url: str, 
                   checksum_type: str = 'sha256') -> None:
        """Add a new ISO source"""
        
        if os_key not in self.sources:
            self.sources[os_key] = {
                'name': os_name,
                'versions': {}
            }
        
        self.sources[os_key]['versions'][version] = {
            'url': iso_url,
            'checksum_url': checksum_url,
            'checksum_type': checksum_type
        }
        
        print(f"✅ Added {os_name} {version}")
        self.save_sources()
    
    def remove_source(self, os_key: str, version: str = None) -> None:
        """Remove an ISO source"""
        if os_key not in self.sources:
            print(f"❌ OS '{os_key}' not found")
            return
        
        if version:
            if version in self.sources[os_key]['versions']:
                del self.sources[os_key]['versions'][version]
                print(f"✅ Removed {os_key} {version}")
                
                # Remove OS entirely if no versions left
                if not self.sources[os_key]['versions']:
                    del self.sources[os_key]
            else:
                print(f"❌ Version '{version}' not found for {os_key}")
        else:
            del self.sources[os_key]
            print(f"✅ Removed all versions of {os_key}")
        
        self.save_sources()
    
    def list_sources(self) -> None:
        """List all custom sources"""
        if not self.sources:
            print("No custom sources configured.")
            return
        
        print("\n=== Custom ISO Sources ===\n")
        for os_key, os_data in self.sources.items():
            print(f"🖥️  {os_data['name']} ({os_key})")
            for version, details in os_data['versions'].items():
                print(f"   └─ {version}")
                print(f"      URL: {details['url']}")
                print(f"      Checksum: {details['checksum_url']}")
            print()
    
    def export_for_downloader(self) -> str:
        """Generate Python code to add to iso_downloader.py"""
        if not self.sources:
            return "# No custom sources to export"
        
        code = "# Custom sources - add this to OS_SOURCES in iso_downloader.py\n\n"
        code += "custom_sources = " + json.dumps(self.sources, indent=4)
        code += "\n\n# Merge with existing OS_SOURCES:\n"
        code += "# OS_SOURCES.update(custom_sources)\n"
        
        return code


def main():
    """Main entry point"""
    import sys
    
    manager = ISOSourceManager()
    
    if len(sys.argv) < 2:
        print("""
ISO Source Manager
==================

Usage:
  python source_manager.py list
  python source_manager.py add <os_key> <os_name> <version> <iso_url> <checksum_url> [checksum_type]
  python source_manager.py remove <os_key> [version]
  python source_manager.py export

Examples:
  python source_manager.py list
  python source_manager.py add kali "Kali Linux" 2024.1 \\
      https://example.com/kali.iso \\
      https://example.com/SHA256SUMS \\
      sha256
  python source_manager.py remove kali 2024.1
  python source_manager.py export
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        manager.list_sources()
    
    elif command == 'add':
        if len(sys.argv) < 7:
            print("❌ Error: Insufficient arguments for 'add' command")
            print("Usage: python source_manager.py add <os_key> <os_name> <version> <iso_url> <checksum_url> [checksum_type]")
            return
        
        os_key = sys.argv[2]
        os_name = sys.argv[3]
        version = sys.argv[4]
        iso_url = sys.argv[5]
        checksum_url = sys.argv[6]
        checksum_type = sys.argv[7] if len(sys.argv) > 7 else 'sha256'
        
        manager.add_source(os_key, os_name, version, iso_url, checksum_url, checksum_type)
    
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("❌ Error: OS key required")
            return
        
        os_key = sys.argv[2]
        version = sys.argv[3] if len(sys.argv) > 3 else None
        manager.remove_source(os_key, version)
    
    elif command == 'export':
        code = manager.export_for_downloader()
        print(code)
        
        # Also save to file
        with open('custom_sources_export.py', 'w') as f:
            f.write(code)
        print("\n✅ Exported to custom_sources_export.py")
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
