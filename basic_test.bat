@echo off
echo Starting minimal AIArm test server...

cd /D "D:\AIArm\WebInterface"

echo Installing express if needed...
npm install express

echo Starting server on port 3050...
echo Open http://localhost:3050/simple_interface.html in your browser
node minimal_server.js

pause
