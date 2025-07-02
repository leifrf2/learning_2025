from datetime import datetime, timedelta
import unittest
import grants

class TestGrants(unittest.TestCase):

    def test_1(self):
        gm = grants.GrantManager()
        
        start = datetime(2025, 1, 1)
        gm.create_grant(1, 5, start, start + timedelta(10))
        gm.create_grant(2, 3, start + timedelta(1), start + timedelta(20))
        gm.create_grant(3, 10, start + timedelta(2), start + timedelta(30))
        assert gm.get_balance(start + timedelta(5)) == 18
        assert gm.get_balance(start + timedelta(15)) == 13
        assert gm.get_balance(start + timedelta(100)) == 0
    
    def test_2(self):
        gm = grants.GrantManager()
        
        start = datetime(2025, 1, 1)
        gm.create_grant(1, 5, start, start + timedelta(10))
        gm.create_grant(2, 3, start + timedelta(1), start + timedelta(20))
        assert gm.get_balance(start + timedelta(5)) == 8
        gm.subtract(7, start + timedelta(2))
        assert gm.get_balance(start + timedelta(7)) == 1
