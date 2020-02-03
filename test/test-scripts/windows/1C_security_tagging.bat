REM --- TAG FILES IN SPECIFIED INPUT DIRECTORY
Echo "Tag files in input directory with the following information"

REM --- DISPLAY INFORMATION THAT WILL INSERTED IN EACH FILE
type .\tags.xml
pause

cd "..\..\..\libraries\windows"
GWQtCLI -i "..\..\test\test-data\1C-Security_Tags" -o "..\..\test\test-output\1C" -t "..\..\test\test-scripts\windows\tags.xml" 2> log_tag_files.txt

REM --- SHOW FILES IN INPUT AND OUTPUT DIRECTORIES AFTER TAGGING THE FILES
dir "..\..\test\test-data\1C-Security_Tags"
dir "..\..\test\test-output\1C"

Echo "Open output location"
start c:\windows\EXPLORER.EXE /n, /e, ..\..\test\test-output\1C

REM --- RETRIEVE TAGS FROM TAGGED FILES
Echo "Retrieve tag information from tagged files"
pause

GWQtCLI -i "..\..\test\test-output\1C" -o "..\..\test\test-output\1C\retrieved_tags" -u "..\..\test\test-output\1C\retrieved_tags"2> log_retrieving_tags.txt

REM --- DISPLAY CONTENTS ALL RETRIEVED TAGS
type "..\..\test\test-output\1C\retrieved_tags\*.xml"
pause