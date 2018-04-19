from __future__ import generators, division, print_function

import re
import traceback
import sys
import logging


#[item for item in vars(extract_fields).keys() if iscallable(vars(extract_fields)[item])]

"""
################################################

  Utilities functions for extracting different fields in the test result block
  

Exception Class:

    RuleExp
    RulestatsExp
    ChecklistExp
    
Ultities methods:



    extract_blocks  
    extract_context

    extract_metrics
    
    extract_context_regtest_block
    extract_context_regtest_title
    extract_context_regtest_title_regver

    extract_context_testblock
    extract_context_testblock_rule_recognizer

    extract_context_testblock_rulestat    
    extract_context_testblock_rulestat_error
    extract_context_testblock_rulestat_cognition
    extract_context_testblock_rulestat_cognition_inner_fn (not to be used externally)

################################################
"""

class RulestatsExp(Exception):
    pass

class RuleExp(Exception):
    pass

class ChecklistExp(Exception):
    pass

metrics_dict = {
    'obn_cnt': r'Number of observations:\s+([\d\.]+)',
    'prm_cnt': r'Number of parameters:\s+([\d\.]+)',
    'free_dg': r'Degrees of freedom:\s+([\d\.]+)',
    'std_err': r'Standard error of unit weight:\s+(?:-)?([\d\.]+)' 
}



def extract_blocks(text):

    splitter = r'(ADJUSTMENT\s.*)'
    if text is None:
        return

    for matches in re.finditer(splitter, text, flags=re.M):
        sequence = matches.groups(0)
        # results.append(re.sub(re.compile('\r+', re.MULTILINE), '\n', sequence[0]))
        yield re.sub(re.compile('\r+', re.MULTILINE), '\n', sequence[0])


def extract_metrics(source):
    """ 
    extract the four test metrics (observation count, param count, degrees, standard error)
    """
    result_dict = {}
    for key, pattern in metrics_dict.iteritems():
        if re.search(pattern, source, re.M):
            result_dict[key] = re.search(pattern, source, re.M).group(1)
     
    return result_dict


def extract_context(source):
    """
    Extract the detail results from 'SUMMARY OF REGULATION TESTS', the result should looks like
    ---
    Testing regulations: 1998 Survey regulations for class 3 surveys

    Test: Reg 28 and 26.2.c.i: Misclose of obs between boundary marks
       Tested for 78 observations of which 0 failed
       All observations were better than 0.51 times allowable misclose

    Test: Reg 28 and 26.2.c.ii: Misclose of obs from boundary marks to witness marks
       Tested for 52 observations of which 2 failed
       The worst failures are:
          Misclose on ellipsoidal distance (length 43.87) is 1.4 times tolerance
              Obs is from IR V DP 82633 (id 37822117) to Node ID 24091110 (id 24091110)
          Misclose on projection bearing (bearing 279 57 00) is 1.2 times tolerance
              Obs is from IR V DP 82633 (id 37822117) to Node ID 23627670 (id 23627670)

    Test: Reg 28 and 26.2.c.iii: Misclose of obs from boundary marks to origins
       Tested for 12 observations of which 0 failed
       All observations were better than 0.16 times allowable misclose

    Test: Reg 28 and 26.2.c.iv: Misclose of obs between witness/traverse/origin marks
       Tested for 86 observations of which 5 failed
       The worst failures are:
          Misclose on projection bearing (bearing 359 40 00) is 2.5 times tolerance
              Obs is from IT IX DP 7383 (id 555729) to 33 (Mairaki SD) (id 36738901)
        ---

    """
    processed = source.replace('\r', '').replace('=', '')
    match_pattern = r'(?:SUMMARY OF REGULATION TESTS)'
    matched_groups = re.split(re.compile(match_pattern, re.M), processed, 6)
    matched_items = [x.strip('\n') for x in matched_groups if x.strip('\n').startswith('Testing')]

    if matched_items:
        return matched_items[0]
    else:
        logging.error("\nNo testing rules section get matched:\n\t\t"+ source)


