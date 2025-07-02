"""
Design and implement a simplified excel sheet API that supports cell references and formula calculations. The system should handle the following operations:

getCell(cellId): Retrieve the value of a cell. This should return the computed value, not the formula.
setCell(cellId, input): Set a cell to either a direct value or a formula referencing other cells.
Direct value example: setCell("A1", "42")
Formula example: setCell("A3", "=A1+A2") where the value is calculated from other cells
Requirements
Formulas should be evaluated correctly when retrieving cell values
Changes to referenced cells should automatically propagate to dependent cells
The system should detect and handle circular references (dependency cycles)
The initial implementation can compute values on-the-fly in getCell(), but the optimized implementation should update affected cells when setCell() is called so that getCell() becomes an O(1) operation
Example Test Cases
spreadsheet = Spreadsheet()
spreadsheet.setCell('A1', '1')
spreadsheet.setCell('A2', '2')
spreadsheet.setCell('A3', '=A1+A2')# A3 should be 3
spreadsheet.setCell('A4', '=A3+A2')# A4 should be 5
spreadsheet.setCell('A5', '=A3+A4')# A5 should be 8
spreadsheet.setCell('B1', '=A1+A2+A3+A4+A5')# B1 should be 19

Dependency Update Example
Initial state:


Cell A = 6
Cell B = 7
Cell C = A + B = 13  (Cell C depends on A and B)
After updating Cell A:


Cell A = 2
Cell B = 7
Cell C = A + B = 9  (Value automatically updated)
"""