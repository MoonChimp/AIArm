// Ultra basic server just to get an interface showing
const express = require('express');
const path = require('path');

// Create the app
const app = express();

// Serve static files
app.use(express.static(path.join(__dirname)));

// Route for the homepage
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Basic AIArm Interface</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #0f1525;
          color: #e0e0e0;
          margin: 20px;
        }
        h1 {
          color: #00bfff;
        }
        .container {
          background-color: rgba(0, 0, 0, 0.2);
          border: 1px solid rgba(0, 191, 255, 0.2);
          border-radius: 10px;
          padding: 20px;
          max-width: 800px;
          margin: 0 auto;
        }
        button {
          background-color: #00bfff;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          margin: 10px 0;
        }
        input {
          background-color: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(0, 191, 255, 0.2);
          color: white;
          padding: 10px;
          border-radius: 5px;
          width: 100%;
          margin: 10px 0;
        }
        .status {
          margin-top: 20px;
          padding: 10px;
          border-radius: 5px;
          background-color: rgba(0, 0, 0, 0.3);
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Basic AIArm Interface</h1>
        <p>This is a simple interface to test if the server is working correctly.</p>
        
        <div>
          <input type="text" id="userInput" placeholder="Type a message...">
          <button onclick="sendMessage()">Send</button>
        </div>
        
        <div class="status" id="status">Server status: Connected</div>
        
        <div id="response" style="margin-top: 20px;"></div>
      </div>
      
      <script>
        function sendMessage() {
          const input = document.getElementById('userInput').value;
          const status = document.getElementById('status');
          const response = document.getElementById('response');
          
          if (!input.trim()) return;
          
          status.textContent = 'Server status: Sending request...';
          
          // Simple response - don't even try to access the API
          response.innerHTML = '<p><strong>Input:</strong> ' + input + '</p>' +
                              '<p><strong>Response:</strong> This is a basic test interface. The actual server functionality is not connected.</p>';
          
          status.textContent = 'Server status: Connected';
          document.getElementById('userInput').value = '';
        }
      </script>
    </body>
    </html>
  `);
});

// Start the server
const PORT = 45680;
app.listen(PORT, () => {
  console.log(`Basic server running at http://localhost:${PORT}`);
});
