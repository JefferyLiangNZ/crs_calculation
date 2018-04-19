import pytest


__doc__ = """ 
A description that contains several regulation blocks, which means

self = [ADJUSTMENT SUMMARY] |
       [SUMMARY OF REGULATION TESTS: =
            [Testing regulations:
                [Test: 
                    Test rule code: Test rule description
                    Test fail number / Total test cases number
                    Test error range 1
                    Test error range 2
                    Test error range 3
                    ...
                ]
                [Test: 
                    Test rule code: Test rule description
                    Test fail number / Total test cases number
                    Test error range 1      
                ]
                [Test: 
                    Test rule code: Test rule description
                    Test fail number / Total test cases number
                    Test error range 1
                    Test error range 2
                ]
            ]
            [Testing regulations:]
            [Testing regulations:]
       ]

"""

# for cases that has multiple test rule under a single Test regulation
# while there is only one regulation
SAMPLE_A = """
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
SAMPLE_TA = """2073|11249|C184|AUTH|FAIL|762|244|518|116.69|8608666|""" + SAMPLE_A


# for cases that  multiple Test regulation
# for cases that there are multiple Test regulations
# and there is only one test rule for each test regulation
#
SAMPLE_B = """
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          111

Number of parameters:             50

Degrees of freedom:               61

Standard error of unit weight:     0.71

==============================================================================
SUMMARY OF REGULATION TESTS
==============================================================================

Testing regulations: Information only: Class 4 data tested against Class 3 regulations

Test: Reg 26.2.a.i: Relative accuracy of boundary marks
  This test was not used in the survey

----------------------------------------------------------------------

Testing regulations: Information only: Class IV data tested against Class III regulations

Test: Reg 26.2.a.ii: Relative accuracy of boundary marks
  Tested for 2 observations of which 0 failed
  All observations were better than 0.23 times allowable misclose

----------------------------------------------------------------------

Testing regulations: Surveyor-General`s Rules 2002/2 for class I surveys

Test: Reg 28 and 26.2.a.i: Misclose of obs1 between boundary marks
   Tested for 2 observations of which 0 failed
   All observations were better than 0.13 times allowable misclose

----------------------------------------------------------------------

Testing regulations: Surveyor-General`s Rules 2002/2 for class II surveys

Test: Reg 28 and 26.2.b.i: Misclose of obs2 between boundary marks
  Tested at 29 marks of which 0 failed

----------------------------------------------------------------------

Testing regulations: Surveyor-General`s Rules 2002/2 for class III surveys

Test: Reg 26.2.c.i: Relative accuracy and proximity of boundary marks to witness marks
  Tested for 946 vectors of which 243 failed
  The worst failures are:
     Vector from Node ID 22465286 (Id 22465286)to PEG SO 8804 (Id 36856076) is 1.8 times tolerance
     Vector from Node ID 22465286 (Id 22465286)to PEG 77A SO 8804 (Id 36856077) is 1.8 times tolerance

----------------------------------------------------------------------

Testing regulations: Information only: Class IV data tested against Class III regulations

Test: Reg 28 and 26.2.c.i: Relative accuracy of boundary marks to origins
  Tested for 66 vectors of which 0 failed
  All vectors were better than 0.22 times allowable error
  1 vectors could not be tested (rejected from adjustment)

----------------------------------------------------------------------

Testing regulations: Information only: Class 4 data tested against Class 3 regulations

Test: Reg 26.2.a.iv: Relative accuracy of witness/traverse/origin marks
  Tested for 21 vectors of which 9 failed
  The worst failures are:
     Vector from RM 6 SO 35242 (Id 36926598)to IT III DP 58426 (Id 36926599) is 1.3 times tolerance
     Vector from IR I DP 87110 (Id 36926595)to IT III DP 58426 (Id 36926599) is 1.2 times tolerance


"""


__all__ = [SAMPLE_A, SAMPLE_B]