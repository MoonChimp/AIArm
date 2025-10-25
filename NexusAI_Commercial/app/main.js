/**
 * NexusAI Commercial - Electron Main Process
 * Handles app lifecycle, window management, and system integration
 */

const { app, BrowserWindow, Menu, ipcMain, shell, dialog, globalShortcut } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const http = require('http');

// Keep a global reference of the window object
let mainWindow;
let backendProcess;
let serverPort = 5000;

// Default app paths
const APP_PATH = app.getAppPath();
const BACKEND_PATH = path.join(APP_PATH, 'backend');
const HTML_PATH = path.join(APP_PATH, 'html');
const ASSETS_PATH = path.join(APP_PATH, 'assets');

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: getIconPath(),
        title: 'NexusAI Commercial - Enterprise AI Solutions',
        show: false, // Don't show until ready
        backgroundColor: '#0a0e17'
    });

    // Load the main cinematic interface
    mainWindow.loadFile(path.join(APP_PATH, 'index.html'));

    // Show window when ready to prevent visual flash
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.focus();
    });

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    // Handle external links
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    // Handle window closed
    mainWindow.on('closed', () => {
        mainWindow = null;
        stopBackend();
    });

    // Handle app activation (macOS)
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
}

function getIconPath() {
    const iconPath = path.join(APP_PATH, 'assets', 'icons', process.platform, 'icon.png');
    return fs.existsSync(iconPath) ? iconPath : undefined;
}

function startBackend() {
    return new Promise((resolve, reject) => {
        try {
            const backendScript = path.join(BACKEND_PATH, 'nexus_functional_api.py');

            if (!fs.existsSync(backendScript)) {
                console.error('Backend script not found:', backendScript);
                reject(new Error('Backend script not found'));
                return;
            }

            // Start the Python backend
            backendProcess = spawn('python', [backendScript], {
                cwd: BACKEND_PATH,
                stdio: ['pipe', 'pipe', 'pipe'],
                env: {
                    ...process.env,
                    PYTHONPATH: BACKEND_PATH,
                    NODE_ENV: 'production'
                }
            });

            let startupOutput = '';
            const startupTimeout = setTimeout(() => {
                reject(new Error('Backend startup timeout'));
            }, 30000);

            backendProcess.stdout.on('data', (data) => {
                const output = data.toString();
                startupOutput += output;
                console.log('Backend:', output.trim());

                // Check for successful startup
                if (output.includes('Starting FUNCTIONAL API server') ||
                    output.includes('Running on http://')) {
                    clearTimeout(startupTimeout);
                    resolve();
                }
            });

            backendProcess.stderr.on('data', (data) => {
                console.error('Backend Error:', data.toString().trim());
            });

            backendProcess.on('close', (code) => {
                console.log(`Backend process exited with code ${code}`);
                if (code !== 0) {
                    dialog.showErrorBox('Backend Error', 'NexusAI backend stopped unexpectedly');
                }
            });

            backendProcess.on('error', (error) => {
                clearTimeout(startupTimeout);
                console.error('Failed to start backend:', error);
                reject(error);
            });

        } catch (error) {
            console.error('Error starting backend:', error);
            reject(error);
        }
    });
}

function stopBackend() {
    if (backendProcess) {
        backendProcess.kill();
        backendProcess = null;
    }
}

