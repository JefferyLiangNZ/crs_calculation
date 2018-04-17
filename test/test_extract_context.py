from __future__ import print_function
from __future__ import division
import pytest

from extract_fields import extract_context, extract_context_testblock_title, extract_context_testblock
import re


@pytest.fixture(scope="module")
def source_extract_context():
  return """
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          704

Number of parameters:            309

Degrees of freedom:              395

Standard error of unit weight:     0.96

==============================================================================
SUMMARY OF REGULATION TESTS
==============================================================================

Testing regulations: Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey

Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)

Test: Reg 28 and 26.2.a.ii: Misclose of obs from boundary marks to witness marks
   Tested for 12 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 16 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iv: Misclose of obs between witness/traverse/origin marks
   Tested for 38 observations of which 1 failed
   The worst failures are:
      Misclose on ellipsoidal distance (length 201.32) is 1.1 times tolerance
          Obs is from SS BLK A SO 7872 (id 36760509) to SS BLK C SO 7872 (id 36751619)

"""

def test_extract_context(source_extract_context):

  assert extract_context(source_extract_context) == """\
Testing regulations: Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey

Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)

Test: Reg 28 and 26.2.a.ii: Misclose of obs from boundary marks to witness marks
   Tested for 12 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 16 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iv: Misclose of obs between witness/traverse/origin marks
   Tested for 38 observations of which 1 failed
   The worst failures are:
      Misclose on ellipsoidal distance (length 201.32) is 1.1 times tolerance
          Obs is from SS BLK A SO 7872 (id 36760509) to SS BLK C SO 7872 (id 36751619)\
"""


@pytest.fixture(scope="module")
def source_extract_context_testblock_title1():

  return """\
Testing regulations: Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey

Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)\
"""

@pytest.fixture(scope="module")
def source_extract_context_testblock_title2():

  return """\
Testing regulations: 1999 Survey regulations for class 3 surveys

Test: Reg 26.2.c.i: Relative accuracy of boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
"""

def test_extract_context_testblock_title(source_extract_context_testblock_title1):
  res = extract_context_testblock_title(source_extract_context_testblock_title1)
  assert res[0] == '2002/2'
  assert res[1] == 'Information only - the Surveyor-General\'s Rules 2002/2 do not apply to this survey'

def test_extract_context_testblock_title(source_extract_context_testblock_title2):
  res = extract_context_testblock_title(source_extract_context_testblock_title2)
  assert res[0] == '1999-3'
  assert res[1] == '1999 Survey regulations for class 3 surveys'

@pytest.fixture(scope="module")
def source_extract_context_testblock():
  return """\
Testing regulations: Information only - the Surveyor-General's Rules 2002/2 do not apply to this survey

Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)

Test: Reg 28 and 26.2.a.ii: Misclose of obs from boundary marks to witness marks
   Tested for 12 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 16 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose

Test: Reg 28 and 26.2.a.iv: Misclose of obs between witness/traverse/origin marks
   Tested for 38 observations of which 1 failed
   The worst failures are:
      Misclose on ellipsoidal distance (length 201.32) is 1.1 times tolerance
          Obs is from SS BLK A SO 7872 (id 36760509) to SS BLK C SO 7872 (id 36751619)\
"""

def test_extract_context_testblock(source_extract_context_testblock):
  res = extract_context_testblock(source_extract_context_testblock)

  assert res[0] == """\
Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
   Tested for 24 observations of which 3 failed
   The worst failures are:
      Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 75.38) is 1.2 times tolerance
          Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
      Misclose on ellipsoidal distance (length 140.94) is 1.1 times tolerance
          Obs is from PEG DP 5284 (id 22288902) to PEG DEED 306 (id 22232881)\
"""

  assert res[1] == """\
Test: Reg 28 and 26.2.a.ii: Misclose of obs from boundary marks to witness marks
   Tested for 12 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose\
"""
  assert res[2] == """\
Test: Reg 28 and 26.2.a.iii: Misclose of obs from boundary marks to origins
   Tested for 16 observations of which 0 failed
   All observations were better than 0.69 times allowable misclose\
"""
  assert res[3] == """\
Test: Reg 28 and 26.2.a.iv: Misclose of obs between witness/traverse/origin marks
   Tested for 38 observations of which 1 failed
   The worst failures are:
      Misclose on ellipsoidal distance (length 201.32) is 1.1 times tolerance
          Obs is from SS BLK A SO 7872 (id 36760509) to SS BLK C SO 7872 (id 36751619)\
"""