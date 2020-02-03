
REM --- Process all supported files in the input directory.
Echo "Run all files with default policy settings"

REM --- List all the files in the input directory
dir "..\..\test-data\1D-All_File_Types"
pause
cd "..\..\..\libraries\windows"
GWQtCLI -i "..\..\test\test-data\1D-All_File_Types" -o "..\..\test\test-output\1D" 2> log_process_all_files.txt

REM --- List all the files in the output directory
dir "..\..\test\test-output\1D"

REM --- Show ouput directory
start c:\windows\EXPLORER.EXE /n, /e, ..\..\test\test-output\1D