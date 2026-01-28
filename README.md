# ISO Downloader & Verification Tool

A Python utility for finding, downloading, and verifying the integrity of operating system ISO images with automatic checksum verification.

## Features

- 🔍 **Search & Discovery**: Find ISOs for popular Linux distributions
- ⬇️ **Smart Downloads**: Download with progress tracking and resume capability
- ✅ **Integrity Verification**: Automatic SHA256/SHA1/MD5 checksum verification
- 🖥️ **Multiple OSes**: Support for Ubuntu, Debian, Fedora, Arch, Manjaro, and Linux Mint
- 📊 **Progress Tracking**: Visual progress bars during downloads
- 🔒 **Security**: Validates file integrity before use

## Supported Operating Systems

| OS | Versions |
|---|---|
| Ubuntu | 24.04, 22.04 |
| Debian | 12 |
| Fedora Workstation | 41 |
| Arch Linux | latest |
| Manjaro | GNOME 24.1.2 |
| Linux Mint | 22 |

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd iso-downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (optional, Linux/Mac):
```bash
chmod +x iso_downloader.py
```

## Usage

### Interactive Mode

Simply run the script without arguments for an interactive experience:

```bash
python iso_downloader.py
```

The script will:
1. Display all available operating systems and versions
2. Prompt you to select an OS
3. Prompt you to select a version
4. Download and verify the ISO

### Command Line Mode

#### List Available ISOs

```bash
python iso_downloader.py list
```

#### Download a Specific ISO

```bash
python iso_downloader.py download <os> <version>
```

**Examples:**
```bash
python iso_downloader.py download ubuntu 24.04
python iso_downloader.py download debian 12
python iso_downloader.py download fedora 41
python iso_downloader.py download arch latest
```

#### Search for ISOs

```bash
python iso_downloader.py search <term>
```

**Example:**
```bash
python iso_downloader.py search ubuntu
```

## How It Works

### 1. Download Process

The tool downloads ISOs from official mirrors and repositories:
- **Ubuntu**: releases.ubuntu.com
- **Debian**: cdimage.debian.org
- **Fedora**: download.fedoraproject.org
- **Arch**: mirror.rackspace.com
- **Manjaro**: download.manjaro.org
- **Linux Mint**: mirrors.kernel.org

### 2. Checksum Verification

After downloading, the tool:
1. Fetches the official checksum file from the source
2. Calculates the checksum of the downloaded ISO
3. Compares them to ensure file integrity
4. Reports verification status

### 3. Security Features

- Uses official sources only
- Verifies checksums from official repositories
- Detects corrupted downloads
- Warns about mismatches

## Output

Downloaded ISOs are saved to the `downloads/` directory in the same folder as the script.

Example output:
```
============================================================
  Downloading: Ubuntu 24.04
============================================================

Downloading from: https://releases.ubuntu.com/24.04/ubuntu-24.04.1-desktop-amd64.iso
Destination: downloads/ubuntu-24.04.1-desktop-amd64.iso

[████████████████████████████████████████] 100.0% (5621.2/5621.2 MB)
✅ Download complete: ubuntu-24.04.1-desktop-amd64.iso

============================================================
  Verifying Integrity
============================================================

Fetching checksum from: https://releases.ubuntu.com/24.04/SHA256SUMS
Calculating SHA256 checksum...

Checksum Verification:
Expected: a435f6f393dda581172490eda9f683c32e495158a780b5a1de422ee77d98e909
Actual:   a435f6f393dda581172490eda9f683c32e495158a780b5a1de422ee77d98e909
✅ Checksum verification PASSED

✅ SUCCESS: ubuntu-24.04.1-desktop-amd64.iso is ready to use!
📁 Location: /path/to/downloads/ubuntu-24.04.1-desktop-amd64.iso
```

## Troubleshooting

### Download Failed

- Check your internet connection
- Verify the source server is accessible
- Try again later (servers may be temporarily unavailable)

### Checksum Verification Failed

If checksum verification fails:
1. Delete the downloaded file
2. Run the download again
3. If it fails again, the official checksum may have been updated

### File Already Exists

If a file already exists, you'll be prompted:
- Press `y` to re-download
- Press `n` to verify the existing file

## Extending the Tool

To add new operating systems, edit the `OS_SOURCES` dictionary in `iso_downloader.py`:

```python
'newos': {
    'name': 'New OS Name',
    'versions': {
        'version1': {
            'url': 'https://example.com/newos.iso',
            'checksum_url': 'https://example.com/checksums.txt',
            'checksum_type': 'sha256'
        }
    }
}
```

## Security Considerations

- Always verify checksums before using ISOs
- Only add trusted sources to the OS_SOURCES dictionary
- Download from official mirrors when possible
- Keep the tool updated with latest ISO versions

## Common Use Cases

### Creating Bootable USB Drives

After downloading and verifying an ISO:

**Linux/Mac:**
```bash
sudo dd if=downloads/ubuntu-24.04.1-desktop-amd64.iso of=/dev/sdX bs=4M status=progress
```

**Windows:**
Use tools like:
- Rufus
- Etcher
- UNetbootin

### Virtual Machine Installation

Use the verified ISO directly with:
- VirtualBox
- VMware
- QEMU/KVM
- Hyper-V

## License

This tool is provided as-is for educational and personal use. Respect the licenses of the operating systems you download.

## Disclaimer

This tool downloads files from third-party sources. While it verifies integrity through checksums, users should:
- Verify they have the right to download the software
- Check license agreements of downloaded operating systems
- Use official mirrors when available

## Contributing

To contribute:
1. Add new OS sources with official download links
2. Improve checksum parsing for different formats
3. Add support for GPG signature verification
4. Enhance error handling and recovery

## Version History

- **v1.0.0**: Initial release with core functionality
  - Download manager with progress tracking
  - SHA256/SHA1/MD5 checksum verification
  - Support for 6 popular Linux distributions
  - Interactive and command-line modes

## Support

For issues, questions, or suggestions, please refer to the project documentation or create an issue in the repository.
