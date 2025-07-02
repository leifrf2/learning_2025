from typing import Dict, List, Callable, Tuple, Set
from abc import abstractmethod
from pprint import pprint

# 1.1 Is Unique: Implement an algorithm to determine if a string 
# has all unique characters.
# what if you cannot use addiitonal data structures?

# 1.1 A: we need to go through the string at least once, so
# O(n) is the floor
class Question1p1:

    def isUniqueString(in_str: str) -> bool:
        seen_set: set = set()

        for c in in_str:
            if c in seen_set:
                return False
            else:
                seen_set.add(c)

        return True

    tests: List[str] = [
        "hello",
        "goodbye",
        "khushboo",
        "abcdefg",
        "123456"
    ]

    def testRunnerStr(test_cases: List[str], test_function: Callable[[str], bool]) -> None:
        for test_case in test_cases:
            print(f"{test_case}: {test_function(test_case)}")

    testRunnerStr(tests, isUniqueString)

# 1.2 Check Permutation: Given two strings, 
# write a method to decide if one is a permutation of the other

# A: we at least need to look at every char of a and b, so it's O(a+b)
# can do a dict and add from each str O(a+b) space, O(a+b) time
# could sort and compare, O(1) space, O(aloga + blogb) time
class Question1p2:

    def isPermutationTuple(ab: tuple[str, str]) -> bool:
        a = ab[0]
        b = ab[1]

        if len(a) != len(b):
            return False

        char_count_dict: Dict[str, int] = dict()

        for c in a:
            if c not in char_count_dict.keys():
                char_count_dict[c] = 0
            char_count_dict[c] += 1
        
        for c in b:
            if c not in char_count_dict.keys():
                return False
            elif char_count_dict[c] == 0:
                return False
            else:
                char_count_dict[c] -= 1
        
        # why is True guaranteed at this stage?
        # the two strings are the same length to reach dict compare,
        # so there will be the same number of chars added to the dict as removed
        # if every char in B exists in A and there is a char in B that is not in A
        # then 
        return True

    test_cases: List[tuple[str, str]] = {
        ("abc", "cba"),
        ("bbb", "bba"),
        ("", "123"),
        ("", ""),
        ("aaaaaabc", "aaaaabcc")
    }

    def testRunnerGeneric(test_cases: List[tuple[str, str]], test_function: Callable[[tuple[str, str]], bool]) -> None:
            for test_case in test_cases:
                print(f"{test_case}: {test_function(test_case)}")

    testRunnerGeneric(test_cases, isPermutationTuple)


# 1.3 URLify write a method to replace all spaces with %20
# the string has sufficient space at the end for the additional characters

# run A to the end of the string
# run B to the end of the chars in the string
# read B backwards
# when B hits a char, write the char at A and decrement A
# when B hits a space, write %20 and decrement A for 3 chars
# repeat until start of string is hit
class Question1p3:

    def urlify(url: str) -> str:
        if len(url) == 0:
            # nothing to do
            return url
        elif not any(c == ' ' for c in url):
            # nothing to replace
            return url

        output: str = ''

        # writer
        writer: int = len(url) - 1
        # reader
        reader: int = len(url) - 1

        while url[reader] == ' ':
            reader -= 1

        # reader is now at last character in word

        while reader >= 0:
            if url[reader] == ' ':
                output = '%20' + output
                writer -= 3
            else:
                output = url[reader] + output
                writer -= 1
            reader -= 1
        
        return output

    def urlify_2(url: str) -> str:
        # is this needed?
        if url == "":
            return ""
        
        url_list: List[str] = [c for c in url]

        a = len(url) - 1
        b = len(url) - 1

        # get b to starting position
        while url[b] == ' ' and b > 0:
            b -= 1

        while a >= 0:
            if url[b] == ' ':
                url_list[a] = '0'
                url_list[a-1] = '2'
                url_list[a-2] = '%'
                a -= 3
            else:
                url_list[a] = url[b]
                a -= 1
            b -= 1
        
        return ''.join(url_list)

    # length of string space is len(non-spaces) + len(spaces) * 3

    test_cases: List[str] = [
        "hello",
        "hell o   ",
        "www.testmy code.com  ",
        ""
    ]

    for tc in test_cases:
        print(f"{tc}: {urlify(tc)}")

# Given a string, write a function to check if it is a permutation of a palin-
# drome. A palindrome is a word or phrase that is the same forwards and backwards. A permutation
# is a rearrangement of letters. The palindrome does not need to be limited to just dictionary words.
class Question1p4:
    
    def isPalindromePermutation(input: str) -> bool:
        # a palindrome is when the character at n appears at len(str) - n - 1
        # so a character must appear a multiple of 2. i.e. aa is a palindrome, aabbaa is a palindrome
        # but it can also be that there is one character in the middle which appears only once, because the 
        # forward and backward index is the same.
        # so there should be either an even number of all characters, and up to one character that appears an odd number

        occurrences: Dict[str, int] = dict()
        for c in input:
            if c not in occurrences.keys():
                occurrences[c] = 0
            
            occurrences[c] += 1
        
        one_odd: bool = False
        for val in occurrences.values():
            if not val % 2 == 0:
                if one_odd:
                    # we hit our second odd
                    # this is no longer a palindrome
                    # early return
                    return False
                else:
                    # we've hit our allowed one odd
                    # if we hit another, early return
                    one_odd = True
        
        # if we got here, then we did not hit an invalid case
        return True
    
    test_cases: List[str] = [
        "",
        "a",
        "aa",
        "aaa",
        "aba",
        "ab",
        "abc",
        "abcba",
        "abba",
        "as9d8faoshudflauhelf"
    ]

    for tc in test_cases:
        print(f"{tc}: {isPalindromePermutation(tc)}")

