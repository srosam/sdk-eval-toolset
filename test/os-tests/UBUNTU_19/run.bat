docker build -t python_wrapper_ubuntu:19.04 .
docker run -it -v %cd%\input:/home/glasswall/input -v %cd%\output:/home/glasswall/output python_wrapper_ubuntu:19.04
PAUSE