function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'New Chat Session',
                    accelerator: 'CmdOrCtrl+N',
                    click: () => {
                        mainWindow.webContents.send('new-chat-session');
                    }
                },
                {
                    label: 'Clear Memory',
                    click: () => {
                        mainWindow.webContents.send('clear-memory');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Settings',
                    accelerator: 'CmdOrCtrl+,',
                    click: () => {
                        mainWindow.webContents.send('open-settings');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                {
                    label: 'Reload',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.webContents.reload();
                    }
                },
                {
                    label: 'Force Reload',
                    accelerator: 'CmdOrCtrl+Shift+R',
                    click: () => {
                        mainWindow.webContents.reloadIgnoringCache();
                    }
                },
                { type: 'separator' },
                {
                    label: 'Toggle Developer Tools',
                    accelerator: process.platform === 'darwin' ? 'Alt+Command+I' : 'Ctrl+Shift+I',
                    click: () => {
                        mainWindow.webContents.toggleDevTools();
                    }
                },
                { type: 'separator' },
                {
                    label: 'Actual Size',
                    accelerator: 'CmdOrCtrl+0',
                    click: () => {
                        mainWindow.webContents.setZoomLevel(0);
                    }
                },
                {
                    label: 'Zoom In',
                    accelerator: 'CmdOrCtrl+Plus',
                    click: () => {
                        const currentZoom = mainWindow.webContents.getZoomLevel();
                        mainWindow.webContents.setZoomLevel(currentZoom + 1);
                    }
                },
                {
                    label: 'Zoom Out',
                    accelerator: 'CmdOrCtrl+-',
                    click: () => {
                        const currentZoom = mainWindow.webContents.getZoomLevel();
                        mainWindow.webContents.setZoomLevel(currentZoom - 1);
                    }
                }
            ]
        },
        {
            label: 'AI',
            submenu: [
                {
                    label: 'Chat Interface',
                    accelerator: 'CmdOrCtrl+1',
                    click: () => {
                        mainWindow.loadFile(path.join(APP_PATH, 'html', 'chat.html'));
                    }
                },
                {
                    label: 'Landing Page',
                    accelerator: 'CmdOrCtrl+2',
                    click: () => {
                        mainWindow.loadFile(path.join(APP_PATH, 'index.html'));
                    }
                },
                { type: 'separator' },
                {
                    label: 'Personality: Balanced',
                    click: () => setPersonality('balanced')
                },
                {
                    label: 'Personality: Caring',
                    click: () => setPersonality('caring')
                },
                {
                    label: 'Personality: Professional',
                    click: () => setPersonality('professional')
                },
                {
                    label: 'Personality: Honest',
                    click: () => setPersonality('honest')
                },
                {
                    label: 'Personality: Thoughtful',
                    click: () => setPersonality('thoughtful')
                }
            ]
        },
        {
            label: 'Tools',
            submenu: [
                {
                    label: 'Generate Image',
                    accelerator: 'CmdOrCtrl+G',
                    click: () => {
                        mainWindow.webContents.send('generate-image');
                    }
                },
                {
                    label: 'Execute Code',
                    accelerator: 'CmdOrCtrl+E',
                    click: () => {
                        mainWindow.webContents.send('execute-code');
                    }
                },
                { type: 'separator' },
                {
                    label: 'System Monitor',
                    click: () => {
                        mainWindow.webContents.send('toggle-system-monitor');
                    }
                },
                {
                    label: 'Memory Status',
                    click: () => {
                        mainWindow.webContents.send('show-memory-status');
                    }
                }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Documentation',
                    click: () => {
                        shell.openExternal('file://' + path.join(APP_PATH, 'README_BUSINESS.md'));
                    }
                },
                {
                    label: 'API Documentation',
                    click: () => {
                        shell.openExternal(`http://localhost:${serverPort}/api/`);
                    }
                },
                { type: 'separator' },
                {
                    label: 'About NexusAI',
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'About NexusAI Commercial',
                            message: 'NexusAI Commercial - Enterprise AI Solutions',
                            detail: 'The most advanced AI assistant for business.\n\n' +
                                   'Features:\n' +
                                   '• Self-Aware Intelligence\n' +
                                   '• Continuous Learning\n' +
                                   '• Memory System\n' +
                                   '• Code Execution\n' +
                                   '• Image Generation\n' +
                                   '• ML Integration\n\n' +
                                   'Version: 1.0.0\n' +
                                   '© 2024 NexusAI Commercial'
                        });
                    }
                }
            ]
        }
    ];

    // macOS specific adjustments
    if (process.platform === 'darwin') {
        template.unshift({
            label: app.getName(),
            submenu: [
                { role: 'about' },
                { type: 'separator' },
                { role: 'services' },
                { type: 'separator' },
                { role: 'hide' },
                { role: 'hideothers' },
                { role: 'unhide' },
                { type: 'separator' },
                { role: 'quit' }
            ]
        });

        // Window menu
        template.splice(3, 0, {
            label: 'Window',
            submenu: [
                { role: 'close' },
                { role: 'minimize' },
                { role: 'zoom' },
                { type: 'separator' },
                { role: 'front' }
            ]
        });
    }

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function setPersonality(mode) {
    if (mainWindow) {
        mainWindow.webContents.send('set-personality', mode);
    }
}

// App event handlers
app.whenReady().then(async () => {
    console.log('Starting NexusAI Commercial...');

    try {
        // Start the backend server
        await startBackend();
        console.log('Backend started successfully');

        // Create main window
        createWindow();

        // Create application menu
        createMenu();

        // Register global shortcuts
        globalShortcut.register('CommandOrControl+Shift+C', () => {
            if (mainWindow) {
                mainWindow.webContents.send('clear-chat');
            }
        });

        globalShortcut.register('CommandOrControl+Shift+N', () => {
            if (mainWindow) {
                mainWindow.webContents.send('new-chat-session');
            }
        });

        console.log('NexusAI Commercial is ready!');

    } catch (error) {
        console.error('Failed to start application:', error);
        dialog.showErrorBox('Startup Error', 'Failed to start NexusAI Commercial. Please check the logs for details.');
        app.quit();
    }
});

app.on('window-all-closed', () => {
    // On macOS, keep app running even when all windows are closed
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    stopBackend();
});

app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});

// IPC handlers for communication with renderer process
ipcMain.handle('get-app-path', () => APP_PATH);
ipcMain.handle('get-backend-status', async () => {
    return new Promise((resolve) => {
        const req = http.request(`http://localhost:${serverPort}/api/status`, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch {
                    resolve({ error: 'Backend not responding' });
                }
            });
        });

        req.on('error', () => {
            resolve({ error: 'Cannot connect to backend' });
        });

        req.setTimeout(5000, () => {
            req.destroy();
            resolve({ error: 'Backend timeout' });
        });

        req.end();
    });
});

ipcMain.handle('show-save-dialog', async (event, options) => {
    return dialog.showSaveDialog(mainWindow, options);
});

ipcMain.handle('show-open-dialog', async (event, options) => {
    return dialog.showOpenDialog(mainWindow, options);
});

// Security: Prevent new window creation except for external links
app.on('web-contents-created', (event, contents) => {
    contents.on('new-window', (event, navigationUrl) => {
        event.preventDefault();
        shell.openExternal(navigationUrl);
    });
});

console.log('NexusAI Commercial main process loaded');
