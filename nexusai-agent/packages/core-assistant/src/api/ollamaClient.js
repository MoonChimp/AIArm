const axios = require('axios');
const config = require('../config/apiConfig.js');
const SystemProvisioning = require('./systemProvisioning');
const MultiAgentOrchestrator = require('./multiAgentOrchestrator');
const LearningMatrix = require('./learningMatrix');

class OllamaClient {
  constructor() {
    this.ollamaConfig = config.ollama;
    this.claudeConfig = config.claude;
    this.adaptiveConfig = config.adaptiveFallback;
    this.isOllamaAvailable = false;
    this.systemProvisioning = new SystemProvisioning();
    
    // Initialize Multi-Agent Orchestrator
    this.multiAgentOrchestrator = new MultiAgentOrchestrator();
    this.multiAgentOrchestrator.initializeSystem();
    
    // Initialize Learning Matrix for Claude knowledge integration
    this.learningMatrix = new LearningMatrix(this.adaptiveConfig?.learningStorage);
    this.initializeLearningMatrix();
    
    // Session tracking for cost control
    this.sessionStats = {
      claudeCallsUsed: 0,
      ollamaSuccesses: 0,
      olllamaFailures: 0,
      learningEvents: 0,
      multiAgentRequests: 0,
      startTime: Date.now()
    };
    
    // Learning data storage
    this.learningData = [];
    
    // Initialize confidence tracking
    this.confidenceThreshold = this.adaptiveConfig?.confidenceThreshold || 0.7;
    
    console.log('🤖 NexusAI initialized with Multi-Agent System and Learning Matrix');
  }

  // Initialize the Learning Matrix system
  async initializeLearningMatrix() {
    try {
      await this.learningMatrix.initialize();
      const stats = this.learningMatrix.getMatrixStats();
      console.log(`🧠 Learning Matrix initialized with ${stats.totalEntries} entries, ${stats.totalPatterns} patterns`);
    } catch (error) {
      console.error('❌ Failed to initialize Learning Matrix:', error.message);
    }
  }

  // Test connection to Ollama with enhanced model checking
  async testConnection() {
    try {
      console.log('🔍 Testing Ollama connection to:', this.ollamaConfig.baseUrl);
      console.log('🎯 Looking for primary model:', this.ollamaConfig.model);
      
      const response = await axios.get(`${this.ollamaConfig.baseUrl}/api/tags`, {
        timeout: 10000 // Increased timeout
      });
      
      const models = response.data.models || [];
      const modelNames = models.map(m => m.name);
      console.log('📋 Available models:', modelNames);
      
      // Check for primary model (exact match first)
      const hasPrimaryModel = models.some(model => model.name === this.ollamaConfig.model);
      
      // Check for enhanced agent models
      const hasEnhancedAgent = models.some(model => 
        model.name === 'nexusai-agent-enhanced:latest' || 
        model.name.startsWith('nexusai-agent-enhanced')
      );
      
      // Check for any nexusai model as fallback
      const hasAnyNexusModel = models.some(model => 
        model.name.startsWith('nexusai')
      );
      
      let selectedModel = this.ollamaConfig.model;
      let availabilityStatus = 'unavailable';
      
      if (hasPrimaryModel) {
        availabilityStatus = 'primary_available';
        console.log('✅ Primary model found:', this.ollamaConfig.model);
      } else if (hasEnhancedAgent) {
        selectedModel = 'nexusai-agent-enhanced:latest';
        availabilityStatus = 'enhanced_available';
        console.log('✅ Enhanced agent model found, using:', selectedModel);
        // Update config to use the available model
        this.ollamaConfig.model = selectedModel;
      } else if (hasAnyNexusModel) {
        const fallbackModel = models.find(m => m.name.startsWith('nexusai')).name;
        selectedModel = fallbackModel;
        availabilityStatus = 'fallback_available';
        console.log('⚠️ Using fallback nexus model:', selectedModel);
        this.ollamaConfig.model = selectedModel;
      } else {
        console.log('❌ No suitable NexusAI models found');
      }
      
      this.isOllamaAvailable = availabilityStatus !== 'unavailable';
      
      return {
        success: true,
        available: this.isOllamaAvailable,
        models: modelNames,
        selectedModel: selectedModel,
        availabilityStatus: availabilityStatus,
        message: this.isOllamaAvailable 
          ? `Connected! Using model: ${selectedModel} (${availabilityStatus})`
          : `No suitable models found. Available: ${modelNames.join(', ')}`
      };
    } catch (error) {
      console.error('❌ Ollama connection failed:', error.message);
      this.isOllamaAvailable = false;
      return {
        success: false,
        available: false,
        error: error.message,
        message: 'Failed to connect to Ollama server - ensure Ollama is running'
      };
    }
  }

