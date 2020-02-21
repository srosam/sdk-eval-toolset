#!/bin/bash
# CALL ARCHIVE WRAPPER AND PROCESS ARCHIVES
echo "Archive wrapper"

# DISPLAY INPUT FILES
echo "Display input files"
ls "../../test-data/1D-Archives"

# USE GLASSWALL CLASSIC TO CALL ARCHIVE WRAPPER AND PROCESS ARCHIVES
echo "Calls Archive Wrapper to process Archives"
cd "../../../libraries/linux"
./glasswallCLI -config="../../test/test-scripts/linux/config.ini" -xmlconfig="../../test/test-scripts/linux/config.xml"
read

# --- List all the files in the output directory
echo "All output files"
ls "../../test/test-output/1D_Archive"

# --- Show ouput directory
echo "Open the output folder"
xdg-open "../../test/test-output/1D_Archive"
read


