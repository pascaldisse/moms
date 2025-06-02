# MOMS - Matrix Online Modding Suite

A comprehensive web-based tool for viewing and analyzing The Matrix Online game assets, including 3D models, textures, animations, scripts, and game data.

## Overview

MOMS (Matrix Online Modding Suite) is a single-file web application that provides an interactive interface for exploring MXO game files. It features a modern React-based UI with support for viewing 3D models, editing scripts, analyzing combat logs, and playing cutscenes.

## Features

- **3D Model Viewer** - View character models (.moa), props (.prop), and model groups (.mga/.mgc)
- **Texture Viewer** - Support for DTX, DDS, TGA, PNG, JPG formats
- **Code Editor** - Monaco Editor for LUA, CS, TXT, PY scripts
- **Archive Browser** - Explore REZ, LTA, LTB, PKB archives
- **Video Player** - BIK cutscene playback (with FFmpeg conversion)
- **Combat Analyzer** - Analyze game logs for combat events, RPC calls, and GameObject creation
- **Enhanced Controls** - WADR movement keys with camera-relative motion
- **Export Functions** - Export 3D models to OBJ format

## Quick Start

### 1. Start the Servers
```bash
cd /Users/pascaldisse/Downloads/mxo/moms
./start_servers.sh
```

This starts:
- HTTP server on port 8000 (main application)
- BIK proxy server on port 8002 (video conversion)

### 2. Open in Browser
Navigate to:
- **Original Version**: http://localhost:8000/index.html
- **Modern Version**: http://localhost:8000/index_modern.html (with ES modules)

## File Structure

```
moms/
├── index.html              # Main application (copy of index_legacy.html)
├── index_modern.html       # Modernized version with THREE.js r169
├── server.py               # Simple HTTP server with CORS (port 8000)
├── simple-bik-server.py    # BIK to MP4 conversion proxy (port 8002)
├── api-server.py           # Full API server (optional, not required)
├── mxo-protocol-parser.js  # MXO packet parsing library
├── start_servers.sh        # Server startup script
├── modernize_three.py      # THREE.js modernization script
├── cache/                  # Directory for converted files
├── backup/                 # Backup of modular approach attempts
└── moms-master/            # Original source files
    ├── index_legacy.html   # Complete single-file MOMS application
    ├── README.md           # Original documentation
    └── CLAUDE.md           # Detailed technical documentation
```

## Technical Details

### Supported File Types
- **Models**: .moa (characters/clothing/vehicles), .prop (static objects), .iprf/.eprf (specialized data)
- **Model Groups**: .mga/.mgc (model collections)
- **Textures**: DTX, DDS, TGA, PNG, JPG
- **Levels**: DAT, WORLD
- **Scripts**: LUA, CS, TXT, PY
- **Archives**: REZ, LTA, LTB, PKB
- **Videos**: BIK (Bink Video, converted to MP4)
- **Animations**: ANM, ANI
- **Logs**: .log, .txt, .out (for combat analysis)

### Matrix Online Specifics
- **Engine**: Modified Lithtech Discovery (unique to MXO)
- **Scale**: 1 unit = 1 centimeter
- **Model Format**: MXO does NOT use .mob files (common misconception)
- **Combat System**: D100 roll-based with Interlock grids
- **Cutscenes**: CNB files (real-time) and BIK videos (pre-rendered)

### 3D Viewer Controls
- **W/A/S/D**: Camera movement (forward/left/backward/right)
- **Mouse drag**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click drag**: Pan
- **Toggle Lights**: Turn scene lighting on/off
- **Export OBJ**: Export current model to Wavefront OBJ format

## Current Status

### ✅ Working Features
- Single-file application fully functional
- 3D model viewing with enhanced lighting
- BIK video playback via FFmpeg proxy
- Combat log analysis with pattern recognition
- GameObject tab with transform controls
- OBJ export functionality

### ⚠️ Known Issues
- Some .moa files may show vertex stretching (format variations)
- BIK server path hardcoded (edit line 67 in simple-bik-server.py)
- THREE.OrbitControls may fail to load (manual controls as fallback)
- API status calls return 404 (can be ignored)

### 🚀 Recent Improvements (June 2025)
- Migrated to THREE.js r169 with ES modules
- Fixed model format misconceptions (.moa not .mob)
- Enhanced combat analyzer with 30+ pattern recognitions
- Added export functionality for 3D models
- Improved lighting system with multiple light sources

## BIK Video Configuration

To enable BIK video playback, edit `simple-bik-server.py` line 67:
```python
bik_path = "/path/to/your/Matrix Online/resource/Bink/" + filename
```

## Development Notes

### Frontend Stack
- **React 18.2.0** - UI framework (loaded from CDN)
- **THREE.js 0.169.0** - 3D rendering (ES modules in modern version)
- **Monaco Editor 0.43.0** - Code editing
- **Babel Standalone** - JSX transformation
- **Tailwind CSS** - Styling (via CDN)

### Architecture
- Single HTML file containing all code (~5000 lines)
- React components defined inline
- No build process required
- CORS enabled for development

## Future Enhancements

### Priority Tasks
1. Implement proper .moa/.prop binary parsing
2. Add texture support for 3D models
3. Create CNB viewer for real-time cutscenes
4. Implement animation playback system

### Long-term Goals
1. Split into modular architecture
2. Add WebSocket support for real-time updates
3. Implement mod injection system
4. Create comprehensive file format documentation

## Credits

- Original MOMS by the MXO emulation community
- Combat analyzer patterns from Discord analysis of 32,000+ messages
- Model format corrections from community research
- Enhanced by Pascal Disse (2025)