"""
Overview
You are to build a simple key-value store for storing integers (keys are strings, values are integers) and a global version (integer). You will not persist data to disk. You will store the data in memory.

The version number is an integer that increases monotonically. Every time any key is written with a value, the version number is increased. The first write is version number 1. The second write is version number 2, and so on.

The store supports three operations. The first is PUT, which returns the version number of this write. The second operation is the simple GET. This returns the last value mapped to the key. The third operation is the versioned GET. This takes a key and a version number and returns the value mapped to the key at the time of the version number. Assume that all inputs are case sensitive.

The input contains three types of commands corresponding to the three operations supported by the store:

PUT <key> <value>

Set the key name to the value. Key strings will not contain spaces. Print out the version number, the key and the value as PUT(#<version number>) <key> = <value>. The first write in the file should be version number 1, the second should be version number 2, etc.

GET <key>

Print out the key and the last value of the key, or <NULL> if that key has never been set as in: GET <key> = <value>

GET <key> <version number>

Print out the key, the version number and the value of key as it was at the time of the version number, as in GET <key>(#version) = <value>. If the key was not set at the time of the version number, print <NULL> for value. If the input version number is not recorded for a key, return the latest version recorded for that key that is smaller than the input version. See below for examples of formatted output.

Sample Input
PUT key1 5
GET key1 1
PUT key2 6
GET key1
GET key1 1
GET key2 2
PUT key1 7
GET key1 1
GET key1 2
GET key1 3
GET key4
GET key1 4
GET key2 1
Sample Output
PUT(#1) key1 = 5
GET key1(#1) = 5
PUT(#2) key2 = 6
GET key1 = 5
GET key1(#1) = 5
GET key2(#2) = 6
PUT(#3) key1 = 7
GET key1(#1) = 5
GET key1(#2) = 5
GET key1(#3) = 7
GET key4 = <NULL>
GET key1(#4) = 7
GET key2(#1) = <NULL>
"""

