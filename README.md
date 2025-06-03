# MOMS - Matrix Online Modding Suite

A comprehensive web-based tool for viewing, analyzing, and modifying The Matrix Online game assets, including 3D models, textures, animations, scripts, and game data.

## 🎯 Overview

MOMS (Matrix Online Modding Suite) is a powerful single-file web application that provides an interactive interface for exploring Matrix Online game files. Built with React and THREE.js, it features modern UI components and advanced file analysis capabilities.

## ✨ Features

### Core Functionality
- **🎮 3D Model Viewer** - View character models (.moa), props (.prop), and model groups (.mga/.mgc)
  - Real-time transform controls (position, rotation, scale)
  - Export to OBJ format
  - GameObject properties editing
  - Material and lighting controls
- **🖼️ Texture Viewer** - Support for DTX, TXA/TXB, DDS, TGA, PNG, JPG formats  
- **📝 Code Editor** - Monaco Editor with syntax highlighting for LUA, CS, TXT, PY scripts
- **📦 Archive Browser** - Explore and extract from REZ, LTA, LTB, PKB archives
  - Auto-loads PKB files when switching to 3D Models tab
  - Visual extraction UI with file listing
  - Click-to-view extracted files
- **🎬 Video Player** - BIK cutscene playback
  - Automatic server detection with user-friendly instructions
  - Real-time FFmpeg conversion when server available
  - Fallback instructions for manual setup
- **⚔️ Combat Analyzer** - Advanced analysis of game logs
  - GameObject creation events
  - Combat system analysis (damage, defense, crowd control)
  - RPC calls and network packets
  - Animation references
  - Pattern recognition for 30+ combat types
- **🎮 Enhanced Controls** - WADR movement keys with camera-relative motion
- **📤 Export Functions** - Export 3D models to OBJ format with proper vertex/normal/UV data

### Recent Improvements (v2.2.0)
- **✅ PKB Extraction Fixed** - Proper file loading and extraction with UI
- **✅ GameObject Properties** - Live connection between UI and 3D model transforms
- **✅ BIK Video Support** - Enhanced player with automatic server detection
- **✅ Enhanced Combat Analyzer** - Better categorization and pattern matching
- **✅ Auto-initialization** - 3D Models tab automatically loads required files

## 🚀 Quick Start

### 1. Start the Servers
```bash
cd /path/to/moms
./start_servers.sh
```

Or manually:
```bash
python3 server.py &           # Main server (port 8000)
python3 simple-bik-server.py & # BIK conversion (port 8002) - Optional
```

### 2. Open in Browser
- **Main Application**: http://localhost:8000

### 3. Load Matrix Online Files
1. Click "Load Directory" and select your Matrix Online folder
2. Browse files using the tabs:
   - **Game Files** - File explorer with code editor
   - **3D Models** - Automatic PKB loading and extraction
   - **Textures** - Image viewer
   - **Cutscenes** - Video player with BIK support
   - **Archives** - PKB/REZ file browser
   - **GameObjects** - Log file analyzer

## 📦 PKB Archive Extraction

### Automatic Workflow
1. Go to **3D Models** tab
2. PKB files and index are auto-loaded from cache/
3. Click **"Extract & View"** to extract and see files
4. Click **"View"** on any file to open in 3D viewer

### Manual Workflow
1. Go to **Archives** tab
2. Click on PKB files to load them
3. Return to **3D Models** tab
4. Use extraction buttons

## 🎬 BIK Video Playback

### With Server (Recommended)
1. Start `simple-bik-server.py`
2. BIK files play automatically

### Without Server
1. Instructions appear when opening BIK files
2. Follow setup guide for FFmpeg installation

## 🎮 GameObject Properties

When viewing 3D models:
1. Click **GameObject** tab
2. Modify transform properties:
   - Position (X, Y, Z)
   - Rotation (X, Y, Z) in degrees
   - Scale (X, Y, Z)
3. Changes apply in real-time
4. Click **Reset** to restore original values

## 🔧 Technical Details

### Supported File Types

#### Models
- `.moa` - Character models, clothing, vehicles
- `.prop` - Static props and objects
- `.iprf/.eprf` - Specialized model data
- `.mga/.mgc` - Model group/collection files

#### Textures
- `.dtx` - Matrix Online texture format
- `.dds` - DirectDraw Surface
- `.tga/.txa/.txb` - Targa and variants
- `.png/.jpg` - Standard images

#### Archives
- `.pkb` - Packed game assets (requires index)
- `.rez` - Resource archives
- `.lta/.ltb` - Lithtech archives

#### Scripts
- `.lua` - Lua scripts
- `.cs` - C# scripts
- `.txt/.ini/.cfg` - Configuration files

#### Media
- `.bik` - Bink Video (cutscenes)
- `.wav/.ogg/.mp3` - Audio files

## 🛠️ Requirements

- Python 3.7+
- Modern web browser (Chrome/Edge recommended)
- FFmpeg (optional, for BIK video conversion)
- Matrix Online game files

## 📊 Performance

- Single-file application (~8000 lines)
- Performance monitoring built-in
- Handles large PKB archives efficiently
- Real-time 3D rendering with THREE.js r169

## 🐛 Known Issues

- Some model formats show placeholder geometry
- DTX textures require conversion
- Animation playback not implemented
- Level/world files show grid placeholder

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and preservation purposes only. All Matrix Online assets remain property of their respective owners.

## 🔗 Resources

- [GitHub Repository](https://github.com/yourusername/moms)
- [Matrix Online Wiki](https://wiki.mxoemu.com)
- [THREE.js Documentation](https://threejs.org/docs/)

---

**Version**: 2.2.0  
**Last Updated**: January 2025