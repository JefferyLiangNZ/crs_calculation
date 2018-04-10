import pytest

@pytest.fixture
def samplerule_stats_1():
    return """Test: Rule 3.7 and Rule 3.1(a): Residual of obs between all new and old non-boundary marks excluding adopted marks
    Test did not achieve 95.0% pass rate
    5 of 60 observations did not meet accuracy requirement
    The worst failures are: Residual on ellipsoidal distance (length 6.22) is 1.9 times tolerance"""

@pytest.fixture
def samplerule_stats_2():
    return """Test: Rule 3.7 and Rule 3.3.1a(i): Residual of 95% of obs between boundary marks (RSS) excluding adopted marks
   Test achieved required 95.0% pass rate
   177 of 180 observations meet accuracy requirement"""

@pytest.fixture
def samplerule_stats_3():
    return """Test: Rule 3.7 and Rule 3.3.1a(ii): Residual of all obs between boundary marks including adopted marks
    Test failed for 3 of 184 observations"""

@pytest.fixture
def samplerule_stats_4():
    return """Test: Rule 3.7 and Rule 3.1(a): Residual of obs between all new and old non-boundary marks excluding adopted marks
    Test passed for all 16 observations
    All observations were better than 0.43 times allowable error"""

