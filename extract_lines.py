
import re
import os
import collections
import gzip

# Specify the crs_check_entity namedtuple.
ChkEntity = collections.namedtuple('crs_check_entity', \
    ['wrk_id', 'chi_code', 'exec_staq', 'result', 'ref_id', 'summary_txt'])

line_pattern = '(\d+\|C184\|\w+\|\w+\|\d+\|[^|]*\|)'


def collect_unloaded_data(directory):

    for filename in os.listdir(directory):        
        if filename.endswith('.gz'):
            
            print "\n---loading %s ..." % filename
            fullpath = os.path.join(directory, filename)

            with gzip.open(fullpath, 'rb') as f:
                yield (filename, f.read())

        
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
     
    """
    cnt = 0
    matched_rows = re.findall(line_pattern, source, re.M)
    
    if matched_rows is None:
        raise StopIteration
        return
        
    for row in matched_rows:

        items = re.sub(re.compile("\r\n", re.M), '', row).replace('\\', '').split('|')[:-1]
        try:
            cnt += 1
            yield ChkEntity(*items)
        except Exception as e:
            print e

    print "Collect c184 check item: {} out of {}".format(cnt, len(matched_rows)) 

if __name__ == '__main__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    directory = './custom'    
    files_content_collection = collect_unloaded_data(directory)
    
    with open('temp_chk_results.txt', 'w') as temp_write_object:
        for file_name, file_content in files_content_collection:
            for item in chklines_collection(file_content):
                if item.summary_txt.find('=') > 0:
                    temp_write_object.write(item.summary_txt + '\n')
                
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