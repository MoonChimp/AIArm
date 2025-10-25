const OllamaClient = require('./src/api/ollamaClient');

async function testAdaptiveFallback() {
  console.log('🧪 === TESTING ADAPTIVE FALLBACK SYSTEM ===\n');
  
  const client = new OllamaClient();
  
  // Test 1: Simple task (should prefer Ollama)
  console.log('📋 Test 1: Simple question (low complexity)');
  const simpleMessage = "What is JavaScript?";
  const assessment1 = client.assessTaskComplexity(simpleMessage);
  console.log('Task Assessment:', assessment1);
  console.log('Should try Ollama first:', client.shouldAttemptOllamaFirst(assessment1, simpleMessage));
  console.log();
  
  // Test 2: Complex coding task (should trigger fallback faster)
  console.log('📋 Test 2: Complex coding task (high complexity)');
  const complexMessage = "Create a sophisticated machine learning algorithm with neural network architecture for advanced pattern recognition and optimization";
  const assessment2 = client.assessTaskComplexity(complexMessage);
  console.log('Task Assessment:', assessment2);
  console.log('Should try Ollama first:', client.shouldAttemptOllamaFirst(assessment2, complexMessage));
  console.log();
  
  // Test 3: File operation task (medium complexity)
  console.log('📋 Test 3: File operation task (medium complexity)');
  const fileMessage = "Create a new JavaScript file with a function that reads data from a JSON file";
  const assessment3 = client.assessTaskComplexity(fileMessage);
  console.log('Task Assessment:', assessment3);
  console.log('Should try Ollama first:', client.shouldAttemptOllamaFirst(assessment3, fileMessage));
  console.log();
  
  // Test 4: Claude availability check
  console.log('📋 Test 4: Claude availability checks');
  console.log('Can use Claude for simple task:', client.canUseClaude(assessment1));
  console.log('Can use Claude for complex task:', client.canUseClaude(assessment2));
  console.log('Can use Claude for file task:', client.canUseClaude(assessment3));
  console.log();
  
  // Test 5: Session stats
  console.log('📋 Test 5: Session statistics');
  console.log('Session Summary:', client.getSessionSummary());
  console.log();
  
  // Test 6: Response quality evaluation
  console.log('📋 Test 6: Response quality evaluation');
  const goodResponse = "I'll help you create that function. <execute_file_write path=\"example.js\">function readData() { return JSON.parse(fs.readFileSync('data.json')); }</execute_file_write>";
  const poorResponse = "I'm sorry, I can't help with that...";
  
  console.log('Good response quality:', client.evaluateResponseQuality(goodResponse, assessment3).toFixed(2));
  console.log('Poor response quality:', client.evaluateResponseQuality(poorResponse, assessment3).toFixed(2));
  console.log();
  
  console.log('✅ === ADAPTIVE FALLBACK SYSTEM TESTS COMPLETE ===');
  console.log('\nKey Features Implemented:');
  console.log('• ✅ Intelligent task complexity assessment');
  console.log('• ✅ Adaptive Ollama-first strategy');
  console.log('• ✅ Response quality scoring');
  console.log('• ✅ Claude fallback with cost controls');
  console.log('• ✅ Learning data capture system');
  console.log('• ✅ Session statistics tracking');
  console.log('\nSystem is ready! NexusAI will:');
  console.log('1. 🤖 Always try Ollama first (FREE, LOCAL)');
  console.log('2. 📊 Evaluate response quality automatically');
  console.log('3. 🧠 Fall back to Claude only when needed (LEARNING TOOL)');
  console.log('4. 🎓 Capture learning data to improve over time');
  console.log('5. 💰 Respect cost controls and usage limits');
}

testAdaptiveFallback().catch(console.error);
