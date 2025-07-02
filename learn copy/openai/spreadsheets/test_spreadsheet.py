import unittest
from spreadsheet_1 import Spreadsheet
from spreadsheet_2 import Spreadsheet as Spreadsheet2
from spreadsheet_2 import CycleException

def helpers(ops):
    ss = Spreadsheet()

    for cell_name, val_fn, expected_val in ops:
        ss.setCell(cell_name=cell_name, val_fn=val_fn)
        assert ss.getCell(cell_name) == expected_val

def helpers_2(ops):
    ss2 = Spreadsheet2()

    for cell_name, val_fn, expected_val in ops:
        ss2.setCell(cell_name=cell_name, val_fn=val_fn)
        assert ss2.getCell(cell_name) == expected_val

def test_spreadsheet_1():
    ops = [
        ("A1", "1", 1)
    ]

    helpers(ops)

def test_spreadsheet_2():
    ops = [
        ("D9", "=A1+B1", 0)
    ]

    helpers(ops)

def test_spreadsheet_3():
    ops = [
        ("A1", "1", 1),
        ("B1", "2", 2),
        ("D9", "=A1+B1", 3)
    ]

    helpers(ops)

def test_ss2_1():
    ops = [
        ("A1", "1", 1),
        ("B1", "2", 2),
        ("D9", "=A1+B1", 3)
    ]

    helpers_2(ops)

def test_ss2_2():
    ss2 = Spreadsheet2()

    ss2.setCell(cell_name="A1", val_fn="1")
    ss2.setCell(cell_name="B1", val_fn="2")
    ss2.setCell(cell_name="D1", val_fn="=A1+B1")
    assert ss2.getCell("D1") == 3
    ss2.setCell(cell_name="B1", val_fn="5")
    assert ss2.getCell("D1") == 6

class TestClass(unittest.TestCase):
    def test_ss2_cycle(self):
        ss2 = Spreadsheet2()
        ss2.setCell(cell_name="A1", val_fn="1")
        ss2.setCell(cell_name="B1", val_fn="=A1")
        with self.assertRaises(CycleException):
            ss2.setCell(cell_name="A1", val_fn="=B1")
        