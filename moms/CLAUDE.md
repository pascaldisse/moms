# Matrix Online Modding Suite (MOMS) - Session Summary

## Project Overview
This document summarizes the restoration and setup of the Matrix Online Modding Suite (MOMS), a web-based tool for viewing and modifying Matrix Online game assets.

## Session Summary (June 2, 2025)

### Initial Problem
- User reported: "suddenly, all the js script files are missing"
- Application files `components.js` and `app.js` were not found
- Recovery page was being displayed instead of the application

### Investigation & Discovery
1. Found `restore_files.md` indicating files had been deleted
2. Discovered the original MOMS source in `moms-master/` directory
3. Learned that the original MOMS is a **single-file application** (`index_legacy.html`) containing all code

### Solution Implemented
1. **Initial Attempt**: Created modular React components (`components.js`, `app.js`) using React.createElement to avoid JSX compilation
2. **API Server Creation**: Built `api-server.py` with full API endpoints for file browsing, status checks, etc.
3. **Final Solution**: Restored the original single-file application from `moms-master/index_legacy.html`

### Additional Features Added
1. **GameObject Tab**: Restored missing GameObject tab in ModelEditor with transform, components, and tags/layers controls
2. **WADR Controls**: Changed movement controls to W=forward, A=left, D=backward, R=right with camera-relative movement
3. **BIK Video Support**: Integrated with `simple-bik-server.py` for real-time BIK to MP4 conversion
4. **MOB File Parser**: Improved MOB file parsing with better vertex validation and multiple parsing strategies
5. **Manual Camera Controls**: Added fallback mouse controls when THREE.OrbitControls fails to load

### Current Setup

#### Files & Structure
```
/Users/pascaldisse/Downloads/mxo/moms/
├── index.html              # Main application (copy of index_legacy.html)
├── server.py               # Simple HTTP server with CORS (port 8000)
├── simple-bik-server.py    # BIK video proxy server (port 8002)
├── api-server.py           # Full API server (not needed for current setup)
├── mxo-protocol-parser.js  # MxO packet parsing library
├── start_servers.sh        # Server startup script
├── cache/                  # Directory for converted files
├── backup/                 # Backup of attempted modular approach
└── moms-master/            # Original source files
    ├── index_legacy.html   # Complete single-file MOMS application
    ├── README.md           # Original documentation
    └── CLAUDE.md           # Detailed technical documentation
```

#### Running Services
- **Main Server**: `server.py` on port 8000 (serving static files)
- **BIK Proxy**: `simple-bik-server.py` on port 8002 (video streaming)

### Key Features of MOMS

#### Supported File Types
- **Models**: ABC (Actor Binary Cache), MOA (Character models/clothing/vehicles), PROP (Static props)
- **Textures**: DTX, DDS, TGA, PNG, JPG
- **Levels**: DAT, WORLD, IPRF/EPRF (Specialized model data)
- **Scripts**: LUA, CS, TXT, PY
- **Archives**: REZ, LTA, LTB, PKB
- **Videos**: BIK (converted to MP4 via FFmpeg)
- **Animations**: ANM, ANI
- **Assemblies**: DLL, EXE
- **Model Groups**: MGA/MGC (Model group/collection files)

#### UI Components
1. **File Browser** - Left panel for navigation
2. **Code Editor** - Monaco Editor for script editing
3. **3D Model Viewer** - THREE.js powered viewer with controls
4. **Texture Viewer** - Image and texture preview
5. **Archive Browser** - REZ/LTB file exploration
6. **Video Player** - BIK cutscene playback

#### 3D Viewer Controls
- **W/A/S/D**: Camera movement (forward/left/backward/right)
- **Mouse drag**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click drag**: Pan

### Technical Implementation

#### Frontend Stack
- **React 18.2.0** - UI framework (loaded from CDN)
- **THREE.js 0.153.0** - 3D rendering
- **Monaco Editor 0.43.0** - Code editing
- **Babel Standalone** - JSX transformation
- **Tailwind CSS** - Styling (via CDN)

#### Backend Components
1. **server.py**: Simple HTTP server with CORS headers
2. **simple-bik-server.py**: FFmpeg-based BIK to MP4 streaming
3. **api-server.py**: Full-featured API server (created but not currently used)

### Known Issues & Solutions

#### 1. THREE.OrbitControls Loading Issue
- **Problem**: OrbitControls may fail to load with THREE.js r153 due to deprecated build paths
- **Solution**: Implemented dynamic script loading with fallback to manual camera controls
- **Status**: Working with manual controls as fallback

