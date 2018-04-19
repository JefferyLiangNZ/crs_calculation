from __future__ import absolute_import
from __future__ import generators

import re
import sys
import os
import collections
import gzip
import traceback

# https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/
# https://stackoverflow.com/questions/35483359/handling-exceptions-inside-context-managers
# Specify the crs_check_entity namedtuple.
ChkEntity = collections.namedtuple('crs_check_entity', \
    ['wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'])


def collect_lines_decorator(orgin_gen):

    escape_special_char = lambda line: \
        line.strip(' ').replace('\\', '').replace(r'\r', '')

    escape_tab_splitter = lambda line: line.replace('\|', '$ ')

    def new_gen(dirname):

        line_pattern = '^(\d+\|\w+\|\w+\|\w+\|\d+\|[^|]*\|)'
        concat_flag = False
        carry_over = ''

        for line in orgin_gen(dirname):

            line = escape_tab_splitter(line)

            if not concat_flag and re.match(re.compile(line_pattern), line):
                yield escape_special_char(line)
                continue

            carry_over += line

            if not re.match(re.compile(line_pattern), line) and not line.endswith('|\n'):
                concat_flag = True
                continue

            if concat_flag and line == '|\n':
                concat_flag = False
                yield escape_special_char(carry_over)
                carry_over = ''

    return new_gen


def glob_files(dirname):
    """ 
    collect files(full/abstract path) in a given folder, who shares the same extension name gz. 
    glob_file('my_directory') ->  generator
    """
    return (os.path.join(dirname, filename) for filename in sorted(os.listdir(dirname)) if filename.endswith('.gz'))


@collect_lines_decorator
def collect_unloaded_dir(dirname):

    def inner(dirname):

        for file_full_path in glob_files(dirname):
            # if file_full_path.endswith('crs_wrk_check_list8.unl.gz'):
            #     continue
            print 'Loading {} '.format(file_full_path),
            with gzip.open(file_full_path, 'rb') as read_file:
                for line in read_file:
                    yield line
                print('\n')

    return inner(dirname)


@collect_lines_decorator
def collect_unloaded_file(filename):

    def inner(filename):

        with gzip.open(filename, 'rb') as readf:
            for line in readf:
                yield line

    return inner(filename)


def chklines_collection(source):
    """
    parameter for the function

    Input: single row in the data dump file, i.e. '11096|C184|AUTH|UNTD|5195569|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\

\
'
     >>> len(list(match_line(source))
     4
     >>> match_line(source)[1]
     
    """
    items = re.sub(re.compile("\r", re.M), '', source).split('|')[:-1]
    try:
        # print items
        return ChkEntity(*items)
    except Exception as e:
        print e

    # print "Collect total {} c184 check results".format(cnt) 


class Checklist_readlines():
    def __init__(self, source):
        self.line_text = source

    def __enter__(self):
        items = re.sub(re.compile("\r\n", re.M), os.linesep, self.line_text).split('|')[:-1]
        # items = self.line_text.split('|')[:-1]

        try:
            # print items
            res = ChkEntity(*items)
            res.wrk_id and res.chi_code
            return res

        except Exception as e:
            print repr(self.line_text)

            traceback.print_exc(file=sys.stdout)
            print e

    def __exit__(self, exc_type, exc_val, traceback):
        # print "closing up"
        if exc_type or exc_val:
            print exc_type, exc_val

        return True


def unit_test2(file_path, code):

    for idx, line in  enumerate(collect_unloaded_file(file_path)):
        if line.find('|{}|'.format(code)) > 0:
            
            if not idx%500:
                sample = chklines_collection(line)
                print sample.wrk_id, sample.chi_code, sample.exec_stag, sample.summary_txt[220:320]
            
            idx += 1

    print idx
        
def unit_test3(directory, code):

    check_fn = lambda line: line.find('|{}|'.format(code)) > 0

    for idx, line in  enumerate(collect_unloaded_dir(directory)):
        
        if check_fn(line):
            if idx%500 == 0:
                sample = chklines_collection(line)
                print sample.wrk_id, sample.chi_code, sample.exec_stag, sample.summary_txt[220:300]
    print idx


def unit_test4(directory, code):

    check_fn = lambda line: line.find('|{}|'.format(code)) > 0

    for idx, line in enumerate((line for line in collect_unloaded_dir(directory) if check_fn(line))):
        with Checklist_readlines(line) as row_object:
            v = row_object.summary_txt[220:300]
            # if not idx % 500:
            print row_object.wrk_id, '<>', '\n'.join(row_object.summary_txt.splitlines()[:25])
                    # print sample.wrk_id, sample.chi_code, sample.exec_stag, sample.summary_txt[220:300]
    print idx


def unit_test5(filename, code):
    check_fn = lambda line: line.find('|{}|'.format(code)) > 0

    for idx, line in enumerate((line for line in collect_unloaded_file(filename) if check_fn(line))):
        with Checklist_readlines(line) as row_object:
            if row_object.ref_id == '597276':
                assert re.search(r'SUMMARY OF REGULATION', row_object.summary_txt)

    assert idx == 4
    print("All good")


if __name__ == '__main__':

    directory = 'L:\\NORA\\Geodetic\\Data\\Cadastral\\National WACA Programme 2016-2020\\wrk_chk_list'
    file_name = './custom/crs_wrk_check_list2.unl.gz'
    directory = './custom'

    unit_test5('./testdata/sample.log.gz', 'C184')
    # unit_test4(directory, 'C184')
    # unit_test3(directory, 'C184')
    # unit_test2(file_name, 'C184')
    # embed_test1(directory)
