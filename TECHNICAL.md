# MOMS Technical Documentation

## File Format Specifications

### Matrix Online Model Formats

#### MOA Files (Character Models)
- **Purpose**: Character models, clothing, vehicles
- **Features**: Multiple LOD levels, bone weights, skeletal data
- **Structure**: Index files that reference other assets
- **Critical Data**:
  - UV coordinates
  - Normal vectors
  - Bone weights (essential for animation)
  - Per-vertex color data

#### PROP Files (Static Objects)
- **Purpose**: Static props and environmental objects
- **Features**: Simpler than MOA, no bone weights needed
- **Structure**: Self-contained geometry data
- **Use Cases**: Buildings, furniture, decorations

#### IPRF/EPRF Files
- **Purpose**: Specialized model data
- **Features**: Extended property data
- **Structure**: Proprietary format, partially understood

#### MGA/MGC Files
- **Purpose**: Model group/collection files
- **Features**: References to multiple models
- **Structure**: Index of model references

### Parser Implementation

#### Binary Structure (Based on Lithtech Discovery)
```javascript
// Header structure (assumed)
struct ModelHeader {
    uint32 signature;      // 4 bytes - file type identifier
    uint32 version;        // 4 bytes - format version
    uint32 numVertices;    // 4 bytes - vertex count
    uint32 numFaces;       // 4 bytes - face count
    // Additional header data...
}

// Vertex structure
struct Vertex {
    float x, y, z;         // 12 bytes - position
    float nx, ny, nz;      // 12 bytes - normal
    float u, v;            // 8 bytes - texture coordinates
    // Bone weights follow in animated models
}
```

#### Parsing Strategy
1. **Header Detection**: Check for known signatures (MOA, PROP, etc.)
2. **Structured Parsing**: Try to parse according to expected format
3. **Pattern-Based Fallback**: Scan for vertex patterns if structured parsing fails
4. **Validation**: Ensure reasonable vertex coordinates and counts

### Combat Analysis Patterns

#### Pattern Recognition
The combat analyzer recognizes the following patterns:

##### Damage Types
- `damage` - General damage
- `critical` - Critical hits
- `dot` - Damage over time
- `melee` - Melee attacks
- `ranged` - Ranged attacks
- `viral` - Viral damage
- `hack` - Hacking damage

##### Defense Mechanisms
- `block` - Blocking attacks
- `evade` - Evading attacks
- `dodge` - Dodging
- `resistance` - Damage resistance

##### Crowd Control
- `stun` - Stun effects
- `root` - Root/immobilize
- `mezz` - Mesmerize
- `slow` - Slow effects
- `confuse` - Confusion
- `blind` - Blind effects
- `powerless` - Power disable
- `disarm` - Disarm effects
- `pacify` - Pacify effects

##### Combat Systems
- `interlock` - Interlock combat
- `pvp` - Player vs Player
- `duel` - Duel system
- `combo` - Combo attacks
- `finisher` - Finisher moves

#### Data Extraction
```javascript
// Extract combat values from log lines
const extractCombatValues = (line) => {
    const values = {};
    
    // Damage numbers: "dealt 150 damage"
    const damageMatch = line.match(/(\d+)\s*damage/i);
    if (damageMatch) values.damage = parseInt(damageMatch[1]);
    
    // Percentages: "75% accuracy"
    const percentMatch = line.match(/(\d+)%/);
    if (percentMatch) values.percentage = parseInt(percentMatch[1]);
    
    // Dice rolls: "d100: 85"
    const rollMatch = line.match(/\bd(\d+)\s*[:=]\s*(\d+)/i);
    if (rollMatch) {
        values.diceType = `d${rollMatch[1]}`;
        values.rollResult = parseInt(rollMatch[2]);
    }
    
    return values;
};
```

### Network Protocols

#### Protocol 03 (GameObject)
- **Purpose**: GameObject creation and distribution
- **Function**: `CreateGoObjAndDistrObjView`
- **Identifiers**: Object IDs in hex format (0xCA7...)

#### Protocol 04 (RPC)
- **Purpose**: Remote Procedure Calls
- **Common IDs**: 8113, 8114, 8115
- **Usage**: Combat actions, state changes

### Performance Considerations

#### Memory Management
- **Vertex Limits**: Cap at 100,000 vertices for browser performance
- **Face Limits**: Cap at 200,000 faces
- **Texture Size**: Limit to 2048x2048 for WebGL compatibility

#### Optimization Strategies
1. **LOD System**: Use appropriate detail level based on distance
2. **Geometry Instancing**: Reuse geometry for repeated objects
3. **Texture Atlasing**: Combine multiple textures
4. **Culling**: Don't render off-screen objects

### WebGL Implementation

#### Renderer Settings
```javascript
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    preserveDrawingBuffer: true
});
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
```

#### Lighting Configuration
- **Ambient Light**: 0x404040, intensity 0.4
- **Directional Light**: 0xffffff, intensity 0.8, with shadows
- **Point Light**: 0x00ff00, intensity 0.3 (Matrix green accent)
- **Fill Light**: 0x004400, intensity 0.3

### Export Functionality

#### OBJ Export Format
```
# Exported from Matrix Online Modding Suite (MOMS)
# File generated on [timestamp]

# Vertices
v x y z
v x y z
...

# Texture coordinates
vt u v
vt u v
...

# Normals
vn nx ny nz
vn nx ny nz
...

# Faces (with texture and normal indices)
f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
...
```

### Error Handling

#### Common Issues and Solutions

1. **OrbitControls Loading Failure**
   - **Issue**: THREE.OrbitControls not available
   - **Solution**: Fallback to manual mouse controls
   - **Implementation**: Spherical coordinate system

2. **Binary Parsing Failures**
   - **Issue**: Unknown file format structure
   - **Solution**: Pattern-based vertex scanning
   - **Validation**: Coordinate range checks

3. **Memory Limitations**
   - **Issue**: Large files crash browser
   - **Solution**: Streaming parsing, vertex limits
   - **Warning**: Display file size warnings

### Future Implementation Notes

#### Bone Weight Support
```javascript
// Future implementation for bone weights
struct BoneWeight {
    uint8 boneIndex[4];    // Up to 4 bones per vertex
    float weight[4];       // Weight for each bone
}
```

#### Animation System
- **Skeletal Hierarchy**: 4x4 transformation matrices
- **Keyframe Data**: Position, rotation, scale over time
- **Retargeting**: Map animations between different skeletons

#### Texture Support
- **TXA Format**: Custom header + DDS data
- **Conversion**: Replace TXA header with DDS header
- **Formats**: DXT compression, RGB16, V8U8

---

*For more information, see the main [CLAUDE.md](CLAUDE.md) documentation.*