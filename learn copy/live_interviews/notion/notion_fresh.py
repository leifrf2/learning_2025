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
        self.completed_operations: List[Operation] = list()
        self.undone_operations: List[Operation] = list()
        self.content: str = str()


    def execute_do(self, op: Operation) -> Operation:
        if type(op) == InsertAtEndOperation:
            self.content += op.chars_to_insert
            return op
        
        elif type(op) == DeleteFromEndOperation:
            if op.num_chars_to_delete >= len(self.content):
                deleted_content = self.content
                self.content = str()
            else:
                deleted_content = self.content[-op.num_chars_to_delete:]
                self.content = self.content[:-op.num_chars_to_delete]

            return DeleteFromEndOperationCompleted(
                chars_deleted=deleted_content
            )
        
        elif type(op) == DeleteFromEndOperationCompleted:
            self.content = self.content[:-len(op.chars_deleted)]
            return op
        
        else:
            raise ValueError(f"unsupported operation type: {type(op)}")


    def execute_undo(self, op: Operation) -> None:
        if type(op) == InsertAtEndOperation:
            self.content = self.content[:len(op.chars_to_insert)]
        elif type(op) == DeleteFromEndOperationCompleted:
            self.content += op.chars_deleted
        else:
            raise ValueError(f"unsupported operation type: {type(op)}")


    def apply_operation(self, op: Operation) -> None:
        completed_operation: Operation = self.execute_do(op)
        self.completed_operations.append(completed_operation)
        self.undone_operations = list()


    def undo_last(self) -> None:
        if len(self.completed_operations) > 0:
            op: Operation = self.completed_operations.pop()
            self.undone_operations.append(op)
            self.execute_undo(op)


    def redo_last(self) -> None:    
        if len(self.undone_operations) > 0:
            op: Operation = self.undone_operations.pop()
            self.completed_operations.append(op)
            self.execute_do(op)


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

