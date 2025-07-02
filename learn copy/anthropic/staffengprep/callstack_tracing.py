"""
Given a list of strings representing a call stack trace of function executions. Your task is to identify and output the start and end points of each function execution within the call stack.

Part 2:
Modify your implementation to output only those functions that appear N consecutive times, where N is configurable.
Pay careful attention to cases where different functions call the same function. For example, if function a calls b and function c also calls b, these should be considered separate execution instances, even though both involve b.
"""