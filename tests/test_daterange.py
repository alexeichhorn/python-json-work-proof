import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from datetime import datetime, timedelta
from json_work_proof import JWP

class TestDateRange:

    def test_unlimited(self):
        dr = JWP.DateRange.unlimited

        assert dr.start == None
        assert dr.end == None
    

    def test_start_with_duration(self):
        start = datetime.fromtimestamp(123456789)
        timedelta_seconds = 3008
        calculated_end = datetime.fromtimestamp(123459797)

        dr1 = JWP.DateRange.start_until(start, duration=timedelta_seconds)
        dr2 = JWP.DateRange.start_until(start, duration=timedelta(seconds=3008))

        assert dr1.start == start
        assert dr1.end == calculated_end
        assert dr2.start == start
        assert dr2.end == calculated_end