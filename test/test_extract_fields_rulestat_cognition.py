from __future__ import print_function
from __future__ import division
import pytest

from extract_fields import extract_context_testblock_rulestat_cognition
import re

"""
#################################3

       602    2 observations could not be tested (rejected from adjustment)
     16380    2 observations were not tested (rejected from adjustment)
      1826    2 vectors could not be tested (rejected from adjustment)
      3181    Test achieved required 2.2% pass rate
      4126    Test did not achieve 2.2% pass rate
     93674    Tested at 2 marks of which 2 failed
    808027    Tested for 2 observations of which 2 failed
    317093    Tested for 2 vectors of which 2 failed
      3618    Test failed for 2 of 2 applicable marks
      2040    Test failed for 2 of 2 marks
      5701    Test failed for 2 of 2 observations
      1119    Test failed for 2 of 2 vectors
      6992    Test passed for 2 marks
     11841    Test passed for all 2 applicable marks
    270755    Test passed for all 2 observations
    135400    Test passed for all 2 vectors
    490427    This test was not used in the survey


#########################################################
"""
# Tested for 180 observations of which 2 failed
    # if result:
    #     if re.search(re.compile(match_pattern), source).groups()[3]:
    #         logging.debug('parsing {} '.format(source))

    #     filter(lambda x: bool(x), result.groups())[0]
    #     return filter(lambda x: bool(x), result.groups())[0]

samplerule_stats = {
    'Tested for 180 observations of which 2 failed': 
    ("""Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 180 observations of which 2 failed""",
        ('2', '180', '1.111')
    ),

    'Test failed for 3 of 98 observations':
    ("""Test: Rule 3.7 and Rule 3.3.1a(ii): Residual of all obs between boundary marks including adopted marks
    Test failed for 3 of 98 observations
    The worst failures are:
        Residual on ellipsoidal distance (length 184.38) is 2.2 times tolerance """,
        ('3', '98', '3.061')
    ),
    
    '2 of 180 observations did not meet accuracy requirement':
    ("""Test: Rule 3.7 and Rule 3.1(a): Residual of obs between all new and old non-boundary marks excluding adopted marks
    Test did not achieve 95.0% pass rate
    2 of 180 observations did not meet accuracy requirement
    The worst failures are: Residual on ellipsoidal distance (length 6.22) is 1.9 times tolerance""", 
        ('2', '180', '1.111')
    ),

    '178 of 180 observations meet accuracy requirement':
    ("""Test: Rule 3.7 and Rule 3.3.1a(i): Residual of 95% of obs between boundary marks (RSS) excluding adopted marks
    Test achieved required 95.0% pass rate
    178 of 180 observations meet accuracy requirement""", 
        ('2', '180', '1.111')
    ),

    'Test passed for 0 marks':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Test passed for 0 marks""",
        ('0', '0', '100')
    )


}
    # return test_inputs[request.param]
samplerule_stats_cases = [(key, item[1]) for key, item in samplerule_stats.items()]

@pytest.mark.parametrize("case_key,expected", samplerule_stats_cases)
def test_context_testblock_rulestat_cognition(case_key, expected):
    source, _ = samplerule_stats[case_key]
    assert extract_context_testblock_rulestat_cognition(source) == expected



