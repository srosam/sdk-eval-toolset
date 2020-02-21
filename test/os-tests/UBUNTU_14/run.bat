docker build -t python_wrapper_ubuntu:14.04 .
docker run -it -v %cd%\input:/home/glasswall/input -v %cd%\output:/home/glasswall/output -w="/home/glasswall" python_wrapper_ubuntu:14.04
PAUSE
