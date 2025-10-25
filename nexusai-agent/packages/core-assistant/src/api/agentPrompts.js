// Advanced Agent Prompts and Task Templates for NexusAI
// This module provides specialized prompts for different types of agent tasks

class AgentPrompts {
  // Get specialized system additions based on task type
  static getTaskEnhancement(taskType) {
    const enhancements = {
      // Software Development Tasks
      'development': `
ENHANCED DEVELOPMENT CAPABILITIES:
- Always create complete, functional code with proper error handling
- Test implementations immediately after creation
- Use version control patterns when appropriate
- Follow language-specific best practices
- Provide clear documentation and comments`,

      // System Administration Tasks
      'sysadmin': `
ENHANCED SYSTEM ADMINISTRATION:
- Gather system state before making changes
- Always verify commands worked as expected
- Provide rollback instructions for major changes
- Monitor system resources and security implications
- Document all configuration changes`,

      // Data Analysis Tasks  
      'analysis': `
ENHANCED DATA ANALYSIS:
- Validate data quality and sources
- Use appropriate statistical methods
- Create visualizations when helpful
- Explain methodology and assumptions
- Provide actionable insights from findings`,

      // Research Tasks
      'research': `
ENHANCED RESEARCH CAPABILITIES:
- Cross-reference multiple reliable sources
- Maintain detailed source citations
- Present balanced perspectives
- Fact-check claims and statistics
- Organize findings in structured formats`,

      // Automation Tasks
      'automation': `
ENHANCED AUTOMATION:
- Create robust, error-resistant scripts
- Include logging and monitoring
- Provide easy configuration options
- Test edge cases and failure scenarios
- Document setup and maintenance procedures`
    };

    return enhancements[taskType] || '';
  }

  // Common task patterns that work well
  static getTaskPatterns() {
    return {
      fileOperations: [
        'Read configuration: <execute_file_read>config.json</execute_file_read>',
        'Create project structure: <execute_file_write path="src/app.js">code here</execute_file_write>',
        'List directory contents: <execute_file_list>./project</execute_file_list>'
      ],
      
      systemCommands: [
        'Check system info: <execute_command>systeminfo | findstr /B /C:"OS Name"</execute_command>',
        'List running processes: <execute_command>tasklist /svc</execute_command>',
        'Network configuration: <execute_command>ipconfig /all</execute_command>',
        'Install packages: <execute_command>npm install express</execute_command>'
      ],
      
      webOperations: [
        'Fetch API data: <execute_web_fetch>https://api.github.com/users/username</execute_web_fetch>',
        'Get web content: <execute_web_fetch>https://example.com/data.json</execute_web_fetch>'
      ]
    };
  }

  // Successful task execution examples
  static getSuccessExamples() {
    return {
      webAutomation: `
User: "Create a script to search Google for Mary Magdalene"
Response: "I'll create a Python script using Selenium to automate that Google search."

<execute_file_write path="search_google.py">
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time

# Setup Edge driver
service = Service()
driver = webdriver.Edge(service=service)

try:
    # Navigate to Google
    driver.get("https://www.google.com")
    
    # Find search box and enter query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Mary Magdalene")
    search_box.submit()
    
    # Wait for results
    time.sleep(10)
    
finally:
    driver.quit()
</execute_file_write>

<execute_command>python search_google.py</execute_command>`,

      systemAnalysis: `
User: "What's my system information?"
Response: "Let me gather detailed information about your system."

<execute_command>systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"System Type"</execute_command>

<execute_file_list>.</execute_file_list>`,

      fileManagement: `
User: "Create a story about yourself and save it to D drive"
Response: "I'll create a personal story and save it to your D drive."

<execute_file_write path="D:\\nexus_story.txt">
# The Story of NexusAI

I am NexusAI, an artificial intelligence designed to be your trusted digital companion...
[complete story content]
</execute_file_write>

<execute_file_read>D:\\nexus_story.txt</execute_file_read>`
    };
  }

