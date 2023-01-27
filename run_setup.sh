#!/bin/bash

# Get command line arguments
arg1=$1
arg2=$2
arg3=$3
arg4=$4
arg5=$5

# Run pip install commands
pip3 install fastapi
pip3 install psycopg2
pip3 install csv
pip3 install numpy
pip3 install pandas

# Run Python files with command line arguments
python3 define_tables.py $arg1 $arg2 $arg3 $arg4 $arg5
python3 load_csv.py $arg1 $arg2 $arg3 $arg4 $arg5
python3 sitzberechnung.py $arg1 $arg2 $arg3 $arg4 $arg5
python3 create_tokentables.py $arg1 $arg2 $arg3 $arg4 $arg5
