// Matrix Online Modding Suite - UI Components
// Recreated version with core functionality

const { createElement: h } = React;

// File Browser Component
class FileBrowser extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPath: '/',
            files: [],
            loading: false,
            error: null,
            selectedFile: null
        };
    }

    componentDidMount() {
        this.loadDirectory(this.state.currentPath);
    }

    async loadDirectory(path) {
        this.setState({ loading: true, error: null });
        try {
            const response = await fetch(`/api/files?path=${encodeURIComponent(path)}`);
            const data = await response.json();
            this.setState({ 
                files: data.files, 
                currentPath: path,
                loading: false 
            });
        } catch (error) {
            this.setState({ 
                error: `Failed to load directory: ${error.message}`,
                loading: false 
            });
        }
    }

    handleFileClick(file) {
        if (file.type === 'directory') {
            this.loadDirectory(file.path);
        } else {
            this.setState({ selectedFile: file });
            if (this.props.onFileSelect) {
                this.props.onFileSelect(file);
            }
        }
    }

    navigateUp() {
        const parts = this.state.currentPath.split('/').filter(p => p);
        parts.pop();
        const newPath = '/' + parts.join('/');
        this.loadDirectory(newPath);
    }

    render() {
        return h('div', { className: 'file-browser' },
            h('div', { className: 'browser-header' },
                h('button', {
                    onClick: () => this.navigateUp(),
                    disabled: this.state.currentPath === '/',
                    className: 'nav-button'
                }, '↑ Up'),
                h('span', { className: 'current-path' }, this.state.currentPath)
            ),
            this.state.loading && h('div', { className: 'loading' }, 'Loading...'),
            this.state.error && h('div', { className: 'error' }, this.state.error),
            h('div', { className: 'file-list' },
                this.state.files.map((file, index) =>
                    h('div', {
                        key: index,
                        className: `file-item ${file.type} ${this.state.selectedFile?.path === file.path ? 'selected' : ''}`,
                        onClick: () => this.handleFileClick(file)
                    },
                        h('span', { className: 'file-icon' },
                            file.type === 'directory' ? '📁' :
                            file.name.endsWith('.bik') ? '🎬' :
                            file.name.endsWith('.rec') ? '📼' : '📄'
                        ),
                        h('span', { className: 'file-name' }, file.name),
                        file.size && h('span', { className: 'file-size' }, formatFileSize(file.size))
                    )
                )
            )
        );
    }
}

// Video Player Component
class VideoPlayer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            playing: false,
            currentTime: 0,
            duration: 0,
            volume: 1,
            loading: false,
            error: null,
            processedUrl: null
        };
        this.videoRef = React.createRef();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.file?.path !== this.props.file?.path) {
            this.loadVideo();
        }
    }

    async loadVideo() {
        if (!this.props.file) return;
        
        this.setState({ loading: true, error: null });
        
        try {
            if (this.props.file.name.endsWith('.bik')) {
                const response = await fetch('/api/convert-bik', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: this.props.file.path })
                });
                const data = await response.json();
                this.setState({ 
                    processedUrl: `http://localhost:8002${data.url}`,
                    loading: false 
                });
            } else {
                this.setState({ 
                    processedUrl: `/api/file?path=${encodeURIComponent(this.props.file.path)}`,
                    loading: false 
                });
            }
        } catch (error) {
            this.setState({ 
                error: `Failed to load video: ${error.message}`,
                loading: false 
            });
        }
    }

    togglePlay() {
        if (this.videoRef.current) {
            if (this.state.playing) {
                this.videoRef.current.pause();
            } else {
                this.videoRef.current.play();
            }
            this.setState({ playing: !this.state.playing });
        }
    }

    handleTimeUpdate = () => {
        if (this.videoRef.current) {
            this.setState({
                currentTime: this.videoRef.current.currentTime,
                duration: this.videoRef.current.duration
            });
        }
    }

    handleSeek = (e) => {
        const time = parseFloat(e.target.value);
        if (this.videoRef.current) {
            this.videoRef.current.currentTime = time;
            this.setState({ currentTime: time });
        }
    }

    handleVolumeChange = (e) => {
        const volume = parseFloat(e.target.value);
        if (this.videoRef.current) {
            this.videoRef.current.volume = volume;
            this.setState({ volume });
        }
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    render() {
        if (!this.props.file) {
            return h('div', { className: 'video-player-empty' },
                h('p', null, 'Select a video file to play')
            );
        }

        return h('div', { className: 'video-player' },
            h('div', { className: 'video-header' },
                h('h3', null, this.props.file.name)
            ),
            this.state.loading && h('div', { className: 'loading' }, 'Processing video...'),
            this.state.error && h('div', { className: 'error' }, this.state.error),
            this.state.processedUrl && [
                h('video', {
                    key: 'video',
                    ref: this.videoRef,
                    src: this.state.processedUrl,
                    onTimeUpdate: this.handleTimeUpdate,
                    onLoadedMetadata: this.handleTimeUpdate,
                    className: 'video-element'
                }),
                h('div', { key: 'controls', className: 'video-controls' },
                    h('button', {
                        onClick: () => this.togglePlay(),
                        className: 'play-button'
                    }, this.state.playing ? '⏸️' : '▶️'),
                    h('div', { className: 'time-display' },
                        `${this.formatTime(this.state.currentTime)} / ${this.formatTime(this.state.duration)}`
                    ),
                    h('input', {
                        type: 'range',
                        min: '0',
                        max: this.state.duration || 0,
                        value: this.state.currentTime,
                        onChange: this.handleSeek,
                        className: 'seek-bar'
                    }),
                    h('div', { className: 'volume-control' },
                        '🔊',
                        h('input', {
                            type: 'range',
                            min: '0',
                            max: '1',
                            step: '0.1',
                            value: this.state.volume,
                            onChange: this.handleVolumeChange,
                            className: 'volume-slider'
                        })
                    )
                )
            ]
        );
    }
}

