docker build -t python_wrapper_ubuntu:19.04 .
docker run -it -v "Specify input location":/home/glasswall/input -v "Specify output location":/home/glasswall/output python_wrapper_ubuntu:19.04
PAUSE
