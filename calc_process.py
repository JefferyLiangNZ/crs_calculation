from __future__ import absolute_import

import sys
import re
from StringIO import StringIO
import logging

from collections import ( OrderedDict, namedtuple )
from collections import deque
import functools

import copy
import argparse

from extract_fields import  \
(
    metrics_dict,
    extract_metrics, 
    
    extract_context, 
    extract_context_regtest_title,
    extract_context_regtest_block,

    extract_context_testblock, 
    extract_context_testblock_rule_recognizer, 
    extract_context_testblock_rulestat,
    extract_context_testblock_rulestat_cognition,
    extract_context_testblock_rulestat_error
)


wac_wrk_chk_item = namedtuple('wac_wrk_chk', \
    ['wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'] + metrics_dict.keys())

wac_wrk_rule_test_item = namedtuple('wac_wrk_rule_test_item', \
    ['reg_ver', 'reg_desc', 'rule_title', 'rule_desc', 'rule_block'])

wac_rule_test_stats_item = namedtuple('wac_rule_test_stats_item', \
    ['chk_id', 'rule_id', 'fail_cnt', 'obn_cnt', 'ratio', 'error'])

# skip_stats = {}

# test_rule_stats = {}


class waca_base():
    def __init__(self):
        self.store = OrderedDict()

    @staticmethod
    def null_value_handler(data_dict):

        for key in data_dict.copy().keys():
            # print(key)
            # print(data_dict[key])
            if data_dict[key] is None:
                data_dict[key] = 'NULL'
            if isinstance(data_dict[key], str) and data_dict[key] == '':
                data_dict[key] = ' '

    @property
    def size(self):
        return len(self.store)

    @staticmethod
    def strip_trailing_leading_nonsense(source):
        """
            triming all trailing and leading = or line breaks
            a better way could be regex in the future
        """
        source = re.sub(re.compile(r'(NOTES((.|\n)*))'), '', source)
        if source.find('NOTES') > 0:
            print source
            raise Exception

        """Test passed for all 122 observations"""
        return source.strip().strip('=').strip()

    @staticmethod
    def escape_single_quotes(source):
        # print repr(source), '-->'
        return re.sub(re.compile('\''), '`', source)

    def output(self, limit):
        
        bb = StringIO()
        cnt = 0

        for key, item in self.store.items():
            
            cnt += 1
            if self.__class__.__name__ == 'wac_rule_test':
                bb.write('{}, {}\n'.format(str(item[0]), str(item[1])))
            else:
                bb.write('{},{}\n'.format(str(key), str(item)))

            if cnt > limit:
                break


        bb.write('output {} - {}'.format(len(self.store.keys()), self.__class__.__name__))
        return bb.getvalue()

    def waca_sql_format(self):
        raise Exception

    @staticmethod
    def waca_sql_boilplate(table_name, data_tuples_str, seq_cnt):
        head = 'INSERT INTO waca.{} values '.format(table_name)
        body = data_tuples_str.strip('\n,')
        closing = '\echo ---> {}'.format(seq_cnt)
        return '{}\n{};\n{}\n'.format(head, body, closing)

    def data_sqldump(self):

        with open(self.TABLE+'.sql', 'w') as wfile:

            row_cnt = 0
            base = StringIO()
            wfile.write('truncate table waca.{} cascade;\n'.format(self.TABLE))

            for row in self.data_export():

                base.write(' ({}),\n'.format(row))
                if row_cnt % 500 == 499:
                    wfile.write(waca_base.waca_sql_boilplate(self.TABLE, base.getvalue(), row_cnt))
                    base = StringIO()
                row_cnt += 1

            wfile.write(waca_base.waca_sql_boilplate(self.TABLE, base.getvalue(), row_cnt))


class wac_rule_test_stats(waca_base):
    TABLE = 'wac_test_rule_stats'
    def __init__(self):
        # super.__init__(self)
        waca_base.__init__(self)
        # self.store    = OrderedDict()
        self.__init_seq = 29999
        sql_fn = functools.partial(waca_base.waca_sql_boilplate, self.TABLE)
        self.export = data_exporter(self.TABLE, sql_fn)

    def __next_key(self):

        self.__init_seq += 1
        return self.__init_seq

    def append(self, chk_id, rule_id, fail_cnt, obn_cnt, ratio, error):

        store_key = self.__next_key()
        self.store[store_key] = wac_rule_test_stats_item(chk_id, rule_id, fail_cnt, obn_cnt, ratio, error)
        return store_key

    def data_export(self):

        for key, item in self.store.items():
            data_dict = item._asdict()
            data_dict.update({'id': key })
            waca_base.null_value_handler(data_dict)
            yield "{id}, {chk_id}, {rule_id}, {fail_cnt}, {obn_cnt}, {ratio}, {error}".format(**data_dict)