// Packet Analyzer Component
class PacketAnalyzer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            packets: [],
            filter: '',
            selectedPacket: null,
            autoScroll: true,
            recording: false
        };
    }

    componentDidMount() {
        this.startListening();
    }

    componentWillUnmount() {
        this.stopListening();
    }

    startListening() {
        // WebSocket connection for real-time packet updates
        this.ws = new WebSocket('ws://localhost:8001/packets');
        this.ws.onmessage = (event) => {
            const packet = JSON.parse(event.data);
            this.addPacket(packet);
        };
        this.ws.onerror = () => {
            console.log('WebSocket connection failed - packet capture not available');
        };
    }

    stopListening() {
        if (this.ws) {
            this.ws.close();
        }
    }

    addPacket(packet) {
        this.setState(prevState => ({
            packets: [...prevState.packets.slice(-999), packet]
        }), () => {
            if (this.state.autoScroll) {
                this.scrollToBottom();
            }
        });
    }

    scrollToBottom() {
        if (this.packetListEnd) {
            this.packetListEnd.scrollIntoView({ behavior: 'smooth' });
        }
    }

    clearPackets() {
        this.setState({ packets: [], selectedPacket: null });
    }

    exportPackets() {
        const data = JSON.stringify(this.state.packets, null, 2);
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `packets_${new Date().toISOString()}.json`;
        a.click();
    }

    matchesFilter(packet) {
        if (!this.state.filter) return true;
        const filterLower = this.state.filter.toLowerCase();
        return packet.type.toLowerCase().includes(filterLower) ||
               packet.hex.toLowerCase().includes(filterLower) ||
               (packet.decoded && JSON.stringify(packet.decoded).toLowerCase().includes(filterLower));
    }

    render() {
        const filteredPackets = this.state.packets.filter(p => this.matchesFilter(p));

        return h('div', { className: 'packet-analyzer' },
            h('div', { className: 'analyzer-header' },
                h('h3', null, 'Packet Analyzer'),
                h('div', { className: 'analyzer-controls' },
                    h('input', {
                        type: 'text',
                        placeholder: 'Filter packets...',
                        value: this.state.filter,
                        onChange: (e) => this.setState({ filter: e.target.value }),
                        className: 'filter-input'
                    }),
                    h('button', { onClick: () => this.clearPackets() }, 'Clear'),
                    h('button', { onClick: () => this.exportPackets() }, 'Export'),
                    h('label', null,
                        h('input', {
                            type: 'checkbox',
                            checked: this.state.autoScroll,
                            onChange: (e) => this.setState({ autoScroll: e.target.checked })
                        }),
                        'Auto-scroll'
                    )
                )
            ),
            h('div', { className: 'packet-list' },
                filteredPackets.map((packet, index) =>
                    h('div', {
                        key: index,
                        className: `packet-item ${packet.direction} ${this.state.selectedPacket === packet ? 'selected' : ''}`,
                        onClick: () => this.setState({ selectedPacket: packet })
                    },
                        h('span', { className: 'packet-time' }, new Date(packet.timestamp).toLocaleTimeString()),
                        h('span', { className: 'packet-direction' }, packet.direction === 'in' ? '←' : '→'),
                        h('span', { className: 'packet-type' }, packet.type),
                        h('span', { className: 'packet-size' }, packet.size + ' bytes')
                    )
                ),
                h('div', { ref: el => this.packetListEnd = el })
            ),
            this.state.selectedPacket && h('div', { className: 'packet-details' },
                h('h4', null, 'Packet Details'),
                h('div', { className: 'detail-section' },
                    h('strong', null, 'Hex Data:'),
                    h('pre', { className: 'hex-view' }, this.state.selectedPacket.hex)
                ),
                this.state.selectedPacket.decoded && h('div', { className: 'detail-section' },
                    h('strong', null, 'Decoded:'),
                    h('pre', { className: 'decoded-view' },
                        JSON.stringify(this.state.selectedPacket.decoded, null, 2)
                    )
                )
            )
        );
    }
}

