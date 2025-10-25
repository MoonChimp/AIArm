const OllamaClient = require('./src/api/ollamaClient');

async function debugToolExecution() {
    console.log('🔍 DEBUG: Testing tool execution patterns...\n');
    
    const client = new OllamaClient();
    
    // Test various response formats that might come from Ollama
    const testResponses = [
        {
            name: "Standard XML Format",
            response: `I'll create the autosave file for you.
<execute_file_write path="C:\\Users\\moonc\\TylerBeats-App\\autosave.py">
class AutoSaveManager:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
    
    def start(self):
        self.running = True
        print("AutoSave started")
    
    def stop(self):
        self.running = False
        print("AutoSave stopped")
</execute_file_write>

The autosave system has been created successfully.`
        },
        {
            name: "Alternative Format",
            response: `I'll create the autosave functionality:

<execute_file_write path="../TylerBeats-App/autosave.py">
class AutoSaveManager:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
    
    def start(self):
        self.running = True
        print("AutoSave started")
</execute_file_write>

File created successfully.`
        },
        {
            name: "Broken Pattern",
            response: `Creating autosave.py file:

execute_file_write path="C:\\Users\\moonc\\TylerBeats-App\\autosave.py":
class AutoSaveManager:
    def __init__(self):
        pass

Done!`
        }
    ];
    
    for (const test of testResponses) {
        console.log(`\n--- Testing: ${test.name} ---`);
        console.log('Original response length:', test.response.length);
        
        try {
            const processed = await client.executeToolRequests(test.response);
            console.log('Processed response length:', processed.length);
            console.log('Response changed:', test.response !== processed);
            
            if (test.response !== processed) {
                console.log('✅ Tool execution detected and processed');
                console.log('Changes made:\n', processed.substring(0, 200) + '...');
            } else {
                console.log('❌ No tool execution detected - patterns may not match');
            }
        } catch (error) {
            console.error('❌ Error during tool execution:', error.message);
        }
    }
    
    // Test actual file creation
    console.log('\n\n🧪 Testing direct file creation...');
    try {
        const fs = require('fs').promises;
        const path = require('path');
        
        const testPath = '../TylerBeats-App/test-debug-file.txt';
        const testContent = 'This is a test file created by debug script.';
        
        console.log('Creating test file at:', testPath);
        const fullPath = path.resolve(testPath);
        console.log('Full path:', fullPath);
        
        await fs.mkdir(path.dirname(fullPath), { recursive: true });
        await fs.writeFile(fullPath, testContent, 'utf8');
        
        console.log('✅ Direct file creation successful');
        
        // Verify it exists
        const exists = await fs.access(fullPath).then(() => true).catch(() => false);
        console.log('File exists after creation:', exists);
        
        // Clean up
        await fs.unlink(fullPath);
        console.log('Test file cleaned up');
        
    } catch (error) {
        console.error('❌ Direct file creation failed:', error.message);
    }
}

// Run the debug
debugToolExecution().catch(console.error);
