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
- **Models**: ABC (Actor Binary Cache), MOB (Matrix Online Binary)
- **Textures**: DTX, DDS, TGA, PNG, JPG
- **Levels**: DAT, WORLD
- **Scripts**: LUA, CS, TXT, PY
- **Archives**: REZ, LTA, LTB, PKB
- **Videos**: BIK (converted to MP4 via FFmpeg)
- **Animations**: ANM, ANI
- **Assemblies**: DLL, EXE

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

### Known Issues
1. **API Status Calls**: The restored application makes periodic `/api/status` calls that return 404 errors
   - These can be ignored as they don't affect core functionality
   - The application was designed to work with or without API endpoints

2. **File Browsing**: Currently shows demo/placeholder data
   - Real file system integration would require the API server

3. **BIK Path**: The BIK server expects files in specific paths:
   - `/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN/`

## Next Tasks

### Immediate Tasks
1. **Stop API Status Polling**
   - Edit `index.html` to remove or comment out the status polling code
   - This will eliminate the 404 errors in server logs

2. **Configure File Paths**
   - Update file paths in `simple-bik-server.py` to match actual MxO installation
   - Or create symlinks to expected directories

3. **Enable Real File Browsing**
   - Option 1: Use the `api-server.py` instead of `server.py`
   - Option 2: Modify the application to use the File System Access API

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

---
*Last Updated: June 2, 2025*