from pprint import pprint
from dataclasses import dataclass
from typing import Any, Dict, List
import logging

logging.basicConfig(level=logging.DEBUG)

class Operation:
    pass

class InsertAtEndOperation(Operation):
    def __init__(self, chars_to_insert: str):
        self.chars_to_insert = chars_to_insert

class DeleteFromEndOperation(Operation):
    def __init__(self, num_chars_to_delete: int):
        self.num_chars_to_delete = num_chars_to_delete

class DeleteFromEndOperationExecuted(DeleteFromEndOperation):
    def __init__(self, deleted_content: str):
        self.deleted_content = deleted_content

# implement this
class TextDocument:
    ### need to track ALL operations in history
    # so if we undo operations, then insert a NEW operation
    # those "undone" operations are now GONE

    def __init__(self) -> None:
        self.content: str = str()
        self.operation_stack: List[Operation] = list()
        # when operation_index is 0, the document is EMPTY
        self.operation_index: int = -1


    def execute_operation(self, op:Operation, is_new_operation: bool) -> None:
        # TODO
        # when we add, we're not just adding to the END of operations
        # we're adding such that we need to OVERWRITE the oeprations we previously had
        # after this point in history

        if type(op) == InsertAtEndOperation:
            self.content += op.chars_to_insert
            
            if is_new_operation:
                if self.operation_index != len(self.operation_stack) - 1:
                    # we are not at the tip
                    # so we need to OVERWRITE history

                    self.operation_stack = self.operation_stack[:self.operation_index+1]

                self.operation_stack.append(op)
        elif type(op) == DeleteFromEndOperation:
            deleted_content:str = str()
            if op.num_chars_to_delete >= len(self.content):
                deleted_content = self.content
                self.content = str()
            else:
                # TODO check for off by one
                # TODO check the off by one for deleted_content
                deleted_content = self.content[-op.num_chars_to_delete:]
                self.content = self.content[:-op.num_chars_to_delete]

                if is_new_operation:
                    if self.operation_index != len(self.operation_stack) - 1:
                        # we are not at the tip
                        # so we need to OVERWRITE history

                        # TODO - check off by one error
                        self.operation_stack = self.operation_stack[:self.operation_index+1]
                    self.operation_stack.append(DeleteFromEndOperationExecuted(
                        deleted_content = deleted_content
                    )
                    )
        elif type(op) == DeleteFromEndOperationExecuted:
            self.content = self.content[:-len(op.deleted_content)]
        else:
            raise ValueError(f"unknown operation type: {type(op)}")

        self.operation_index += 1


    # specifically supporting two operations:
    # InsertAtEndOperation
    # DeleteFromEndOperation
    # if we're asked to delte more characters than we have in content
    # just delete until it's empty
    def apply_operation(self, op: Operation) -> None:
        self.execute_operation(op, True)

    # we can keep doing undo
    # until there's nothing left to undo
    ### implies we'll need a stack
    def undo_last(self) -> None:
        if self.operation_index >= 0:
            op: Operation = self.operation_stack[self.operation_index]
            self.operation_index -= 1

            if type(op) == InsertAtEndOperation:
                # TODO check that this isn't going to ever go off the end
                self.content = self.content[:len(op.chars_to_insert)]

            elif type(op) == DeleteFromEndOperationExecuted:
                self.content += op.deleted_content

            else:
                raise ValueError(f"unsupported operation type in undo_last: {type(op)}")


    # if we undid the oepration
    # then redo it
    # we can execute this multiple times in a row
    # to redo multiple actions
    def redo_last(self) -> None:
        # in redo last, we're not changing the operation stack at all
        # we ARE changing the operation index

        # make sure we get the LAST operation and not the one we're waiting to execute
        # we should never execute the tip of the operation stack

        # TODO come back to check off by one logic
        if self.operation_index + 1 < len(self.operation_stack):
            # we know that we have something to redo
            operation_to_redo = self.operation_stack[self.operation_index + 1]
            self.operation_index += 1

            self.execute_operation(operation_to_redo, False)


    def get_current_content(self) -> str:
        return self.content
        

def test_simple_undo_redo():
    doc = TextDocument()
    assert doc.get_current_content() == ""

    # index is at 1
    # there's one thing on the stack
    doc.apply_operation(InsertAtEndOperation("hello"))
    assert doc.get_current_content() == "hello"


    # index is at 2
    # there's two things on the stack
    doc.apply_operation(InsertAtEndOperation("world"))
    assert doc.get_current_content() == "helloworld"

    # index is at 3
    # there's three things on the stack
    doc.apply_operation(DeleteFromEndOperation(5))
    assert doc.get_current_content() == "hello"


    # index is at 2
    # there's two things on the stack
    doc.undo_last()
    assert doc.get_current_content() == "helloworld"

    # index is at 3
    # there's three things on the stack
    doc.redo_last()
    assert doc.get_current_content() == "hello"
    
    print("test_simple_undo_redo passes")

# happy with how applyoperation is working on its own
def test_adds_undos():
    doc = TextDocument()
    doc.apply_operation(InsertAtEndOperation("a"))
    assert doc.get_current_content() == "a"
    doc.apply_operation(InsertAtEndOperation("a"))
    assert doc.get_current_content() == "aa"
    doc.apply_operation(InsertAtEndOperation("a"))
    assert doc.get_current_content() == "aaa"
    doc.apply_operation(InsertAtEndOperation("a"))
    assert doc.get_current_content() == "aaaa"

    doc.apply_operation(DeleteFromEndOperation(1))
    assert doc.get_current_content() == "aaa"
    doc.apply_operation(DeleteFromEndOperation(1))
    assert doc.get_current_content() == "aa"
    doc.apply_operation(DeleteFromEndOperation(1))
    assert doc.get_current_content() == "a"
    doc.apply_operation(DeleteFromEndOperation(1))
    assert doc.get_current_content() == ""

    print("test_adds_undos passes")    

def test_overwrite():
    doc = TextDocument()
    assert doc.get_current_content() == ""

    # index is at 1
    # there's one thing on the stack
    doc.apply_operation(InsertAtEndOperation("hello"))
    assert doc.get_current_content() == "hello"


    # index is at 2
    # there's two things on the stack
    doc.apply_operation(InsertAtEndOperation("world"))
    assert doc.get_current_content() == "helloworld"

    # index is at 3
    # there's three things on the stack
    doc.apply_operation(DeleteFromEndOperation(5))
    assert doc.get_current_content() == "hello"


    # index is at 2
    # there's two things on the stack
    doc.undo_last()
    assert doc.get_current_content() == "helloworld"

    # index is at 2
    # there's two things on the stack
    doc.undo_last()
    assert doc.get_current_content() == "hello"


    # index is at 1
    # there's one thing on the stack
    doc.apply_operation(InsertAtEndOperation("overwrite"))
    assert doc.get_current_content() == "hellooverwrite"

    ## index is at 3
    ## there's three things on the stack
    doc.redo_last()
    assert doc.get_current_content() == "hellooverwrite"
    
    print("test_overwrite passes")    


# additional scenarios to test:
"""
1. do multiple undos, then do an apply operation

"""

test_simple_undo_redo()
test_adds_undos()
test_overwrite()