class wac_rule_test(waca_base):
    TABLE = 'wac_test_rule'    
    def __init__(self):
        waca_base.__init__(self)
        self.__init_seq = 99
        self.__unique_value_pool = {}
        self.__tablename__ = 'wac_rule_test_tbl'

    def __next_key(self):
        self.__init_seq += 1
        return self.__init_seq

    def append(self, reg_ver, reg_desc, rule_title, rule_desc, rule_block):

        if (reg_ver, reg_desc, rule_title, rule_desc) in self.store:
            return self.store[(reg_ver, reg_desc, rule_title, rule_desc)][0]
        else:
            store_key = self.__next_key()
            self.store[(reg_ver, reg_desc, rule_title, rule_desc)] = (store_key,   \
                wac_wrk_rule_test_item(reg_ver=reg_ver, reg_desc=reg_desc, rule_title=rule_title, rule_desc=rule_desc, rule_block=rule_block))
            logging.debug('{}'.format(self.store[(reg_ver, reg_desc, rule_title, rule_desc)]))
            return store_key

    def data_export(self):

        for item in self.store.values():

            key, rule_tuple = item
            data_dict = rule_tuple._asdict()
            data_dict.update({'id': key})

            data_dict['rule_block'] = waca_base.strip_trailing_leading_nonsense(data_dict['rule_block'])
            data_dict['rule_block'] = waca_base.escape_single_quotes(data_dict['rule_block'])
            data_dict['reg_desc'] = waca_base.escape_single_quotes(data_dict['reg_desc'])
            yield "'{id}', '{reg_ver}', '{rule_title}', '{reg_desc}', '{rule_desc}', '{rule_block}'".format(**data_dict)


class wac_wrk_chk(waca_base):
    TABLE = 'wac_wrk_check_list'


    def __init__(self):
        waca_base.__init__(self)        
        self.__init_seq = 1999
        self.__ref_id_pool = {}

        # sql_fn is responsible for formating the 'INSERT XXX' query
        sql_fn = functools.partial(waca_base.waca_sql_boilplate, self.TABLE)
        self.export = data_exporter(self.TABLE, sql_fn)

    @property
    def size(self):
        return self.export.size

    def __next_key(self):
        self.__init_seq += 1
        return self.__init_seq

    def __uniq_ref_check(self, ref_id):
        if ref_id in self.__ref_id_pool:
            return False
        else:
            self.__ref_id_pool[ref_id] = 1
            return True

    def append(self, record):

        # print record
        if not self.__uniq_ref_check(record.ref_id):
            raise Exception
            return None

        base = None
        store_key = self.__next_key()
        metrics = extract_metrics(record.summary_txt)

        if metrics:
            try:
                base = metrics.copy()
                base.update(record._asdict())
            except:
                print metrics
                print base
        else:
            base = {'obn_cnt': None, 'prm_cnt': None, 'free_dg': None, 'std_err':None}
            base.update(record._asdict())
            base['summary_txt'] = base['summary_txt'][:7000]

        store_item = copy.copy(wac_wrk_chk_item(**base))
        store_item_dict = store_item._asdict()
        store_item_dict['id'] = store_key

        waca_base.null_value_handler(store_item_dict)
        new_summary = waca_base.strip_trailing_leading_nonsense(store_item_dict['summary_txt'])

        store_item_dict['summary_txt'] = waca_base.escape_single_quotes(new_summary)
        if store_item_dict['summary_txt'] == '':
            store_item_dict['summary_txt'] = ' '

        self.export.add(store_item_dict)
        return store_key

    def finish(self):
        self.export.finish()

    def data_export(self):

        for key, item in self.store.items():
            data_dict = item._asdict()
            data_dict.update({'id': key })
            waca_base.null_value_handler(data_dict)
            new_summary = waca_base.strip_trailing_leading_nonsense(data_dict['summary_txt'])
            # print(new_summary)

            data_dict['summary_txt'] = waca_base.escape_single_quotes(new_summary)
            if data_dict['summary_txt'] == '':
                data_dict['summary_txt'] = ' '
            yield "{id}, {wrk_id}, '{chi_code}', '{exec_stag}', '{result}', {obn_cnt}, {prm_cnt}, {free_dg}, {std_err}, {ref_id}, {summary_txt}".format(**data_dict)


