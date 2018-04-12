from __future__ import absolute_import

import re
from StringIO import StringIO
import logging
from collections import ( OrderedDict, namedtuple )


from extract_fields import  \
(
    match_dict,
    extract_metrics, 
    extract_context, 
    extract_context_testblock_title, 
    extract_context_testblock, 
    extract_testblock_ruleitem_proc, 
    extract_context_testblock_rulestat,
    extract_context_testblock_rulestat_cognition
)


wac_wrk_chk_item = namedtuple('wac_wrk_chk', \
    ['wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'] + match_dict.keys())

wac_wrk_rule_test_item = namedtuple('wac_wrk_rule_test_item', \
    ['reg_ver', 'reg_desc', 'rule_title', 'rule_desc', 'rule_block'])

wac_rule_test_stats_item = namedtuple('wac_rule_test_stats_item', \
    ['chk_id', 'rule_id', 'fail_cnt', 'obn_cnt', 'ratio'])

skip_stats = {}

test_rule_stats = {}




class waca_base():
    def __init__(self):
        self.store = OrderedDict()

    @staticmethod
    def null_value_handler(data_dict):

        for key in data_dict.copy().keys():
            # print(key)
            # print(data_dict[key])
            # print('')
            if data_dict[key] is None:
                data_dict[key] = 'NULL'
            if isinstance(data_dict[key], str) and data_dict[key] == '':
                data_dict[key] = ' '

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

    def data_sqldump(self):

        with open(self.TABLE+'.sql', 'w') as wfile:

            round_up = 0
            for row in self.data_export():

                round_up = (round_up + 1) % 300
                base = StringIO()
                base.write('INSERT INTO waca.{}'.format(self.TABLE))
                base.write(' values ({});\n'.format(row))
                if row.find('NOTES') > 0:
                    print row
                    raise Exception
                wfile.write(base.getvalue())
                if round_up == 1:
                    wfile.write('COMMIT;\n')




class wac_rule_test_stats(waca_base):
    TABLE = 'wac_test_rule_stats'
    def __init__(self):
        # super.__init__(self)
        waca_base.__init__(self)
        # self.store    = OrderedDict()
        self.__init_seq = 29999

    def __next_key(self):

        self.__init_seq += 1
        return self.__init_seq

    def append(self, chk_id, rule_id, fail_cnt, obn_cnt, ratio):

        store_key = self.__next_key()
        self.store[store_key] = wac_rule_test_stats_item(chk_id, rule_id, fail_cnt, obn_cnt, ratio)
        # print '++ + ', store_key, len(self.store.keys())
        return store_key

    def data_export(self):

        for key, item in self.store.items():
            data_dict = item._asdict()
            data_dict.update({'id': key })
            yield "{id}, {chk_id}, {rule_id}, {fail_cnt}, {obn_cnt}, {ratio}".format(**data_dict)

        print(len(self.store))

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
            # print "===>Reuse : {:9s} {:25s} {:8s} {}".format(reg_ver, reg_desc, rule_title, rule_desc), \
            # '==>Match{}'.format(self.store[(reg_ver, reg_desc, rule_title, rule_desc)][0]) 
            # print self.store[(reg_ver, reg_desc, rule_title, rule_desc)][1], "\n<==rule_context"

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

        print(len(self.store))

class wac_wrk_chk(waca_base):
    TABLE = 'wac_wrk_check_list'       
    # Specify the crs_check_entity namedtuple.
    def __init__(self):
        waca_base.__init__(self)        
        # self.store    = OrderedDict()
        self.__init_seq = 1999
        self.__ref_id_pool = {}

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
            base = metrics.copy()
            base.update(record._asdict())
            try:
                self.store[store_key] = wac_wrk_chk_item(**base)
            except:
                print metrics
                print base
        else:
            base = {'obn_cnt': None, 'prm_cnt': None, 'free_dg': None, 'std_err':None}
            base.update(record._asdict())
            self.store[store_key] = wac_wrk_chk_item(**base)

        store_item = self.store[store_key]
        # print store_key, store_item.wrk_id, store_item.chi_code, store_item.exec_staq, store_item.result, store_item.ref_id, store_item.obn_cnt, store_item.free_dg, ' --->'
        return store_key

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
            yield "{id}, {wrk_id}, '{chi_code}', '{exec_stag}', '{result}', {obn_cnt}, {prm_cnt}, {free_dg}, {std_err}, {ref_id}, '{summary_txt}' ".format(**data_dict)



def main_handler(record, wrk_chk_obj, wrk_testrule_obj, wac_rule_test_stats_obj):

    source = record.summary_txt
    source = re.sub(re.compile('NOTES(.|\n)+', re.M), '', source)

    test_rule_stats = set()

    wrk_chk_fk_id = wrk_chk_obj.append(record)
    # metrics_block = extract_metrics(source)
    # print metrics_block
    # print '\n## ' * 20
    # print record

    
    rule_result_block = extract_context(source)

    if rule_result_block is None:
        skip_stats['rule_result_block'] = skip_stats.get('rule_result_block', 0) + 1
        return

    # print rule_result_block.split('\n')[0]


    regulation_ver, regulartion_desc = extract_context_testblock_title(rule_result_block)

    for testrule_block in extract_context_testblock(rule_result_block+'\n'):
        
        # print testrule_block

        rule_title, rule_descr = extract_testblock_ruleitem_proc(testrule_block, rule_result_block)

        if not rule_title:
            # print '\n\n', rule_result_block
            # raw_input('>>')
            logging.warn('Test rule skipped - because:{}->{}'.format(regulation_ver, testrule_block.replace('\n', '').replace('----', '-')))
            continue

        wrk_testrule_fk_id = wrk_testrule_obj.append(regulation_ver, regulartion_desc, rule_title, rule_descr, testrule_block[:240])
        # print wrk_testrule_fk_id, 'FK_ID', wrk_chk_fk_id

        try:
            applied_cnt, total_cnt, ratio = extract_context_testblock_rulestat_cognition(testrule_block)
            wac_rule_test_stats_obj.append(wrk_chk_fk_id, wrk_testrule_fk_id, applied_cnt, total_cnt, ratio)
        except ValueError:
            logging.error("Cant deduct from test rule results because: "+ source.replace('\n', ''))
            break
        except Exception as e:
            print e

        logging.info('{}'.format(testrule_block.strip().strip('\n')))

    # all_test_rules = [ xitem.split('\n')[0] for xitem in extract_context_testblock(rule_result_block) ]
    # check_list_item = (metrics_block, regulation_ver, regulartion_desc, all_test_rules)

    # summary_blocks = list(extract_blocks(test_file))

    '''
    for matches in summary_blocks:
        # print blk[:600], '>>>', blk[-100:]
        sequence = matches.groups(0)

        print re.sub(re.compile('\r+', re.MULTILINE), '\n', sequence[0])
        # print sequence[1]
        # print sequence[2]
        print '\n\n\n\####################################n'
        raw_input('--next--\n')
    # files_content_collection = extract_numeric_fields(test_file)
    '''

if __name__ == '__main__':

    test_file = 'temp_chk_results.txt'
    with open(test_file, 'r') as rfile:
        text = rfile.read()
        cnt = 0
        check_list_items = []

        for block in extract_blocks(text):

            cnt += 1
            summary_handler(block)
