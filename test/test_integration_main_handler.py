import pytest
from calc_process import (main_handler, wac_wrk_chk_item)

from conftest import (SAMPLE_A, SAMPLE_B)

def record_case1():
    # 'wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'
    return wac_wrk_chk_item(1, '1', '1', '1', 1, SAMPLE_A, 0, 0, 0, '0')


def record_case2():
    # 'wrk_id', 'chi_code', 'exec_stag', 'result', 'ref_id', 'summary_txt'
    return wac_wrk_chk_item(1, '1', '1', '1', 1, SAMPLE_B, 0, 0, 0, '0')


@pytest.mark.parametrize("record", [record_case2(), ])
def test_embed_main_handler_c2(record):
    def f1(_):
        pass

    class f2c():
        expected = [
            (
                'INFO-4',
                "Information only: Class 4 data tested against Class 3 regulations",
                'Reg 26.2.a.i',
                'Relative accuracy of boundary marks',
            ),

            (
                'INFO-IV',
                "Information only: Class IV data tested against Class III regulations",
                'Reg 26.2.a.ii',
                'Relative accuracy of boundary marks',
            ),
            (
                '2002/2-I',
                "Surveyor-General`s Rules 2002/2 for class I surveys",
                'Reg 28 and 26.2.a.i', 
                'Misclose of obs1 between boundary marks'
            ),            
            (
                '2002/2-II',
                'Surveyor-General`s Rules 2002/2 for class II surveys',
                'Reg 28 and 26.2.b.i', 
                'Misclose of obs2 between boundary marks'
            ),
            (
                '2002/2-III',
                'Surveyor-General`s Rules 2002/2 for class III surveys',
                'Reg 26.2.c.i',
                'Relative accuracy and proximity of boundary marks to witness marks'
            ),
            (
                '2002/2-IV',
                'Information only: Class IV data tested against Class III regulations',
                'Reg 28 and 26.2.c.i', 
                'Relative accuracy of boundary marks to origins'
            ),
            (
                '2002/2-4',
                'Information only: Class 4 data tested against Class 3 regulations',
                'Reg 26.2.a.iv', 
                'Relative accuracy of witness/traverse/origin marks'
            )
        ]

        count = 0
        @staticmethod
        def append(*args):

            res = f2c.expected.pop(0)
            f2c.count += 1

            regulation_ver, regulartion_desc, rule_title, rule_descr, testrule_block = args
            print((regulation_ver, regulartion_desc, rule_title, rule_descr))
            assert (regulation_ver, regulartion_desc, rule_title, rule_descr) == res

            print(">> Pass for case {}".format(f2c.count))

    class f3c():
        called_with_param = []

        @staticmethod
        def append(*args):
            f3c.called_with_param.append(args)

    main_handler(record, f1, f2c.append, f3c.append)


@pytest.mark.parametrize("record", [record_case1(), ])
def test_embed_main_handler_c1(record):
    f1_expected = SAMPLE_A

    def f1(source):
        print repr(source.summary_txt)
        assert source.summary_txt == f1_expected

    class f2c():
        called_with_param = []
        expected = [
            (
                '2002/2', 
                "Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey", 
                'Reg 28 and 26.2.a.i', 
                'Misclose of obs between boundary marks', 
            ),
            (
                '2002/2', 
                "Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey", 
                'Reg 28 and 26.2.a.ii', 
                'Misclose of obs from boundary marks to witness marks'
            ),
            (
                '2002/2', 
                "Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey", 
                'Reg 28 and 26.2.a.iii', 
                'Misclose of obs from boundary marks to origins'
            ),
            (
                '2002/2', 
                "Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey", 
                'Reg 28 and 26.2.a.iv', 'Misclose of obs between witness/traverse/origin marks'
            )            
        ]

        @staticmethod
        def append(*args):
            print('f2c(args) ---->')
            regulation_ver, regulartion_desc, rule_title, rule_descr, testrule_block = args


            f2c.called_with_param.append((regulation_ver, regulartion_desc, rule_title, rule_descr))

            print((regulation_ver, regulartion_desc, rule_title, rule_descr))
            assert (regulation_ver, regulartion_desc, rule_title, rule_descr) in f2c.expected

    class f3c():
        called_with_param = []

        @staticmethod
        def append(*args):
            # assert source in ('', )
            # print(source)
            f3c.called_with_param.append(args)

    main_handler(record, f1, f2c.append, f3c.append)