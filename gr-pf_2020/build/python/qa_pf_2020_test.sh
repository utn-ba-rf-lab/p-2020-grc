#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/home/gnuradio/persistent/gr-pf_2020/python"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/gnuradio/persistent/gr-pf_2020/build/python":$PATH
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/gnuradio/persistent/gr-pf_2020/build/swig:$PYTHONPATH
/usr/bin/python3 /home/gnuradio/persistent/gr-pf_2020/python/qa_pf_2020.py 
