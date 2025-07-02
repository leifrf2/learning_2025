"""
Implement an in-memory SQL like database which supports the following operations. Note that we do not need to implement Primary Indexes, Generic columns, multiple tables etc. A basic database class with a single table which supports inserting a record, executing select queries with where clauses.

Part A: The In-memory SQL database should allow the following operations:

Creation of table using a schema (list of column names)
Insert records in the table with list of values for each column
Run Select query with ability to chose one or multiple columns in the output (For eg, select name, age FROM employee or select name FROM employee etc).
Part B: Now extend the Select query to accept a where clause for a single column name and a value (For eg select name, age FROM employee where age = 10).

Part C: Extend where clause in select query to accept multiple column names and logical operators like || and && operators between multiple where clauses. (For eg: select name, age FROM employee where age = 10 && name = blah ). Also support different comparision operators for where clauses (greaterThan , lessThan or equal). For eg select name, age FROM employee where age > 10 && name = blah )

Part D: Extend select query to order the output based on one (or more) column names. For eg, select name, age FROM employee where age > 10 && name = blah order by name, age . The output should order by name first and if name is equal, order by age. Also, support ASC or DESC operators for ascending or descending order of rows.
"""