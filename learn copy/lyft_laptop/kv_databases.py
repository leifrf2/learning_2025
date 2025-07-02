import copy
from dataclasses import dataclass
import sys
from typing import Dict, List


"""
In-Memory Key-Value Database
Overview
You are to build a data structure for storing integers. You will not persist the database to disk, you will store the data in memory.

For simplicity's sake, instead of dealing with multiple clients and communicating over the network, 
your program will receive commands via stdin, and should write appropriate responses to stdout. 
Each line of the input will be a command (specified below) followed by a specific number of arguments depending on the command.

For example:

COMMAND a b
COMMAND2 c
END
Your database should accept the following commands.

SET name value

Set the variable name to the value value. Neither variable names nor values will contain spaces.

GET name

Print out the value of the variable name, or NULL if that variable is not set.

UNSET name

Unset the variable name, making it just like that variable was never set.

NUMWITHVALUE value

Print out the number of variables that are currently set to value. If no variables equal that value, print 0.

END

Exit the program. Your program will always receive this as its last command.

Once your database accepts the above commands and is tested and works, implement commands below.






BEGIN

Open a new transaction block. Transaction blocks can be nested (BEGIN can be issued inside of an existing block)
but you should get non-nested transactions working first before starting on nested. A GET within a transaction 
returns the latest value by any command. Any data command that is run outside of a transaction block should commit immediately.

ROLLBACK

Undo all of the commands issued in the most recent transaction block,
and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.

COMMIT

Close all open transaction blocks, permanently applying the changes made in them.
Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.

Your output should contain the output of the GET and NUMWITHVALUE commands.
GET will print out the value of the specified key, or NULL.
NUMWITHVALUE will return the number of keys which have the specified value.

Sample Input
SET ex 10
GET ex
UNSET ex
GET ex
END
Sample Output
10
NULL
"""

"""
SET name value
GET name
UNSET name
NUMWITHVALUE value
END
"""

"""
BEGIN
ROLLBACK
COMMIT
"""

# without NUMWITHVALUE, this is just maintaining a dictionary
# but NUMWITHVALUE means we need to keep a reverse dictionary as well


# how can we do transaction blocks?
### 1
# make a copy of the dictionary 1 level above
# perform all the operations on it
# if rollback is performed, discard it and refer to the above dictionary
# if commit is performed, overwrite the above dictionary and refer to it
# cons: copying the entire data size with every block, including nested
# pros: simple
### 2
# track changes made in the nested block
# eg. set and unset are queued in a frame
# then apply those on commit
# or discard them otherwise
# this is challenging, because there could be set/unset multiple times, and need to track the final state
# to propagate back up
# cons: compex
# pros: don't need to copy entire data frame
### notes
# get needs to return the latest value
# so that value needs to be updated in time
# which makes option 2 even trickier
# seems more like it's time to do option 1...
# could do a middle ground of the lower dict is a first-check layer, then upper dict is later checked
# this means that as we nest more, we need to call up more
# we could maintain just one top-level dictionary, but track the value like a stack
### conclusion
# 2 and 3 have lower initialization time, would take time on order of # of transactions done to apply
# 1 has high initialization time and size, on order of dict, but is just moving around pointers (const time) for apply
# 1 is also simpler to implement
# so we're doing 1, given the time constraints of the interview

NULL = "NULL"
NO_TRANSACTION = "NO TRANSACTION"

SET = "SET"
GET = "GET"
UNSET = "UNSET"
NUMWITHVALUE = "NUMWITHVALUE"
END = "END"
BEGIN = "BEGIN"
ROLLBACK = "ROLLBACK"
COMMIT = "COMMIT"


@dataclass
class ComboDict:
    main_dict:Dict[str, int]
    reverse_dict: Dict[int, List[str]]
    transaction_count: int # this is imprecise

    def __init__(self):
        self.main_dict = dict()
        self.reverse_dict = dict()
        self.transaction_count = 0


frame_levels: List[ComboDict] = [ComboDict()]


def get_current_dict() -> ComboDict:
    return frame_levels[0]


def set_value(name: str, value: int) -> None:
    if name not in get_current_dict().main_dict.keys():
        get_current_dict().main_dict[name] = value
        
        if value not in get_current_dict().reverse_dict.keys():
            get_current_dict().reverse_dict[value] = list()
        
        get_current_dict().reverse_dict[value].append(name)


def get_value(name: str) -> None:
    print(get_current_dict().main_dict.get(name, NULL))


def unset_name(name: str) -> None:
    if name in get_current_dict().main_dict.keys():
        value = get_current_dict().main_dict[name]
        get_current_dict().reverse_dict[value].remove(name)
        del(get_current_dict().main_dict[name])

        # keep dict from staying huge unnecessarily
        if len(get_current_dict().reverse_dict[value]) == 0:
            del(get_current_dict().reverse_dict[value])


# Print out the number of variables that are currently set to value. If no variables equal that value, print 0.
def get_num_with_value(value: int) -> None:
    print(len(get_current_dict().reverse_dict.get(value, list())))


def begin():
    frame_levels.insert(0, copy.deepcopy(frame_levels[0]))


def commit():
    if len(frame_levels) > 1:

        # TODO if no transactions, print it
        if get_current_dict().transaction_count == 0:
            print(NO_TRANSACTION)

        frame_levels[1] = frame_levels[0]
        frame_levels.pop()

        # main_dict and reverse_dict should still be pointing to the same object
        # so no re-assignment is necessary

    else:
        print(NO_TRANSACTION)


def rollback():
    if len(frame_levels) > 1:
        frame_levels.pop(0)
    else:
        print(NO_TRANSACTION)


def process_command(cmd_inputs: List[str]) -> None:
    cmd = cmd_inputs[0]

    if cmd == SET:
        set_value(cmd_inputs[1], cmd_inputs[2])
        get_current_dict().transaction_count += 1
    elif cmd == GET:
        get_value(cmd_inputs[1])
    elif cmd == UNSET:
        unset_name(cmd_inputs[1])
        get_current_dict().transaction_count += 1
    elif cmd == NUMWITHVALUE:
        get_num_with_value(cmd_inputs[1])
    elif cmd == END:
        exit()
    elif cmd == BEGIN:
        begin()
    elif cmd == ROLLBACK:
        rollback()
    elif cmd == COMMIT:
        commit()
    else:
        raise ValueError(f"Unrecognized command: {cmd}")


def main(filename: str):
    with open(filename, 'r') as f:
        line = f.readline()
        
        while line:
            process_command(line.strip().split(' '))
            line = f.readline()


if __name__=="__main__":
    filename = \
        "lyft_laptop/kv_databases_sample_input_2.txt" \
        if len(sys.argv) < 2 \
        else sys.argv[1]
    main(filename)
