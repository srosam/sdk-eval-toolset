i#!/bin/bash
#CHECK THAT GLASSWALL RUNS WITH IP6 DISABLED
echo "Run with ip6 disabled (This needs to be done before running this script)"

#CONFIRM IP6 NOT RUNNING
echo "
Check no ip6 addresses in use (no net6 addresses shown)
(Loopback addresses only relevant if ipv6 enabled.)"
ip a s

read -p "Press any key to continue.. " -n1 -s

#DISPLAY INPUT FILES
echo "

Display input files"

ls "../../test-data/1D-All_File_Types"
read -p "Press any key to continue.. " -n1 -s

#RUN RUN GLASSWALL INVOKING ALL CAMERAS USING SHOW PROCESSING
echo "

Run Glasswall to process all filetypes"
cd "../../../libraries/linux"
./GWQtCLI -i "../../test/test-data/1D-All_File_Types/" -o "../../test/test-output/G15" 2> log_no_ip6.txt

# --- List all the files in the output directory
echo "All output files"
ls "../../test/test-output/G15"

# --- Show ouput directory
xdg-open "../../test/test-output/G15"