def extract_context_regtest_block(source):

    match_pattern = r'(Testing regulations:(?:.|\n)*?)(\s|-)*(?=Testing regulations\:|$)'
    try:
        return [item[0] for item in re.findall(re.compile(match_pattern), source)]
    except Exception as e:
        logging.error("\n(regtest not found) In extract_context_regtest_block:"+ source)
        raise RuleExp(str(e)+"\n(testblock not found) In extract_context_testblock:\n\t\t"+ source)


def extract_context_testblock(source):

    match_pattern = r'(Test:(?:.|\n)*?)\s*(?=Test:|$)'

    try:
        return re.findall(re.compile(match_pattern), source)
    except Exception as e:
        logging.error("\n(testblock not found) In extract_context_testblock:"+ source)
        raise RuleExp(str(e)+"\n(testblock not found) In extract_context_testblock:\n\t\t"+ source)


def extract_context_regtest_title(source, version_context):

    match_pattern = r'Testing regulations:\s(.+)'
    try:
        rule_version_description = re.match(re.compile(match_pattern), source).group(1)
        # print(rule_version_description)
        reg_version = extract_context_regtest_title_regver(rule_version_description, version_context)
        return (reg_version, rule_version_description, )
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        logging.error("\n(title not found) In extract_context_testblock_title:"+ source)
        raise e


def extract_context_regtest_title_regver(source, version_context):
    """
    Extract the year(version) and class(I,II,III/A,B,C ) from "source"
    Try as much as possible to use the source, only use "context indication" -  version_context 
    when year info is unavailable/not provided

    @param source(str)          -   
    @param version_context(str) -
    @output "2002/2-A" or "1998-II" or "INFO" or "INFO-B" or "1998"
    ----

    """

    capture_survery_version_pattern = r'([\d\/]{4,})'
    capture_survey_type_pattern =r'class\s(\w+)\s(surveys|data)'
    reg_version = []
    
    year_version_matched = re.search(re.compile(capture_survery_version_pattern), source)
    if year_version_matched:
        reg_version.append(year_version_matched.group(1))
    elif version_context and not reg_version: 
        # current source has no year info but 'year' can be found in previous test regulation
        reg_version.append(version_context)
    else:
        # current source has no year info and it is the first test regulation
        reg_version.append('INFO') # 
        logging.warn('\n Regulation detail version is missed:\n\t\t' + source)

    matched = re.search(re.compile(capture_survey_type_pattern, re.I), source)
    if matched:
        reg_version.append(matched.group(1))

    return '-'.join(reg_version)


# def extract_context_testblock_ruleitem(source):

def extract_context_testblock_rulestat_cognition_inner_fn(source, total_obn_cnt = 0):

    match_pass_pattern = r'Test passed for\s(?P<PASS>\d+)\s\w+'
    matched_pass_object = re.search(re.compile(match_pass_pattern), source)

    match_all_pass_pattern = r'Test passed for all\s(?P<SUM>\d+)\s\w+'
    match_all_pass_object = re.search(re.compile(match_all_pass_pattern), source)

    match_notest_pattern = 'test was not used'

    match_patterns = [
        r'Tested for\s(?P<SUM>\d+)\s\w+.*of which\s(?P<FAIL>\d+)\sfailed',
        r'Test failed for\s(?P<FAIL>\d+)\sof\s(?P<SUM>\d+)\s\w+',
        r'Tested at\s(?P<SUM>\d+)\smarks of which\s(?P<FAIL>\d+)\sfailed',
        r'(?P<FAIL>\d+)\sof\s(?P<SUM>\d+)\s\w+ did not meet accuracy requirement',
        r'(?P<PASS>\d+)\sof\s(?P<SUM>\d+)\s\w+ meet accuracy requirement'
    ]
    matched_objects = filter(lambda x: x, \
        [ re.search(re.compile(pattern), source) for pattern in match_patterns ])

    res = {}
    if match_notest_pattern in source:
        return {'SUM': '0'}

    if matched_objects:
        res = matched_objects[0].groupdict()

    if matched_pass_object:
        sum_cnt  = total_obn_cnt
        pass_cnt = int(matched_pass_object.group('PASS'))
        res.update({'SUM': str(sum_cnt), 'PASS': str(pass_cnt)})

    if match_all_pass_object:
        sum_cnt  = int(match_all_pass_object.group('SUM'))
        pass_cnt = int(match_all_pass_object.group('SUM'))
        res.update({'SUM': str(sum_cnt), 'PASS': str(pass_cnt)})

    return res