# There are three types of edits that can be performed on strings: insert a character,
# remove a character, or replace a character. Given two strings, write a function to check if they are
# one edit (or zero edits) away.
class Question1p5:
    def __init__(self):
        pass

    class str2:
        def __init__(self, word: str):
            self.word: List[str] = list(word)

        def insert(self, index: int, char: str):
            self.word.insert(index, char)
        
        def remove(self, index: int):
            self.word.remove(index)
        
        def replace(self, index: int, char: str):
            self.word[index] = char
    
    def oneAway(self, str_in1: str, str_in2: str, mismatch_consumed: bool = False) -> bool:
        # okay, so how do we check if they're one away
        # how could two strings be different?
        # first off, the 2 strings must have length difference by at most 1

        # difference of more than 1 operation guaranteed
        len_diff: int = abs(len(str_in1) - len(str_in2))

        if len_diff > 0 and mismatch_consumed:
            # no way to match
            return False
        elif len_diff > 1:
            # no way to match
            return False
        
        # strings are the same, nothing to do
        if str_in1 == str_in2:
            return True

        # at this stage we need to do some kind of comparison
        # we could do this as exploration with backtracking?
        # compare character by character
        # if we hit one mismatch, that's okay because it could be insert replace or remove
        # continue with or'ing each path


        # strings could still be of length 1 here
        i: int = 0

        min_len: int = min(len(str_in1), len(str_in2))

        while i < min_len:
            if str_in1[i] != str_in2[i]:
                if mismatch_consumed:
                    # or the strings are more than 1 operation away
                    return False
                else:
                    # recurse and check each one
                    # case A:
                    # if a character was removed from 2, then the next char in 1 should match
                    # if a character was added to 1, then the next char in 1 should match
                    # case B:
                    # same but inverse
                    # case C:
                    # if a character was replaced, then the current char in both strings is not expected
                    # to match, so move on
                    return self.oneAway(str_in1[i+1:], str_in2[i:], True) or \
                        self.oneAway(str_in1[i:], str_in2[i+1:], True) or \
                        self.oneAway(str_in1[i+1:], str_in2[i+1:], True)

            i += 1
            
        # if we get here then we haven't found a contradiction
        return True        

    test_cases = [
        ["pale", "ple"],
        ["pales", "pale"],
        ["pale", "bale"],
        ["pale", "bake"],
        ["hi", "joe"],
        ["", ""],
        ["a", "b"],
        ["aa", "aa"],
        ["aa", "ab"],
        ["aaa", "ab"]
    ]

    def run_tests(self):
        for tc in self.test_cases:
            print(f"{tc}: {self.oneAway(tc[0], tc[1])}")

#q1p5 = Question1p5()
#q1p5.run_tests()

"""
String Compression: Implement a method to perform basic string compression using the counts
of repeated characters. For example, the string aabcccccaaa would become a2blc5a3. If the
"compressed" string would not become smaller than the original string, your method should return
the original string. You can assume the string has only uppercase and lowercase letters (a - z).
"""
class Question1p6:

    def __init__(self):
        pass

    def solve(self, str_input: str) -> str:
        if len(str_input) == 0:
            return ""
        elif len(str_input) == 1:
            return f"{str_input}1"
        
        # from here on out, string has at least 2 characters
        
        output_str: str = ""
        
        i: int = 1
        prev: str = str_input[0]
        count: int = 1
        while i < len(str_input) - 1:
            if str_input[i] == prev:
                # there is more to add
                count += 1
            else:
                output_str += f"{prev}{count}"
                count = 1
            prev = str_input[i]
            i += 1

        # check if we added the last one
        output_str += f"{prev}{count}"
        
        return output_str

        
    test_cases = [
        ['aabcccccaaa', 'a2blc5a3.']
    ]

    def run_tests(self):
        for tc in self.test_cases:
            r = self.solve(tc[0])
            print(f"{tc}: {r}: {r == tc[1]}")


#q1p6 = Question1p6()
#q1p6.run_tests()

