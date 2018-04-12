from __future__ import generators, division, print_function

import re
import traceback
import sys
import logging

match_dict = {
    'obn_cnt': r'Number of observations:\s+([\d\.]+)',
    'prm_cnt': r'Number of parameters:\s+([\d\.]+)',
    'free_dg': r'Degrees of freedom:\s+([\d\.]+)',
    'std_err': r'Standard error of unit weight:\s+(?:-)?([\d\.]+)' 
}
    
splitter = r'(ADJUSTMENT\s.*)'
# splitter ='=+\s'

def extract_blocks(text):

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
    for key, pattern in match_dict.iteritems():
        if re.search(pattern, source, re.M):
            result_dict[key] = re.search(pattern, source, re.M).group(1)
     
    return result_dict

def extract_context(source):
    processed = source.replace('\r', '').replace('=', '')
    """ 
        use the full result text of a test record, which is the same as extract_metrics 
        extract the rule test text description, return as the paragraph below 
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

    match_pattern = r'(?:SUMMARY OF REGULATION TESTS)'
    matched_groups = re.split(re.compile(match_pattern, re.M), processed, 6)

    matched_items = [x.strip('\n') for x in matched_groups if x.strip('\n').startswith('Testing')]
    # print matched_items

    if matched_items:
        return matched_items[0]
    else:
        # 'No testing rules section get matched, so only a ERROR SUMMARY'
        pass


def extract_context_testblock(source):

    match_pattern = r'Test:[^\:]+:[^\:]+\n'
    try:
        return re.findall(re.compile(match_pattern, re.M), source)

    except Exception as e:
        logging.error("\n(testblock not found) In extract_context_testblock:"+ source)
        raise e

def extract_context_testblock_title(source):

    match_pattern = r'Testing regulations:\s(.+)'
    try:
        rule_version_text = re.match(re.compile(match_pattern), source).group(1)
        reg_version = extract_context_testblock_title_regver(rule_version_text)
        return (reg_version, rule_version_text, )

    except Exception as e:
        logging.error("\n(title not found) In extract_context_testblock_title:"+ source)
        raise e

def extract_context_testblock_title_regver(source):
    capture_survery_version_pattern = r'([\d\/]{4,})'
    capture_survey_type_pattern =r'class\s(\w)+\ssurveys'

    reg_version = ''
    # print '>>>', source
    # print '<<<', re.search(re.compile(capture_survery_version_pattern), source).group(1)

    if re.search(re.compile(capture_survery_version_pattern), source):
        reg_version += re.search(re.compile(capture_survery_version_pattern), source).group(1)
        # print reg_version
    else:
        reg_version += 'INFO'
        # raise ValueError

    if re.search(re.compile(capture_survey_type_pattern), source):
        reg_version += '-' + re.search(re.compile(capture_survey_type_pattern), source).group(1)
    
    # print "VERSION: ", reg_version
    return reg_version

def extract_context_testblock_ruleitem(source):
    
    match_pattern = r'\:\s+'
    values = re.split(re.compile(match_pattern), source)
    return values[1:]

# Tested for 180 observations of which 2 failed
# def extract_context_testblock_rulestat_cognition(source):
#     # raw_input('source')    (?P<x>
    
#     match_pattern = r'Tested for\s(?P<SUM>\d+)\sobservation.*of which\s(?P<FAIL>\d+)\sfailed|\
#     Test failed for.+\s(?P<SUM>\d+)\sobservations|\
#     Test passed for.*\s(?P<SUM>\d+)\sobservations|\
#     of\s(?P<SUM>\d+)\sobservations did not meet'

#     result = re.search(re.compile(match_pattern), source)

#     if result:
#         if re.search(re.compile(match_pattern), source).groups()[3]:
#             logging.debug('parsing {} '.format(source))

#         filter(lambda x: bool(x), result.groups())[0]
#         return filter(lambda x: bool(x), result.groups())[0]
def extract_context_testblock_rulestat_cognition(source):
    # raw_input('source')    (?P<x>
    
    match_patterns = [
        r'Tested for\s(?P<SUM>\d+)\s\w+.*of which\s(?P<FAIL>\d+)\sfailed',
        r'Test failed for\s(?P<FAIL>\d+)\sof\s(?P<SUM>\d+)\s\w+',
        r'Test passed for.*\s(?P<SUM>\d+)\s\w+',
        r'(?P<FAIL>\d+)\sof\s(?P<SUM>\d+)\s\w+ did not meet accuracy requirement',
        r'(?P<PASS>\d+)\sof\s(?P<SUM>\d+)\s\w+ meet accuracy requirement'
    ]

    matched_objects = filter(lambda x: bool(x), 
        [ re.search(re.compile(pattern), source) for pattern in match_patterns ])
    # print(matched_objects)
    sum_cnt, fail_cnt, pass_cnt = 0, 0, 0
    # result = re.search(re.compile(match_pattern), source)
    if matched_objects:
        try:
            sum_cnt = int(matched_objects[0].group('SUM'))
            if sum_cnt == 0:
                logging.error("Cant deduct from test rule results because: " + source)
                return ("0", "0", "0.0")

            if 'PASS' in matched_objects[0].groupdict() and matched_objects[0].group('PASS'):
                pass_cnt = int(matched_objects[0].group('PASS'))
                fail_cnt = sum_cnt - pass_cnt

            if 'FAIL' in matched_objects[0].groupdict() and matched_objects[0].group('FAIL'):
                fail_cnt = int(matched_objects[0].group('FAIL'))
        except:
            # logging.error("No match group for test result {}".format(source))
            logging.error("matched {}".format(str(matched_objects[0].groupdict())))
            logging.error("Cant deduct from test rule results because: " + source)


        return ("%d" % fail_cnt, "%d" % sum_cnt, "%4.3f" % (100*fail_cnt/sum_cnt))
    else:
        logging.error("Exception from: extract_context_testblock_rulestat_cognition")
        raise ValueError

def extract_context_testblock_rulestat(source):

    match_pattern = r'Tested for\s(\d+)'
    match_applied_pattern = r'of which\s(\d+)\sfailed'
    # print source
    # print '----'

    try:
        # total_cnt = re.search(re.compile(match_pattern, re.I|re.M), source).group(1)
        total_cnt = int(extract_context_testblock_rulestat_cognition(source))

    except Exception as e:

        logging.error("\n(stats not found) In extract_context_testblock_rulestat:"+ source)
        total_cnt = 0
        raise ValueError

    if total_cnt > 0:
        applied_cnt = re.search(re.compile(match_applied_pattern, re.I), source).group(1)
    else:
        # print source
        return (0, 0, 0)

    # print '==', total_cnt, applied_cnt
    return (total_cnt, applied_cnt)



def extract_testblock_ruleitem_proc(testrule_block, context):
    if testrule_block.find('of which') < 0:

        if testrule_block.find('not used') < 0 and testrule_block.find('not tested') < 0 and testrule_block.find('Test passed for ') < 0:
            logging.error('Exception: '+ testrule_block)
            logging.error('Context: '+ repr(context))
            # raw_input('>>')
            pass
        return (None, None)

    testrule_title = testrule_block.split('\n')[0]
    return extract_context_testblock_ruleitem(testrule_title)

