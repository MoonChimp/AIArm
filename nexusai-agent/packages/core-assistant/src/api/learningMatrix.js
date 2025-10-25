const fs = require('fs').promises;
const path = require('path');

class LearningMatrix {
  constructor(storageDir = './learning_data') {
    this.storageDir = storageDir;
    this.matrix = {
      patterns: new Map(),
      responses: new Map(),
      contexts: new Map(),
      behaviors: new Map(),
      toolUsage: new Map()
    };
    this.loadedEntries = 0;
    this.initialized = false;
    
    console.log('🧠 Learning Matrix initialized');
  }

  async initialize() {
    try {
      await fs.mkdir(this.storageDir, { recursive: true });
      await this.loadExistingMatrix();
      this.initialized = true;
      console.log(`✅ Learning Matrix loaded with ${this.loadedEntries} entries`);
    } catch (error) {
      console.error('❌ Failed to initialize Learning Matrix:', error.message);
    }
  }

  async loadExistingMatrix() {
    try {
      const files = await fs.readdir(this.storageDir);
      const learningFiles = files.filter(f => f.startsWith('learning_') && f.endsWith('.jsonl'));
      
      for (const file of learningFiles) {
        const filePath = path.join(this.storageDir, file);
        const content = await fs.readFile(filePath, 'utf8');
        const lines = content.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
          try {
            const entry = JSON.parse(line);
            await this.integrateEntry(entry);
            this.loadedEntries++;
          } catch (error) {
            console.warn('⚠️ Skipped malformed learning entry:', error.message);
          }
        }
      }
      
      // Load consolidated matrix file if exists
      const matrixPath = path.join(this.storageDir, 'consolidated_matrix.json');
      try {
        const matrixContent = await fs.readFile(matrixPath, 'utf8');
        const savedMatrix = JSON.parse(matrixContent);
        this.mergeMatrix(savedMatrix);
        console.log('📊 Loaded consolidated matrix');
      } catch (error) {
        // No consolidated matrix yet, that's okay
      }
    } catch (error) {
      console.warn('⚠️ Could not load existing matrix:', error.message);
    }
  }

  async integrateEntry(entry) {
    if (!entry || !entry.originalMessage || !entry.claudeResponse) return;
    
    // Extract key patterns from the original message
    const patterns = this.extractPatterns(entry.originalMessage);
    
    // Analyze Claude's response for successful strategies
    const responseAnalysis = this.analyzeResponse(entry.claudeResponse);
    
    // Extract tool usage patterns
    const toolPattern = this.extractToolUsage(entry.claudeResponse);
    
    // Store patterns with success metrics
    for (const pattern of patterns) {
      if (!this.matrix.patterns.has(pattern)) {
        this.matrix.patterns.set(pattern, {
          count: 0,
          successfulResponses: [],
          contexts: [],
          averageComplexity: 0
        });
      }
      
      const patternData = this.matrix.patterns.get(pattern);
      patternData.count++;
      patternData.successfulResponses.push({
        response: entry.claudeResponse.substring(0, 500),
        complexity: entry.taskComplexity,
        tools: toolPattern,
        timestamp: entry.timestamp
      });
      patternData.contexts.push(entry.taskComplexity);
    }
    
    // Store successful response strategies
    for (const strategy of responseAnalysis.strategies) {
      if (!this.matrix.responses.has(strategy.type)) {
        this.matrix.responses.set(strategy.type, {
          examples: [],
          effectiveness: 0,
          contexts: []
        });
      }
      
      const responseData = this.matrix.responses.get(strategy.type);
      responseData.examples.push(strategy.example);
      responseData.effectiveness += strategy.quality;
      responseData.contexts.push(entry.taskComplexity);
    }
    
    // Store tool usage patterns
    if (toolPattern.tools.length > 0) {
      const toolKey = toolPattern.tools.join('+');
      if (!this.matrix.toolUsage.has(toolKey)) {
        this.matrix.toolUsage.set(toolKey, {
          frequency: 0,
          contexts: [],
          successRate: 0
        });
      }
      
      const toolData = this.matrix.toolUsage.get(toolKey);
      toolData.frequency++;
      toolData.contexts.push(entry.taskComplexity);
      toolData.successRate += entry.success ? 1 : 0;
    }

    // Store behavioral patterns
    const behavior = this.extractBehavior(entry.claudeResponse);
    if (behavior) {
      if (!this.matrix.behaviors.has(behavior.type)) {
        this.matrix.behaviors.set(behavior.type, {
          examples: [],
          effectiveness: 0,
          frequency: 0
        });
      }
      
      const behaviorData = this.matrix.behaviors.get(behavior.type);
      behaviorData.examples.push(behavior.example);
      behaviorData.effectiveness += behavior.quality;
      behaviorData.frequency++;
    }
  }

  extractPatterns(message) {
    const patterns = [];
    
    // Task type patterns
    if (/create|build|make|generate/i.test(message)) patterns.push('creation_task');
    if (/fix|debug|solve|repair/i.test(message)) patterns.push('problem_solving');
    if (/explain|describe|how|what|why/i.test(message)) patterns.push('explanation_request');
    if (/analyze|review|examine|check/i.test(message)) patterns.push('analysis_task');
    if (/install|setup|configure/i.test(message)) patterns.push('setup_task');
    
    // Domain patterns
    if (/code|programming|script|function/i.test(message)) patterns.push('coding_domain');
    if (/file|directory|folder|path/i.test(message)) patterns.push('file_operations');
    if (/web|website|html|css|javascript/i.test(message)) patterns.push('web_development');
    if (/data|database|sql|json/i.test(message)) patterns.push('data_handling');
    if (/system|command|terminal|shell/i.test(message)) patterns.push('system_operations');
    
    // Complexity patterns
    if (message.length > 200) patterns.push('complex_request');
    if (message.includes('step by step')) patterns.push('detailed_process');
    if (message.includes('automatically')) patterns.push('automation_request');
    
    return patterns;
  }

  analyzeResponse(response) {
    const strategies = [];
    
    // Tool usage strategy
    const toolMatches = response.match(/<execute_[^>]*>/g);
    if (toolMatches && toolMatches.length > 0) {
      strategies.push({
        type: 'tool_usage',
        example: toolMatches[0],
        quality: Math.min(1.0, toolMatches.length * 0.2)
      });
    }
    
    // Code generation strategy
    const codeBlocks = response.match(/```[\s\S]*?```/g);
    if (codeBlocks && codeBlocks.length > 0) {
      strategies.push({
        type: 'code_generation',
        example: codeBlocks[0].substring(0, 200),
        quality: Math.min(1.0, codeBlocks.length * 0.3)
      });
    }
    
    // Step-by-step approach
    if (/step \d+|first|then|next|finally/i.test(response)) {
      strategies.push({
        type: 'step_by_step',
        example: response.match(/(?:step \d+|first|then|next|finally)[^.]*\./i)?.[0] || '',
        quality: 0.8
      });
    }
    
    // Explanation strategy
    if (/explanation|because|reason|this is|here's why/i.test(response)) {
      strategies.push({
        type: 'explanation_focused',
        example: response.match(/(?:explanation|because|reason|this is|here's why)[^.]*\./i)?.[0] || '',
        quality: 0.6
      });
    }
    
    // Verification strategy
    if (/test|verify|check|ensure|confirm/i.test(response)) {
      strategies.push({
        type: 'verification_included',
        example: response.match(/(?:test|verify|check|ensure|confirm)[^.]*\./i)?.[0] || '',
        quality: 0.7
      });
    }
    
    return { strategies };
  }

  extractToolUsage(response) {
    const tools = [];
    const matches = response.match(/<execute_([^>]*?)>/g);
    
    if (matches) {
      for (const match of matches) {
        const toolName = match.match(/<execute_([^>\s]*)/)?.[1];
        if (toolName && !tools.includes(toolName)) {
          tools.push(toolName);
        }
      }
    }
    
    return {
      tools,
      count: matches ? matches.length : 0,
      pattern: tools.join(' -> ')
    };
  }

  extractBehavior(response) {
    // Proactive behavior
    if (/let me|i'll|i will|immediately/i.test(response)) {
      return {
        type: 'proactive',
        example: response.match(/(?:let me|i'll|i will|immediately)[^.]*\./i)?.[0] || '',
        quality: 0.8
      };
    }
    
    // Thorough behavior
    if (/complete|comprehensive|detailed|thorough/i.test(response)) {
      return {
        type: 'thorough',
        example: response.match(/(?:complete|comprehensive|detailed|thorough)[^.]*\./i)?.[0] || '',
        quality: 0.7
      };
    }
    
    // Error handling behavior
    if (/error|fail|try|catch|fallback/i.test(response)) {
      return {
        type: 'error_handling',
        example: response.match(/(?:error|fail|try|catch|fallback)[^.]*\./i)?.[0] || '',
        quality: 0.6
      };
    }
    
    return null;
  }

  async queryMatrix(message, context = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const patterns = this.extractPatterns(message);
    const recommendations = {
      suggestedApproach: [],
      recommendedTools: [],
      behaviorGuidance: [],
      confidenceLevel: 0
    };
    
    let totalConfidence = 0;
    let relevantPatterns = 0;
    
    // Find matching patterns and their successful strategies
    for (const pattern of patterns) {
      if (this.matrix.patterns.has(pattern)) {
        const patternData = this.matrix.patterns.get(pattern);
        relevantPatterns++;
        
        // Get most successful responses for this pattern
        const topResponses = patternData.successfulResponses
          .sort((a, b) => (b.tools?.count || 0) - (a.tools?.count || 0))
          .slice(0, 3);
        
        for (const response of topResponses) {
          recommendations.suggestedApproach.push({
            pattern,
            approach: response.response,
            confidence: Math.min(1.0, patternData.count / 10),
            tools: response.tools
          });
          totalConfidence += Math.min(1.0, patternData.count / 10);
        }
      }
    }
    
    // Find recommended tool combinations
    const contextComplexity = context.complexity || 'medium';
    for (const [toolCombo, data] of this.matrix.toolUsage.entries()) {
      if (data.contexts.includes(contextComplexity) || data.frequency > 5) {
        recommendations.recommendedTools.push({
          tools: toolCombo.split('+'),
          frequency: data.frequency,
          successRate: data.successRate / data.frequency,
          confidence: Math.min(1.0, data.frequency / 10)
        });
      }
    }
    
    // Sort recommendations by effectiveness
    recommendations.recommendedTools.sort((a, b) => 
      (b.successRate * b.frequency) - (a.successRate * a.frequency)
    );
    
    // Find behavioral guidance
    for (const [behaviorType, data] of this.matrix.behaviors.entries()) {
      if (data.frequency > 3) {
        recommendations.behaviorGuidance.push({
          type: behaviorType,
          example: data.examples[data.examples.length - 1],
          effectiveness: data.effectiveness / data.frequency,
          confidence: Math.min(1.0, data.frequency / 10)
        });
      }
    }
    
    recommendations.confidenceLevel = relevantPatterns > 0 ? totalConfidence / relevantPatterns : 0;
    
    return recommendations;
  }

  async enhancePrompt(basePrompt, message, context = {}) {
    const recommendations = await this.queryMatrix(message, context);
    
    if (recommendations.confidenceLevel < 0.3) {
      return basePrompt; // Not enough learned data to enhance
    }
    
    let enhancement = '\n\n=== LEARNED BEHAVIORS FROM CLAUDE MATRIX ===\n';
    
    // Add successful approach patterns
    if (recommendations.suggestedApproach.length > 0) {
      enhancement += '\nSuccessful approaches for similar tasks:\n';
      for (const approach of recommendations.suggestedApproach.slice(0, 2)) {
        enhancement += `- Pattern "${approach.pattern}": ${approach.approach.substring(0, 150)}...\n`;
      }
    }
    
    // Add recommended tools
    if (recommendations.recommendedTools.length > 0) {
      enhancement += '\nRecommended tool combinations:\n';
      for (const toolRec of recommendations.recommendedTools.slice(0, 3)) {
        enhancement += `- Tools: ${toolRec.tools.join(' + ')} (success rate: ${(toolRec.successRate * 100).toFixed(1)}%)\n`;
      }
    }
    
    // Add behavioral guidance
    if (recommendations.behaviorGuidance.length > 0) {
      enhancement += '\nEffective behaviors:\n';
      for (const behavior of recommendations.behaviorGuidance.slice(0, 2)) {
        enhancement += `- ${behavior.type}: ${behavior.example.substring(0, 100)}...\n`;
      }
    }
    
    enhancement += `\nMatrix confidence: ${(recommendations.confidenceLevel * 100).toFixed(1)}%\n`;
    enhancement += '=== END LEARNED BEHAVIORS ===\n\n';
    
    return basePrompt + enhancement;
  }

  async addLearningEntry(entry) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    await this.integrateEntry(entry);
    
    // Save to daily learning file
    const filename = `learning_${new Date().toISOString().split('T')[0]}.jsonl`;
    const filepath = path.join(this.storageDir, filename);
    
    try {
      await fs.appendFile(filepath, JSON.stringify(entry) + '\n');
    } catch (error) {
      console.error('❌ Failed to save learning entry:', error.message);
    }
    
    // Periodically consolidate the matrix
    if (this.loadedEntries % 50 === 0) {
      await this.consolidateMatrix();
    }
  }

  async consolidateMatrix() {
    try {
      const consolidatedPath = path.join(this.storageDir, 'consolidated_matrix.json');
      
      // Convert Maps to Objects for JSON serialization
      const matrixData = {
        patterns: Object.fromEntries(this.matrix.patterns),
        responses: Object.fromEntries(this.matrix.responses),
        contexts: Object.fromEntries(this.matrix.contexts),
        behaviors: Object.fromEntries(this.matrix.behaviors),
        toolUsage: Object.fromEntries(this.matrix.toolUsage),
        metadata: {
          totalEntries: this.loadedEntries,
          lastUpdate: new Date().toISOString(),
          version: '1.0'
        }
      };
      
      await fs.writeFile(consolidatedPath, JSON.stringify(matrixData, null, 2));
      console.log('📊 Matrix consolidated and saved');
    } catch (error) {
      console.error('❌ Failed to consolidate matrix:', error.message);
    }
  }

  mergeMatrix(savedMatrix) {
    if (!savedMatrix) return;
    
    // Merge patterns
    if (savedMatrix.patterns) {
      for (const [key, value] of Object.entries(savedMatrix.patterns)) {
        if (!this.matrix.patterns.has(key)) {
          this.matrix.patterns.set(key, value);
        } else {
          // Merge existing data
          const existing = this.matrix.patterns.get(key);
          existing.count += value.count;
          existing.successfulResponses.push(...value.successfulResponses);
          existing.contexts.push(...value.contexts);
        }
      }
    }
    
    // Merge other matrix components similarly
    ['responses', 'behaviors', 'toolUsage'].forEach(component => {
      if (savedMatrix[component]) {
        for (const [key, value] of Object.entries(savedMatrix[component])) {
          if (!this.matrix[component].has(key)) {
            this.matrix[component].set(key, value);
          }
        }
      }
    });
  }

  getMatrixStats() {
    return {
      totalPatterns: this.matrix.patterns.size,
      totalResponses: this.matrix.responses.size,
      totalBehaviors: this.matrix.behaviors.size,
      totalToolCombos: this.matrix.toolUsage.size,
      totalEntries: this.loadedEntries,
      initialized: this.initialized
    };
  }
}

module.exports = LearningMatrix;
