# Matrix Online Modding Suite (MOMS)

A web-based tool for viewing and modifying Matrix Online game assets.

## Features

- 3D model viewer with WASD movement and mouse rotation
- Texture and image viewer
- File tree navigation
- Code editor with syntax highlighting
- Matrix-themed UI

## Supported File Types

- **Models**: ABC, MOB (Matrix Online Binary)
- **Textures**: DTX, DDS, TGA, PNG, JPG
- **Levels**: DAT, WORLD
- **Scripts**: LUA, CS, TXT, PY
- **Archives**: REZ, LTA, LTB, PKB

## Getting Started

You can run the application directly by opening `index.html` or `index_standalone.html` in a browser.

For development with modules:
1. Serve the files using a local web server (Python's `http.server` or Node.js `http-server`)
2. Open the served index.html in a browser

## Controls

### 3D Viewer:
- **WASD**: Move camera
- **Mouse drag**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click drag**: Pan

## Development

This project uses:
- React for UI components
- THREE.js for 3D rendering
- Monaco Editor for code editing
- Tailwind CSS for styling

## License

MIT