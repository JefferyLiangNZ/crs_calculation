from __future__ import print_function
from __future__ import division
import pytest

from extract_fields import extract_context_testblock_rulestat_cognition

# the following method shouldn't be used independently
from extract_fields import extract_context_testblock_rulestat_cognition_inner_fn
# end

import re

"""

The text/description of test rule results are enumerated from the data dump files

#########################################################

       602    2 observations could not be tested (rejected from adjustment)
     16380    2 observations were not tested (rejected from adjustment)
      1826    2 vectors could not be tested (rejected from adjustment)

              All observations were better than 2.2 times allowable error
              All observations were better than 2.2 times allowable misclose
              All vectors were better than 2.2 times allowable error
              More than the required 2.2% passed
              Test achieved required 2.2% pass rate
              Test did not achieve 2.2% pass rate

#########Above situation is excluded from results #########

 The first numer is the count of occurances, besides, 2 represents one or more digits

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


samplerule_stats = {
    'Tested for 180 observations of which 2 failed': 
    ("""Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
    Tested for 180 observations of which 2 failed""", 
        220,
        ('2', '180', '1.111')
    ),

    'Test failed for 3 of 98 observations':
    ("""Test: Rule 3.7 and Rule 3.3.1a(ii): Residual of all obs between boundary marks including adopted marks
    Test failed for 3 of 98 observations
    The worst failures are:
        Residual on ellipsoidal distance (length 184.38) is 2.2 times tolerance """, 
        220,
        ('3', '98', '3.061')
    ),
    
    '2 of 180 observations did not meet accuracy requirement':
    ("""Test: Rule 3.7 and Rule 3.1(a): Residual of obs between all new and old non-boundary marks excluding adopted marks
    Test did not achieve 95.0% pass rate
    2 of 180 observations did not meet accuracy requirement
    The worst failures are: Residual on ellipsoidal distance (length 6.22) is 1.9 times tolerance""",
        220,
        ('2', '180', '1.111')
    ),

    '178 of 180 observations meet accuracy requirement':
    ("""Test: Rule 3.7 and Rule 3.3.1a(i): Residual of 95% of obs between boundary marks (RSS) excluding adopted marks
    Test achieved required 95.0% pass rate
    178 of 180 observations meet accuracy requirement""", 
        220,
        ('2', '180', '1.111')
    ),

    'This test was not used in the survey':
    ("""Test: Reg 13.b.ii: Proximity of natural boundary fix to witness marks
    This test was not used in the survey""", 
        220,
        ('0', '0', '0.000')
    ),

    'Test passed for 0 marks':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Test passed for 0 marks""", 
        20,
        ('20', '20', '100.000')
    ),

    'Test passed for all 120 vectors':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Test passed for all 120 vectors""", 
        120,
        ('0', '120', '0.000')
    )    
}


samplerule_stats_inner = {
    'Tested for 180 observations of which 2 failed': 
    ("""Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
    Tested for 180 observations of which 2 failed""", 
        220,
        {'FAIL':'2', 'SUM':'180'}
    ),

    'Test passed for 0 marks':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Test passed for 0 marks""", 
        20,
        {'PASS':'0', 'SUM':'20'}
    ),

    'Test passed for all 120 vectors':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Test passed for all 120 vectors""", 
        120,
        {'PASS':'120', 'SUM':'120'}
    ),

    'Tested at 180 marks of which 2 failed':
    ("""Test: Rule 3.6 and 7.3.2a: Boundary mark defined by survey requires a witness mark within 150 m
    Tested at 180 marks of which 2 failed""", 
        220,
        {'FAIL':'2', 'SUM':'180'}
    ),

    'This test was not used in the survey':
    ("""Test: Reg 13.b.ii: Proximity of natural boundary fix to witness marks
    This test was not used in the survey""", 
        220,
        {'SUM':'0'}
    ),
}

samplerule_stats_cases = [(key, item[2]) for key, item in samplerule_stats.items()]

samplerule_stats_inner_cases = [(key, item[2]) for key, item in samplerule_stats_inner.items()]

@pytest.mark.parametrize("case_key,expected", samplerule_stats_inner_cases)
def test_extract_context_testblock_rulestat_cognition_inner_fn(case_key, expected):
    source, extra, _ = samplerule_stats_inner[case_key]
    assert sorted(extract_context_testblock_rulestat_cognition_inner_fn(source, extra).items()) == \
        sorted(expected.items())


@pytest.mark.parametrize("case_key,expected", samplerule_stats_cases)
def test_context_testblock_rulestat_cognition(case_key, expected):
    source, extra, _ = samplerule_stats[case_key]
    assert extract_context_testblock_rulestat_cognition(source, extra) == expected

