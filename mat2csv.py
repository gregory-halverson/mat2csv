#!/usr/bin/python
#PBS -q verylongq
#PBS -l walltime=00:10:00
#PBS -l select=20:ncpus=12
#PBS -V

import os
import subprocess
import multiprocessing
from glob import glob

PROCESSES = 20

RSCRIPT_COMMAND_BASE = 'Rscript'

path = os.path.dirname(os.path.abspath(__file__))
mat2csv_script = path + '/mat2csv.r'

def mat2csv(matlab_filename, csv_filename, nodata_value):
    subprocess.call([RSCRIPT_COMMAND_BASE, mat2csv_script, matlab_filename, csv_filename, nodata_value])

if __name__ == '__main__':
    if not os.getenv('PBS_ENVIRONMENT'):
        print('usage:')
        print("set SOURCE_MAT_DIRECTORY to directory containing '.mat' files")
        print("set DESTINATION_CSV_DIRECTORY to directory containing '.csv' files")
        print("qsub mat2csv.py")
        exit()

    # parse source directory
    if os.getenv('SOURCE_MAT_DIRECTORY'):
        source_mat_directory = os.getenv('SOURCE_MAT_DIRECTORY')
        print("source '.mat' directory: '%s'" % source_mat_directory)
    else:
        source_mat_directory = None
        exit()

    # parse source directory
    if os.getenv('DESTINATION_CSV_DIRECTORY'):
        destination_csv_directory = os.getenv('DESTINATION_CSV_DIRECTORY')
        print("destination '.csv' directory: '%s'" % destination_csv_directory)
    else:
        destination_csv_directory = None
        exit()

    # parse nodata value
    if os.getenv('NODATA_VALUE'):
        nodata_value = os.getenv('NODATA_VALUE')
        print("nodata value: '%s'" % nodata_value)
    else:
        nodata_value = None
        exit()

    matlab_files = glob(source_mat_directory + '/*.mat')

    args_list = []

    for matlab_filename in matlab_files:
        csv_filename = destination_csv_directory + '/' + \
                       os.path.basename(matlab_filename).replace('.mat', '.csv')

        args = (matlab_filename, csv_filename, nodata_value)
        args_list += [args]

    pool = multiprocessing.Pool(processes=PROCESSES)
