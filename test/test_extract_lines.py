from extract_lines import chklines_collection

def test_chklines_collection_four_items(rawtext_case1):
    
    # assert response == 250
    result = list(chklines_collection(rawtext_case1))
    sample = result[0]

    assert len(result) 		== 4
    assert sample.wrk_id 	== '11096'
    assert sample.chi_code  == 'C184'
    assert sample.exec_staq == 'AUTH'
    assert sample.result	== 'UNTD'
    assert sample.ref_id	== '5195569'
    print ">>", repr(sample.summary_txt)
    assert sample.summary_txt == """
Not enough information to calculate node POST SO 20083 (39247071)
Node automatically rejected from the adjustment

"""


    sample = result[-1]
    assert sample.wrk_id 	== '11046'
    assert sample.chi_code	== 'C184'
    assert sample.exec_staq	== 'AUTH'
    assert sample.result	== 'UNTD'
    assert sample.ref_id	== '51955672'
    assert sample.summary_txt == ''


def test_chklines_collection_one_item(rawtext_case2):
    
    # assert response == 250
    result = list(chklines_collection(rawtext_case2))
    assert len(result) == 1
    print result[0].summary_txt

    assert result[0].summary_txt == '''
==============================================================================
ADJUSTMENT SUMMARY
==============================================================================
Number of observations:           78
Number of parameters:             44
Degrees of freedom:               34
Standard error of unit weight:     0.41
'''

def test_chklines_collection_zero_item(rawtext_case3):
    
    # assert response == 250
    result = list(chklines_collection(rawtext_case3))
    assert len(result) == 0