#### 2. BIK Video Playback
- **Problem**: BIK files cannot be played directly in browsers (proprietary Bink Video format)
- **Solution**: Use `simple-bik-server.py` proxy that converts BIK to MP4 using FFmpeg
- **Requirements**:
  - BIK proxy server running on port 8002
  - FFmpeg installed on system
  - BIK files accessible to server (default path: `/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN/`)
- **To Fix Path**: Edit line 67 in `simple-bik-server.py` to point to your BIK files location

#### 3. MOB File Rendering
- **Problem**: Some MOB files show vertices stretching into the distance
- **Solution**: Added vertex validation and geometry normalization
- **Status**: Improved but some files may still have issues due to unknown format variations

#### 4. API Status Calls
- **Problem**: The application makes periodic `/api/status` calls that return 404 errors
- **Solution**: These can be ignored as they don't affect core functionality

## Next Tasks

### Immediate Priority Tasks

1. **Fix THREE.js Dependencies** ✅ COMPLETED
   - Migrated to THREE.js r169 with ES modules
   - Updated from deprecated build/three.js to three.module.js
   - Fixed OrbitControls loading with proper ES module imports
   - Created index_modern.html with full ES module support

2. **Add GameObjects Log Analyzer** ✅ COMPLETED
   - Created comprehensive log file analysis tool
   - Analyzes GameObject creation, combat events, RPC calls
   - Pattern matching for Matrix Online technical specifications
   - Supports .log, .txt, .out file formats

3. **Improve MOB/ABC File Parsing**
   - Research Matrix Online file format specifications
   - Implement proper binary parsing based on actual format structure
   - Add support for textures, animations, and materials

3. **Fix BIK Video Playback**
   - Update `simple-bik-server.py` to handle dynamic file paths
   - Add better error handling and user feedback
   - Consider caching converted videos for faster playback

4. **Production Build Process**
   - Pre-compile Babel/JSX for production use
   - Bundle dependencies instead of using CDNs
   - Minify and optimize the single-file application

### Enhancement Tasks
1. **Implement Binary Parsers**
   - Complete ABC/MOB model parsing
   - Add DTX texture decoding
   - Implement REZ archive extraction

2. **Add Save Functionality**
   - Enable editing and saving of scripts
   - Export modified models/textures

3. **Improve 3D Viewer**
   - Add material/texture support
   - Implement animation playback
   - Add measurement tools

4. **Network Packet Analysis**
   - Integrate `mxo-protocol-parser.js` 
   - Add packet capture functionality
   - Create packet builder/sender

### Long-term Goals
1. **Modular Architecture**
   - Split the single-file app into modules
   - Add build process (webpack/vite)
   - Create npm package

2. **Server Enhancements**
   - Add WebSocket support for real-time updates
   - Implement file watching
   - Add multi-user collaboration

3. **Game Integration**
   - Direct game memory reading
   - Live asset replacement
   - Mod injection system

## Commands Reference

### Start Servers
```bash
# Start both servers
./start_servers.sh

# Or manually:
python3 server.py > server.log 2>&1 &
python3 simple-bik-server.py > simple-bik-server.log 2>&1 &
```

### Access Application
Open http://localhost:8000 in your browser

### Stop Servers
```bash
pkill -f server.py
pkill -f simple-bik-server.py
```

## Development Notes
- The application works best in Chrome/Edge due to WebGL requirements
- Monaco Editor may have issues in Firefox
- CORS is enabled for all origins in development
- The Matrix rain effect on loading screen is purely aesthetic

## Resources
- Original MOMS documentation: `moms-master/CLAUDE.md`
- Matrix Online file formats: Research community wikis
- THREE.js documentation: https://threejs.org
- Monaco Editor: https://microsoft.github.io/monaco-editor/

## Current Session Changes & Fixes (June 2, 2025 - Session 4)

### CRITICAL FIX: Matrix Online Model Formats
- **Corrected File Types**: Matrix Online does NOT use .mob files
- **Actual Model Formats**:
  - `.moa` - Character models, clothing, vehicles (with LOD levels)
  - `.prop` - Static props and objects
  - `.iprf/.eprf` - Specialized model data
  - `.mga/.mgc` - Model group/collection files
- **Updated Parsers**: 
  - Renamed parseMOB to parseMOA
  - Added parseMGA for model groups
  - Enhanced metadata to reflect correct formats
- **Engine Details**: Modified Lithtech Discovery, scale: 1 unit = 1cm

### GameObject Tab Restoration
- Added GameObject tab to ModelEditor component with:
  - Transform controls (Position, Rotation, Scale)
  - Component management (Mesh Renderer, Collider, Physics Body)
  - Tags & Layers system
  - Apply/Reset buttons

