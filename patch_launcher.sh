#!/bin/bash
# Matrix Online launcher.exe patcher script

echo "Matrix Online Launcher Patcher"
echo "==============================="

# Navigate to game directory
cd "/Users/pascaldisse/Downloads/mxo/Matrix Online HDS"

echo "Creating backup of launcher.exe..."
sudo cp launcher.exe launcher.exe.original

echo "Applying patches to launcher.exe..."

# Patch 1: Replace testauth.mxoemu.info with localhost (offset 0xB6198)
echo "  - Patching auth server address..."
sudo sh -c 'printf "localhost\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" | dd of=launcher.exe bs=1 seek=$((0xB6198)) conv=notrunc 2>/dev/null'

# Patch 2: Replace atch.mxoemu.info with localhost/ (offset 0xAB380)  
echo "  - Patching patch server address..."
sudo sh -c 'printf "localhost/\x00\x00\x00\x00\x00\x00" | dd of=launcher.exe bs=1 seek=$((0xAB380)) conv=notrunc 2>/dev/null'

# Patch 3: Null out .test.mxoemu.info DNS suffix (offset 0xB1990)
echo "  - Removing DNS suffix..."
sudo sh -c 'printf "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" | dd of=launcher.exe bs=1 seek=$((0xB1990)) conv=notrunc 2>/dev/null'

echo ""
echo "Verifying patches were applied..."
echo "Looking for 'localhost' in patched file:"
strings launcher.exe | grep localhost

echo ""
echo "Checking if old mxoemu domains are still present:"
remaining=$(strings launcher.exe | grep -c "mxoemu.info")
if [ $remaining -gt 0 ]; then
    echo "WARNING: $remaining mxoemu.info references still found!"
    strings launcher.exe | grep "mxoemu.info"
else
    echo "SUCCESS: All mxoemu.info references have been patched!"
fi

echo ""
echo "Patch complete!"
echo "Original file backed up as: launcher.exe.original"
echo "You can now run: ./launcher.exe"