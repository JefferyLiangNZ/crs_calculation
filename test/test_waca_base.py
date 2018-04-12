
import pytest

from calc_process import waca_base

samplerule_stats = [
    ("""

==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          163

Number of parameters:            163

Degrees of freedom:                0

Standard error of unit weight:     1.00

Note: 163 parameters fixed automatically to avoid singularity

==============================================================================

SUMMARY OF REGULATION TESTS
""",
   """ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          163

Number of parameters:            163

Degrees of freedom:                0

Standard error of unit weight:     1.00

Note: 163 parameters fixed automatically to avoid singularity

==============================================================================

SUMMARY OF REGULATION TESTS"""
),

(
"""

==============================================================================
ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          163

Number of parameters:            163

Degrees of freedom:                0

Standard error of unit weight:     1.00

Note: 163 parameters fixed automatically to avoid singularity

==============================================================================
NOTES
==============================================================================

Not enough information to calculate node IS LIII SO 4859 (615053)
Node automatically rejected from the adjustment

Not enough information to calculate node IS XXXVIII (621774)
Node automatically rejected from the adjustment
""",

   """ADJUSTMENT SUMMARY
==============================================================================

Number of observations:          163

Number of parameters:            163

Degrees of freedom:                0

Standard error of unit weight:     1.00

Note: 163 parameters fixed automatically to avoid singularity"""
),

]

@pytest.mark.parametrize("case,expected", samplerule_stats)
def test_waca_base_strip(case, expected):
	assert waca_base.strip_trailing_leading_nonsense(case) == expected