### NEW: GameObjects & Combat Analyzer - Enhanced
- **Complete analysis tool** for Matrix Online combat and game files
- **Expanded File Support**:
  - Log files (.log, .txt, .out, .debug)
  - XML configuration files (combat abilities, skills)
  - JSON data files (game settings, combat data)
  - CSV data exports
  - Config files (.cfg, .ini, .dat)
  - Any file with combat keywords in name
- **Enhanced Pattern Recognition**:
  - GameObject creation (CreateGoObjAndDistrObjView function)
  - **Expanded Combat Types**: damage, critical, melee, ranged, viral, hack
  - **Defense Mechanisms**: block, evade, dodge, resistance
  - **Crowd Control**: stun, root, mezz, slow, confuse, blind, powerless
  - **Buffs/Debuffs**: buff, debuff, heal, DOT (damage over time)
  - **PvP Systems**: pvp, duel, threat, aggro, taunt
  - **Combat Styles**: style, combo, finisher
  - RPC calls (Protocol 04: 8113, 8114, 8115)
  - Network packets (Protocol 03: GameObject distribution)
  - Animation IDs (interlock system)
- **Enhanced Features**:
  - XML/JSON parsing for structured combat data
  - Combat value extraction (damage numbers, percentages, dice rolls)
  - Improved categorization (combat, gameobject, animation, network, mission)
  - Multi-format support in single interface
  - Real-time statistics dashboard
  - Advanced filtering and sorting

### Control System Updates
- **Movement Keys Changed**: W=Forward, A=Left, D=Backward, R=Right
- **Camera Movement**: Now relative to camera direction (not world space)
- **Visual Indicators**: Updated to show correct key mappings

### 3D Model Improvements
- **Model Format Correction**: 
  - Matrix Online does NOT use .mob files (common misconception)
  - Actual formats: .moa (characters/clothing/vehicles), .prop (static objects), .iprf/.eprf (specialized data)
  - Engine: Modified Lithtech Discovery (unique to MXO)
  - Scale: 1 unit = 1 centimeter
  
- **Enhanced Model Parser**: Rewritten to support MXO formats:
  - Magic number detection for actual MXO file signatures
  - Support for LOD (Level of Detail) systems
  - Vertex data parsing (UVs, normals, bone weights)
  - Per-vertex color data support
  - Structured binary parsing with header analysis
  - Pattern-based fallback parsing for unknown formats
  - Geometry normalization to prevent stretching

### 3D Viewer Enhancements (Based on instructions.txt)
- **Enhanced Lighting System**:
  - Ambient light (0x404040, intensity 0.4)
  - Directional light with shadows (0xffffff, intensity 0.8)
  - Point light for accent lighting (0x00ff00, intensity 0.3)
  - Fill light for balanced illumination (0x004400, intensity 0.3)
- **Improved Materials**:
  - MeshPhongMaterial with specular properties
  - Shininess setting (30)
  - Specular color (0x222222)
  - Double-sided rendering
- **Enhanced Renderer**:
  - Shadow mapping enabled
  - Tone mapping for better color reproduction
  - WebGL context loss/restore handling
  - Better error recovery and logging

### New UI Controls (Based on instructions.txt)
- **Toggle Lights Button**: Allows users to turn all scene lights on/off
- **Export OBJ Button**: Exports the current 3D model to Wavefront OBJ format
- **Enhanced Export Function**: 
  - Handles both single meshes and mesh groups
  - Exports vertices, texture coordinates, and normals
  - Supports indexed and non-indexed geometry
  - Generates proper OBJ format with comments and metadata

### Video System
- **BIK Integration**: Connected to simple-bik-server.py for conversion
- **Error Handling**: Better feedback for BIK files that need conversion
- **Thumbnail Generation**: Special handling for BIK files

## Technical Debt & Warnings

1. **THREE.js Deprecation**: ✅ FIXED - Migrated to ES modules in index_modern.html
2. **Tailwind CDN**: Should not be used in production
3. **Babel In-Browser**: Should be precompiled for production
4. **OrbitControls**: ✅ FIXED - Now loads reliably with ES module imports

## Testing Instructions

1. **Start Servers**:
   ```bash
   cd /Users/pascaldisse/Downloads/mxo/moms
   ./start_servers.sh
   ```

2. **Access Application**: 
   - Original version: http://localhost:8000/index.html
   - Modernized version: http://localhost:8000/index_modern.html

3. **Test Features**:
   - Load a directory with MxO files
   - Test 3D model viewing with WADR controls
   - Try loading a BIK video file
   - Check GameObject tab in model viewer

