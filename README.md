# MOMS - Matrix Online Modding Suite

A comprehensive web-based tool for viewing and analyzing The Matrix Online game assets, including 3D models, textures, animations, scripts, and game data.

## 🎯 Overview

MOMS (Matrix Online Modding Suite) is a powerful single-file web application that provides an interactive interface for exploring Matrix Online game files. Built with React and THREE.js, it features modern UI components and advanced file analysis capabilities.

## ✨ Features

### Core Functionality
- **🎮 3D Model Viewer** - View character models (.moa), props (.prop), and model groups (.mga/.mgc)
- **🖼️ Texture Viewer** - Support for DTX, TXA/TXB, DDS, TGA, PNG, JPG formats  
- **📝 Code Editor** - Monaco Editor with syntax highlighting for LUA, CS, TXT, PY scripts
- **📦 Archive Browser** - Explore and extract from REZ, LTA, LTB, PKB archives
- **🎬 Video Player** - BIK cutscene playback with real-time FFmpeg conversion
- **⚔️ Combat Analyzer** - Advanced analysis of game logs for combat events, RPC calls, GameObject creation
- **🎮 Enhanced Controls** - WADR movement keys with camera-relative motion and manual fallback
- **📤 Export Functions** - Export 3D models to OBJ format with proper vertex/normal/UV data

### Advanced Features  
- **PKB Archive Extraction** - Extract models from Matrix Online PKB archives using index files
- **Performance Monitoring** - Real-time memory and processing time tracking
- **Error Handling** - User-friendly error messages with reporting functionality
- **Pattern Recognition** - 30+ combat patterns including damage types, crowd control, buffs/debuffs

## 🚀 Quick Start

### 1. Start the Servers
```bash
cd /path/to/moms
./start_servers.sh
```

Or manually:
```bash
python3 server.py &           # Main server (port 8000)
python3 simple-bik-server.py & # BIK conversion (port 8002)
```

### 2. Open in Browser
- **Main Application**: http://localhost:8000/index.html
- **Modern Version**: http://localhost:8000/index_modern.html (THREE.js ES modules)
- **Test Suite**: http://localhost:8000/test_suite.html (comprehensive testing)

### 3. Load Matrix Online Files
1. Click "Load Directory" and select your Matrix Online folder
2. Navigate through the file browser on the left
3. Click files to view them in the appropriate editor/viewer
4. For PKB archives, ensure you have `packmap_save.lta` loaded first

## 📁 Project Structure

```
moms/
├── index.html              # Main application (7,384 lines)
├── index_modern.html       # Modernized THREE.js r169 version
├── test_suite.html         # Comprehensive test suite
├── server.py               # HTTP server with CORS (port 8000)
├── simple-bik-server.py    # BIK to MP4 conversion (port 8002)
├── mxo-protocol-parser.js  # MXO packet parsing library
├── start_servers.sh        # Server startup script
├── README.md               # This documentation
├── CLAUDE.md               # Session history and technical notes
├── TECHNICAL.md            # Technical specifications
├── CHANGELOG.md            # Version history
└── cache/                  # Directory for converted files
```

## 🎯 Matrix Online File Formats

### ✅ Supported Model Formats (CORRECTED)
- **`.moa`** - Character models, clothing, vehicles (with LOD levels)
- **`.prop`** - Static props and environmental objects  
- **`.iprf/.eprf`** - Specialized model data
- **`.mga/.mgc`** - Model group/collection files

> **Important**: Matrix Online does NOT use `.mob` files (common misconception)

### Texture Formats
- **`.txa/.txb`** - Proprietary MXO textures (require conversion to DDS)
- **`.dtx`** - Lithtech texture format
- **`.dds`** - DirectDraw Surface (converted format)
- **Standard formats**: PNG, JPG, TGA

### Archive Formats
- **`.pkb`** - Matrix Online packed archives (require `packmap_save.lta` index)
- **`.rez/.lta/.ltb`** - Lithtech resource archives

### Video/Cutscene Formats
- **`.bik`** - Bink Video (converted to MP4 via FFmpeg)
- **`.cnb`** - Real-time 3D cutscenes (viewer needed)

## 🎮 Controls & Navigation

