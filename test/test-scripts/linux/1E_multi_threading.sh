# --- USE THE RESOURCE MONITOR TO DISPLAY THE DIFFERENCE BETWEEN SINGLE THREAD AND MULTI-THREAD EXECUTION

# --- OPEN THE RESOURCE MONTIOR
echo "Open mate system monitor (CPU) to see impact of threading"
mate-system-monitor &
read

# --- SHOW ALL INPUT FILES
echo "Process all files in a single thread"
ls "../../test-data/1E-Multithread"
read

# --- RUN GLASSWALL ACROSS ALL FILES IN A SINGLE THREAD
echo "See run in single thread first (uses single CPU per file and switches between CPUs)"
cd "../../../libraries/linux"
./GWQtCLI -i "../../test/test-data/1E-Multithread" -o "../../test/test-output/1E_S" -x export 2> log_singlethread.txt
echo "Now in multithread mode (should use multiple CPUs and be quicker)"
read

# --- RUN GLASSWALL ACCROSS ALL FILES, 1 THREAD PER FILE (MULTITHREADED) '-m' option
killall mate-system-monitor
mate-system-monitor &
./GWQtCLI -i "../../test/test-data/1E-Multithread" -o "../../test/test-output/1E_M" -m -x export 2> log_multithread.txt
xdg-open "../../test/test-output/1E_S"
xdg-open "../../test/test-output/1E_M"
read


