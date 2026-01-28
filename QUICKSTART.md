# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: List Available ISOs

```bash
python iso_downloader.py list
```

### Step 3: Download an ISO

```bash
python iso_downloader.py download ubuntu 24.04
```

## Common Commands

### See What's Available
```bash
python iso_downloader.py list
```

### Search for an OS
```bash
python iso_downloader.py search ubuntu
python iso_downloader.py search debian
```

### Download Specific ISOs

**Ubuntu 24.04 LTS**
```bash
python iso_downloader.py download ubuntu 24.04
```

**Debian 12**
```bash
python iso_downloader.py download debian 12
```

**Fedora 43**
```bash
python iso_downloader.py download fedora 43
```

**Arch Linux (latest)**
```bash
python iso_downloader.py download arch latest
```

**Linux Mint 22**
```bash
python iso_downloader.py download mint 22
```

**Manjaro GNOME**
```bash
python iso_downloader.py download manjaro gnome
```

## What Happens During Download?

1. **Download**: The ISO is downloaded with a progress bar
2. **Verify**: SHA256 checksum is automatically fetched and verified
3. **Confirm**: You get a success message with the file location

## Where Are My Files?

All downloaded ISOs are saved to the `downloads/` folder in the same directory as the script.

## Run Tests

To verify everything is working:
```bash
python test_iso_downloader.py
```

## Interactive Mode

Just run the script without arguments:
```bash
python iso_downloader.py
```

Then follow the prompts!

## Need Help?

- Check the full README.md for detailed documentation
- Use `python iso_downloader.py` without arguments for interactive mode
- Checksums are verified automatically - if verification fails, the file may be corrupted

## Example Output

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

## Tips

1. **Large Files**: ISOs can be 1-5 GB - make sure you have enough space
2. **Resume**: If a download fails, just run the command again
3. **Existing Files**: If a file exists, you'll be asked if you want to re-download
4. **Verification**: Always wait for checksum verification to complete
5. **Custom Sources**: Use `source_manager.py` to add your own ISO sources

## Troubleshooting

**Download fails?**
- Check internet connection
- Try a different mirror (you can add custom sources)

**Checksum fails?**
- Delete the file and download again
- Check if the official checksum was updated

**Command not found?**
- Make sure Python 3 is installed
- Use `python3` instead of `python` on some systems
