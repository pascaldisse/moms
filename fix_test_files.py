#!/usr/bin/env python3
"""
Fix the test PKB and index files to have matching offsets
"""

import struct
import os

def create_fixed_pkb_files():
    """Create PKB files with correct structure"""
    print("📦 Creating Fixed PKB Files...")
    
    cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
    
    # Create worlds_3g.pkb with correct structure
    worlds_pkb = os.path.join(cache_dir, 'worlds_3g.pkb')
    
    with open(worlds_pkb, 'wb') as f:
        # PKB header
        f.write(b'PKB\x00')  # Magic
        f.write(struct.pack('<I', 5))  # Number of files
        
        # Calculate where file data will start
        header_size = 8
        entry_size = 40
        num_files = 5
        data_start = header_size + (num_files * entry_size)
        
        # File entries
        files = [
            ('building1.prop', 1000),
            ('terrain.prop', 1500),
            ('vehicle.moa', 2300),
            ('character.moa', 3500),
            ('effects.prop', 4100)
        ]
        
        # Write file table
        current_offset = data_start
        file_table = []
        
        for filename, size in files:
            # Store info for later
            file_table.append((filename, current_offset, size))
            
            # Write filename (32 bytes)
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            
            # Write offset and size
            f.write(struct.pack('<I', current_offset))
            f.write(struct.pack('<I', size))
            
            current_offset += size
        
        # Write file data
        for filename, offset, size in file_table:
            # Create some recognizable data for each file type
            if filename.endswith('.prop'):
                # PROP file header
                data = b'PROP' + b'\x00' * (size - 4)
            elif filename.endswith('.moa'):
                # MOA file header
                data = b'MOA\x00' + b'\x00' * (size - 4)
            else:
                data = b'\x00' * size
            
            f.write(data[:size])
    
    file_size = os.path.getsize(worlds_pkb)
    print(f"✅ Created worlds_3g.pkb: {file_size} bytes")
    
    # Create char_npc.pkb
    char_pkb = os.path.join(cache_dir, 'char_npc.pkb')
    
    with open(char_pkb, 'wb') as f:
        # PKB header
        f.write(b'PKB\x00')
        f.write(struct.pack('<I', 3))  # Number of files
        
        # Calculate data start
        data_start = 8 + (3 * 40)
        
        # Character files
        files = [
            ('agent_smith.moa', 800),
            ('neo.moa', 900),
            ('morpheus.moa', 850)
        ]
        
        # Write file table
        current_offset = data_start
        file_table = []
        
        for filename, size in files:
            file_table.append((filename, current_offset, size))
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            f.write(struct.pack('<I', current_offset))
            f.write(struct.pack('<I', size))
            current_offset += size
        
        # Write file data
        for filename, offset, size in file_table:
            # MOA file header
            data = b'MOA\x00' + b'\x00' * (size - 4)
            f.write(data[:size])
    
    char_size = os.path.getsize(char_pkb)
    print(f"✅ Created char_npc.pkb: {char_size} bytes")
    
    # Create matching index file
    index_file = os.path.join(cache_dir, 'packmap_save.lta')
    
    with open(index_file, 'wb') as f:
        # LTAI header
        f.write(b'LTAI')  # Magic
        
        # Count total entries
        worlds_entries = [
            ('building1.prop', 'worlds_3g.pkb', 208, 1000),
            ('terrain.prop', 'worlds_3g.pkb', 1208, 1500),
            ('vehicle.moa', 'worlds_3g.pkb', 2708, 2300),
            ('character.moa', 'worlds_3g.pkb', 5008, 3500),
            ('effects.prop', 'worlds_3g.pkb', 8508, 4100)
        ]
        
        char_entries = [
            ('agent_smith.moa', 'char_npc.pkb', 128, 800),
            ('neo.moa', 'char_npc.pkb', 928, 900),
            ('morpheus.moa', 'char_npc.pkb', 1828, 850)
        ]
        
        all_entries = worlds_entries + char_entries
        f.write(struct.pack('<I', len(all_entries)))  # Number of entries
        
        # Write entries
        for filename, pkb_name, offset, size in all_entries:
            # Filename (32 bytes)
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            
            # PKB name (32 bytes)
            pkb_bytes = pkb_name.encode('ascii')[:31]
            f.write(pkb_bytes + b'\x00' * (32 - len(pkb_bytes)))
            
            # Offset and size
            f.write(struct.pack('<I', offset))
            f.write(struct.pack('<I', size))
    
    index_size = os.path.getsize(index_file)
    print(f"✅ Created packmap_save.lta: {index_size} bytes")
    
    # Verify the files
    print("\n🔍 Verifying file structure...")
    
    # Check worlds_3g.pkb
    with open(worlds_pkb, 'rb') as f:
        data = f.read()
        if data[:4] == b'PKB\x00':
            num_files = struct.unpack('<I', data[4:8])[0]
            print(f"✅ worlds_3g.pkb: {num_files} files")
            
            # Check first file data
            first_file_offset = struct.unpack('<I', data[40:44])[0]
            if data[first_file_offset:first_file_offset+4] == b'PROP':
                print("✅ First file has valid PROP header")
    
    return True

def test_extraction():
    """Test if extraction would work with these files"""
    print("\n🧪 Testing extraction logic...")
    
    # Simulate the extraction
    with open('/Users/pascaldisse/Downloads/mxo/moms/cache/packmap_save.lta', 'rb') as f:
        index_data = f.read()
    
    with open('/Users/pascaldisse/Downloads/mxo/moms/cache/worlds_3g.pkb', 'rb') as f:
        pkb_data = f.read()
    
    # Parse index
    if index_data[:4] == b'LTAI':
        num_entries = struct.unpack('<I', index_data[4:8])[0]
        print(f"Index has {num_entries} entries")
        
        # Extract first file as test
        offset = 8
        filename = index_data[offset:offset+32].split(b'\x00')[0].decode('ascii')
        pkb_name = index_data[offset+32:offset+64].split(b'\x00')[0].decode('ascii')
        file_offset = struct.unpack('<I', index_data[offset+64:offset+68])[0]
        file_size = struct.unpack('<I', index_data[offset+68:offset+72])[0]
        
        print(f"\nTesting extraction of '{filename}' from '{pkb_name}'")
        print(f"Offset: {file_offset}, Size: {file_size}")
        
        # Extract data
        if file_offset + file_size <= len(pkb_data):
            extracted_data = pkb_data[file_offset:file_offset+file_size]
            print(f"✅ Successfully extracted {len(extracted_data)} bytes")
            print(f"First 4 bytes: {extracted_data[:4]}")
            return True
        else:
            print(f"❌ Invalid offset/size: {file_offset} + {file_size} > {len(pkb_data)}")
            return False
    
    return False

if __name__ == "__main__":
    print("🔧 Fixing PKB Test Files")
    print("=" * 40)
    
    if create_fixed_pkb_files():
        if test_extraction():
            print("\n✅ Test files created successfully!")
            print("PKB extraction should now work.")
        else:
            print("\n❌ Extraction test failed")
    else:
        print("\n❌ Failed to create test files")