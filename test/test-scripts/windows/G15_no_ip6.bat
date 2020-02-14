REM CHECK THAT GLASSWALL RUNS WITH IP6 DISABLED
Echo "Run with ip6 disabled (This needs to be done before running this script)"

REM CONFIRM IP6 NOT RUNNING
Echo "Check no ip6 addresses in use (only ip4 addresses shown)"
ipconfig
pause

REM DISPALY INPUT
Echo "Show output"
dir "..\..\test\test-output\1D-All_File_Types"
pause

REM RUN GLASSWALL INVOKING ALL CAMERAS USING SHOW PROCESSING
Echo "Run Glasswall to process all filetypes"
GWQtCLI -i "..\..\test\test-data\1D-All_File_Types" -o "..\..\test\test-output\G15" 2> log_no_ip6.log

REM DISPLAY OUTPUT
Echo "Show output"
dir "..\..\test\test-output\G15"

REM OPEN OUTPUT DIRECTORY
Echo "Open the output folder"
start "c:\windows\EXPLORER.EXE /n, /e, ..\..\test\test-output\G15"
pause