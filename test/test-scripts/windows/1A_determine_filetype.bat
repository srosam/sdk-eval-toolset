REM CALL DETERMINE FILE TYPE API AND PROCESS EXTENSION-LESS FILES
Echo "Determine file type"

REM DISPLAY INPUT FILES
Echo "Display input files"
dir "..\..\test-data\1A-Determine_file_type"

REM USE PYTHON SDK WRAPPER TO DIRECTLY CALL THE DETERMINE FILE TYPE API AND PRINT TYPE ENUM VALUE AND CORRESPONDING FILE TYPE
Echo "Calls determine file type using core 2 Python SDK Wrapper (Display file type enum value and file type)"
cd "..\..\..\libraries\windows"
python determine-file-type.py "..\..\test\test-data\1A-Determine_file_type" glasswall_core2.dll 2> log_determine_file_type_sdk_wrapper.log
pause

REM PROCESS FILES 
Echo "Run Glasswall on extension-less input files"
GWQtCLI -i "..\..\test\test-data\1A-Determine_file_type" -o "..\..\test\test-output\1A" 2> log_determine_file_type.log

REM DISPLAY OUTPUT
Echo "Show output"
dir "..\..\test\test-output\1A"

REM OPEN OUTPUT DIRECTORY
Echo "Open the output folder"
start "c:\windows\EXPLORER.EXE /n, /e, ..\..\test-output\1A"
pause