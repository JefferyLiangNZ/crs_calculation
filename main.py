
from __future__ import absolute_import

# from extract_lines import collect_unloaded_data, chklines_collection
from extract_lines import (collect_unloaded_dir, chklines_collection)

from calc_process import ( main_handler, wac_wrk_chk, wac_rule_test, wac_rule_test_stats )

import logging
import sys
# format=' %(message)s'
logging.basicConfig(format='%(asctime)s $ %(levelname)s $ %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='data_load.log',level=logging.DEBUG)

# logger = logging.getLogger(__name__) # pylint: disable=invalid-name
# logger.setLevel(logging.INFO)

# loggerStreamHandler = logging.StreamHandler()
# loggerStreamHandler.setLevel(logging.INFO)
# logger.addHandler(loggerStreamHandler)

if __name__ == '__test__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    directory = './custom'

    logging.info('Using {} as folder.'.format(directory))
    files_content_collection = collect_unloaded_data(directory)
    

    wac_wrk_chk_object = wac_wrk_chk()
    wac_rule_test_object = wac_rule_test()
    wac_rule_test_stats_object = wac_rule_test_stats()

    with open('temp_chk_results.txt', 'w') as temp_write_object:
        for file_name, file_content in files_content_collection:
            logging.info('Unzipping {}.'.format(file_name))
            for item in chklines_collection(file_content):
            	main_handler(item, wac_wrk_chk_object, wac_rule_test_object, wac_rule_test_stats_object)

    print '>>'*8
    print wac_wrk_chk_object.output(300)
    # print '>>'*8
    # print wac_rule_test_object.output(300)
    # print '>>'*8
    # print wac_rule_test_stats_object.output(300)
    # print '>>'*4
    print("... Dumping "+wac_wrk_chk_object.TABLE)
    wac_wrk_chk_object.data_sqldump()

    print("... Dumping "+wac_rule_test_object.TABLE)
    wac_rule_test_object.data_sqldump()

    print("... Dumping "+wac_rule_test_stats_object.TABLE)    
    wac_rule_test_stats_object.data_sqldump()
    # for entry in wac_wrk_chk_object.data_export():
    #      print entry
    # for entry in wac_rule_test_stats_object.data_export():
    #     print entry

def run_program(directory, user_criteria = None):
    if not user_criteria:
        user_criteria = lambda line: line.find('|{}|'.format('C184')) > 0
    
    wac_wrk_chk_object = wac_wrk_chk()
    wac_rule_test_object = wac_rule_test()
    wac_rule_test_stats_object = wac_rule_test_stats()

    for idx, line in  enumerate(collect_unloaded_dir(directory)):

        if user_criteria(line):
            row_object = chklines_collection(line)
            main_handler(
                record                     = row_object, 
                wac_wrk_check_list_append  = wac_wrk_chk_object.append,
                wac_test_rule_append       = wac_rule_test_object.append,
                wac_test_rule_stats_append = wac_rule_test_stats_object.append
            )

            if not idx % 1000:
                sys.stdout.write('.')
                sys.stdout.flush()

    # print '>>'*8
    # print wac_rule_test_stats_object.output(300)
    # print '>>'*8
    # print wac_rule_test_object.output(300)
    # print '>>'*8
    # print wac_rule_test_stats_object.output(300)
    # print '>>'*4

    
    print("... Dumping "+wac_wrk_chk_object.TABLE)
    wac_wrk_chk_object.finish()
    # wac_wrk_chk_object.data_sqldump()

    print("... Dumping "+wac_rule_test_object.TABLE)
    wac_rule_test_object.data_sqldump()

    print("... Dumping "+wac_rule_test_stats_object.TABLE)    
    wac_rule_test_stats_object.data_sqldump()


if __name__ == '__main__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    directory = './custom'

    logging.info('Using {} as folder.'.format(directory))
    run_program(directory)