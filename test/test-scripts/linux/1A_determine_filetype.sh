#!/bin/bash
#CALL DETERMINE FILE TYPE API AND PROCESS EXTENSION-LESS FILES
echo "Determine file type"

#DISPLAY INPUT FILES
echo "Display input files"
ls "../../test-data/1A-Determine_file_type"

#USE PYTHON SDK WRAPPER TO DIRECTLY CALL THE DETERMINE FILE TYPE API AND PRINT TYPE ENUM VALUE AND CORRESPONDING FILE TY[E
#echo "Calls determine file type using core 2 python SDK wrapper (Display file type enum value and file type)"
#python determine-file-type.py "../Demo_Data/1A-Determine_file_type" /home/glasswall/Shared/linux/IQT/Core2_CLI/libglasswall_core2.so > log_determine_file_type_sdk_wrapper.log
#read "Press any key to continue"

#PROCESS FILES
echo "Run Glasswall on extension-less input files"
cd "../../../libraries/linux"
./GWQtCLI -i "../../test/test-data/1A-Determine_file_type" -o "../../test/test-output/1A" 2> log_determine_file_type.log

# DISPLAY OUTPUT
echo "Show output"
ls "../../test/test-output/1A"

# OPEN OUTPUT DIRECTORY
echo "Open the output folder"
xdg-open  "../../test/test-output/1A"
read