// Combat Log Analyzer Component
class CombatAnalyzer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            combatEvents: [],
            stats: {
                totalDamage: 0,
                totalHealing: 0,
                dps: 0,
                hps: 0,
                combatDuration: 0
            },
            filter: 'all',
            selectedPlayer: null
        };
    }

    analyzeCombat(events) {
        const stats = {
            totalDamage: 0,
            totalHealing: 0,
            players: {},
            startTime: null,
            endTime: null
        };

        events.forEach(event => {
            if (!stats.startTime) stats.startTime = event.timestamp;
            stats.endTime = event.timestamp;

            if (event.type === 'damage') {
                stats.totalDamage += event.amount;
                if (!stats.players[event.source]) {
                    stats.players[event.source] = { damage: 0, healing: 0, skills: {} };
                }
                stats.players[event.source].damage += event.amount;
            } else if (event.type === 'healing') {
                stats.totalHealing += event.amount;
                if (!stats.players[event.source]) {
                    stats.players[event.source] = { damage: 0, healing: 0, skills: {} };
                }
                stats.players[event.source].healing += event.amount;
            }
        });

        const duration = stats.endTime ? (stats.endTime - stats.startTime) / 1000 : 0;
        stats.dps = duration > 0 ? stats.totalDamage / duration : 0;
        stats.hps = duration > 0 ? stats.totalHealing / duration : 0;
        stats.combatDuration = duration;

        return stats;
    }

    render() {
        return h('div', { className: 'combat-analyzer' },
            h('div', { className: 'analyzer-header' },
                h('h3', null, 'Combat Analysis'),
                h('div', { className: 'filter-controls' },
                    h('select', {
                        value: this.state.filter,
                        onChange: (e) => this.setState({ filter: e.target.value })
                    },
                        h('option', { value: 'all' }, 'All Events'),
                        h('option', { value: 'damage' }, 'Damage Only'),
                        h('option', { value: 'healing' }, 'Healing Only'),
                        h('option', { value: 'buffs' }, 'Buffs/Debuffs')
                    )
                )
            ),
            h('div', { className: 'combat-stats' },
                h('div', { className: 'stat-box' },
                    h('div', { className: 'stat-label' }, 'Total Damage'),
                    h('div', { className: 'stat-value' }, this.state.stats.totalDamage.toLocaleString())
                ),
                h('div', { className: 'stat-box' },
                    h('div', { className: 'stat-label' }, 'DPS'),
                    h('div', { className: 'stat-value' }, this.state.stats.dps.toFixed(1))
                ),
                h('div', { className: 'stat-box' },
                    h('div', { className: 'stat-label' }, 'Total Healing'),
                    h('div', { className: 'stat-value' }, this.state.stats.totalHealing.toLocaleString())
                ),
                h('div', { className: 'stat-box' },
                    h('div', { className: 'stat-label' }, 'HPS'),
                    h('div', { className: 'stat-value' }, this.state.stats.hps.toFixed(1))
                )
            ),
            h('div', { className: 'combat-log' },
                this.state.combatEvents.map((event, index) =>
                    h('div', { key: index, className: `combat-event ${event.type}` },
                        h('span', { className: 'event-time' }, new Date(event.timestamp).toLocaleTimeString()),
                        h('span', { className: 'event-source' }, event.source),
                        h('span', { className: 'event-action' }, event.action),
                        h('span', { className: 'event-target' }, event.target),
                        h('span', { className: 'event-amount' }, event.amount)
                    )
                )
            )
        );
    }
}

