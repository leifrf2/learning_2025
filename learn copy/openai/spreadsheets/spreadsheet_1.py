"""
Excel sheets, getCell(), setCell(), handle cycles in sheets. 
Expected to write tests. 
First-part is OK to be implemented with sub-optimal getCell() implementation where the value is computed on the fly. 
Second part, the setCell() is supposed to update the values of impacted cells so that getCell is O(1)
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass
class Cell:
    row: int
    col: str
    val_fn: Callable[[], int]

    @property
    def val(self):
        return self.compute_val()

    @property
    def name(self):
        return f"{self.row}{self.col}"

    def compute_val(self):
        return self.val_fn()

    def __hash__(self):
        return self.name

    def __repr__(self):
        return self.name


def is_valid_cell_name(cell_name: str) -> bool:
    return len(cell_name) > 0 and \
        cell_name[0].isalpha() and \
        cell_name[1:].isnumeric()
    

class Spreadsheet:
    ADDITION = "+"
    SUBTRACTION = "-"
    _valid_operations = [SUBTRACTION, ADDITION]

    def __init__(self):
        self.cell_map: Dict[str, Cell] = dict()


    # assume they mean evaluate cell here
    def getCell(self, cell_name: str) -> Cell:
        upper_cell_name = cell_name.upper()
        if is_valid_cell_name(upper_cell_name) and upper_cell_name in self.cell_map.keys():
            return self.evaluate_cell(cell_name)


    def setCell(self, cell_name: str, val_fn: str) -> None:
        upper_cell_name = cell_name.upper()
        if is_valid_cell_name(cell_name=upper_cell_name):
            len_col = len([c for c in cell_name if c.isalpha()])
            self.cell_map[upper_cell_name] = Cell(
                col=cell_name[:len_col],
                row=cell_name[len_col:],
                val_fn=self.create_val_fn(val_fn)
            )
        else:
            raise ValueError(f"unable to set cell for {cell_name} : {val_fn}")


    def get_row(self, row_number: int) -> List[int]:
        return [cell.val for cell in  self.cell_map.values() if cell.row == row_number]
    
    
    def get_col(self, col_letter: str) -> List[int]:
        return [cell.val for cell in  self.cell_map.values() if cell.col == col_letter]


    def is_valid_val_fn(self, val_fn: str) -> bool:
        if len(val_fn) == 0:
            return False
        elif val_fn.isnumeric():
            # just a number
            return True
        elif val_fn[0] == "=":
            # could be a valid formula
            fn_elements = val_fn[1:].replace(self.ADDITION, ' ').replace(self.SUBTRACTION, ' ').split(' ')
            return all(is_valid_cell_name(cell_name) for cell_name in fn_elements)
        else:
            return False


    def evaluate_cell(self, cell_name: str) -> int:
        cell = self.cell_map.get(cell_name, None)

        if cell:
            return cell.compute_val()
        else:
            return 0
        

    # assume it's well formed
    def create_val_fn(self, val_fn: str) -> Callable[[], int]:
        if not self.is_valid_val_fn(val_fn=val_fn):
            raise ValueError(f"cannot create value function. given val_fn is invalid: {val_fn}")
        
        if val_fn.isnumeric():
            int_val_fn = int(val_fn)
            return lambda: int_val_fn
        else:
            # val_fn starts with = character
            i = 1
            current_op = self.ADDITION
            compute_vals: List[Callable[[], int]] = list()

            while i < len(val_fn):
                next_operator_index = min((val_fn.find(op, i) for op in self._valid_operations if op in val_fn[i:]),default=None)
                if next_operator_index:
                    next_index = next_operator_index
                    next_op = val_fn[next_operator_index]
                else:
                    next_op = None
                    next_index = len(val_fn)

                token_str = val_fn[i:next_index]
                i = next_index + 1

                if token_str.isdigit():
                    int_token = int(token_str)
                    if current_op == self.SUBTRACTION:
                        def eval_fn(val) -> Callable[[], int]:
                            return lambda: -val
                        
                        compute_vals.append(eval_fn(int_token))
                    elif current_op == self.ADDITION:
                        def eval_fn(val) -> Callable[[], int]:
                            return lambda: val
                        
                        compute_vals.append(eval_fn(int_token))
                    else:
                        raise ValueError(f"unsupported operation type: {current_op}")
                elif is_valid_cell_name(token_str):
                    if current_op == self.SUBTRACTION:
                        def eval_fn(val) -> Callable[[], int]:
                            return lambda: -self.evaluate_cell(val)

                        compute_vals.append(eval_fn(token_str))
                    elif current_op == self.ADDITION:
                        def eval_fn(val) -> Callable[[], int]:
                            return lambda: self.evaluate_cell(val)
                        
                        compute_vals.append(eval_fn(token_str))
                    else:
                        raise ValueError(f"unsupported operation type: {current_op}")
                else:
                    raise ValueError(f"unrecognized token string: {token_str}")
                current_op = next_op

            return lambda: sum(fn() for fn in compute_vals)
