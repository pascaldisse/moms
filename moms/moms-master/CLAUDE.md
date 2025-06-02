# Matrix Online Modding Suite (MOMS) Documentation

This document provides a detailed overview of the `index_legacy.html` file structure and functionality.

## Table of Contents

1. [Document Structure](#document-structure)
2. [CSS Styles](#css-styles)
3. [React Components](#react-components)
4. [JavaScript Utilities](#javascript-utilities)
5. [THREE.js Implementation](#threejs-implementation)
6. [Binary Format Handling](#binary-format-handling)
7. [Application Logic](#application-logic)
8. [Visual Effects](#visual-effects)
9. [Application Initialization](#application-initialization)
10. [Key Functions Reference](#key-functions-reference)

## Document Structure

The application is built as a single HTML file with embedded JavaScript and CSS:

- **HTML5 Document**: Standard HTML5 document with UTF-8 encoding
- **Head Section**: Contains metadata, CSS styles, and external script loading
- **Body Section**: Contains the loading screen and root React mount point
- **External Dependencies**:
  - React 18.2.0
  - ReactDOM 18.2.0
  - Babel 7.23.5
  - Three.js 0.153.0
  - Monaco Editor 0.43.0
  - Tailwind CSS

## CSS Styles

The application uses a Matrix-inspired theme with custom CSS classes:

- **Matrix Theme Variables**:
  - `--matrix-green`: #00ff00
  - `--matrix-dark`: #001a00
  - `--matrix-black`: #000800
  - `--matrix-light`: #ccffcc

- **Major Component Styles**:
  - `.matrix-button`: Interactive buttons with hover effects
  - `.file-tree`: File navigation sidebar (left panel)
  - `.editor-container`: Monaco editor container (middle panel)
  - `.preview-container`: 3D model and media preview area (right panel)
  - `.webgl-container`: THREE.js rendering area
  - `.matrix-header`: Navigation header
  - `.loading-matrix`: Initial loading screen with Matrix rain effect

- **Utility Classes**: Tailwind-like utility classes for layout (flex, p-2, etc.)

## React Components

The application is built with React components organized in a hierarchy:

- **App Component**: Main application component that manages the overall state
  - Handles loading screen
  - Manages file selection and viewer state
  - Coordinates between different viewers and panels

- **Viewer Components**:
  - `ModelViewer`: 3D model viewer for ABC/MOB files using THREE.js
  - `TextureViewer`: Image and texture viewer for DTX/DDS files
  - `ArchiveViewer`: Archive browser for REZ/LTB files
  - `ScriptViewer`: Code editor with syntax highlighting
  - `AssemblyViewer`: DLL/EXE analysis
  - `CutsceneViewer`: Video player for cutscenes

- **UI Components**:
  - `FileTree`: Navigation sidebar showing file hierarchy
  - `Header`: Application header with controls and title
  - `MatrixRain`: Digital rain effect for loading screen
  - `LoadingScreen`: Initial application loading animation
  - `Tabs`: Tab-based navigation within viewers

## JavaScript Utilities

The application includes several utility functions for file handling:

- **File Type Detection**:
  - `getFileType()`: Determines file type based on extension
  - `FILE_TYPES` object: Maps file extensions to handlers

- **Binary Parsing**:
  - `LithtechParsers`: Collection of parsers for Lithtech engine formats
  - `parseABC()`: Actor Binary Cache parser
  - `parseMOB()`: Matrix Online Binary parser
  - `parseDTX()`: DirectX Texture parser
  - `parseFile()`: Generic file parser that routes to specific parsers

- **Helper Functions**:
  - `formatFileSize()`: Formats byte sizes into readable format
  - `createDataURL()`: Creates data URLs from files
  - `generateId()`: Generates unique IDs
  - `isDirectory()`: Checks if a path is a directory

## THREE.js Implementation

The 3D viewer is implemented with THREE.js:

- **Scene Setup**:
  - Scene creation with Matrix-themed background
  - PerspectiveCamera configuration
  - WebGLRenderer with anti-aliasing

- **Camera Controls**:
  - **WASD Movement**: 
    - W: Move forward along camera's direction
    - A: Strafe left (move camera left)
    - S: Move backward along camera's direction
    - D: Strafe right (move camera right)
  - **Mouse Rotation**:
    - Click and drag to rotate the view/camera
    - Simulates first-person style camera control
    - Movement relative to current camera orientation
  - Zoom with mouse wheel

- **Implementation Details**:
  - Keyboard event listeners track WASD key states
  - Camera translation uses `camera.translateZ()` and `camera.translateX()`
  - Mouse drag events update camera rotation
  - Animation loop applies movement based on current key states
  - Camera movement speed is configurable (default: 0.1 units/frame)

- **Model Rendering**:
  - Vertex and index buffer creation from parsed model data
  - Material creation with Matrix-themed appearance
  - Animation system for model animations

- **Lighting**:
  - Ambient light for base illumination
  - Directional light for shadows and depth
  - Matrix-themed lighting colors (green tint)

## Binary Format Handling

The application can process various Lithtech engine binary formats:

- **Model Formats**:
  - ABC (Actor Binary Cache): Character and object models
  - MOB (Matrix Online Binary): Game-specific model format

- **Texture Formats**:
  - DTX (DirectX Texture): Lithtech engine texture format
  - DDS: DirectDraw Surface textures

- **Archive Formats**:
  - REZ: Lithtech resource archive format
  - LTB/LTA: Lithtech binary/ASCII formats

- **Parsing Strategy**:
  - Binary header detection
  - Structure size estimation
  - Vertex/index extraction
  - Texture data extraction

## Application Logic

Core application logic manages the overall user experience:

- **State Management**:
  - File selection state
  - Active viewer state
  - Content loading state
  - Animation playback state

- **File Handling**:
  - File loading and parsing
  - Content extraction
  - Preview generation
  - Editing capabilities

- **Monaco Editor Integration**:
  - Code editor configuration
  - Syntax highlighting based on file type
  - Matrix-themed editor appearance

## Visual Effects

Matrix-themed visual effects enhance the user experience:

- **Matrix Digital Rain**:
  - Canvas-based implementation of falling characters
  - Dynamic character generation
  - Color and opacity variations

- **3D Rendering Effects**:
  - Matrix-themed materials and lighting
  - Grid and coordinate helpers
  - Wireframe rendering option

## Application Initialization

The application starts with a sequence of initialization steps:

1. **Loading Screen**: Displays Matrix rain animation
2. **React Initialization**: Mounts the main App component
3. **File Type Registration**: Sets up file type handlers
4. **UI Rendering**: Displays the main interface
5. **Demo Content**: Loads sample files for demonstration

## Key Functions Reference

Important functions in the codebase:

- `getFileType(filename)`: Determines file type from extension
- `LithtechParsers.parseFile(file)`: Routes files to appropriate parsers
- `formatFileSize(bytes)`: Formats byte sizes into readable format
- `animate()`: Main THREE.js animation loop
- `handleFileSelect(file)`: Handles file selection in UI
- `handleContentChange(content)`: Handles content changes in editor
- `handleFileUpload(e)`: Processes file uploads
- `initializeMatrixRain()`: Sets up the Matrix digital rain effect

---

## Development Notes

- The 3D viewer now supports WASD movement for camera navigation
- Mouse rotation is implemented in threejs_viewer.html
- Future improvements could include implementing file saving and modification
- Consider splitting the application into smaller modules for better maintainability