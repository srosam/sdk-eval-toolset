docker build -t python_wrapper_amazon:2016.09 .
docker run -it -v "Specify input location":/home/glasswall/input -v "Specify output location":/home/glasswall/output python_wrapper_amazon:2016.09
PAUSE