class data_exporter(object):
    def __init__(self, table_name, sql_writer, size = 500):

        self.__container__ = deque(maxlen = size+10)
        self.max_size = size
        self.dat_filename = table_name + '.sql'
        self.sql_writer = sql_writer
        self.sum_cnt = 0

        with open(self.dat_filename, 'w') as wfile:
            wfile.write('truncate table waca.{} cascade;\n'.format(table_name))

    def add(self, elem):
        self.sum_cnt += 1
        self.__container__.append(elem)
        if len(self.__container__) >= self.max_size:
            self._data_export(self.sum_cnt)

    @property
    def size(self):
        return self.sum_cnt

    def _data_export(self, count):

        data_tuples = []
        # print("FILENAME:{}>>{}".format(self.dat_filename, count))

        while len(self.__container__):
            data_dict = self.__container__.popleft()
            formatted = (
                "({id}, {wrk_id}, '{chi_code}', '{exec_stag}',"
                " '{result}', {obn_cnt}," 
                "{prm_cnt}, {free_dg}, {std_err}, {ref_id}, "
                "'{summary_txt}')"
            ).format(**data_dict)

            data_tuples.append(formatted)

        with open(self.dat_filename, 'a') as wfile:
            wfile.write(
                self.sql_writer(
                    ', \n'.join(data_tuples), 
                    count-1
                )
            )

    def finish(self):
        self._data_export(self.sum_cnt)


def main_handler(record, 
                 wac_wrk_check_list_append_fn, 
                 wac_test_rule_append_fn, 
                 wac_test_rule_stats_append_fn):

    # source = re.sub(re.compile('NOTES(.|\n)+', re.M), '', source)
    wrk_chk_fk_id = wac_wrk_check_list_append_fn(record)
    rule_result_block = extract_context(record.summary_txt)

    if not rule_result_block:
        return

    regulation_year_context = ''
    for rule_result_chain_block in extract_context_regtest_block(rule_result_block):
        
        regulation_ver, regulartion_desc = \
            extract_context_regtest_title(rule_result_chain_block, regulation_year_context)

        regulation_year_context = regulation_ver.split('-')[0] \
            if regulation_ver else regulation_year_context
        
        for testrule_block in extract_context_testblock(rule_result_chain_block+'\n'):
            
            # print testrule_block
            rule_title, rule_descr = extract_context_testblock_rule_recognizer(testrule_block, rule_result_chain_block)
            wrk_testrule_fk_id = wac_test_rule_append_fn(regulation_ver, regulartion_desc, rule_title, rule_descr, testrule_block)

            try:
                applied_cnt, total_cnt, ratio = extract_context_testblock_rulestat_cognition(testrule_block)
                err_bound = extract_context_testblock_rulestat_error(testrule_block)
                wac_test_rule_stats_append_fn(wrk_chk_fk_id, wrk_testrule_fk_id, applied_cnt, total_cnt, ratio, err_bound)           
            except ValueError:
                logging.error("Cant deduct from test rule results because: "+ source)
                break
            except Exception as e:
                print e

            logging.info('{}'.format(testrule_block.strip('\n ')))


def ctest_extract_context(source):

    test_file = 'temp_chk_results.txt'
    with open(test_file, 'r') as rfile:
        text = rfile.read()
        cnt = 0
        check_list_items = []

        for block in extract_blocks(text):
            cnt += 1
            summary_handler(block)


def ctest_main_handler():

    from conftest import (SAMPLE_A, SAMPLE_B)
    #mocked input for the main_handler
    record_A = wac_wrk_chk_item(1, '2', '3', '4', 5, SAMPLE_A, 11, 12, 13, '0.1')
    record_B = wac_wrk_chk_item(1, '1', '1', '1', 1, SAMPLE_B, 0, 0, 0, '0')

    def f1(*args):
        print('f1 get called with: \n' + str(args[0]._asdict()))

    def f2(*args):
        print('\n\n>>f2 get called with: \n' + ';\n'.join([str(item) for item in args]) + ';')

    def f3(*args):
        print('\n\n>>>>f3 get called with: \n' + ';  '.join([str(item) for item in args]))

    print(''.join(['\n\n', 'record_A ', '+'*28 + '\n\n']))
    main_handler(record_A, f1, f2, f3)

    print(''.join(['\n\n', 'record_B ', '+'*28 + '\n\n']))
    main_handler(record_B, f1, f2, f3)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', 
                        dest='tests', 
                        default=['main_handler'],
                        help='run a bunch of example data')
    
    args = parser.parse_args()
    try:
        locals()['ctest_' + args.tests]()
    except KeyError:
        logging.error('No such tests, check again')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('Exception')

