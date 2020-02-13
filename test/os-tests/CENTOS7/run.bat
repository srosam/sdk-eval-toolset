docker build -t python_wrapper_centos:7 .
docker run -it -v "Specify input location":/home/glasswall/input -v "Specify output location":/home/glasswall/output python_wrapper_centos:7
PAUSE