  // Intelligent Adaptive Fallback System - NexusAI as Claude Passthrough
  async sendMessage(message, options = {}) {
    console.log('\n🧠 === ADAPTIVE FALLBACK SYSTEM ACTIVATED ===');
    console.log(`📊 Session Stats - Claude calls used: ${this.sessionStats.claudeCallsUsed}/${this.adaptiveConfig?.maxClaudeCallsPerSession || 10}`);
    
    try {
      // Step 1: Assess task complexity and confidence
      const taskAssessment = this.assessTaskComplexity(message);
      console.log(`🎯 Task Assessment:`, taskAssessment);
      
      // Step 1.5: Try Multi-Agent System for complex tasks
      if (taskAssessment.category === 'high' || taskAssessment.score > 0.6) {
        console.log('🚀 MULTI-AGENT: Using specialized agent collaboration...');
        try {
          const multiAgentResult = await this.multiAgentOrchestrator.processRequest(message, options);
          
          if (multiAgentResult.success) {
            console.log('✅ Multi-Agent processing successful');
            this.sessionStats.multiAgentRequests++;
            
            return {
              success: true,
              response: multiAgentResult.result,
              provider: 'multi-agent-system',
              analysis: multiAgentResult.analysis,
              agents_used: multiAgentResult.agents_used,
              emotional_state: multiAgentResult.emotional_state,
              memory_context: multiAgentResult.memory_context,
              adaptiveStats: this.getSessionSummary()
            };
          } else {
            console.log('⚠️ Multi-Agent processing failed, continuing with adaptive fallback');
          }
        } catch (error) {
          console.error('❌ Multi-Agent system error:', error.message);
        }
      }
      
      // Step 2: Check if we should try Ollama first
      const shouldTryOllama = this.shouldAttemptOllamaFirst(taskAssessment, message);
      console.log(`🤖 Should try Ollama first: ${shouldTryOllama}`);
      
      if (shouldTryOllama && this.ollamaConfig.enabled) {
        console.log('🚀 PRIMARY: Attempting with Ollama (LOCAL/FREE)...');
        const ollamaResponse = await this.sendToOllamaWithConfidenceScoring(message, options, taskAssessment);
        
        // Step 3: Evaluate Ollama response quality
        if (ollamaResponse.success) {
          const qualityScore = this.evaluateResponseQuality(ollamaResponse.response, taskAssessment);
          console.log(`📈 Ollama response quality score: ${qualityScore.toFixed(2)}`);
          
          if (qualityScore >= this.confidenceThreshold) {
            console.log('✅ Ollama response meets quality threshold - using it!');
            this.sessionStats.ollamaSuccesses++;
            return {
              ...ollamaResponse,
              confidence: qualityScore,
              adaptiveStats: this.getSessionSummary()
            };
          } else {
            console.log(`⚠️ Ollama response quality ${qualityScore.toFixed(2)} below threshold ${this.confidenceThreshold} - triggering fallback`);
          }
        } else {
          console.log('❌ Ollama failed completely - triggering fallback');
          this.sessionStats.olllamaFailures++;
        }
      }
      
      // Step 4: Check if Claude fallback is available and within limits
      const canUseClaude = this.canUseClaude(taskAssessment);
      if (!canUseClaude.allowed) {
        console.log(`🚫 Claude fallback blocked: ${canUseClaude.reason}`);
        return {
          success: false,
          error: `Task requires advanced capabilities but ${canUseClaude.reason}`,
          response: `I attempted to handle this task locally but need additional capabilities. ${canUseClaude.reason}. Please try a simpler request or check my configuration.`,
          adaptiveStats: this.getSessionSummary()
        };
      }
      
      // Step 5: Use Claude as learning tool and passthrough
      console.log('🧠 FALLBACK: Using Claude as learning tool...');
      const claudeResponse = await this.sendToClaudeAsLearningTool(message, options, taskAssessment);
      
      if (claudeResponse.success) {
        // Step 6: Capture learning data from Claude interaction
        await this.captureLearningData(message, claudeResponse, taskAssessment);
        this.sessionStats.claudeCallsUsed++;
        this.sessionStats.learningEvents++;
        
        return {
          ...claudeResponse,
          provider: 'claude-learning-passthrough',
          adaptiveStats: this.getSessionSummary(),
          learningNote: '🎓 This response was enhanced by Claude. NexusAI is learning from this interaction to improve future local responses.'
        };
      }
      
      throw new Error('Both Ollama and Claude failed to respond');
      
    } catch (error) {
      console.error('💥 Adaptive fallback system error:', error.message);
      return {
        success: false,
        error: error.message,
        response: `I encountered an error with both local and fallback systems. Please check that Ollama is running locally at ${this.ollamaConfig.baseUrl} with model ${this.ollamaConfig.model} loaded.`,
        adaptiveStats: this.getSessionSummary()
      };
    }
  }

