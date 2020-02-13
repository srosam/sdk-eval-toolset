docker build -t python_wrapper_amazon:2018.03 .
docker run -it -v "Specify input location":/home/glasswall/input -v "Specify output location":/home/glasswall/output python_wrapper_amazon:2018.03
PAUSE
