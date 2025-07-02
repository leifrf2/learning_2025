"""
Excel sheets, getCell(), setCell(), handle cycles in sheets. 
Expected to write tests. 
First-part is OK to be implemented with sub-optimal getCell() implementation where the value is computed on the fly. 
Second part, the setCell() is supposed to update the values of impacted cells so that getCell is O(1)
"""

from typing import Any, Callable, Dict, List, Set


class Cell:
    def __init__(self, name, val_fn, refs):
        self.name = name
        self.val_fn = val_fn
        self.refs: Set[str] = refs
        # upate on first pass
        self.val = None
    
    def update_val(self):
        self.val = self.val_fn()


def is_valid_cell_name(cell_name: str) -> bool:
    return len(cell_name) > 0 and \
        cell_name[0].isalpha() and \
        cell_name[1:].isnumeric()

ADDITION = "+"

class CycleException(Exception):
    pass

class Spreadsheet:
    def __init__(self):
        self.cell_map: Dict[str, Cell] = dict()

    def getCell(self, cell_name: str) -> int:
        cell_name_upper = cell_name.upper()
        if cell_name_upper in self.cell_map.keys():
            return self.cell_map[cell_name_upper].val
        else:
            return 0

    def has_cycle(self, cell_name: str) -> bool:
        to_update = set([cell_map_name for cell_map_name, cell in self.cell_map.items() if cell_name in cell.refs])
        while len(to_update) > 0:
            current = to_update.pop()
            if current == cell_name:
                return True
            next_layer = [cell_map_name for cell_map_name, cell in self.cell_map.items() if current in cell.refs]
            to_update.update(next_layer)

        return False


    def updateUpstreams(self, cell_name: str) -> None:
        to_update = set([cell_name])
        while len(to_update) > 0:
            current = to_update.pop()
            self.cell_map[current].update_val()

            next_layer = [cell_map_name for cell_map_name, cell in self.cell_map.items() if current in cell.refs]
            to_update.union(next_layer)


    def setCell(self, cell_name: str, val_fn: str) -> None:
        fn, refs = self.parse_val_fn(val_fn)
        self.cell_map[cell_name.upper()] = Cell(
            name=cell_name.upper(),
            val_fn=fn,
            refs=refs
        )

        if self.has_cycle(cell_name):
            raise CycleException(f"Found cycle including {cell_name}")

        self.updateUpstreams(cell_name)

    def evalCell(self, cell_name: str) -> int:
        if cell_name in self.cell_map.keys():
            self.cell_map[cell_name].update_val()
            return self.cell_map[cell_name].val
        else:
            return 0

    def parse_val_fn(self, val_fn: str):
        if val_fn.isdigit():
            int_val_fn = int(val_fn)
            return lambda: int_val_fn, set()
        
        # else it's a function
        referenced_cell_names: List[str] = val_fn[1:].split(ADDITION)

        return lambda: sum(self.evalCell(c) for c in referenced_cell_names), set(referenced_cell_names)

        # returns the callable function, and the referenced_cells