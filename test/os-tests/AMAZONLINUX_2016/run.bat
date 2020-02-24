docker build -t python_wrapper_amazon:2016.09 .
docker run -it -v %cd%\input:/home/glasswall/input -v %cd%\output:/home/glasswall/output python_wrapper_amazon:2016.09
PAUSE