// Tab Manager Component
class TabManager extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTab: 'files',
            tabs: [
                { id: 'files', name: 'File Browser', icon: '📁' },
                { id: 'video', name: 'Video Player', icon: '🎬' },
                { id: 'packets', name: 'Packet Analyzer', icon: '📡' },
                { id: 'combat', name: 'Combat Log', icon: '⚔️' },
                { id: 'settings', name: 'Settings', icon: '⚙️' }
            ]
        };
    }

    componentDidMount() {
        window.addEventListener('switch-tab', (event) => {
            if (event.detail && event.detail.tab) {
                this.setState({ activeTab: event.detail.tab });
            }
        });
    }

    render() {
        return h('div', { className: 'tab-manager' },
            h('div', { className: 'tab-header' },
                this.state.tabs.map(tab =>
                    h('div', {
                        key: tab.id,
                        className: `tab ${this.state.activeTab === tab.id ? 'active' : ''}`,
                        onClick: () => this.setState({ activeTab: tab.id })
                    },
                        h('span', { className: 'tab-icon' }, tab.icon),
                        h('span', { className: 'tab-name' }, tab.name)
                    )
                )
            ),
            h('div', { className: 'tab-content' },
                this.props.renderContent(this.state.activeTab)
            )
        );
    }
}

// Settings Component
class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            settings: {
                theme: 'matrix',
                autoDecodePackets: true,
                recordingPath: '/recordings',
                serverPort: 8000,
                bikProxyPort: 8002
            }
        };
    }

    componentDidMount() {
        const savedSettings = localStorage.getItem('moms-settings');
        if (savedSettings) {
            try {
                this.setState({ settings: JSON.parse(savedSettings) });
            } catch (e) {
                console.error('Failed to load settings:', e);
            }
        }
    }

    updateSetting(key, value) {
        this.setState(prevState => ({
            settings: {
                ...prevState.settings,
                [key]: value
            }
        }), () => {
            localStorage.setItem('moms-settings', JSON.stringify(this.state.settings));
            if (key === 'theme') {
                window.dispatchEvent(new CustomEvent('theme-change', { detail: { theme: value } }));
            }
        });
    }

    render() {
        return h('div', { className: 'settings-panel' },
            h('h3', null, 'Settings'),
            h('div', { className: 'setting-group' },
                h('label', null, 'Theme'),
                h('select', {
                    value: this.state.settings.theme,
                    onChange: (e) => this.updateSetting('theme', e.target.value)
                },
                    h('option', { value: 'matrix' }, 'Matrix Green'),
                    h('option', { value: 'dark' }, 'Dark'),
                    h('option', { value: 'light' }, 'Light')
                )
            ),
            h('div', { className: 'setting-group' },
                h('label', null,
                    h('input', {
                        type: 'checkbox',
                        checked: this.state.settings.autoDecodePackets,
                        onChange: (e) => this.updateSetting('autoDecodePackets', e.target.checked)
                    }),
                    'Auto-decode packets'
                )
            ),
            h('div', { className: 'setting-group' },
                h('label', null, 'Recording Path'),
                h('input', {
                    type: 'text',
                    value: this.state.settings.recordingPath,
                    onChange: (e) => this.updateSetting('recordingPath', e.target.value)
                })
            ),
            h('div', { className: 'setting-group' },
                h('label', null, 'Server Port'),
                h('input', {
                    type: 'number',
                    value: this.state.settings.serverPort,
                    onChange: (e) => this.updateSetting('serverPort', parseInt(e.target.value))
                })
            ),
            h('div', { className: 'setting-group' },
                h('label', null, 'BIK Proxy Port'),
                h('input', {
                    type: 'number',
                    value: this.state.settings.bikProxyPort,
                    onChange: (e) => this.updateSetting('bikProxyPort', parseInt(e.target.value))
                })
            ),
            h('div', { className: 'server-status' },
                h('h4', null, 'Server Status'),
                h('div', { className: 'status-item' },
                    h('span', null, 'Main Server:'),
                    h('span', { className: 'status-indicator running' }, `Running on port ${this.state.settings.serverPort}`)
                ),
                h('div', { className: 'status-item' },
                    h('span', null, 'BIK Proxy:'),
                    h('span', { className: 'status-indicator running' }, `Running on port ${this.state.settings.bikProxyPort}`)
                )
            )
        );
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

// Export components
window.FileBrowser = FileBrowser;
window.VideoPlayer = VideoPlayer;
window.PacketAnalyzer = PacketAnalyzer;
window.CombatAnalyzer = CombatAnalyzer;
window.TabManager = TabManager;
window.Settings = Settings;