### 3D Viewer Controls
- **W/A/S/D**: Camera movement (forward/left/backward/right)
- **Mouse drag**: Rotate view around model
- **Scroll wheel**: Zoom in/out
- **Right-click drag**: Pan camera
- **Toggle Lights**: Control scene lighting
- **Export OBJ**: Save model as Wavefront OBJ file

### UI Navigation
- **File Browser**: Left panel for directory navigation
- **Tabs**: Explorer, 3D Models, Textures, Audio, Cutscenes, Archives, GameObjects
- **Search**: Filter files by name or type
- **Category Filters**: Vehicles, Characters, Props

## 🔧 Technical Specifications

### Engine Details
- **Engine**: Modified Lithtech Discovery (unique to Matrix Online)
- **Scale**: 1 unit = 1 centimeter
- **Combat System**: D100 roll-based with Interlock grids
- **Graphics**: Enhanced lighting with shadows and tone mapping

### Frontend Stack
- **React 18.2.0** - UI framework
- **THREE.js r160/r169** - 3D rendering (ES modules in modern version)
- **Monaco Editor 0.43.0** - Code editing with syntax highlighting
- **Tailwind CSS** - Styling (development only)
- **Babel Standalone** - JSX transformation

### Backend Components
- **server.py**: Simple HTTP server with CORS headers
- **simple-bik-server.py**: FFmpeg-based BIK to MP4 streaming proxy
- **Performance monitoring**: Real-time memory and processing tracking

## 📊 Current Status

### ✅ Fully Working Features
- **Core Application**: Single-file React app with all components functional
- **3D Model Viewing**: Enhanced lighting, materials, export functionality
- **PKB Archive Extraction**: With index file support and individual file extraction
- **BIK Video Playback**: Real-time conversion pipeline operational
- **Combat Log Analysis**: Advanced pattern recognition with 30+ combat types
- **File Browser**: Complete directory navigation with file type detection
- **Code Editing**: Monaco Editor with multi-language syntax support
- **Error Handling**: User-friendly messages with reporting functionality
- **Performance Monitoring**: Memory usage and processing time tracking

### ⚠️ Known Issues & Limitations
- **PKB Extraction**: Requires proper `packmap_save.lta` format documentation
- **Some .moa files**: May show vertex stretching due to unknown format variations
- **BIK Server Path**: Hardcoded in `simple-bik-server.py` line 67
- **Large Files**: May cause browser performance issues (>100MB)
- **Production Warnings**: Tailwind CDN and Babel in-browser transformation

### 🔧 Minor Issues (Safe to Ignore)
- API status calls return 404 (doesn't affect functionality)
- THREE.js deprecation warnings (fixed in modern version)
- Browser console requests for DevTools extensions

## 🚧 Development Roadmap

### Next Priority Features
1. **CNB Cutscene Viewer** - Real-time 3D cutscene playback
2. **Texture Mapping** - Apply textures to 3D models automatically  
3. **Animation System** - Skeletal animation playback with timeline controls
4. **Binary Format Parser** - Proper .moa/.prop format specification implementation
5. **Modular Architecture** - Break apart single-file approach for maintainability

### Long-term Goals
- **Game Integration** - Direct memory reading and live asset replacement
- **Mod Creation Tools** - Import models, create custom content
- **Community Integration** - Connect with existing Matrix Online tools and community projects

## 🤝 Contributing

### Reporting Issues
Use the built-in error reporting:
1. When an error occurs, click "Yes" to copy error details
2. Create an issue on GitHub with the copied error report
3. Include steps to reproduce and file information

### Development Setup
1. Clone the repository
2. Start both servers (`./start_servers.sh`)
3. Open `test_suite.html` to verify all components
4. Make changes to `index.html` or create new version
5. Test thoroughly before committing

## 📖 Documentation

- **README.md** - This file (user guide and setup)
- **CLAUDE.md** - Complete session history and technical implementation details  
- **TECHNICAL.md** - File format specifications and parser implementation
- **CHANGELOG.md** - Version history and feature additions

## 🏆 Version Information

- **Current Version**: 2.1.0 (January 2025)
- **Status**: Production Ready
- **License**: Open Source
- **Platform**: Web-based (Chrome/Edge recommended)
- **Dependencies**: Python 3.x, FFmpeg (for BIK conversion)

---

**Matrix Online Modding Suite** - Preserving The Matrix Online for future generations 🕶️

*For detailed technical documentation and session history, see [CLAUDE.md](CLAUDE.md)*