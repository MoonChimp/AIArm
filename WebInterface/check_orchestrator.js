const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Path to Python orchestrator
const ORCHESTRATOR_PATH = path.join(__dirname, '..', 'MultiAgent', 'enhanced_orchestrator.py');

// Check if orchestrator exists
const orchestratorExists = fs.existsSync(ORCHESTRATOR_PATH);
console.log(`Orchestrator ${orchestratorExists ? 'found' : 'NOT FOUND'} at: ${ORCHESTRATOR_PATH}`);

// Try to get info about the orchestrator
if (orchestratorExists) {
    console.log('Checking orchestrator capabilities...');
    
    try {
        // First, check if Python is available
        const pythonCheck = spawn('python', ['--version']);
        
        pythonCheck.on('error', (err) => {
            console.error('Failed to execute Python. Make sure Python is installed and in your PATH.');
            console.error('Error:', err.message);
        });
        
        pythonCheck.on('close', (code) => {
            if (code === 0) {
                console.log('Python is available. Checking orchestrator...');
                
                // Now try to import the orchestrator to see if it works
                const testFile = path.join(__dirname, 'test_orchestrator.py');
                
                // Create a simple test script
                fs.writeFileSync(testFile, `
import sys
import os

try:
    # Get the directory of the orchestrator
    orchestrator_dir = os.path.dirname('${ORCHESTRATOR_PATH.replace(/\\/g, '\\\\')}')
    
    # Add the directory to the Python path
    sys.path.append(orchestrator_dir)
    
    # Try to import the orchestrator module
    import enhanced_orchestrator
    
    # Print information about the orchestrator
    print("SUCCESS: Orchestrator module loaded")
    print(f"Functions: {dir(enhanced_orchestrator)}")
    
    # Try to create an instance
    try:
        orchestrator = enhanced_orchestrator.EnhancedOrchestrator()
        print("SUCCESS: Created orchestrator instance")
        
        # Try to process input
        try:
            result = orchestrator.process_input("hello", "orchestrator")
            print(f"SUCCESS: Processed input, result: {result}")
        except Exception as e:
            print(f"ERROR: Could not process input: {e}")
    except Exception as e:
        print(f"ERROR: Could not create orchestrator instance: {e}")
except Exception as e:
    print(f"ERROR: Could not import orchestrator module: {e}")
`);
                
                // Execute the test script
                const orchestratorTest = spawn('python', [testFile]);
                
                orchestratorTest.stdout.on('data', (data) => {
                    console.log(`Orchestrator test output: ${data}`);
                });
                
                orchestratorTest.stderr.on('data', (data) => {
                    console.error(`Orchestrator test error: ${data}`);
                });
                
                orchestratorTest.on('close', (code) => {
                    console.log(`Orchestrator test exited with code ${code}`);
                    
                    // Clean up test file
                    fs.unlinkSync(testFile);
                });
            }
        });
    } catch (error) {
        console.error('Error testing orchestrator:', error);
    }
}
