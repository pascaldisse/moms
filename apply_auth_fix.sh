#!/bin/bash

echo "Matrix Online Auth Server Fix Script"
echo "===================================="
echo ""
echo "This script will fix the authentication deadlock issue by modifying"
echo "the server to send an initial packet when a client connects."
echo ""
echo "Choose which fix version to apply:"
echo "1) Simple empty packet (0x00 0x00)"
echo "2) Handshake packet with opcode 0x01"
echo "3) Server ready packet with opcode 0x05"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        SOURCE_FILE="/Users/pascaldisse/Downloads/mxo/AuthSocket_Fixed.cs"
        echo "Applying fix version 1..."
        ;;
    2)
        SOURCE_FILE="/Users/pascaldisse/Downloads/mxo/AuthSocket_FixedV2.cs"
        echo "Applying fix version 2..."
        ;;
    3)
        SOURCE_FILE="/Users/pascaldisse/Downloads/mxo/AuthSocket_FixedV3.cs"
        echo "Applying fix version 3..."
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

TARGET_FILE="/Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/auth/AuthSocket.cs"
BACKUP_FILE="/Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/auth/AuthSocket.cs.backup"

echo ""
echo "Source file: $SOURCE_FILE"
echo "Target file: $TARGET_FILE"
echo ""

# Check if we need sudo
if [ -w "$TARGET_FILE" ]; then
    echo "Creating backup..."
    cp "$TARGET_FILE" "$BACKUP_FILE"
    
    echo "Applying fix..."
    cp "$SOURCE_FILE" "$TARGET_FILE"
    
    echo "Fix applied successfully!"
else
    echo "The target file requires sudo access to modify."
    echo "Please run: sudo cp \"$SOURCE_FILE\" \"$TARGET_FILE\""
    echo ""
    echo "To create a backup first, run:"
    echo "sudo cp \"$TARGET_FILE\" \"$BACKUP_FILE\""
fi

echo ""
echo "After applying the fix, you'll need to rebuild the server:"
echo "cd /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020"
echo "msbuild /p:Configuration=Debug /p:Platform=x86"
echo ""
echo "Then restart the server to test the authentication."