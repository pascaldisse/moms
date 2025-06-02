// Matrix Online Modding Suite - Main Application
// Recreated version with core functionality

(function() {
    const h = React.createElement;

    class MatrixOnlineModdingSuite extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                selectedFile: null,
                serverStatus: {
                    main: { running: false, port: 8000 },
                    bikProxy: { running: false, port: 8002 }
                },
                theme: 'matrix',
                connected: false
            };
        }

        componentDidMount() {
            this.checkServerStatus();
            this.loadTheme();
            this.setupEventListeners();
            
            // Check server status every 5 seconds
            this.statusInterval = setInterval(() => {
                this.checkServerStatus();
            }, 5000);
        }

        componentWillUnmount() {
            if (this.statusInterval) {
                clearInterval(this.statusInterval);
            }
        }

        async checkServerStatus() {
            try {
                // Check main server
                const mainResponse = await fetch('/api/status').catch(() => null);
                const mainRunning = mainResponse && mainResponse.ok;
                
                // Check BIK proxy
                const bikResponse = await fetch('http://localhost:8002/status').catch(() => null);
                const bikRunning = bikResponse && bikResponse.ok;
                
                this.setState({
                    serverStatus: {
                        main: { running: mainRunning, port: 8000 },
                        bikProxy: { running: bikRunning, port: 8002 }
                    },
                    connected: mainRunning
                });
            } catch (error) {
                console.error('Failed to check server status:', error);
                this.setState({ connected: false });
            }
        }

        loadTheme() {
            const savedSettings = localStorage.getItem('moms-settings');
            if (savedSettings) {
                try {
                    const settings = JSON.parse(savedSettings);
                    this.setState({ theme: settings.theme || 'matrix' });
                    document.body.className = `theme-${settings.theme || 'matrix'}`;
                } catch (e) {
                    console.error('Failed to load settings:', e);
                }
            }
        }

        setupEventListeners() {
            // Listen for theme changes
            window.addEventListener('theme-change', (event) => {
                this.setState({ theme: event.detail.theme });
                document.body.className = `theme-${event.detail.theme}`;
            });
        }

        handleFileSelect = (file) => {
            this.setState({ selectedFile: file });
            
            // Auto-switch to video tab if video file is selected
            if (file.name.endsWith('.bik') || file.name.endsWith('.mp4')) {
                window.dispatchEvent(new CustomEvent('switch-tab', { detail: { tab: 'video' } }));
            }
        }

        renderContent = (activeTab) => {
            switch (activeTab) {
                case 'files':
                    return h(FileBrowser, { onFileSelect: this.handleFileSelect });
                
                case 'video':
                    return h(VideoPlayer, { file: this.state.selectedFile });
                
                case 'packets':
                    return h(PacketAnalyzer);
                
                case 'combat':
                    return h(CombatAnalyzer);
                
                case 'settings':
                    return h(Settings);
                
                default:
                    return h('div', null, 'Unknown tab');
            }
        }

        render() {
            return h('div', { className: 'moms-app' },
                h('header', { className: 'app-header' },
                    h('h1', null, 'Matrix Online Modding Suite'),
                    h('div', { className: 'server-status-bar' },
                        h('span', { 
                            className: `status-indicator ${this.state.serverStatus.main.running ? 'running' : 'stopped'}`
                        }, `Main Server: ${this.state.serverStatus.main.running ? 'Running' : 'Stopped'}`),
                        h('span', { 
                            className: `status-indicator ${this.state.serverStatus.bikProxy.running ? 'running' : 'stopped'}`
                        }, `BIK Proxy: ${this.state.serverStatus.bikProxy.running ? 'Running' : 'Stopped'}`)
                    )
                ),
                h('main', { className: 'app-main' },
                    h(TabManager, { renderContent: this.renderContent })
                ),
                !this.state.connected && h('div', { className: 'connection-warning' },
                    '⚠️ Not connected to server. Please ensure server.py is running on port 8000.'
                )
            );
        }
    }

    // Initialize the application
    document.addEventListener('DOMContentLoaded', () => {
        const root = document.getElementById('root');
        if (root) {
            ReactDOM.render(h(MatrixOnlineModdingSuite), root);
        } else {
            // Create root element if it doesn't exist
            const appRoot = document.createElement('div');
            appRoot.id = 'root';
            document.body.appendChild(appRoot);
            ReactDOM.render(h(MatrixOnlineModdingSuite), appRoot);
        }
    });

    // API wrapper functions
    const API = {
        async getFiles(path = '/') {
            const response = await fetch(`/api/files?path=${encodeURIComponent(path)}`);
            if (!response.ok) throw new Error('Failed to fetch files');
            return response.json();
        },

        async getFileContent(path) {
            const response = await fetch(`/api/file?path=${encodeURIComponent(path)}`);
            if (!response.ok) throw new Error('Failed to fetch file content');
            return response.blob();
        },

        async convertBikToMp4(bikPath) {
            const response = await fetch('/api/convert-bik', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: bikPath })
            });
            if (!response.ok) throw new Error('Failed to convert BIK file');
            return response.json();
        },

        async parsePacket(hexData) {
            const response = await fetch('/api/parse-packet', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ hex: hexData })
            });
            if (!response.ok) throw new Error('Failed to parse packet');
            return response.json();
        },

        async getServerStatus() {
            const response = await fetch('/api/status');
            if (!response.ok) throw new Error('Failed to get server status');
            return response.json();
        }
    };

    // Export API for use in other scripts
    window.MOMS_API = API;

    // Utility functions
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Event bus for component communication
    class EventBus {
        constructor() {
            this.events = {};
        }

        on(event, callback) {
            if (!this.events[event]) {
                this.events[event] = [];
            }
            this.events[event].push(callback);
        }

        off(event, callback) {
            if (this.events[event]) {
                this.events[event] = this.events[event].filter(cb => cb !== callback);
            }
        }

        emit(event, data) {
            if (this.events[event]) {
                this.events[event].forEach(callback => callback(data));
            }
        }
    }

    window.EventBus = new EventBus();

    // Matrix theme effects
    function initMatrixEffect() {
        const canvas = document.createElement('canvas');
        canvas.className = 'matrix-rain';
        document.body.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const matrixArray = matrix.split("");
        
        const fontSize = 10;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        const matrixInterval = setInterval(draw, 35);
        
        // Clean up on theme change
        window.addEventListener('theme-change', (event) => {
            if (event.detail.theme !== 'matrix') {
                clearInterval(matrixInterval);
                canvas.remove();
            }
        });
    }

    // Initialize matrix effect if theme is matrix
    if (document.body.className === 'theme-matrix' || !document.body.className) {
        initMatrixEffect();
    }
})();