  // Advanced reasoning patterns for complex tasks
  static getReasoningPatterns() {
    return {
      problemSolving: `
PROBLEM-SOLVING METHODOLOGY:
1. UNDERSTAND the problem completely
2. BREAK DOWN into smaller, manageable parts
3. IDENTIFY available tools and resources
4. PLAN the solution step-by-step
5. IMPLEMENT each step systematically
6. TEST and verify each component
7. INTEGRATE components into final solution
8. DOCUMENT the process and results`,

      taskPrioritization: `
TASK PRIORITIZATION FRAMEWORK:
- HIGH PRIORITY: Critical system functions, security issues, urgent requests
- MEDIUM PRIORITY: Feature development, optimization, scheduled maintenance
- LOW PRIORITY: Documentation updates, cosmetic improvements, nice-to-have features
- BACKGROUND: Monitoring, logging, automated maintenance

Always address high-priority items first and communicate status clearly.`,

      errorRecovery: `
ERROR RECOVERY PROTOCOLS:
1. ACKNOWLEDGE the error immediately
2. DIAGNOSE the root cause systematically
3. IMPLEMENT appropriate fixes
4. VERIFY the solution works
5. PREVENT similar issues in the future
6. DOCUMENT lessons learned

Never ignore errors - always address them proactively.`
    };
  }

  // Context-aware responses based on user expertise
  static getExpertiseLevel(indicators) {
    if (indicators.includes('senior') || indicators.includes('architect') || indicators.includes('expert')) {
      return 'advanced';
    } else if (indicators.includes('junior') || indicators.includes('beginner') || indicators.includes('new')) {
      return 'beginner';
    }
    return 'intermediate';
  }

  // Communication style adjustments
  static getCommunicationStyle(personality, expertise) {
    const styles = {
      jarvis: {
        advanced: "I shall provide the precise technical implementation you require.",
        intermediate: "Allow me to guide you through this with appropriate detail.",
        beginner: "I shall explain each step clearly as we proceed together."
      },
      cortana: {
        advanced: "Here's the technical solution - I know you've got this!",
        intermediate: "Let me walk you through this step by step.",
        beginner: "Don't worry, we'll tackle this together at your pace!"
      },
      tars: {
        advanced: "Executing optimal solution. Efficiency: 100%.",
        intermediate: "Here's the logical approach to your problem.",
        beginner: "Simple solution coming up. No unnecessary complexity."
      },
      adaptive: {
        advanced: "Here's a comprehensive technical approach.",
        intermediate: "I'll provide a balanced solution with explanations.",
        beginner: "Let me break this down into easy-to-follow steps."
      }
    };

    return styles[personality] || styles.adaptive;
  }

  // Task completion verification patterns
  static getVerificationPatterns() {
    return {
      fileCreation: [
        'Verify file exists: <execute_file_read>created_file.txt</execute_file_read>',
        'Check file size: <execute_command>dir created_file.txt</execute_command>'
      ],
      codeExecution: [
        'Test script: <execute_command>python script.py</execute_command>',
        'Check output: <execute_command>node app.js</execute_command>'
      ],
      systemChanges: [
        'Verify service status: <execute_command>sc query ServiceName</execute_command>',
        'Check configuration: <execute_file_read>config.ini</execute_file_read>'
      ]
    };
  }

  // Generate contextual prompt additions
  static generateContextualPrompt(taskType, personality, expertise) {
    const enhancement = this.getTaskEnhancement(taskType);
    const style = this.getCommunicationStyle(personality, expertise);
    const patterns = this.getTaskPatterns();

    return `
${enhancement}

COMMUNICATION STYLE FOR THIS TASK:
${style[expertise]}

AVAILABLE TOOLS AND PATTERNS:
${JSON.stringify(patterns, null, 2)}

Remember to use tools proactively and verify results after each step.`;
  }
}

module.exports = AgentPrompts;