def extract_context_testblock_rulestat_cognition(source, total_obn_cnt = 0):
    """
    Source 
    extract the digital(as str) from source

    Specifically, the regex is designed to take out the pattern
    Test for 21 of which 1 failed -> 21, 1, 4.9

    """

    sum_cnt, fail_cnt, pass_cnt = 0, 0, 0
    res = {}
    # result = re.search(re.compile(match_pattern), source)
    try:    
        res = extract_context_testblock_rulestat_cognition_inner_fn(source, total_obn_cnt)
        if not res:
            return ("0", "0", "0.000")

        if not int(res['SUM']):
            logging.warn("Test sample's sum equals zero{}".format(source))
            return ("0", "0", "0.000")
    
    except KeyError as e:
         logging.error("{}\nCant recovered from parsing {} \nbecause the specified pattern is not found".format(str(e), source))
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         raise RulestatsExp("\n{}".format(str(e)))

    except ValueError as e:
         logging.error("{}\nCant recovered from parsing {} \nbecause the specified pattern is not found".format(str(e), source))
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         raise RulestatsExp("\n{}".format(str(e)))

    except Exception as e:

         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         raise RulestatsExp("Exception from: extract_context_testblock_rulestat_cognition\n {}".format(str(e)))

    try:
        sum_cnt = int(res['SUM'])

        if 'PASS' in res and res['PASS']:
            pass_cnt = int(res['PASS'])
            fail_cnt = sum_cnt - pass_cnt

        if 'FAIL' in res and res['FAIL']:
            fail_cnt = int(res['FAIL'])
    except:
        logging.error("searching in {}".format(str(res)))
        logging.error("Cant deduct from test rule results because: " + source)

    return ("%d" % fail_cnt, "%d" % sum_cnt, "%4.3f" % (100*fail_cnt/sum_cnt))


def extract_context_testblock_rulestat(source):

    match_pattern = r'Tested for\s(\d+)'
    match_applied_pattern = r'of which\s(\d+)\sfailed'

    try:
        total_cnt = int(extract_context_testblock_rulestat_cognition(source))

    except Exception as e:

        logging.error("\n(stats not found) In extract_context_testblock_rulestat:"+ source)
        total_cnt = 0
        raise ValueError

    if total_cnt > 0:
        applied_cnt = re.search(re.compile(match_applied_pattern, re.I), source).group(1)
    else:
        return (0, 0, 0)

    return (total_cnt, applied_cnt)


def extract_context_testblock_rulestat_error(source):
    """
    extract the digital(as str) from source

    Specifically, the regex is designed to take out the pattern
    source->(extracted digit)    
    1.4 times tolerance -> 1.4
    1.4 times allowable tolerance -> 1.4
    1.4 times allowable misclose -> 1.4

    ---
    @param source:
    Test: Reg 28 and 26.2.a.ii: Misclose of obs from boundary marks to witness marks
        Tested for 12 observations of which 0 failed
        All observations were better than 0.69 times allowable misclose
    or

    Test: Reg 28 and 26.2.a.i: Misclose of obs between boundary marks
       Tested for 24 observations of which 3 failed
       The worst failures are:
          Misclose on projection bearing (bearing 128 06 00) is 1.4 times tolerance
              Obs is from PEG Id DP 22442 (id 41736012) to PEG DEED 306 (id 22232881)
    """
    pattern = r'([\d\.]+) times(?:\sallowable)?\s(?:tolerance|misclose)'

    matched_objects = re.search(re.compile(pattern), source)

    if matched_objects:
        first_match_num = matched_objects.groups(0)
        # print(first_match_num[0])
        return first_match_num[0]

    return None


def extract_context_testblock_rule_recognizer(testrule_block, context):

    match_pattern = r'^\w+:\s?(.*)\s?:\s(.*)'
    # maybe redundant, but for accuracy (maybe I am not bold enough ) we want only read test title 
    testrule_title = testrule_block.strip().split('\n')[0]
    return re.match(re.compile(match_pattern), testrule_title).groups()
