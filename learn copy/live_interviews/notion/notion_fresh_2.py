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

class DeleteFromEndOperationCompleted(Operation):
    def __init__(self, chars_deleted: str):
        self.chars_deleted = chars_deleted


class TextDocument:

    def __init__(self) -> None:
        # we need the content
        # we need the stack of operations
        self.content: str = str()
        self.operation_stack: List[Operation] = list()
        self.operation_index: int = -1


    def execute_operation(self, op: Operation) -> Operation:
        if type(op) == InsertAtEndOperation:
            self.content += op.chars_to_insert
            return op
        
        elif type(op) == DeleteFromEndOperation:
            if len(self.content) <= op.num_chars_to_delete:
                deleted_content = self.content
                self.content = str()
            else:
                deleted_content = self.content[-op.num_chars_to_delete:]
                self.content = self.content[:-op.num_chars_to_delete]
            
            return DeleteFromEndOperationCompleted(
                deleted_content
            )
        elif type(op) == DeleteFromEndOperationCompleted:
            self.content = self.content[:-len(op.chars_deleted)]
            return op
        
        else:
            raise ValueError(f"unsupported operation type {type(op)}")


    def execute_operation_reverse(self, op: Operation) -> Operation:
        if type(op) == InsertAtEndOperation:
            self.content = self.content[:-len(op.chars_to_insert)]
            return op
        
        elif type(op) == DeleteFromEndOperationCompleted:
            self.content += op.chars_deleted
            return op
        
        else:
            raise ValueError(f"unsupported oepration type {type(op)}")
        

    def apply_operation(self, op: Operation) -> None:
        # execute the operation
        # update the stack of operations
        completed_operation: Operation = self.execute_operation(op)

        # if we're not working on the tip
        if self.operation_index != len(self.operation_stack) - 1:
            # we're not at the tip
            # we need to overwrite the operation stack
            # and start from where we are now
            self.operation_stack = self.operation_stack[:self.operation_index+1]

        self.operation_stack.append(completed_operation)
        self.operation_index += 1


    def undo_last(self) -> None:
        # get the last completed command
        # execute the opposite of it
        # update the current position in stack

        if self.operation_index >= 0:
            operation_to_undo = self.operation_stack[self.operation_index]
            self.operation_index -= 1
            self.execute_operation_reverse(operation_to_undo)


    def redo_last(self) -> None:
        # get the last undone command
        # re-execute it
        # update the current position in stack

        last_operation_index: int = self.operation_index + 1
        if last_operation_index >= 0 and last_operation_index < len(self.operation_stack):
            operation_to_undo = self.operation_stack[last_operation_index]
            self.execute_operation(operation_to_undo)
            self.operation_index = last_operation_index


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

test_simple_undo_redo()
test_adds_undos()
test_overwrite()

