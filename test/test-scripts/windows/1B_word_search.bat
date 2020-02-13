REM WORD SEARCH
Echo "Word search"

REM DISPLAY INPUT FILE
Echo "Display input files"
dir "..\..\test-data\1B-Word_Search\"
pause

REM DISPLAY CONTENT MANAGEMENT CONFIG
Echo "Content management configuration"
cd "..\..\..\libraries\windows\dws_lib"
type .\config.xml
pause

REM DISPLAY CLI CONFIG
Echo "CLI Configuration"
type .\config.txt
pause

REM DISPLAY HOMOGLYPHS MAP
Echo "Homoglyph mapping"
notepad.exe .\homoglyphs.json
pause

REM RUN GLASSWALL WORD SEARCH AND REDACT
Echo "Run Glasswall word search and redact"
glasswall.wordsearch.cli.exe -config=.\config.txt -xmlconfig=.\config.xml >log_wordsearch.log

REM SHOW FILES IN OUTPUT DIRECTORY
Echo "Files in output directory"
dir "..\..\..\test\test-output\1B\Managed"
pause