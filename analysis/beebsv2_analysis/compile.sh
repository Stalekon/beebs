plugin=../../gcc-python-plugin/python.so
script=../analysis/beebsv2_analysis/gimple-analyse.py
make LD_LIBRARY_PATH=../../gcc-python-plugin/gcc-c-api CFLAGS="-fplugin=$plugin -fplugin-arg-python-script=$script"


