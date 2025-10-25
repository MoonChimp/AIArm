/**
 * NexusAI File Tree Component
 * Browse and manage project files
 */

class FileTree {
    constructor(containerId, apiBaseUrl = 'http://localhost:5000') {
        this.container = document.getElementById(containerId);
        this.apiBaseUrl = apiBaseUrl;
        this.currentPath = 'D:\\AIArm';
        this.expandedDirs = new Set();
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error('File tree container not found');
            return;
        }
        
        // Create file tree HTML
        this.container.innerHTML = `
            <div class="file-tree-window">
                <div class="file-tree-header">
                    <span class="file-tree-title">Files</span>
                    <div class="file-tree-controls">
                        <button class="tree-btn" onclick="fileTree.refresh()" title="Refresh">
                            <i class="iconsax" data-icon="refresh-1"></i>
                        </button>
                        <button class="tree-btn" onclick="fileTree.collapse()" title="Collapse All">
                            <i class="iconsax" data-icon="arrow-up"></i>
                        </button>
                    </div>
                </div>
                <div class="file-tree-path">
                    <input type="text" id="file-tree-path-input" value="${this.currentPath}" />
                    <button class="tree-btn-go" onclick="fileTree.changePath()">Go</button>
                </div>
                <div class="file-tree-body" id="file-tree-content">
                    <div class="loading">Loading files...</div>
                </div>
            </div>
        `;
        
        // Load initial directory
        this.loadDirectory(this.currentPath);
    }
    
    async loadDirectory(path, parentElement = null) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/files/list`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    directory: path === this.currentPath ? '' : path,
                    recursive: false
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.renderTree(result, parentElement || document.getElementById('file-tree-content'));
            } else {
                this.showError(result.error || 'Failed to load directory');
            }
            
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        }
    }
    
    renderTree(data, container) {
        if (!container) return;
        
        // Clear loading or previous content
        container.innerHTML = '';
        
        // Render directories first
        data.directories?.forEach(dir => {
            const dirElement = this.createDirectoryElement(dir);
            container.appendChild(dirElement);
        });
        
        // Then render files
        data.files?.forEach(file => {
            const fileElement = this.createFileElement(file);
            container.appendChild(fileElement);
        });
        
        if (data.directories?.length === 0 && data.files?.length === 0) {
            container.innerHTML = '<div class="tree-empty">Empty directory</div>';
        }
    }
    
    createDirectoryElement(dir) {
        const div = document.createElement('div');
        div.className = 'tree-item tree-directory';
        
        const isExpanded = this.expandedDirs.has(dir.path);
        
        div.innerHTML = `
            <div class="tree-item-content" onclick="fileTree.toggleDirectory('${dir.path}', this)">
                <i class="tree-icon iconsax" data-icon="${isExpanded ? 'arrow-down' : 'arrow-right'}"></i>
                <i class="tree-icon iconsax" data-icon="folder"></i>
                <span class="tree-label">${dir.name}</span>
            </div>
            <div class="tree-children" style="display: ${isExpanded ? 'block' : 'none'}"></div>
        `;
        
        return div;
    }
    
    createFileElement(file) {
        const div = document.createElement('div');
        div.className = 'tree-item tree-file';
        
        const icon = this.getFileIcon(file.extension);
        const sizeStr = this.formatFileSize(file.size);
        
        div.innerHTML = `
            <div class="tree-item-content" onclick="fileTree.openFile('${file.path}')">
                <i class="tree-icon">${icon}</i>
                <span class="tree-label">${file.name}</span>
                <span class="tree-size">${sizeStr}</span>
            </div>
        `;
        
        return div;
    }
    
    async toggleDirectory(path, element) {
        const parentItem = element.closest('.tree-item');
        const childrenContainer = parentItem.querySelector('.tree-children');
        const arrow = element.querySelector('.iconsax[data-icon^="arrow"]');
        
        if (this.expandedDirs.has(path)) {
            // Collapse
            this.expandedDirs.delete(path);
            childrenContainer.style.display = 'none';
            arrow.setAttribute('data-icon', 'arrow-right');
        } else {
            // Expand
            this.expandedDirs.add(path);
            childrenContainer.style.display = 'block';
            arrow.setAttribute('data-icon', 'arrow-down');
            
            // Load children if not loaded
            if (childrenContainer.children.length === 0) {
                childrenContainer.innerHTML = '<div class="loading">Loading...</div>';
                await this.loadDirectory(path, childrenContainer);
            }
        }
    }
    
    async openFile(path) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/files/read`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ path })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Dispatch event for other components to handle
                window.dispatchEvent(new CustomEvent('file-opened', {
                    detail: {
                        path: path,
                        content: result.content,
                        size: result.size
                    }
                }));
            } else {
                alert(`Error reading file: ${result.error}`);
            }
            
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
    
    changePath() {
        const input = document.getElementById('file-tree-path-input');
        const newPath = input.value.trim();
        
        if (newPath) {
            this.currentPath = newPath;
            this.expandedDirs.clear();
            this.loadDirectory(newPath);
        }
    }
    
    refresh() {
        this.expandedDirs.clear();
        this.loadDirectory(this.currentPath);
    }
    
    collapse() {
        this.expandedDirs.clear();
        this.loadDirectory(this.currentPath);
    }
    
    getFileIcon(extension) {
        const icons = {
            '.py': '🐍',
            '.js': '📜',
            '.ts': '📘',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.md': '📝',
            '.txt': '📄',
            '.xml': '📰',
            '.yml': '⚙️',
            '.yaml': '⚙️',
            '.sh': '🖥️',
            '.bat': '🖥️',
            '.jpg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.svg': '🖼️'
        };
        
        return icons[extension] || '📄';
    }
    
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
    
    showError(message) {
        const container = document.getElementById('file-tree-content');
        if (container) {
            container.innerHTML = `<div class="tree-error">${message}</div>`;
        }
    }
}

// Global instance
let fileTree = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    fileTree = new FileTree('file-tree-container');
});
