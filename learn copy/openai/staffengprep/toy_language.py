"""
A toy programming language has the following grammar:

Primitive types: char, int, float
Type variables: Uppercase letters with numbers (T1, T2, etc.)
Tuples: Ordered collections of types, which can be nested (e.g., [int, T1, [char, float]])
Part A: Implement a Node class that can represent both primitive types and tuple types. Constructor input is value (optional str) and children (optional list of Node). value passed if primitive or children passed if tuple.

class Node:
    def __init__(self, value=None, children=None):
        """
        Constructor for Node class
        :param value: String value for primitive types (int, char, float) or type variables (T1, T2, etc.)
        :param children: List of Node objects for tuple types
        """
Part B: Implement a Function class that represents function signatures with parameter types and return type. For example: [int, [int, T1], T2] -> [char, T2, [float, float]]. Constructor takes params (list of Node) and return (Node).

class Function:
    def __init__(self, params, return_type):
        """
        Constructor for Function class
        :param params: List of Node objects representing parameter types
        :param return_type: Node object representing return type
        """
Part C: Implement a to_str method for both classes Node and Function that creates a readable string representation of types and functions.

Part D: Implement a infer_return method that:

Takes a function type and actual parameter types
Substitutes type variables with concrete types
Returns the concrete return type
Validates type consistency and raises appropriate errors
Example:
Function: [T1, T2, int, T1] -> [T1, T2]
Parameters: [int, char, int, int]
Should return: [int, char]
Error cases:
[int, int, int, int] should fail (T2 should be char, not int)
[int, int, int, char] should fail (T1 can’t be both int and char)
"""