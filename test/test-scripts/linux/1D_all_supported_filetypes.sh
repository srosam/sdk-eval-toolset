#!/bin/bash
# --- Process all supported files in the input directory.
echo "Run all files with default policy settings"

# --- List all the files in the input directory
echo "All input files"
ls "../../test-data/1D-All_File_Types"
read
cd "../../../libraries/linux"
./GWQtCLI -i "../../test/test-data/1D-All_File_Types/" -o "../../test/test-output/1D" 2> log_process_all_files.txt

# --- List all the files in the output directory
echo "All output files"
ls "../../test/test-output/1D"

# --- Show ouput directory
xdg-open "../../test/test-output/1D"
read 
