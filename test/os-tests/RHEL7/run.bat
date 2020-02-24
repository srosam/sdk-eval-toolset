docker build -t pythonwrapperrhel:7 .
docker run -it -v "%cd%\input:/home/glasswall/input" -v "%cd%\output:/home/glasswall/output" pythonwrapperrhel:7
PAUSE
