#Expects to be executed in beebs/build and also assumes that
#the gcc-with-python plugin directory is in the same directory as beebs
#Also, I only managed to run the plugin with gcc for x86, so beebs
#has to be configured for x86 as well.

build_dir=$PWD

script=$build_dir/../analysis/beebsv2_analysis/gimple-analyse.py
python_plugin_dir=$build_dir/../../gcc-python-plugin
plugin=$python_plugin_dir/python.so

make LD_LIBRARY_PATH=$python_plugin_dir/gcc-c-api CFLAGS="-fplugin=$plugin -fplugin-arg-python-script=$script"


