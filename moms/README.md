# Matrix Online Modding Suite (MOMS)

A comprehensive web-based tool for viewing, analyzing, and modifying Matrix Online game assets.

![Matrix Online](https://img.shields.io/badge/Matrix%20Online-Modding%20Suite-00ff00?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-3.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

## 🎮 Overview

MOMS (Matrix Online Modding Suite) is a powerful browser-based application for exploring and modifying Matrix Online game files. It provides tools for viewing 3D models, analyzing combat logs, browsing textures, and much more.

## ✨ Features

### 🗂️ File Support

#### 3D Models
- `.moa` - Character models, clothing, vehicles (with LOD levels)
- `.prop` - Static props and objects
- `.iprf/.eprf` - Specialized model data
- `.mga/.mgc` - Model group/collection files
- `.abc` - Actor Binary Cache (Lithtech format)

#### Other Formats
- **Textures**: DTX, DDS, TGA, PNG, JPG
- **Levels**: DAT, WORLD
- **Scripts**: LUA, CS, TXT, PY
- **Archives**: REZ, LTA, LTB, PKB
- **Videos**: BIK (with FFmpeg conversion)
- **Logs**: LOG, TXT, OUT, DEBUG
- **Config**: XML, JSON, CSV, CFG, INI

### 🛠️ Core Features

#### 3D Model Viewer
- Real-time 3D rendering with THREE.js
- WADR camera controls (W=forward, A=left, D=backward, R=right)
- Mouse rotation and zoom
- Export to OBJ format
- Toggle lighting controls
- Wireframe/solid rendering modes

#### Combat & GameObject Analyzer
- Analyze game logs and combat data
- Support for 30+ combat patterns
- XML/JSON structured data parsing
- Real-time statistics dashboard
- Advanced filtering and search

#### Code Editor
- Monaco Editor integration
- Syntax highlighting for multiple languages
- Full editing capabilities

#### Video Player
- BIK video playback (via FFmpeg proxy)
- Standard video format support
- Thumbnail generation

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- FFmpeg (for BIK video conversion)
- Modern web browser (Chrome/Edge recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mxo-moms.git
cd mxo-moms
```

2. Install FFmpeg (if not already installed):
```bash
# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html

# Linux
sudo apt-get install ffmpeg
```

### Running MOMS

1. Start the servers:
```bash
./start_servers.sh
```

Or manually:
```bash
# Main server
python3 server.py

# BIK video proxy (in another terminal)
python3 simple-bik-server.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

### Configuration

#### BIK Video Path
Edit `simple-bik-server.py` line 67 to set your BIK files location:
```python
bik_base_path = "/path/to/your/matrix/online/files/"
```

## 🎮 Usage

### Loading Files
1. Click "Load Directory" or drag & drop files
2. Navigate through the file tree on the left
3. Click files to preview them

### 3D Model Viewer Controls
- **WADR Keys**: Move camera (Forward/Left/Backward/Right)
- **Mouse Drag**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click Drag**: Pan

### Combat Analyzer
1. Go to the "GameObjects" tab
2. Load a directory containing log files
3. Select files to analyze
4. Use filters to find specific combat events

### Exporting Models
1. Load a 3D model file (.moa, .prop, etc.)
2. Click "Export OBJ" button in the 3D viewer
3. File will download automatically

## 🏗️ Architecture

MOMS is built as a single-page application using:
- **React 18.2.0** - UI framework
- **THREE.js 0.153.0** - 3D rendering
- **Monaco Editor 0.43.0** - Code editing
- **Tailwind CSS** - Styling
- **Babel Standalone** - JSX transformation

## 🐛 Known Issues

1. **THREE.js OrbitControls** may fail to load (fallback to manual controls)
2. **Large files** may cause performance issues due to in-browser Babel
3. **Some model files** show placeholders due to unknown format variations
4. **BIK video path** must be manually configured

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📚 Documentation

- [Technical Documentation](CLAUDE.md) - Detailed technical information
- [Original MOMS Docs](moms-master/CLAUDE.md) - Historical documentation

## 🔧 Development

### File Structure
```
moms/
├── index.html              # Main application
├── server.py               # HTTP server
├── simple-bik-server.py    # BIK video proxy
├── start_servers.sh        # Startup script
├── CLAUDE.md              # Technical documentation
├── README.md              # This file
└── moms-master/           # Original source files
```

### Adding New File Types
1. Add extension to `FILE_TYPES` object in `index.html`
2. Create parser function in `LithtechParsers`
3. Add UI component for preview/editing

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Matrix Online community for format research
- rajkosto for reverse engineering work
- codejunky for modding tools inspiration
- All contributors to the MXO preservation effort

## 📞 Support

- Report issues on [GitHub Issues](https://github.com/yourusername/mxo-moms/issues)
- Join the [MXO Discord](https://discord.gg/matrixonline) community

---

**Remember**: The Matrix has you... and now you have the tools to mod it! 🐰🔴💊