# PROCESS ALL FILES IN EXPORT AND IMPORT MODE
echo "Export Mode Test"

#DISPLAY INPUT FILES
echo "Display input files"
ls "../../test-data/Export_Import-Test_Files"

#PROCESS FILES IN EXPORT MODE
cd "../../../libraries/linux"
./GWQtCLI -i "../../test/test-data/Export_Import-Test_Files" -o "../../test/test-output/GW_Export" -x export 2> export_log.txt

#DISPLAY EXPORT OUTPUT FILES
echo "Display output files"
ls "../../test/test-output/GW_Export"
echo "Export complete"
read

#PROCESS FILES IN IMPORT MODE
echo "Import Mode Test"
./GWQtCLI -i "../../test/test-output/GW_Export" -o "../../test/test-output/GW_Import" -x import 2> import_log.txt


#DISPLAY IMPORT OUTPUT FILES
echo "Display output files"
ls "../../test/test-output/GW_Import"
echo "Import complete"
read

