// Advanced System Provisioning and Self-Bootstrapping for NexusAI
// This module enables NexusAI to find, acquire, and create required tools autonomously

class SystemProvisioning {
  constructor() {
    this.knownTools = this.initializeToolDatabase();
    this.installationMethods = this.initializeInstallationMethods();
  }

  // Database of common tools and their detection methods
  initializeToolDatabase() {
    return {
      // Programming Languages
      'python': {
        detectCommands: ['python --version', 'python3 --version', 'py --version'],
        installMethods: ['winget', 'chocolatey', 'direct_download'],
        downloadUrl: 'https://www.python.org/downloads/',
        packageManagers: ['pip'],
        verifyCommand: 'python --version'
      },
      'node': {
        detectCommands: ['node --version', 'nodejs --version'],
        installMethods: ['winget', 'chocolatey', 'direct_download'],
        downloadUrl: 'https://nodejs.org/dist/latest/',
        packageManagers: ['npm', 'yarn'],
        verifyCommand: 'node --version'
      },
      'git': {
        detectCommands: ['git --version'],
        installMethods: ['winget', 'chocolatey', 'direct_download'],
        downloadUrl: 'https://git-scm.com/downloads',
        verifyCommand: 'git --version'
      },
      // Package Managers
      'winget': {
        detectCommands: ['winget --version'],
        installMethods: ['windows_feature'],
        verifyCommand: 'winget --version'
      },
      'chocolatey': {
        detectCommands: ['choco --version'],
        installMethods: ['powershell_script'],
        installScript: 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))',
        verifyCommand: 'choco --version'
      },
      // Development Tools
      'vscode': {
        detectCommands: ['code --version'],
        installMethods: ['winget', 'direct_download'],
        wingetId: 'Microsoft.VisualStudioCode',
        verifyCommand: 'code --version'
      },
      'chrome': {
        detectCommands: ['chrome --version'],
        registryPaths: ['HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe'],
        installMethods: ['winget', 'direct_download'],
        wingetId: 'Google.Chrome',
        verifyCommand: 'chrome --version'
      },
      // System Utilities
      'curl': {
        detectCommands: ['curl --version'],
        installMethods: ['winget', 'built_in'],
        verifyCommand: 'curl --version'
      },
      'powershell': {
        detectCommands: ['powershell -Command "Get-Host"', 'pwsh --version'],
        installMethods: ['winget', 'built_in'],
        verifyCommand: 'powershell -Command "Get-Host"'
      }
    };
  }

  // Methods for installing software
  initializeInstallationMethods() {
    return {
      winget: {
        install: (packageId) => `winget install ${packageId} --accept-package-agreements --accept-source-agreements`,
        search: (query) => `winget search ${query}`,
        available: () => this.checkToolAvailability('winget')
      },
      chocolatey: {
        install: (packageName) => `choco install ${packageName} -y`,
        search: (query) => `choco search ${query}`,
        available: () => this.checkToolAvailability('chocolatey')
      },
      direct_download: {
        method: 'download_and_install',
        requiresManualSetup: true
      },
      powershell_script: {
        method: 'execute_script',
        requiresElevation: true
      }
    };
  }

  // Check if a specific tool is available on the system
  async checkToolAvailability(toolName) {
    const tool = this.knownTools[toolName];
    if (!tool) return { available: false, reason: 'Unknown tool' };

    // Try detection commands
    for (const command of tool.detectCommands || []) {
      try {
        const result = await this.executeCommand(command);
        if (result.success && !result.output.includes('not found') && !result.output.includes('not recognized')) {
          return { 
            available: true, 
            version: this.extractVersion(result.output),
            detectedBy: command 
          };
        }
      } catch (error) {
        continue; // Try next detection method
      }
    }

    // Try registry paths (Windows)
    if (tool.registryPaths) {
      for (const regPath of tool.registryPaths) {
        try {
          const result = await this.executeCommand(`reg query "${regPath}"`);
          if (result.success) {
            return { available: true, detectedBy: 'registry', path: regPath };
          }
        } catch (error) {
          continue;
        }
      }
    }

    return { available: false, reason: 'Not detected' };
  }

  // Scan entire system for available tools
  async performSystemScan() {
    const results = {};
    const toolNames = Object.keys(this.knownTools);
    
    console.log(`🔍 Scanning system for ${toolNames.length} known tools...`);
    
    for (const toolName of toolNames) {
      try {
        results[toolName] = await this.checkToolAvailability(toolName);
      } catch (error) {
        results[toolName] = { available: false, error: error.message };
      }
    }

    return results;
  }

  // Install a missing tool using the best available method
  async installTool(toolName) {
    const tool = this.knownTools[toolName];
    if (!tool) {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    console.log(`📦 Installing ${toolName}...`);

    // Try installation methods in order of preference
    for (const method of tool.installMethods) {
      try {
        const installer = this.installationMethods[method];
        
        if (method === 'winget' && await installer.available()) {
          const packageId = tool.wingetId || toolName;
          const command = installer.install(packageId);
          const result = await this.executeCommand(command);
          
          if (result.success) {
            console.log(`✅ Successfully installed ${toolName} via winget`);
            return await this.verifyInstallation(toolName);
          }
        }
        
        else if (method === 'chocolatey' && await installer.available()) {
          const command = installer.install(toolName);
          const result = await this.executeCommand(command);
          
          if (result.success) {
            console.log(`✅ Successfully installed ${toolName} via chocolatey`);
            return await this.verifyInstallation(toolName);
          }
        }
        
        else if (method === 'powershell_script' && tool.installScript) {
          const result = await this.executeCommand(`powershell -Command "${tool.installScript}"`);
          
          if (result.success) {
            console.log(`✅ Successfully installed ${toolName} via PowerShell script`);
            return await this.verifyInstallation(toolName);
          }
        }
        
        else if (method === 'direct_download') {
          return await this.handleDirectDownload(toolName);
        }
        
      } catch (error) {
        console.log(`❌ Failed to install ${toolName} via ${method}: ${error.message}`);
        continue;
      }
    }

    throw new Error(`Failed to install ${toolName} using any available method`);
  }

  // Handle direct download and installation
  async handleDirectDownload(toolName) {
    const tool = this.knownTools[toolName];
    
    return {
      success: false,
      requiresManualIntervention: true,
      downloadUrl: tool.downloadUrl,
      instructions: `Please download and install ${toolName} from: ${tool.downloadUrl}`,
      alternativeScript: this.generateInstallationScript(toolName)
    };
  }

  // Generate a custom installation script when no other method works
  generateInstallationScript(toolName) {
    const tool = this.knownTools[toolName];
    
    return `
# Auto-generated installation script for ${toolName}
# This script attempts to download and install ${toolName} automatically

$downloadUrl = "${tool.downloadUrl || 'UPDATE_URL'}"
$tempPath = "$env:TEMP\\${toolName}_installer"
New-Item -ItemType Directory -Path $tempPath -Force

try {
    Write-Host "Downloading ${toolName}..."
    $installerPath = "$tempPath\\installer.exe"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
    
    Write-Host "Installing ${toolName}..."
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
    
    Write-Host "${toolName} installation completed!"
} catch {
    Write-Error "Installation failed: $_"
}

# Cleanup
Remove-Item -Path $tempPath -Recurse -Force
`;
  }

  // Verify that installation was successful
  async verifyInstallation(toolName) {
    const tool = this.knownTools[toolName];
    
    if (tool.verifyCommand) {
      try {
        const result = await this.executeCommand(tool.verifyCommand);
        if (result.success) {
          return { 
            verified: true, 
            version: this.extractVersion(result.output),
            output: result.output 
          };
        }
      } catch (error) {
        return { verified: false, error: error.message };
      }
    }
    
    // Fallback to availability check
    return await this.checkToolAvailability(toolName);
  }

  // Create missing capabilities from scratch
  async createCapability(capabilityName, requirements) {
    console.log(`🛠️ Creating ${capabilityName} capability from scratch...`);
    
    const templates = {
      'web_scraper': this.generateWebScraperTemplate(),
      'file_processor': this.generateFileProcessorTemplate(),
      'api_client': this.generateApiClientTemplate(),
      'automation_script': this.generateAutomationScriptTemplate(),
      'system_monitor': this.generateSystemMonitorTemplate()
    };
    
    const template = templates[capabilityName];
    if (template) {
      const filename = `${capabilityName}_${Date.now()}.py`;
      return {
        created: true,
        filename,
        code: template,
        instructions: `Custom ${capabilityName} created. Save as ${filename} and run with: python ${filename}`
      };
    }
    
    // Generate generic capability
    return this.generateGenericCapability(capabilityName, requirements);
  }

  // Template generators for common capabilities
  generateWebScraperTemplate() {
    return `
import requests
from bs4 import BeautifulSoup
import json
import time

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_url(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'title': soup.find('title').text if soup.find('title') else '',
                'text': soup.get_text(),
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'images': [img.get('src') for img in soup.find_all('img', src=True)]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def scrape_multiple(self, urls, delay=1):
        results = {}
        for url in urls:
            results[url] = self.scrape_url(url)
            time.sleep(delay)
        return results

if __name__ == "__main__":
    scraper = WebScraper()
    # Example usage
    result = scraper.scrape_url("https://example.com")
    print(json.dumps(result, indent=2))
`;
  }

  generateFileProcessorTemplate() {
    return `
import os
import json
import csv
import shutil
from pathlib import Path

class FileProcessor:
    def __init__(self):
        self.processed_count = 0
    
    def process_directory(self, directory_path, file_pattern="*"):
        directory = Path(directory_path)
        files = list(directory.glob(file_pattern))
        
        results = []
        for file_path in files:
            result = self.process_file(file_path)
            results.append(result)
            
        return results
    
    def process_file(self, file_path):
        file_path = Path(file_path)
        
        try:
            stat = file_path.stat()
            result = {
                'path': str(file_path),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'type': file_path.suffix,
                'content_preview': self.get_content_preview(file_path)
            }
            self.processed_count += 1
            return result
        except Exception as e:
            return {'path': str(file_path), 'error': str(e)}
    
    def get_content_preview(self, file_path, max_chars=500):
        try:
            if file_path.suffix.lower() in ['.txt', '.py', '.js', '.html', '.css', '.md']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(max_chars)
                    return content
        except:
            pass
        return "Binary file or unable to read"
    
    def organize_files(self, source_dir, target_dir):
        source = Path(source_dir)
        target = Path(target_dir)
        target.mkdir(exist_ok=True)
        
        organized = {}
        for file_path in source.rglob('*'):
            if file_path.is_file():
                extension = file_path.suffix.lower() or 'no_extension'
                ext_dir = target / extension[1:] if extension != 'no_extension' else target / 'no_extension'
                ext_dir.mkdir(exist_ok=True)
                
                new_path = ext_dir / file_path.name
                shutil.copy2(file_path, new_path)
                
                if extension not in organized:
                    organized[extension] = []
                organized[extension].append(str(new_path))
        
        return organized

if __name__ == "__main__":
    processor = FileProcessor()
    # Example usage
    results = processor.process_directory(".")
    print(f"Processed {len(results)} files")
`;
  }

  generateApiClientTemplate() {
    return `
import requests
import json
import time
from urllib.parse import urljoin

class ApiClient:
    def __init__(self, base_url="", headers=None, timeout=30):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout
        
        if headers:
            self.session.headers.update(headers)
    
    def get(self, endpoint, params=None):
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return {'error': str(e), 'endpoint': endpoint}
    
    def post(self, endpoint, data=None, json_data=None):
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.post(
                url, 
                data=data, 
                json=json_data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {'error': str(e), 'endpoint': endpoint}
    
    def _handle_response(self, response):
        try:
            data = response.json()
        except:
            data = response.text
        
        return {
            'status_code': response.status_code,
            'data': data,
            'headers': dict(response.headers),
            'success': response.status_code < 400
        }
    
    def batch_requests(self, requests_list, delay=1):
        results = []
        for req in requests_list:
            method = req.get('method', 'GET').lower()
            endpoint = req.get('endpoint', '')
            
            if method == 'get':
                result = self.get(endpoint, req.get('params'))
            elif method == 'post':
                result = self.post(endpoint, req.get('data'), req.get('json'))
            else:
                result = {'error': f'Unsupported method: {method}'}
            
            results.append(result)
            time.sleep(delay)
        
        return results

if __name__ == "__main__":
    client = ApiClient("https://jsonplaceholder.typicode.com/")
    result = client.get("posts/1")
    print(json.dumps(result, indent=2))
`;
  }

  generateAutomationScriptTemplate() {
    return `
import subprocess
import os
import time
import json
from datetime import datetime

class AutomationScript:
    def __init__(self):
        self.log = []
    
    def execute_command(self, command, cwd=None):
        timestamp = datetime.now().isoformat()
        self.log.append(f"{timestamp}: Executing: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            self.log.append(f"{timestamp}: Exit code: {result.returncode}")
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command,
                'timestamp': timestamp
            }
        except Exception as e:
            self.log.append(f"{timestamp}: Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'command': command,
                'timestamp': timestamp
            }
    
    def execute_sequence(self, commands, continue_on_error=False):
        results = []
        for cmd in commands:
            result = self.execute_command(cmd)
            results.append(result)
            
            if not result['success'] and not continue_on_error:
                self.log.append("Sequence stopped due to error")
                break
        
        return results
    
    def monitor_process(self, process_name, interval=5, duration=60):
        start_time = time.time()
        monitoring_data = []
        
        while time.time() - start_time < duration:
            result = self.execute_command(f"tasklist /FI \\"IMAGENAME eq {process_name}\\"")
            timestamp = datetime.now().isoformat()
            
            monitoring_data.append({
                'timestamp': timestamp,
                'running': process_name in result.get('stdout', ''),
                'output': result.get('stdout', '')
            })
            
            time.sleep(interval)
        
        return monitoring_data
    
    def save_log(self, filename=None):
        if not filename:
            filename = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write('\\n'.join(self.log))
        
        return filename

if __name__ == "__main__":
    automation = AutomationScript()
    
    # Example automation sequence
    commands = [
        "echo Starting automation...",
        "dir",
        "echo Automation completed."
    ]
    
    results = automation.execute_sequence(commands)
    log_file = automation.save_log()
    
    print(f"Automation completed. Log saved to: {log_file}")
`;
  }

  generateSystemMonitorTemplate() {
    return `
import psutil
import time
import json
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.monitoring = False
        self.data = []
    
    def get_system_info(self):
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': dict(psutil.virtual_memory()._asdict()),
            'disk': dict(psutil.disk_usage('/')._asdict()),
            'network': dict(psutil.net_io_counters()._asdict()),
            'processes': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
    
    def monitor_continuous(self, duration=300, interval=10):
        self.monitoring = True
        start_time = time.time()
        
        while self.monitoring and (time.time() - start_time < duration):
            try:
                system_info = self.get_system_info()
                self.data.append(system_info)
                
                print(f"CPU: {system_info['cpu_percent']}% | "
                      f"Memory: {system_info['memory']['percent']}% | "
                      f"Processes: {system_info['processes']}")
                
                time.sleep(interval)
            except KeyboardInterrupt:
                break
    
    def get_top_processes(self, limit=10):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
    
    def check_disk_space(self, path='/'):
        usage = psutil.disk_usage(path)
        return {
            'path': path,
            'total_gb': usage.total / (1024**3),
            'used_gb': usage.used / (1024**3),
            'free_gb': usage.free / (1024**3),
            'percent_used': (usage.used / usage.total) * 100
        }
    
    def save_monitoring_data(self, filename=None):
        if not filename:
            filename = f"system_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        return filename

if __name__ == "__main__":
    monitor = SystemMonitor()
    
    print("System Information:")
    print(json.dumps(monitor.get_system_info(), indent=2))
    
    print("\\nTop Processes:")
    for proc in monitor.get_top_processes(5):
        print(f"PID: {proc['pid']} | Name: {proc['name']} | CPU: {proc['cpu_percent']}%")
`;
  }

  // Generate a generic capability based on requirements
  generateGenericCapability(capabilityName, requirements) {
    const template = `
# Auto-generated capability: ${capabilityName}
# Requirements: ${JSON.stringify(requirements, null, 2)}

import os
import sys
import json
import time
from datetime import datetime

class ${this.capitalize(capabilityName)}:
    def __init__(self):
        self.name = "${capabilityName}"
        self.created = datetime.now().isoformat()
        print(f"Initialized {self.name} capability")
    
    def execute(self, *args, **kwargs):
        """Main execution method - customize based on requirements"""
        try:
            result = self._process(*args, **kwargs)
            return {
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _process(self, *args, **kwargs):
        """Override this method to implement specific functionality"""
        return f"{self.name} processing completed with args: {args}, kwargs: {kwargs}"
    
    def get_status(self):
        return {
            'capability': self.name,
            'status': 'active',
            'created': self.created
        }

if __name__ == "__main__":
    capability = ${this.capitalize(capabilityName)}()
    result = capability.execute()
    print(json.dumps(result, indent=2))
`;

    return {
      created: true,
      filename: `${capabilityName}_capability.py`,
      code: template,
      instructions: `Custom ${capabilityName} capability created. Modify the _process method to implement specific functionality.`
    };
  }

  // Utility methods
  async executeCommand(command) {
    return new Promise((resolve) => {
      try {
        const { exec } = require('child_process');
        
        // Set larger buffer size and shorter timeout to prevent hanging
        const options = {
          timeout: 15000, // 15 seconds
          maxBuffer: 1024 * 1024 * 10, // 10MB buffer
          encoding: 'utf8'
        };
        
        exec(command, options, (error, stdout, stderr) => {
          if (error) {
            resolve({
              success: false,
              output: error.message,
              stderr: stderr,
              command: command
            });
          } else {
            resolve({
              success: true,
              output: stdout || stderr || 'Command completed',
              command: command
            });
          }
        });
      } catch (error) {
        resolve({
          success: false,
          output: error.message,
          command: command
        });
      }
    });
  }

  extractVersion(output) {
    const versionRegex = /(\d+\.?\d*\.?\d*\.?\d*)/;
    const match = output.match(versionRegex);
    return match ? match[1] : 'unknown';
  }

  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Main provisioning workflow
  async ensureCapability(capabilityName, requirements = {}) {
    console.log(`🎯 Ensuring capability: ${capabilityName}`);
    
    // 1. Check if required tools exist
    const toolCheck = await this.checkToolAvailability(capabilityName);
    
    if (toolCheck.available) {
      console.log(`✅ ${capabilityName} is already available`);
      return { available: true, method: 'existing', ...toolCheck };
    }
    
    // 2. Try to install missing tools
    try {
      const installResult = await this.installTool(capabilityName);
      if (installResult.verified) {
        console.log(`✅ Successfully installed ${capabilityName}`);
        return { available: true, method: 'installed', ...installResult };
      }
    } catch (error) {
      console.log(`⚠️ Installation failed: ${error.message}`);
    }
    
    // 3. Create capability from scratch
    try {
      const createResult = await this.createCapability(capabilityName, requirements);
      console.log(`✅ Created ${capabilityName} capability from scratch`);
      return { available: true, method: 'created', ...createResult };
    } catch (error) {
      console.log(`❌ Failed to create capability: ${error.message}`);
      throw error;
    }
  }
}

module.exports = SystemProvisioning;
