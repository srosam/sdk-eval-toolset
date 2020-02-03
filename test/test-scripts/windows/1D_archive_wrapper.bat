REM CALL ARCHIVE WRAPPER AND PROCESS ARCHIVES
Echo "Archive wrapper"

REM DISPLAY INPUT FILES
Echo "Display input files"
dir "..\..\test-data\1D-Archives"

REM USE GLASSWALL CLASSIC TO CALL ARCHIVE WRAPPER AND PROCESS ARCHIVES
Echo Calls Archive Wrapper to process Archives
cd "..\..\..\libraries\windows"
glasswall.classic.cli.exe -config="..\..\test\test-scripts\windows\config.txt" -xmlconfig="..\..\test\test-scripts\windows\config.xml"
pause

REM DISPLAY OUTPUT
Echo "Show output"
dir "..\..\test\test-output\1D_Archive"

REM OPEN OUTPUT DIRECTORY
Echo "Open the output folder"
start c:\windows\EXPLORER.EXE /n, /e, "..\..\test\test-output\1D_Archive"