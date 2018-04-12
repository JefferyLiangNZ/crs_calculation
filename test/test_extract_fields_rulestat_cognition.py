from __future__ import print_function
from __future__ import division
import pytest

from extract_fields import extract_context_testblock_rulestat_cognition
import re


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


}
    # return test_inputs[request.param]
samplerule_stats_cases = [(key, item[1]) for key, item in samplerule_stats.items()]

@pytest.mark.parametrize("case_key,expected", samplerule_stats_cases)
def test_context_testblock_rulestat_cognition(case_key, expected):
    source, _ = samplerule_stats[case_key]
    assert extract_context_testblock_rulestat_cognition(source) == expected



