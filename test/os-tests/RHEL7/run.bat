docker build -t python_wrapper_rhel:7 .
docker run -it -v "Specify input location":/home/glasswall/input -v "Specify input location":/home/glasswall/output python_wrapper_rhel:7
PAUSE
