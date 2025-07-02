"""
Design and implement a time-aware credit tracking system that manages credits with expiration dates. It should support the following operations:

Add Credit: Add a specified amount of credit that becomes available at a start timestamp and expires at a specified expiration timestamp.
add_credit(amount, start_timestamp, expiration_timestamp, [grant_id])
Each credit grant should track: amount, when it becomes available, and when it expires
Subtract Credit: Use available credits at a given timestamp.
subtract_credit(amount, timestamp)
When subtracting credit, use the oldest non-expired credits first
The system should handle the case where a withdrawal happens before credits are added
Get Balance: Query the total available balance at any given timestamp.
get_balance(timestamp)
This should return the sum of all credits that:
Have a start timestamp ≤ the query timestamp
Have an expiration timestamp > the query timestamp
Have not been consumed by previous subtract operations
Requirements :

Your implementation must maintain the complete transaction history
Operations can be called in any order and with any valid timestamp
The system must handle overlapping time periods for different credit grants
Ensure the balance never becomes negative
"""