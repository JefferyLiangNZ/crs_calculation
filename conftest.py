import pytest
import smtplib

@pytest.fixture(scope="module")
def rawtext_case1():
    return '''11096|C184|AUTH|UNTD|5195569|
\
Not enough information to calculate node POST SO 20083 (39247071)
\
Node automatically rejected from the adjustment
\

\
|
11096|C184|AUTH|UNTD|5195570||
11096|C184|AUTH|PASS|5195571|
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
|
11046|C184|AUTH|UNTD|51955672||'''


@pytest.fixture(scope="module")
def rawtext_case2():
	return '''11096|C184|AUTH|PASS|5195570|
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

@pytest.fixture(scope="module")
def rawtext_case3():
	return '''11096|C185|AUTH|PASS|5195570|
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