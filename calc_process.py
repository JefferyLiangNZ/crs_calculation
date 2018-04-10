
from collections import OrderedDict, namedtuple

from extract_fields import match_dict

from extract_fields import extract_metrics, extract_context, \
    extract_context_testblock_title, \
    extract_context_testblock, \
    extract_testblock_ruleitem_proc, \
    extract_context_testblock_rulestat

import re
from StringIO import StringIO

wac_wrk_chk_item = namedtuple('wac_wrk_chk', \
    ['wrk_id', 'chi_code', 'exec_staq', 'result', 'ref_id', 'summary_txt'] + match_dict.keys())

wac_wrk_rule_test_item = namedtuple('wac_wrk_chk', \
    ['reg_ver', 'reg_desc', 'rule_title', 'rule_desc', 'rule_block'])

wac_rule_test_stats_item = namedtuple('wac_wrk_chk', \
    ['chk_id', 'rule_id', 'obn_cnt', 'fail_cnt', 'ratio'])

skip_stats = {}

test_rule_stats = {}

class waca_base():
    def __init__(self):
        self.store = OrderedDict()

    def output(self):
        bb = StringIO()
        for key, item in self.store.items():
             bb.write('{},{}\n'.format(str(key), str(item)))
        print 'output', len(self.store.keys())
        return bb.getvalue()

class wac_rule_test_stats(waca_base):
    def __init__(self):
        # super.__init__(self)
        waca_base.__init__(self)
        # self.store    = OrderedDict()
        self.__init_seq = 29999

    def __next_key(self):
        self.__init_seq += 1
        return self.__init_seq


    def append(self, chk_id, rule_id, obn_cnt, fail_cnt, ratio):

        store_key = self.__next_key()
        print chk_id, 'append>>>>>>>>>>>>>>>>>>>>>>'

        self.store[store_key] = wac_rule_test_stats_item(chk_id, rule_id, obn_cnt, fail_cnt, ratio)
        print '++ + ', store_key, len(self.store.keys())
        return store_key


class wac_rule_test(waca_base):
    def __init__(self):
        waca_base.__init__(self)
        self.__init_seq = 99
        self.__unique_value_pool = {}        

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
            print '++ + '*2, self.store[(reg_ver, reg_desc, rule_title, rule_desc)]
            return store_key


class wac_wrk_chk(waca_base):
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
            print "skip:" #'{}->{}'.format(regulation_ver, testrule_block.replace('\n', '').replace('----', '-'))
            continue

        wrk_testrule_fk_id = wrk_testrule_obj.append(regulation_ver, regulartion_desc, rule_title, rule_descr, testrule_block[:240])
        # print wrk_testrule_fk_id, 'FK_ID', wrk_chk_fk_id

        try:
            applied_cnt, total_cnt = extract_context_testblock_rulestat(testrule_block)
            wac_rule_test_stats_obj.append(wrk_chk_fk_id, wrk_testrule_fk_id, applied_cnt, total_cnt, 0.0)
        except ValueError:
            print "VALUE=>", source
            print "\n<=Value\n"
            break
        except Exception as e:
            print e

        print '\n\n', testrule_block, applied_cnt, total_cnt
        # # print rule_title, rule_descr
        # test_rule_stats.add((rule_title, rule_descr, regulation_ver, regulartion_desc))

    # all_test_rules = [ xitem.split('\n')[0] for xitem in extract_context_testblock(rule_result_block) ]
    # check_list_item = (metrics_block, regulation_ver, regulartion_desc, all_test_rules)

    # summary_blocks = list(extract_blocks(test_file))
    # print '{} <-> {}'.format(cnt, len(check_list_items))
    # print 'last: {} '.format(check_list_items[-1])
    # print skip_stats

    # for key, item in test_rule_stats.iteritems():
    #     print "{:6d}|{:35s}|{:55s}|{:9s}|{}".format(item, key[0], key[1], key[2], key[3])

    # return {'rule_dict': test_rule_stats.keys(), 'check_list': check_list_items}
    



    # print test_rule_stats

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