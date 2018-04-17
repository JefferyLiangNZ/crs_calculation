from __future__ import print_function
from __future__ import division
import pytest

from extract_fields import extract_context_testblock_rulestat_error
import re

samplerule_stats = {
    'better than x times allowable misclose': 
    ("""Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 180 observations of which 2 failed
   All observations were better than 0.31 times allowable misclose""",
        '0.31'
    ),

    'All observations were better than x times tolerance':
    ("""Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 170 observations of which 2 failed
   All observations were better than 0.31 times tolerance""",
        '0.31'
    ),

    '(bearing blah blah) is x times tolerance':
    ("""Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)""",
          '1.4'
     )
}

    # return test_inputs[request.param]
samplerule_stats_cases = [(key, item[1]) for key, item in samplerule_stats.items()]

@pytest.mark.parametrize("case_key,expected", samplerule_stats_cases)
def test_extract_context_testblock_rulestat_error(case_key, expected):
    source, _ = samplerule_stats[case_key]
    assert extract_context_testblock_rulestat_error(source) == expected