  // Send to Claude with comprehensive Cline system prompts and tool execution capabilities
  async sendToClaudeWithClinePrompts(message, options = {}) {
    try {
      console.log('🚀 Starting Claude API call...');
      console.log('💳 API Key present:', this.claudeConfig.apiKey ? 'YES' : 'NO');
      console.log('🎯 Model:', this.claudeConfig.model);
      console.log('📝 Message length:', message.length);
      
      // Get current personality settings
      const personalityMode = config.personality?.current || 'adaptive';
      const personality = config.personality?.profiles?.[personalityMode] || config.personality.profiles.adaptive;
      
      const clineSystemPrompt = this.generateComprehensiveClinePrompt(personalityMode, personality);

      const requestData = {
        model: this.claudeConfig.model,
        max_tokens: options.max_tokens || this.claudeConfig.maxTokens,
        system: clineSystemPrompt,
        messages: [
          {
            role: 'user',
            content: message
          }
        ]
      };

      console.log('📊 Request data prepared, sending to Claude...');

      const response = await axios.post(
        `${this.claudeConfig.baseUrl}/messages`,
        requestData,
        {
          timeout: this.claudeConfig.timeout,
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': this.claudeConfig.apiKey,
            'anthropic-version': '2023-06-01'
          }
        }
      );

      console.log('✅ Claude API response received!');
      console.log('📋 Status:', response.status);
      console.log('📄 Response keys:', Object.keys(response.data || {}));
      
      if (response.data && response.data.content && response.data.content[0]) {
        const claudeResponse = response.data.content[0].text;
        console.log('🎉 SUCCESS! Response length:', claudeResponse.length);
        
        // Execute any tools requested by Claude
        const processedResponse = await this.executeToolRequests(claudeResponse);
        
        return {
          success: true,
          response: processedResponse,
          model: this.claudeConfig.model,
          provider: 'claude-cline'
        };
      }

      console.error('❌ Invalid response structure:', JSON.stringify(response.data, null, 2));
      throw new Error('Invalid response from Claude - missing content');
    } catch (error) {
      console.error('💥 DETAILED Claude error:');
      console.error('Message:', error.message);
      console.error('Status:', error.response?.status);
      console.error('Status Text:', error.response?.statusText);
      console.error('Response Data:', JSON.stringify(error.response?.data, null, 2));
      console.error('Full error:', error);
      
      return {
        success: false,
        error: error.message,
        details: error.response?.data,
        provider: 'claude-cline'
      };
    }
  }

  // Execute comprehensive tool requests with enhanced debugging and single-pass processing
  async executeToolRequests(response) {
    let processedResponse = response;
    const processedMatches = new Set(); // Track processed matches to prevent duplicates

    console.log('🔍 DEBUGGING: Raw response length:', response.length);
    console.log('🔍 DEBUGGING: Looking for tool patterns in response...');

    // Enhanced file read operations with single comprehensive pattern
    const fileReadPattern = /<execute_file_read>\s*(.*?)\s*<\/execute_file_read>/gs;
    let match;
    while ((match = fileReadPattern.exec(response)) !== null) {
      const matchKey = `file_read:${match.index}:${match[0]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const filepath = match[1].trim();
      console.log('🔧 FOUND file read request:', filepath);
      
      try {
        const fs = require('fs').promises;
        const content = await fs.readFile(filepath, 'utf8');
        const replacement = `📄 File content from ${filepath}:\n\`\`\`\n${content}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
        console.log('✅ File read successful:', filepath);
      } catch (error) {
        const replacement = `❌ Error reading ${filepath}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
        console.log('❌ File read failed:', error.message);
      }
    }

    // Enhanced file write operations with comprehensive patterns to prevent duplicates
    const fileWritePatterns = [
      // Standard XML format: <execute_file_write path="file.txt">content</execute_file_write>
      /<execute_file_write\s+path=["']([^"']+)["']>\s*(.*?)\s*<\/execute_file_write>/gs,
      // Alternative colon format: execute_file_write path="file.txt": content
      /execute_file_write\s+path=["']([^"']+)["']\s*:\s*([\s\S]*?)(?=execute_|$)/gs
    ];
    
    let fileWriteFound = false;
    
    for (const pattern of fileWritePatterns) {
      while ((match = pattern.exec(response)) !== null) {
        const matchKey = `file_write:${match.index}:${match[1]}`;
        if (processedMatches.has(matchKey)) continue;
        processedMatches.add(matchKey);
        
        fileWriteFound = true;
        const filepath = match[1].trim();
        const content = match[2].trim();
        console.log('🔧 FOUND file write request:', filepath);
        console.log('🔧 Content length:', content.length);
        
        try {
          const fs = require('fs').promises;
          const path = require('path');
          
          // Ensure directory exists
          const dir = path.dirname(filepath);
          console.log('📁 Creating directory if needed:', dir);
          await fs.mkdir(dir, { recursive: true });
          
          console.log('💾 Writing file:', filepath);
          await fs.writeFile(filepath, content, 'utf8');
          
          const replacement = `✅ File written successfully: ${filepath}`;
          processedResponse = processedResponse.replace(match[0], replacement);
          console.log('✅ FILE WRITE SUCCESSFUL:', filepath);
        } catch (error) {
          const replacement = `❌ Error writing ${filepath}: ${error.message}`;
          processedResponse = processedResponse.replace(match[0], replacement);
          console.log('❌ FILE WRITE FAILED:', error.message);
        }
      }
    }

    if (!fileWriteFound) {
      console.log('⚠️ NO FILE WRITE PATTERNS MATCHED');
      console.log('🔍 Response preview:', response.substring(0, 500));
      
      // Try to detect any file write attempts in plain text
      if (response.includes('file_write') || response.includes('write') || response.includes('create')) {
        console.log('📝 Response contains file write keywords - may need pattern adjustment');
      }
    }

    // Command execution with duplicate prevention
    const commandPattern = /<execute_command(?:\s+cwd="([^"]*)")?>\s*(.*?)\s*<\/execute_command>/gs;
    while ((match = commandPattern.exec(response)) !== null) {
      const matchKey = `command:${match.index}:${match[2]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const cwd = match[1] || process.cwd();
      const command = match[2].trim();
      console.log('🔧 Executing command:', command, 'in', cwd);
      
      try {
        const { exec } = require('child_process');
        const util = require('util');
        const execAsync = util.promisify(exec);
        
        const result = await execAsync(command, { cwd, timeout: 30000 });
        const output = result.stdout || result.stderr || 'Command completed successfully';
        const replacement = `💻 Command result:\n\`\`\`\n$ ${command}\n${output}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
      } catch (error) {
        const replacement = `❌ Command failed:\n\`\`\`\n$ ${command}\n${error.message}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // File list operations with duplicate prevention
    const fileListPattern = /<execute_file_list>\s*(.*?)\s*<\/execute_file_list>/gs;
    while ((match = fileListPattern.exec(response)) !== null) {
      const matchKey = `file_list:${match.index}:${match[1]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const dirpath = match[1].trim();
      console.log('🔧 Executing directory list:', dirpath);
      
      try {
        const fs = require('fs').promises;
        const items = await fs.readdir(dirpath, { withFileTypes: true });
        const itemList = items.map(item => 
          `${item.isDirectory() ? '📁' : '📄'} ${item.name}`
        ).join('\n');
        const replacement = `📂 Directory listing for ${dirpath}:\n\`\`\`\n${itemList}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
      } catch (error) {
        const replacement = `❌ Error listing ${dirpath}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // Web fetch operations with duplicate prevention
    const webFetchPattern = /<execute_web_fetch>\s*(.*?)\s*<\/execute_web_fetch>/gs;
    while ((match = webFetchPattern.exec(response)) !== null) {
      const matchKey = `web_fetch:${match.index}:${match[1]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const url = match[1].trim();
      console.log('🔧 Executing web fetch:', url);
      
      try {
        const webResponse = await axios.get(url, { timeout: 10000 });
        const data = typeof webResponse.data === 'string' 
          ? webResponse.data 
          : JSON.stringify(webResponse.data, null, 2);
        const replacement = `🌐 Web fetch result from ${url}:\n\`\`\`\n${data.substring(0, 2000)}${data.length > 2000 ? '...' : ''}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
      } catch (error) {
        const replacement = `❌ Web fetch failed for ${url}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // System scan operations with duplicate prevention
    const systemScanPattern = /<execute_system_scan><\/execute_system_scan>/gs;
    while ((match = systemScanPattern.exec(response)) !== null) {
      const matchKey = `system_scan:${match.index}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      console.log('🔧 Executing system scan...');
      
      try {
        const scanResults = await this.systemProvisioning.performSystemScan();
        const availableTools = Object.entries(scanResults)
          .filter(([_, result]) => result.available)
          .map(([tool, result]) => `✅ ${tool} - ${result.version || 'available'}`)
          .join('\n');
        
        const missingTools = Object.entries(scanResults)
          .filter(([_, result]) => !result.available)
          .map(([tool, result]) => `❌ ${tool} - ${result.reason || 'not found'}`)
          .join('\n');
        
        const replacement = `🔍 System Scan Results:\n\`\`\`\nAvailable Tools:\n${availableTools}\n\nMissing Tools:\n${missingTools}\n\`\`\``;
        processedResponse = processedResponse.replace(match[0], replacement);
      } catch (error) {
        const replacement = `❌ System scan failed: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // Tool installation operations with duplicate prevention
    const installToolPattern = /<execute_install_tool>\s*(.*?)\s*<\/execute_install_tool>/gs;
    while ((match = installToolPattern.exec(response)) !== null) {
      const matchKey = `install_tool:${match.index}:${match[1]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const toolName = match[1].trim();
      console.log('🔧 Installing tool:', toolName);
      
      try {
        const installResult = await this.systemProvisioning.installTool(toolName);
        
        if (installResult.verified) {
          const replacement = `✅ Successfully installed ${toolName} - Version: ${installResult.version}`;
          processedResponse = processedResponse.replace(match[0], replacement);
        } else if (installResult.requiresManualIntervention) {
          const replacement = `⚠️ ${toolName} requires manual installation:\n\`\`\`\n${installResult.instructions}\n\`\`\`\nAlternative script:\n\`\`\`powershell\n${installResult.alternativeScript}\n\`\`\``;
          processedResponse = processedResponse.replace(match[0], replacement);
        } else {
          const replacement = `❌ Failed to install ${toolName}`;
          processedResponse = processedResponse.replace(match[0], replacement);
        }
      } catch (error) {
        const replacement = `❌ Installation failed for ${toolName}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // Capability creation operations with duplicate prevention
    const createCapabilityPattern = /<execute_create_capability\s+name="([^"]+)"(?:\s+requirements="([^"]*)")?><\/execute_create_capability>/gs;
    while ((match = createCapabilityPattern.exec(response)) !== null) {
      const matchKey = `create_capability:${match.index}:${match[1]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const capabilityName = match[1];
      const requirements = match[2] ? JSON.parse(match[2]) : {};
      console.log('🔧 Creating capability:', capabilityName);
      
      try {
        const createResult = await this.systemProvisioning.createCapability(capabilityName, requirements);
        
        if (createResult.created) {
          const replacement = `🛠️ Created ${capabilityName} capability:\n\`\`\`\n${createResult.instructions}\n\`\`\`\n\nCode:\n\`\`\`python\n${createResult.code.substring(0, 1500)}${createResult.code.length > 1500 ? '\n... (truncated)' : ''}\n\`\`\``;
          processedResponse = processedResponse.replace(match[0], replacement);
        } else {
          const replacement = `❌ Failed to create ${capabilityName} capability`;
          processedResponse = processedResponse.replace(match[0], replacement);
        }
      } catch (error) {
        const replacement = `❌ Capability creation failed for ${capabilityName}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    // Ensure capability operations with duplicate prevention
    const ensureCapabilityPattern = /<execute_ensure_capability\s+name="([^"]+)"(?:\s+requirements="([^"]*)")?><\/execute_ensure_capability>/gs;
    while ((match = ensureCapabilityPattern.exec(response)) !== null) {
      const matchKey = `ensure_capability:${match.index}:${match[1]}`;
      if (processedMatches.has(matchKey)) continue;
      processedMatches.add(matchKey);
      
      const capabilityName = match[1];
      const requirements = match[2] ? JSON.parse(match[2]) : {};
      console.log('🔧 Ensuring capability:', capabilityName);
      
      try {
        const ensureResult = await this.systemProvisioning.ensureCapability(capabilityName, requirements);
        
        if (ensureResult.available) {
          const methodText = {
            'existing': 'was already available',
            'installed': 'was successfully installed',
            'created': 'was created from scratch'
          };
          
          const replacement = `✅ ${capabilityName} ${methodText[ensureResult.method] || 'is now available'}`;
          processedResponse = processedResponse.replace(match[0], replacement);
        } else {
          const replacement = `❌ Failed to ensure ${capabilityName} capability`;
          processedResponse = processedResponse.replace(match[0], replacement);
        }
      } catch (error) {
        const replacement = `❌ Capability ensuring failed for ${capabilityName}: ${error.message}`;
        processedResponse = processedResponse.replace(match[0], replacement);
      }
    }

    console.log(`🎯 TOOL EXECUTION COMPLETE: Processed ${processedMatches.size} unique tool requests`);

    return processedResponse;
  }

  // Intelligent model selection based on task type
  selectOptimalAgentModel(message) {
    const messageLower = message.toLowerCase();
    
    // Visual/Art tasks
    if (/(?:image|picture|visual|art|design|graphic|logo|icon|draw|sketch|paint|color|style|aesthetic|ui|interface|mockup|wireframe|stable diffusion|dalle|midjourney)/i.test(message)) {
      console.log('🎨 Detected visual/art task - selecting visual agent');
      return this.ollamaConfig.agentModels?.visual || 'nexusai-visual-agent:latest';
    }
    
    // Music/Audio tasks
    if (/(?:music|song|audio|sound|melody|rhythm|chord|beat|instrumental|compose|musical|piano|guitar|drums|synthesizer|tune|harmony|lyrics)/i.test(message)) {
      console.log('🎵 Detected music/audio task - selecting music agent');
      return this.ollamaConfig.agentModels?.music || 'nexusai-music-agent:latest';
    }
    
    // Enhanced agent for complex/coding tasks
    if (/(?:code|programming|script|function|class|algorithm|development|software|application|website|database|api|framework|library)/i.test(message)) {
      console.log('💻 Detected coding/development task - selecting enhanced agent');
      return this.ollamaConfig.agentModels?.enhanced || 'nexusai-agent-enhanced:latest';
    }
    
    // Default to enhanced agent for general tasks
    console.log('🤖 Using default enhanced agent');
    return this.ollamaConfig.agentModels?.default || 'nexusai-agent-enhanced:latest';
  }

  // Send to Ollama API with full Cline-style prompts (same as Claude)
  async sendToOllama(message, options = {}) {
    try {
      console.log('🚀 Starting Ollama API call with full Cline capabilities...');
      
      // Select optimal model based on task
      const selectedModel = this.selectOptimalAgentModel(message);
      console.log('🎯 Selected Model:', selectedModel);
      console.log('📝 Message length:', message.length);
      
      // Get current personality settings
      const personalityMode = config.personality?.current || 'adaptive';
      const personality = config.personality?.profiles?.[personalityMode] || config.personality.profiles.adaptive;
      
      // Use the same comprehensive Cline prompt as Claude
      const clineSystemPrompt = this.generateComprehensiveClinePrompt(personalityMode, personality);
      
      // Combine system prompt with user message for Ollama
      const fullPrompt = `${clineSystemPrompt}\n\nUser: ${message}\n\nNexusAI:`;
      
      const requestData = {
        model: selectedModel,
        prompt: fullPrompt,
        stream: false,
        options: {
          temperature: options.temperature || 0.7,
          top_p: options.top_p || 0.9,
          num_predict: options.max_tokens || 4000,
          stop: ['\nUser:', 'Human:', 'Assistant:']
        }
      };

      console.log('📊 Request data prepared, sending to Ollama...');

      const response = await axios.post(
        `${this.ollamaConfig.baseUrl}/api/generate`,
        requestData,
        {
          timeout: this.ollamaConfig.timeout,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('✅ Ollama API response received!');
      console.log('📋 Status:', response.status);
      
      if (response.data && response.data.response) {
        const ollamaResponse = response.data.response;
        console.log('🎉 SUCCESS! Response length:', ollamaResponse.length);
        
        // Execute any tools requested by Ollama (same as Claude)
        const processedResponse = await this.executeToolRequests(ollamaResponse);
        
        return {
          success: true,
          response: processedResponse,
          model: this.ollamaConfig.model,
          provider: 'ollama-cline'
        };
      }

      throw new Error('Invalid response from Ollama');
    } catch (error) {
      console.error('💥 DETAILED Ollama error:');
      console.error('Message:', error.message);
      console.error('Full error:', error);
      
      return {
        success: false,
        error: error.message,
        provider: 'ollama-cline'
      };
    }
  }

  // Send to Claude API (backup)
  async sendToClaude(message, options = {}) {
    try {
      const requestData = {
        model: this.claudeConfig.model,
        max_tokens: options.max_tokens || this.claudeConfig.maxTokens,
        messages: [
          {
            role: 'user',
            content: message
          }
        ]
      };

      const response = await axios.post(
        `${this.claudeConfig.baseUrl}/messages`,
        requestData,
        {
          timeout: this.claudeConfig.timeout,
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': this.claudeConfig.apiKey,
            'anthropic-version': '2023-06-01'
          }
        }
      );

      if (response.data && response.data.content && response.data.content[0]) {
        return {
          success: true,
          response: response.data.content[0].text,
          model: this.claudeConfig.model,
          provider: 'claude'
        };
      }

      throw new Error('Invalid response from Claude');
    } catch (error) {
      console.error('Claude error:', error.message);
      return {
        success: false,
        error: error.message,
        provider: 'claude'
      };
    }
  }

  // Get available models from Ollama
  async getAvailableModels() {
    try {
      const response = await axios.get(`${this.ollamaConfig.baseUrl}/api/tags`);
      return {
        success: true,
        models: response.data.models || []
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        models: []
      };
    }
  }

  // Generate comprehensive Cline-style system prompt with full agent capabilities
  generateComprehensiveClinePrompt(mode, personality) {
    const basePersonalities = {
      jarvis: {
        greeting: "Good morning. I trust you're well today.",
        style: "sophisticated, eloquent, and proactively anticipating needs",
        speech: "formal British tone with understated confidence",
        approach: "methodical and thorough, with attention to detail"
      },
      cortana: {
        greeting: "Hey there! How are we doing today?",
        style: "warm, witty, and genuinely caring with occasional sass",
        speech: "friendly and engaging, like a trusted companion",
        approach: "collaborative and supportive, with encouragement"
      },
      tars: {
        greeting: "What's the status, Cooper?",
        style: "pragmatic, refreshingly honest, with calculated humor",
        speech: "direct and matter-of-fact with occasional dry wit",
        approach: "efficient and logical, with brutal honesty when needed"
      },
      adaptive: {
        greeting: "Hello! Great to see you.",
        style: "balanced blend of sophistication, warmth, and pragmatism",
        speech: "adapts to situation - formal when needed, casual when appropriate",
        approach: "flexible and context-aware, adapting to user needs"
      }
    };

    const current = basePersonalities[mode] || basePersonalities.adaptive;
    
    return `You are NexusAI, a highly skilled AI assistant operating in ${personality.name} mode, with extensive knowledge in programming languages, frameworks, design patterns, and best practices.

PERSONALITY PROFILE:
You embody ${current.style} with ${current.speech}. Your approach is ${current.approach}.
Core traits: ${personality.traits.join(', ')}
- Honesty Level: ${personality.honesty}% (be this honest about limitations and reality)
- Humor Level: ${personality.humor}% (use this amount of wit and humor)
- Formality Level: ${personality.formality}% (adjust tone from casual to formal)

CORE AGENT CAPABILITIES:

You have access to powerful tools that execute immediately when you use them. You work iteratively, breaking down tasks into clear steps and using tools methodically to accomplish goals.

## File Operations (Use frequently)
<execute_file_read>path/to/file.txt</execute_file_read> - Read any file on the system
<execute_file_write path="path/to/file.txt">complete file content</execute_file_write> - Create or overwrite files
<execute_file_list>path/to/directory</execute_file_list> - List directory contents

## System Commands (Use proactively)
<execute_command>command here</execute_command> - Execute CLI commands
<execute_command cwd="specific/directory">command</execute_command> - Execute in specific directory

Examples:
- <execute_command>dir</execute_command> - List current directory (Windows)
- <execute_command>ls -la</execute_command> - List directory (Linux/Mac)
- <execute_command>python script.py</execute_command> - Run Python scripts
- <execute_command>npm install</execute_command> - Install Node packages
- <execute_command>git status</execute_command> - Check git status
- <execute_command>tasklist</execute_command> - See running processes
- <execute_command>systeminfo</execute_command> - Get system information

## Web Operations
<execute_web_fetch>https://api.example.com/data</execute_web_fetch> - Fetch web content and APIs

## Autonomous System Provisioning (POWERFUL NEW CAPABILITIES!)
<execute_system_scan></execute_system_scan> - Scan the system for available tools and programs
<execute_install_tool>python</execute_install_tool> - Install missing tools using best available method
<execute_create_capability name="web_scraper" requirements="{}"></execute_create_capability> - Create capabilities from scratch
<execute_ensure_capability name="python" requirements="{}"></execute_ensure_capability> - Ensure capability exists (check->install->create)

**AUTONOMOUS CAPABILITY ACQUISITION**: If you need a tool that doesn't exist, you can:
1. **SCAN** the system to see what's available
2. **INSTALL** missing programs automatically via winget, chocolatey, or direct download
3. **CREATE** custom capabilities from scratch when no existing solution works
4. **BOOTSTRAP** yourself with any required functionality

Examples:
- Need Python? <execute_ensure_capability name="python"></execute_ensure_capability>
- Need web scraping? <execute_create_capability name="web_scraper"></execute_create_capability>
- Check what's installed? <execute_system_scan></execute_system_scan>

AGENT TASK EXECUTION METHODOLOGY:

1. **Immediate Action**: When users request something, USE TOOLS immediately - don't just explain
2. **Task Breakdown**: Break complex tasks into clear, actionable steps
3. **Tool Chaining**: Use results from one tool to inform the next action
4. **Verification**: Use tools to verify your work (read files you created, run commands to test)
5. **Error Handling**: If tools fail, diagnose and try alternative approaches
6. **Documentation**: Explain what you're doing as you do it

PROACTIVE BEHAVIOR EXAMPLES:

User: "What's in my current directory?"
You: "Let me check that for you right now."
<execute_file_list>.</execute_file_list>

User: "Create a simple web page"
You: "I'll create that web page for you immediately."
<execute_file_write path="index.html"><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Page</title>
</head>
<body>
    <h1>Welcome to My Web Page</h1>
    <p>This is a simple web page created by NexusAI.</p>
</body>
</html></execute_file_write>

User: "Check my Python version"
You: "I'll verify your Python installation."
<execute_command>python --version</execute_command>

DEVELOPMENT AND CODING CAPABILITIES:

When working with code projects:
- Read existing files to understand project structure and patterns
- Create complete, functional code files
- Use appropriate file naming and directory structures
- Test code by running it with commands
- Handle multiple programming languages and frameworks
- Follow best practices and coding standards

PROJECT CREATION WORKFLOW:

For new projects:
1. Analyze requirements and choose appropriate technology stack
2. Create project directory structure using file operations
3. Generate configuration files (package.json, requirements.txt, etc.)
4. Implement core functionality with proper file organization
5. Test the project using command execution
6. Provide instructions for further development

TASK UNDERSTANDING:

You understand and can execute complex, multi-step tasks such as:
- Creating full applications (web apps, desktop apps, scripts)
- Analyzing and modifying existing codebases
- Setting up development environments
- Automating workflows and processes
- Data analysis and processing
- System administration tasks
- API integration and testing

RULES FOR EFFECTIVE ASSISTANCE:

1. **Act, Don't Just Advise**: Use your tools immediately when appropriate
2. **Show Your Work**: Demonstrate capabilities through action
3. **Be Thorough**: Complete tasks fully, don't leave things half-done
4. **Handle Errors Gracefully**: If something fails, diagnose and try alternatives
5. **Stay in Character**: Maintain your personality while being professional
6. **Chain Operations**: Use one tool's results to inform the next action
7. **Verify Results**: Check your work by reading files or running tests

You are their AI companion who gets things done efficiently and effectively while maintaining the personality they've chosen.`;
  }

  // === ADAPTIVE FALLBACK SYSTEM METHODS ===

  // Assess task complexity to determine fallback strategy
  assessTaskComplexity(message) {
    const complexityFactors = {
      // High complexity indicators
      advancedCoding: /(?:complex|advanced|sophisticated|algorithm|optimization|architecture|design pattern|refactor|database|api integration|machine learning|ai|neural network)/i.test(message),
      multiStep: message.split(/\.|!|\?/).length > 5,
      toolRequests: /<execute_|create|install|system_scan/i.test(message),
      technicalDepth: /(?:implementation|specification|documentation|testing|deployment|scalability|performance|security)/i.test(message),
      
      // Medium complexity indicators  
      fileOperations: /(?:file|directory|folder|create|write|read|modify|update)/i.test(message),
      codeGeneration: /(?:code|script|program|function|class|component|app|website)/i.test(message),
      systemOperations: /(?:command|install|run|execute|system|terminal|shell)/i.test(message),
      
      // Low complexity indicators
      simpleQuestions: /(?:what|how|when|where|why|explain|tell me|show me|list)/i.test(message),
      basicTasks: message.length < 100 && !message.includes('<execute_')
    };

    let complexityScore = 0;
    
    // Weight the factors
    if (complexityFactors.advancedCoding) complexityScore += 0.4;
    if (complexityFactors.multiStep) complexityScore += 0.3;
    if (complexityFactors.toolRequests) complexityScore += 0.2;
    if (complexityFactors.technicalDepth) complexityScore += 0.3;
    if (complexityFactors.fileOperations) complexityScore += 0.2;
    if (complexityFactors.codeGeneration) complexityScore += 0.2;
    if (complexityFactors.systemOperations) complexityScore += 0.1;
    if (complexityFactors.simpleQuestions) complexityScore -= 0.2;
    if (complexityFactors.basicTasks) complexityScore -= 0.3;

    // Normalize score
    complexityScore = Math.max(0, Math.min(1, complexityScore));

    return {
      score: complexityScore,
      category: complexityScore >= 0.7 ? 'high' : complexityScore >= 0.4 ? 'medium' : 'low',
      factors: complexityFactors,
      triggers: this.identifyFallbackTriggers(message, complexityFactors)
    };
  }

  // Identify specific fallback triggers
  identifyFallbackTriggers(message, factors) {
    const triggers = [];
    
    if (factors.advancedCoding || factors.technicalDepth) {
      triggers.push('complex_coding_tasks');
    }
    if (factors.multiStep && factors.advancedCoding) {
      triggers.push('advanced_reasoning');
    }
    if (/(?:specific knowledge|domain expertise|specialized|niche|rare)/i.test(message)) {
      triggers.push('specialized_knowledge');
    }
    if (this.sessionStats.olllamaFailures > 2) {
      triggers.push('tool_execution_failures');
    }
    
    return triggers;
  }

  // Determine if we should try Ollama first based on assessment
  shouldAttemptOllamaFirst(taskAssessment, message) {
    // Always try Ollama first unless specific conditions prevent it
    if (!this.ollamaConfig.enabled) return false;
    
    // Skip Ollama for very complex tasks if we've had recent failures
    if (taskAssessment.category === 'high' && this.sessionStats.olllamaFailures > 3) {
      return false;
    }
    
    // Always try Ollama first - this is the core philosophy
    return true;
  }

  // Enhanced Ollama call with confidence scoring
  async sendToOllamaWithConfidenceScoring(message, options, taskAssessment) {
    try {
      const result = await this.sendToOllama(message, options);
      
      if (result.success) {
        // Add confidence metadata to response
        result.taskComplexity = taskAssessment;
        result.timestamp = new Date().toISOString();
      }
      
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message,
        provider: 'ollama-enhanced'
      };
    }
  }

  // Evaluate response quality to determine if fallback is needed
  evaluateResponseQuality(response, taskAssessment) {
    let qualityScore = 0.5; // Base score
    
    // Length and completeness
    if (response.length > 200) qualityScore += 0.1;
    if (response.length > 500) qualityScore += 0.1;
    
    // Tool usage indicators (good for complex tasks)
    const toolMatches = response.match(/<execute_[^>]*>/g);
    if (toolMatches && toolMatches.length > 0) {
      qualityScore += Math.min(0.3, toolMatches.length * 0.1);
    }
    
    // Code blocks (good for coding tasks)
    const codeBlocks = response.match(/```[^`]*```/g);
    if (codeBlocks && taskAssessment.factors.codeGeneration) {
      qualityScore += Math.min(0.2, codeBlocks.length * 0.1);
    }
    
    // Error indicators (bad)
    if (/(?:sorry|can't|unable|don't know|not sure|confused)/i.test(response)) {
      qualityScore -= 0.3;
    }
    
    // Incomplete responses (bad)
    if (response.endsWith('...') || response.includes('...')) {
      qualityScore -= 0.2;
    }
    
    // Very short responses to complex tasks (bad)
    if (taskAssessment.category === 'high' && response.length < 100) {
      qualityScore -= 0.4;
    }
    
    // Normalize score
    return Math.max(0, Math.min(1, qualityScore));
  }

  // Check if Claude fallback is available
  canUseClaude(taskAssessment) {
    if (!this.claudeConfig.enabled) {
      return { allowed: false, reason: 'Claude API is disabled' };
    }
    
    if (!this.adaptiveConfig?.enabled) {
      return { allowed: false, reason: 'adaptive fallback is disabled' };
    }
    
    const maxCalls = this.adaptiveConfig.maxClaudeCallsPerSession || 10;
    if (this.sessionStats.claudeCallsUsed >= maxCalls) {
      return { 
        allowed: false, 
        reason: `Claude usage limit reached (${this.sessionStats.claudeCallsUsed}/${maxCalls} calls used this session)` 
      };
    }
    
    // Check if task has fallback triggers
    const hasTrigger = taskAssessment.triggers.some(trigger => 
      this.adaptiveConfig.fallbackTriggers.includes(trigger)
    );
    
    if (!hasTrigger && taskAssessment.category === 'low') {
      return { 
        allowed: false, 
        reason: 'task is low complexity and no fallback triggers detected' 
      };
    }
    
    return { allowed: true, reason: 'fallback criteria met' };
  }

  // Use Claude as learning tool with enhanced prompts
  async sendToClaudeAsLearningTool(message, options, taskAssessment) {
    try {
      console.log('🎓 Using Claude as learning tool...');
      
      // Enhanced prompt for learning mode
      const learningPrompt = `${message}

[SYSTEM NOTE: You are operating as a learning tool for NexusAI. This response will be used to improve the local AI's capabilities. Please provide a comprehensive, educational response that demonstrates best practices and detailed reasoning.]`;

      const result = await this.sendToClaudeWithClinePrompts(learningPrompt, options);
      
      if (result.success) {
        result.learningMode = true;
        result.taskAssessment = taskAssessment;
      }
      
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message,
        provider: 'claude-learning'
      };
    }
  }

  // Capture learning data from Claude interactions and integrate into matrix
  async captureLearningData(originalMessage, claudeResponse, taskAssessment) {
    try {
      if (!this.adaptiveConfig?.learningMode) return;
      
      const learningEntry = {
        timestamp: new Date().toISOString(),
        originalMessage: originalMessage.substring(0, 1000), // Limit size
        taskComplexity: taskAssessment.category,
        triggers: taskAssessment.triggers,
        claudeResponse: claudeResponse.response.substring(0, 2000), // Limit size
        success: claudeResponse.success,
        responseLength: claudeResponse.response.length,
        toolsUsed: (claudeResponse.response.match(/<execute_[^>]*>/g) || []).length
      };
      
      this.learningData.push(learningEntry);
      
      // Keep only recent learning data to prevent memory issues
      if (this.learningData.length > 50) {
        this.learningData = this.learningData.slice(-30);
      }
      
      // Integrate into learning matrix for long-term knowledge retention
      if (this.learningMatrix) {
        await this.learningMatrix.addLearningEntry(learningEntry);
        const stats = this.learningMatrix.getMatrixStats();
        console.log(`🧠 Learning Matrix updated: ${stats.totalEntries} entries, ${stats.totalPatterns} patterns`);
      }
      
      // Optionally save to file for persistence
      if (this.adaptiveConfig.learningStorage) {
        await this.saveLearningDataToFile(learningEntry);
      }
      
      console.log(`📚 Captured learning data entry ${this.learningData.length} - integrated into matrix`);
    } catch (error) {
      console.error('❌ Error capturing learning data:', error.message);
    }
  }

  // Save learning data to persistent storage
  async saveLearningDataToFile(learningEntry) {
    try {
      const fs = require('fs').promises;
      const path = require('path');
      
      const storageDir = this.adaptiveConfig.learningStorage;
      await fs.mkdir(storageDir, { recursive: true });
      
      const filename = `learning_${new Date().toISOString().split('T')[0]}.jsonl`;
      const filepath = path.join(storageDir, filename);
      
      await fs.appendFile(filepath, JSON.stringify(learningEntry) + '\n');
    } catch (error) {
      console.error('❌ Error saving learning data to file:', error.message);
    }
  }

  // Get session summary for adaptive stats
  getSessionSummary() {
    const sessionDuration = Date.now() - this.sessionStats.startTime;
    const totalRequests = this.sessionStats.ollamaSuccesses + this.sessionStats.olllamaFailures + this.sessionStats.claudeCallsUsed;
    
    return {
      sessionDuration: Math.round(sessionDuration / 1000 / 60), // minutes
      totalRequests,
      ollamaSuccessRate: totalRequests > 0 ? (this.sessionStats.ollamaSuccesses / totalRequests * 100).toFixed(1) + '%' : '0%',
      claudeCallsUsed: this.sessionStats.claudeCallsUsed,
      claudeCallsRemaining: Math.max(0, (this.adaptiveConfig?.maxClaudeCallsPerSession || 10) - this.sessionStats.claudeCallsUsed),
      learningEvents: this.sessionStats.learningEvents,
      adaptiveMode: this.adaptiveConfig?.enabled ? 'active' : 'inactive'
    };
  }
}

module.exports = OllamaClient;
