#!/bin/bash
#RUN GLASSWALL AS A NON ROOT USER
echo "Run Glasswall as non root user"

#DISPLAY USERS AND GROUPS
echo "
Display current user"
whoami
echo "
Display current group"
groups
echo "
Show users of root group"
getent group root

read -p "Press any key to continue.. " -n1 -s

#DISPLAY INPUT FILES
echo "

Display input files"

ls "../../test-data/1D-All_File_Types"
read -p "Press any key to continue.. " -n1 -s

#SHOW PERMISSIONS OF LIBRARIES
echo "

	Show permissions of libraries"
cd "../../../libraries/linux"
ls -l

#RUN GLASSWALL
echo "

Run Glasswall"

./GWQtCLI -i "../../test/test-data/1D-All_File_Types/" -o "../../test/test-output/G3" 2> log_process_all_files.txt

# --- List all the files in the output directory
echo "All output files"
ls "../../test/test-output/G3"

# --- Show ouput directory
xdg-open "../../test/test-output/G3"


