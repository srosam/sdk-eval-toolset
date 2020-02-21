# --- TAG FILES IN SPECIFIED INPUT DIRECTORY
echo "Tag files in input directory with the following information"

# --- DISPLAY INFORMATION THAT WILL INSERTED IN EACH FILE
xdg-open "./tags.xml"
read

echo "Process files for security tagging"
cd "../../../libraries/linux"
export LD_LIBRARY_PATH="./"
./GWQtCLI -i "../../test/test-data/1C-security_tags" -o "../../test/test-output/1C" -t "../../test/test-scripts/linux/tags.xml" 2> ./log_tag_files.txt

# --- SHOW FILES IN INPUT AND OUTPUT DIRECTORIES AFTER TAGGING THE FILES
echo "Display input files"
ls "../../test/test-data/1C-security_tags"
echo "Display output files"
ls "../../test/test-output"
xdg-open "../../test/test-output/1C"

# --- RETRIEVE TAGS FROM TAGGED FILES
echo "Retrieve tag information from tagged files"
read

./GWQtCLI -i "../../test/test-output/1C" -o "../../test/test-output/1C/retrieved_tags" -u "../../test/test-output/1C/retrieved_tags" 2> ./log_retrieving_tags.txt

# --- DISPLAY CONTENTS ALL RETRIEVED TAGS
xdg-open "../../test/test-output/1C/retrieved_tags"
read



