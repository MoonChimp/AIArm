@echo off
color 0A
cls

echo ================================================================================
echo                      AIARM FUNCTIONALITY TEST LAUNCHER                      
echo ================================================================================
echo.
echo This test will verify that the AIArm system can create REAL files and projects
echo with proper persistence and functionality. It will:
echo.
echo 1. Create an actual project with real files
echo 2. Generate HTML, CSS, and JavaScript
echo 3. Store project data in the memory system
echo 4. Verify file creation with size checks
echo 5. Confirm project persistence in projects.json
echo.
echo ================================================================================
echo.
echo Running AIArm Functionality Test...
echo.

python D:\AIArm\MultiAgent\test_functionality.py

echo.
echo ================================================================================
echo                        TEST COMPLETE                                
echo ================================================================================
echo.
echo Now let's verify the database and mobile agent functionality by creating
echo a real database schema and API connection code.
echo.

pause

python D:\AIArm\MultiAgent\test_database_functionality.py

echo.
echo ================================================================================
echo                        ALL TESTS COMPLETE                                
echo ================================================================================

pause
