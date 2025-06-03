#!/usr/bin/env python3
"""
Create more realistic MXO model files for testing
Based on the parser's expectations
"""

import struct
import os

def create_moa_file(filename, vertex_count=100, face_count=50):
    """Create a realistic .moa file with proper structure"""
    with open(filename, 'wb') as f:
        # Write MOA signature (optional header)
        f.write(b'MOA\x00')
        
        # Add some padding to get to offset 0x40 (64 bytes)
        # This is one of the offsets the parser checks
        f.write(b'\x00' * (64 - 4))
        
        # Write vertex count and face count at offset 0x40
        f.write(struct.pack('<I', vertex_count))  # Vertex count
        f.write(struct.pack('<I', face_count))     # Face count
        
        # Write vertices (x, y, z floats)
        # Create a simple humanoid-like shape
        import math
        for i in range(vertex_count):
            angle = (i / vertex_count) * math.pi * 2
            height = (i / vertex_count) * 200.0  # 200cm tall
            radius = 30.0 if height < 100 else 20.0  # Narrower at top
            
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = height - 100  # Center vertically
            
            # Write as floats (MXO uses centimeters)
            f.write(struct.pack('<f', x))
            f.write(struct.pack('<f', y))
            f.write(struct.pack('<f', z))
        
        # Write faces (triangle indices)
        for i in range(face_count):
            # Create triangles that connect vertices in a mesh
            a = i % vertex_count
            b = (i + 1) % vertex_count
            c = (i + vertex_count // 2) % vertex_count
            
            f.write(struct.pack('<I', a))
            f.write(struct.pack('<I', b))
            f.write(struct.pack('<I', c))
        
        # Add some padding at the end
        f.write(b'\x00' * 256)

def create_prop_file(filename, vertex_count=50, face_count=30):
    """Create a realistic .prop file with proper structure"""
    with open(filename, 'wb') as f:
        # Write PROP signature
        f.write(b'PROP')
        
        # Add padding to offset 0x80 (128 bytes) - another offset the parser checks
        f.write(b'\x00' * (128 - 4))
        
        # Write counts
        f.write(struct.pack('<I', vertex_count))
        f.write(struct.pack('<I', face_count))
        
        # Write vertices for a simple building/prop
        for i in range(vertex_count):
            # Create a box-like structure
            x = (i % 5) * 50.0 - 100  # -100 to 100 cm
            y = (i // 5) * 30.0        # 0 to 300 cm  
            z = ((i % 10) // 5) * 50.0 - 25  # -25 to 25 cm
            
            f.write(struct.pack('<f', x))
            f.write(struct.pack('<f', y))
            f.write(struct.pack('<f', z))
        
        # Write faces
        for i in range(face_count):
            # Simple triangulation
            a = i % vertex_count
            b = (i + 1) % vertex_count
            c = (i + 2) % vertex_count
            
            f.write(struct.pack('<I', a))
            f.write(struct.pack('<I', b))
            f.write(struct.pack('<I', c))
        
        f.write(b'\x00' * 256)

def create_test_pkb_with_models():
    """Create PKB files with realistic model data"""
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    
    # Create individual model files first
    models = [
        ('building1.prop', 80, 60),
        ('terrain.prop', 120, 100),
        ('vehicle.moa', 150, 120),
        ('character.moa', 200, 180),
        ('effects.prop', 60, 40),
        ('agent_smith.moa', 180, 160),
        ('neo.moa', 180, 160)
    ]
    
    # Create model files
    for filename, verts, faces in models:
        filepath = os.path.join(cache_dir, filename)
        if filename.endswith('.moa'):
            create_moa_file(filepath, verts, faces)
        else:
            create_prop_file(filepath, verts, faces)
        print(f"Created {filepath} with {verts} vertices and {faces} faces")
    
    # Now create PKB files containing these models
    # Create worlds_3g.pkb
    with open(os.path.join(cache_dir, 'worlds_3g.pkb'), 'wb') as pkb:
        # PKB header
        pkb.write(b'PKB\x00')
        pkb.write(b'\x00' * 124)  # Header padding
        
        # Write first 5 models
        for i in range(5):
            filename, _, _ = models[i]
            filepath = os.path.join(cache_dir, filename)
            with open(filepath, 'rb') as model:
                data = model.read()
                pkb.write(data)
    
    # Create char_npc.pkb
    with open(os.path.join(cache_dir, 'char_npc.pkb'), 'wb') as pkb:
        # PKB header
        pkb.write(b'PKB\x00')
        pkb.write(b'\x00' * 124)  # Header padding
        
        # Write last 2 models
        for i in range(5, 7):
            filename, _, _ = models[i]
            filepath = os.path.join(cache_dir, filename)
            with open(filepath, 'rb') as model:
                data = model.read()
                pkb.write(data)
    
    # Update the index file to match the new file sizes
    with open(os.path.join(cache_dir, 'packmap_save.lta'), 'wb') as f:
        # LTAI header
        f.write(b'LTAI')
        f.write(struct.pack('<I', 7))  # 7 entries
        
        # Calculate actual offsets and sizes
        current_offset = 128  # PKB header size
        
        for i, (filename, _, _) in enumerate(models):
            # Filename (32 bytes)
            name_bytes = filename.encode('utf-8')[:32]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            
            # PKB filename (32 bytes)
            if i < 5:
                pkb_name = b'worlds_3g.pkb'
            else:
                pkb_name = b'char_npc.pkb'
                if i == 5:
                    current_offset = 128  # Reset for new PKB
            
            f.write(pkb_name + b'\x00' * (32 - len(pkb_name)))
            
            # Get actual file size
            filepath = os.path.join(cache_dir, filename)
            file_size = os.path.getsize(filepath)
            
            # Offset and size
            f.write(struct.pack('<I', current_offset))
            f.write(struct.pack('<I', file_size))
            
            current_offset += file_size
        
        # Pad the rest
        f.write(b'\x00' * (1024 - f.tell()))
    
    print("\n✅ Created realistic MXO model files in cache/")
    print("- Models have proper vertex and face data")
    print("- PKB files contain the actual model data")
    print("- Index file has correct offsets and sizes")

if __name__ == '__main__':
    create_test_pkb_with_models()