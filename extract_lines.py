from __future__ import absolute_import
from __future__ import generators

import re
import os
import collections
import gzip


# Specify the crs_check_entity namedtuple.
ChkEntity = collections.namedtuple('crs_check_entity', \
    ['wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'])

from StringIO import StringIO
import logging


def collect_unloaded_data(directory):

    for filename in os.listdir(directory):        
        if filename.endswith('.gz'):

            if filename != 'crs_wrk_check_list2.unl.gz':
                continue

            print "\n---loading %s ..." % filename
            fullpath = os.path.join(directory, filename)

            with gzip.open(fullpath, 'rb') as input_data:
                round_up = 0
                overall_cnt =0
                read_buff = StringIO()

                line = input_data.readline()
                while line:
                    overall_cnt += 1
                    round_up += 1

                    read_buff.write(line)
                    logging.info("Collect: " + repr(line.replace('\r', '').replace('\\', '')))
                    
                    if round_up > 5000 and re.search(re.compile(r'\d+\|\w+\|\w+\|\w+\|\d+\|\|'), line):
                        logging.warn('passing {} lines to analysi program'.format(round_up))
                        round_up = 0
                        yield (filename, read_buff.getvalue())
                        read_buff = StringIO()
                    line = input_data.readline()
                logging.warn('total number: {}'.format(overall_cnt))


        
def chklines_collection(source):
    """
     >>> source = '''11096|C184|AUTH|UNTD|5195569|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\

\
|
11096|C184|AUTH|UNTD|5195569||
11096|C184|AUTH|PASS|5195570|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\


\
|
11046|C184|AUTH|UNTD|5195569||
'''
     >>> len(list(match_line(source))
     4
     >>> match_line(source)[1]
     

     C182, C183, C185
    """
    line_pattern = '(\d+\|C184\|\w+\|\w+\|\d+\|[^|]*\|)'    
    cnt = 0
    matched_rows = re.finditer(line_pattern, source, re.M)
    
    if matched_rows is None:
        return
        
    for matched_sre_obj in matched_rows:

        row = matched_sre_obj.groups()[0]
        items = re.sub(re.compile("\r\n", re.M), '', row).replace('\\', '').split('|')[:-1]
        try:
            cnt += 1
            yield ChkEntity(*items)
        except Exception as e:
            print e

    # print "Collect total {} c184 check results".format(cnt) 

if __name__ == '__main__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    directory = './custom'    
    files_content_collection = collect_unloaded_data(directory)
    
    verify_cnt = 0

    with open('temp_chk_results.txt', 'w') as temp_write_object:
        for file_name, file_content in files_content_collection:
                verify_cnt += file_content.count('\n')
                # print file_name, file_content.count('\n')
                # print file_content[-700:].replace('\r', '')
                # print 
                
            # for item in chklines_collection(file_content):
            #     if item.summary_txt.find('=') > 0:
            #         temp_write_object.write(item.summary_txt + '\n')
            
    print verify_cnt, "FINISH"

            # if file_name == 'crs_wrk_check_list7.unl.gz':
            #     break




"""

if __name__ == '__main__':
    test_sample = '''11096|C184|AUTH|UNTD|5195569|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\

\
|
11096|C184|AUTH|UNTD|5195569||
11096|C184|AUTH|PASS|5195570|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\


\
|
11046|C184|AUTH|UNTD|5195569||
'''
    ret = match_line(test_sample)
    print ret[2].summary_txt
    
"""