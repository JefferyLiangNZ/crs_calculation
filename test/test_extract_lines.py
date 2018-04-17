import pytest
from extract_lines import chklines_collection

@pytest.fixture(scope="module")
def rawtext_case1():
    return """\
11096|C184|AUTH|PASS|5195571|
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:           78

Number of parameters:             44

Degrees of freedom:               34

Standard error of unit weight:     0.41
|"""


@pytest.fixture(scope="module")
def rawtext_case2():
    return """11096|C184|AUTH|PASS|5195570||"""

@pytest.fixture(scope="module")
def rawtext_case3():
    return '''11096|C184|AUTH|FAIL|5195570|
\
==============================================================================
\
ADJUSTMENT SUMMARY
\
==============================================================================
\
\
Number of observations:           78
\
\
Number of parameters:             44
\
\
Degrees of freedom:               34
\
\
Standard error of unit weight:     0.41
\
\
|'''

def test_chklines_collection_case1(rawtext_case1):
    
    # assert response == 250
    sample = chklines_collection(rawtext_case1)

    assert sample.wrk_id 	== '11096'
    assert sample.chi_code  == 'C184'
    assert sample.exec_stag == 'AUTH'
    assert sample.result	== 'PASS'
    assert sample.ref_id	== '5195571'
    print ">>", repr(sample.summary_txt)
    assert sample.summary_txt == """
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:           78

Number of parameters:             44

Degrees of freedom:               34

Standard error of unit weight:     0.41
"""


def test_chklines_collection_case2(rawtext_case2):
    
    sample = chklines_collection(rawtext_case2)
    assert sample.wrk_id    == '11096'
    assert sample.chi_code  == 'C184'
    assert sample.exec_stag == 'AUTH'
    assert sample.result    == 'PASS'
    assert sample.ref_id    == '5195570'
    assert sample.summary_txt == ''

def test_chklines_collection_case3(rawtext_case3):
    
    # assert response == 250
    sample = chklines_collection(rawtext_case3)

    assert sample.summary_txt == '''
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================
Number of observations:           78
Number of parameters:             44
Degrees of freedom:               34
Standard error of unit weight:     0.41
'''