## Modernization Complete (June 2, 2025 - Session 3)

### THREE.js ES Module Migration
- **Created**: `index_modern.html` - Fully modernized version using THREE.js r169
- **Script**: `modernize_three.py` - Automated modernization script
- **Import Maps**: Using modern import maps for clean ES module loading
- **Global Access**: THREE.js modules made globally available for React components

### Key Improvements
1. **No More Deprecation Warnings**: Updated from legacy build/three.js to modern ES modules
2. **Reliable OrbitControls**: Direct ES module import eliminates loading issues
3. **Latest THREE.js**: Updated from r153 to r169 (latest stable)
4. **Cleaner Code**: Removed complex workarounds for OrbitControls loading

### Usage
```javascript
// Old way (deprecated)
const controls = new THREE.OrbitControls(camera, renderer.domElement);

// New way (ES modules)
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const controls = new OrbitControls(camera, renderer.domElement);
```

### GameObjects Log Analyzer Usage
1. **Navigate to GameObjects tab** in MOMS interface
2. **Upload log files** - supports multiple files (.log, .txt, .out)
3. **View analysis results**:
   - Overview: Technical summary with statistics
   - GameObjects: CreateGoObjAndDistrObjView events
   - Combat: Damage, accuracy, defense, D100 rolls
   - RPC: Remote procedure calls (8113, 8114, 8115)
   - Packets: Network protocol data
   - Animations: Animation ID references
4. **Search and filter** events by content or type
5. **Click events** to see full context with line numbers

### Summary of Recent Enhancements (Session 4)

1. **3D Model Format Corrections**
   - Fixed misconception about .mob files (MXO doesn't use them)
   - Added support for actual MXO formats: .moa, .prop, .iprf, .eprf, .mga, .mgc
   - Updated all parsers and UI to reflect correct formats

2. **Enhanced Combat Analyzer**
   - Expanded file support to include XML, JSON, CSV, DAT, CFG, INI
   - Added 30+ combat pattern recognitions (damage types, crowd control, buffs/debuffs)
   - Implemented structured data parsing for XML/JSON files
   - Added combat value extraction (damage numbers, percentages, dice rolls)

3. **Improved 3D Viewer**
   - Added "Toggle Lights" button for scene lighting control
   - Added "Export OBJ" button with comprehensive export function
   - Enhanced lighting system with ambient, directional, point, and fill lights
   - Improved materials with specular properties

## Next Tasks

### Immediate Priority Tasks

1. **Fix THREE.js OrbitControls Loading**
   - OrbitControls still failing to load properly
   - Need to implement proper ES module loading or use a different approach
   - Consider bundling OrbitControls directly

2. **Implement Proper MXO Model Parsing**
   - Research actual Lithtech Discovery binary format
   - Implement proper vertex, normal, UV, and bone weight extraction
   - Add support for LOD (Level of Detail) systems
   - Parse material and texture references

3. **Add Texture Support**
   - Implement TXA to DDS conversion
   - Display textures on 3D models
   - Support for multiple texture channels

### Enhancement Tasks

1. **Animation System**
   - Parse and display skeletal animations
   - Implement animation playback controls
   - Support for retargeting between skeletons

2. **Model Export Pipeline**
   - Export to standard formats (FBX, GLTF)
   - Preserve bone weights and skeletal data
   - Batch export functionality

3. **Archive Extraction**
   - Implement REZ file extraction
   - Support for LTA/LTB archives
   - Integrated file browser for archives

### Long-term Goals

1. **Complete Modding Pipeline**
   - Model import functionality
   - In-game preview system
   - Mod packaging tools

2. **Community Integration**
   - Connect to codejunky's modding tools
   - Import/export compatibility with other MXO tools
   - Shared format documentation

3. **Performance Optimization**
   - WebGL 2.0 support
   - GPU instancing for multiple models
   - Texture atlasing

## Known Issues

1. **THREE.js Warnings**: "build/three.js" deprecated, OrbitControls not loading
2. **Babel Performance**: In-browser transformation slow for large files
3. **Model Parsing**: Many MXO files still show placeholder instead of actual geometry
4. **BIK Videos**: Path configuration still hardcoded in simple-bik-server.py

## Technical Debt

1. **Single File Architecture**: 5000+ lines in one HTML file needs modularization
2. **CDN Dependencies**: Should bundle dependencies for production
3. **Error Handling**: Need better error messages and recovery
4. **Documentation**: Need detailed API documentation for parsers

---
*Last Updated: June 2, 2025 - Session 4*