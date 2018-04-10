
from __future__ import absolute_import

from extract_lines import collect_unloaded_data, chklines_collection

from calc_process import main_handler, wac_wrk_chk, wac_rule_test, wac_rule_test_stats

if __name__ == '__main__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    directory = './custom'

    files_content_collection = collect_unloaded_data(directory)
    

    wac_wrk_chk_object = wac_wrk_chk()
    wac_rule_test_object = wac_rule_test()
    wac_rule_test_stats_object = wac_rule_test_stats()

    with open('temp_chk_results.txt', 'w') as temp_write_object:
        for file_name, file_content in files_content_collection:
            for item in chklines_collection(file_content):
            	main_handler(item, wac_wrk_chk_object, wac_rule_test_object, wac_rule_test_stats_object)

            	 # 1 of 10 observations did not meet accuracy requirement
            	 # 5 of 60 observations did not meet accuracy requirement
            	 # Test failed for 3 of 98 
            	 # 127 of 128 observations meet accuracy requirement
    print '>>'*8
    print wac_rule_test_stats_object.output()