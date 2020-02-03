REM --- USE THE RESOURCE MONITOR TO DISPLAY THE DIFFERENCE BETWEEN SINGLE THREAD AND MULTI-THREAD EXECUTION

REM --- OPEN THE RESOURCE MONTIOR
Echo "Open Resource monitor (CPU) to see impact of threading"
Start c:\windows\system32\resmon

REM --- SHOW ALL INPUT FILES
Echo "Process all files in a single thread"
dir "..\..\test-data\1E-Multithread"
pause

REM --- RUN GLASSWALL ACROSS ALL FILES IN A SINGLE THREAD
Echo "See run in single thread first (uses single CPU per file and switches between CPUs)"
cd "..\..\..\libraries\windows"
GWQtCLI -i "..\..\test\test-data\1E-Multithread" -o "..\..\test\test-output\1E_S" -x export 2> log_singlethread.txt
Echo "Now in multithread mode (should use multiple CPUs and be quicker)"
Pause

REM --- RUN GLASSWALL ACCROSS ALL FILES, 1 THREAD PER FILE (MULTITHREADED) '-m' option
GWQtCLI -i "..\..\test\test-data\1E-Multithread" -o "..\..\test\test-output\1E_M" -m -x export 2> log_multithread.txt
start c:\windows\EXPLORER.EXE /n, /e, ..\..\test\test-output\1E_S
start c:\windows\EXPLORER.EXE /n, /e, ..\..\test\test-output\1E_M
pause