"""
Rotate Matrix: Given an image represented by an NxN matrix, where each pixel in the image is 4
bytes, write a method to rotate the image by 90 degrees. Can you do this in place?
"""
class Question1p7:
    # what does rotation mean?
    # if it were mirroring, then we'd just swap i and j
    # 


    def __init__(self):
        pass

    def generate_matrix(self, size: int) -> List[List[int]]:
        i: int = 0

        result: List[List[int]] = list()

        for row in range (0, size):
            result.append(list())
            for col in range (0, size):
                result[row].append(i)
                i += 1

        return result

    def rotate_matrix(self, N: int, matrix: List[List[int]]) -> None:
        # N is N * N dimension
        # so each row and column has N-1 elements
        
        # for i, j
        # i_2 = j_1
        # j_2 = n - i_1

        # do this in-place?
        # the first n-1 elements in an array will be rotated in place
        # around this layer of the matrix
        # so we can go to more and more inner layers
        # and rotate each of them, with one cache variable
        # if n is odd, then there will be a single cell in the center (no op)
        # if n is even, then there is a 2x2 matrix to rotate as the last one

        # for each layer, we reduce 1 from each outside

        limit: int = N - 1

        # rotate the outermost layer
        matrix_min: int = 0
        matrix_max: int = limit

        while matrix_min < matrix_max:
            for i in range(matrix_min, matrix_max):
                # rotate one set of 4
                cell_1 = (i, matrix_min)
                cell_2 = (cell_1[1], limit - cell_1[0])
                cell_3 = (cell_2[1], limit - cell_2[0])
                cell_4 = (cell_3[1], limit - cell_3[0])

                # it's overkill to cache 4 times, but it's simpler
                # so do it this way, and refine later in interview
                original_cell_values = [
                    matrix[cell_1[0]][cell_1[1]],
                    matrix[cell_2[0]][cell_2[1]],
                    matrix[cell_3[0]][cell_3[1]],
                    matrix[cell_4[0]][cell_4[1]]
                ]

                matrix[cell_2[0]][cell_2[1]] = original_cell_values[0]
                matrix[cell_3[0]][cell_3[1]] = original_cell_values[1]
                matrix[cell_4[0]][cell_4[1]] = original_cell_values[2]
                matrix[cell_1[0]][cell_1[1]] = original_cell_values[3]

            matrix_min += 1
            matrix_max -= 1

#q1p7 = Question1p7()
#m = q1p7.generate_matrix(5)
#pprint(m)
#q1p7.rotate_matrix(5, m)
#pprint(m)

"""
Zero Matrix: Write an algorithm such that if an element in an MxN matrix is 0, its entire row and
column are set to 0.
"""
class Question1p8:
    def __init__(self):
        pass

    def zero_out_efficient(self, M: int, N: int, matrix: List[List[int]]) -> None:
        # use a row and col to store the values

        first_row_has_zeros = False
        first_col_has_zeros = False

        for row_index, row in enumerate(matrix):
            for col_index, val in enumerate(row):
                if val == 0:
                    matrix[0][col_index] = 0
                    matrix[row_index][0] = 0
                    if row_index == 0:
                        first_row_has_zeros = True
                    if col_index == 0:
                        first_col_has_zeros = True
        
        for col_index in range(1,len(matrix[0])):
            column_value = matrix[0][col_index]
            if column_value == 0:
                for row_index in range(1, len(matrix)):
                    matrix[row_index][col_index] = 0

        for row_index in range(1, len(matrix)):
            row_value = matrix[row_index][0]
            if row_value == 0:
                for col_index in range(1, len(matrix[0])):
                    matrix[row_index][col_index] = 0

        if first_row_has_zeros:
            for i in range(0, len(matrix[0])):
                matrix[0][i] = 0

        if first_col_has_zeros:
            for i in range(0, len(matrix)):
                matrix[i][0] = 0

    def zero_out(self, M: int, N: int, matrix: List[List[int]]) -> None:
        # it's easy enough to do this not in place
        # then just overwrite the given matrix with the found values
        # what's the better way?
        # track all the rows and all the cols to zero out
        # then zero out afterwards

        rows_to_zero: Set[int] = set()
        cols_to_zero: Set[int] = set()

        for row_index, row in enumerate(matrix):
            for col_index, val in enumerate(row):
                if val == 0:
                    rows_to_zero.add(row_index)
                    cols_to_zero.add(col_index)
        
        for row_index, row in enumerate(matrix):
            for col_index, val in enumerate(row):
                if row_index in rows_to_zero or col_index in cols_to_zero:
                    matrix[row_index][col_index] = 0

    def run_tests(self):
        matrix_1 = [
            [1, 2, 3, 4, 5],
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1]
        ]

        matrix_2 = [
            [1, 1, 1],
            [1, 1, 1]
        ]

        matrix_4 = [
            [0]
        ]

        matrix_5 = [
            [1]
        ]

        matrix_6 = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]

        matrices = [
            matrix_1,
            matrix_2,
            matrix_4,
            matrix_5,
            matrix_6
        ]

        for matrix in matrices:
            pprint("test")
            pprint(matrix)
            self.zero_out_efficient(0, 0, matrix)
            pprint(matrix)

#q1p8 = Question1p8()
#q1p8.run_tests()

"""
String Rotation:Assumeyou have a method isSubstringwhich checks if oneword is a substring
of another. Given two strings, sl and s2, write code to check if s2 is a rotation of sl using only one
call to isSubstring (e.g., "waterbottle" is a rotation of"erbottlewat").
"""
class Question1p9:
    def __init__(self):
        pass
    
    """ known answer """


