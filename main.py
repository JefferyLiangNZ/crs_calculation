
from __future__ import absolute_import

# from extract_lines import collect_unloaded_data, chklines_collection
from extract_lines import (collect_unloaded_dir, collect_unloaded_file, chklines_collection)

from calc_process import ( main_handler, wac_wrk_chk, wac_rule_test, wac_rule_test_stats )
import argparse
import logging
import sys

logging.basicConfig(format='%(asctime)s $ %(levelname)s $ %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='data_load.log',level=logging.DEBUG)

def run_program(data_src, process_type = 'dir', user_criteria = None):
    if not user_criteria:
        user_criteria = lambda line: line.find('|{}|'.format('C184')) > 0

    if process_type == 'dir':
        process_func = collect_unloaded_dir
    else:
        process_func = collect_unloaded_file

    wac_wrk_chk_object = wac_wrk_chk()
    wac_rule_test_object = wac_rule_test()
    wac_rule_test_stats_object = wac_rule_test_stats()

    for idx, line in enumerate(process_func(data_src)):

        if user_criteria(line):
            row_object = chklines_collection(line)
            main_handler(
                record                          = row_object, 
                wac_wrk_check_list_append_fn    = wac_wrk_chk_object.append,
                wac_test_rule_append_fn         = wac_rule_test_object.append,
                wac_test_rule_stats_append_fn   = wac_rule_test_stats_object.append
            )
            if not idx % 1000:
                sys.stdout.write('.')
                sys.stdout.flush()

    # print wac_rule_test_stats_object.output(300)
    # print wac_rule_test_object.output(300)
    # print wac_rule_test_stats_object.output(300)
    
    print('\n' + '>>'*30)
    print("... Dumping {} ({})".format(wac_wrk_chk_object.TABLE, wac_wrk_chk_object.size))
    wac_wrk_chk_object.finish()

    print("... Dumping {} ({})".format(wac_rule_test_object.TABLE, wac_rule_test_object.size))
    wac_rule_test_object.data_sqldump()

    print("... Dumping {} ({})".format(wac_rule_test_stats_object.TABLE, wac_rule_test_stats_object.size))
    wac_rule_test_stats_object.data_sqldump()


if __name__ == '__main__':

    # default_directory = './custom'
    default_directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'

    parser = argparse.ArgumentParser(
        description=(
                        'This program helps to process multiple LandOnline data dump files into PostgreSQL sql files'
                    ),

        usage      =(
                        '\nTo transform one file, type(or alike): \npython main.py -f crs_wrk_check_list.unl.gz\n'
                        '\nTo transform multiple files in a directory, type(or alike): '
                        """\npython main.py -d L:\\\\NORA\\\\Geodetic\\\\Data\\\\Cadastral\\\\National WACA Programme 2016-2020\n"""
                    )
    )
    parser.add_argument(
        '-d', 
        dest    =   'dirs', 
        default =   default_directory,
        help    =   ('transform files in a specific directory ' 
                    'dump into proper Postgres Data SQL files')
    )
    parser.add_argument(
        '-f', 
        dest    ='files', 
        help    = ('transform one file ' 
                    'into proper Postgres Data SQL files')
    )

    args = parser.parse_args()
    if args.files:
        run_program(args.files, 'file')

    elif args.dirs:
        logging.info('Using {} as folder.'.format(args.dirs))
        run_program(args.dirs, 'dir')

# logger = logging.getLogger(__name__) # pylint: disable=invalid-name
# logger.setLevel(logging.INFO)
# loggerStreamHandler = logging.StreamHandler()
# loggerStreamHandler.setLevel(logging.INFO)
# logger.addHandler(loggerStreamHandler)
