cd "..\..\..\libraries\windows"
GWQtCLI -i "..\..\test\test-data\Export_Import-Test_Files" -o "..\..\test\test-output\GW_Export" -x export 2> export_log.txt

Echo "Export complete"

Pause

GWQtCLI -i "..\..\test\test-output\GW_Export" -o "..\..\test\test-output\GW_Import" -x import 2> import_log.txt

Echo "Import complete"

Pause