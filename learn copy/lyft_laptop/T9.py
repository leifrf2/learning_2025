from dataclasses import dataclass
import sys
from typing import Any, Dict, List

"""
Overview
Before smartphones existed, mobile phones had buttons for digits. To type words, one had to press the digits repeatedly to cycle through all possible letters on that key. T9 made this somewhat easier by allowing words to be entered with a single keypress for each letter. It combined the digits with a dictionary to return a list of words corresponding to the sequence of key-presses.

For instance, to type the word 'the', one would press 843.



You are to build a data structure that given a sequence of digits will return all words that can be made using the letters corresponding to the digits.

You will write a program to test your data structure.
You will be given an input file that contains a list of dictionary words and a list of keypresses as a sequence of digits.
For each sequence of digit, your program should find all possible words in the dictionary that could match the sequence of digits.

The input file will contain a series of newline separated all-caps words, followed by a series of newline separated test cases. The dictionary is over as soon as numbers start coming into the input.

Your output should contain one line for each line in the input. The outputted words should be in lowercase. Each line will be formatted as follows:

<sequence of digits>: <comma separated list of words> or '<No Results>'
"""

"""
Sample Input
AA
AAH
AAHED
AAHING
AAHS
AAL
AALII
AALIIS
AALS
AARDVARK
AARDVARKS
<...truncated for space...>
ZYMOTIC
ZYMURGIES
ZYMURGY
ZYZZYVA
ZYZZYVAS
ZZZ
968
63
627427482
737456
"""

"""
Sample Output
968: wot, you
63: me, ne, od, oe, of
627427482: margarita
737456: <No Results>
"""

T9_DICT: Dict[str, List[str]] = {
    '1': [],
    '2': ['a', 'b', 'c'],
    '3': ['d', 'e', 'f'],
    '4': ['g', 'h', 'i'],
    '5': ['j', 'k', 'l'],
    '6': ['m', 'n', 'o'],
    '7': ['p', 'q', 'r', 's'],
    '8': ['t', 'u', 'v'],
    '9': ['w', 'x', 'y', 'z'],
    '0': []
}


@dataclass
class TrieNode:
    character: str
    children: Dict[str, Any] # TrieNode
    is_word: bool


@dataclass
class SearchPath:
    current_node: TrieNode
    current_string: str
    remaining_digits: str


# this is just a search of the space
def get_possible_words(digit_string: str, root: TrieNode) -> List[str]:
    if len(digit_string) == 0:
        return list()
    
    possible_words: List[str] = list()

    horizon: List[str] = [
        SearchPath(
            current_node=root,
            current_string=str(),
            remaining_digits=digit_string
        )
    ]
    
    while(len(horizon) > 0):
        current: SearchPath = horizon.pop(0)

        # terminal condition
        if len(current.remaining_digits) == 0:
            # then we've processed everything and we're done
            # we must have a viable word
            if current.current_node.is_word:
                possible_words.append(current.current_string)
        else:
            # there's still work to do
            next_digit = current.remaining_digits[0]

            possible_characters = T9_DICT[next_digit]

            for char in possible_characters:
                if char in current.current_node.children.keys():
                    # there is still a viable path
                    horizon.append(SearchPath(
                        current_node=current.current_node.children[char],
                        current_string=current.current_string + char,
                        remaining_digits=current.remaining_digits[1:]
                    ))

    return possible_words


def add_to_trie(word: str, root: TrieNode) -> None:
    current: TrieNode = root
    for char in word:
        if char not in (child_char for child_char in current.children.keys()):
            current.children[char] = TrieNode(
                character=char,
                children=dict(),
                is_word=False
            )
        current = current.children[char]
    
    current.is_word = True


def get_formatted_result(digit_string: str, word_matches: List[str]) -> str:
    word_match_format = ', '.join(word_matches) if len(word_matches) > 0 else "<No Results>"
    return f"{digit_string}: {word_match_format}"


def main(filename: str):

    root: TrieNode = TrieNode(
        character=".",
        children=dict(),
        is_word=False
    )

    inputs: List[str] = list()

    with open(filename, 'r') as f:
        line = f.readline().strip()

        while line and not line.isdigit():
            print(f"adding {line} to trie")
            add_to_trie(line, root)
            line = f.readline().strip().lower()
        
        # now we're numbers
        while line:
            inputs.append(line)
            line = f.readline().strip().lower()

    for input in inputs:
        possible_words: List[str] = get_possible_words(input, root)
        formatted_result = get_formatted_result(input, possible_words)
        print(formatted_result)


if __name__=="__main__":
    filename = \
        "lyft_laptop/t9_sample_input.txt" \
        if len(sys.argv) < 2 \
        else sys.argv[1]
    main(filename)
