from dataclasses import dataclass
import sys
from typing import Any, Dict, List

"""
Word Jump
Overview
Given two different words of the same length and a dictionary's word list, find all shortest transformation sequences from the word1 to word2, such that:

Only one letter can be changed at a time (a transformation)
Each transformed word must exist in the word list. Note that first word is not a transformed word.
Output the answer as the number of shortest path results and the list of results.

For example, given our dictionary and the words hit and cog, you would output:

2
hit,hot,hog,cog
hit,hot,cot,cog

hitt,higt,hogt,cogt,cogs
hitt,citt,cott,cogt,cogs


If there is no possible transformation, for example given our dictionary and the words vault and crypt, print only 0.

The following describes the format of the input:

Number of pair of input words N
Followed by 2 * N lines with N pair of words, each word on a separate line
Number of words in the dictionary M
Followed by M lines with a dictionary word on a separate line
Sample Input
2
hit
cog
vault
crypt
1015
aah
aal
aas
aba
abo
<...truncated for space...>
zek
zep
zig
zin
zip
zit
zoa
zoo
zuz
zzz
Sample Output
2
hit,hot,hog,cog
hit,hot,cot,cog
0
"""


# this is like a graph traversal problem
# what's the naive solution?
###
# for each word
# explore each word which is 1 char changed
# if we hit cog, add to result
# if not, abandon
###
# the tricky part is you're going to explore the entire dict
# to see if there's a match, even if you don't need to


def get_neighbors(word: str, dictionary: List[str]) -> List[str]:
    for index, _ in enumerate(word):
        sub_word = word[:index] + word[index + 1:]

        for dict_word in dictionary:
            sub_dict_word = 



# assume all words are of same length
def ingest_file(filename: str) -> None:
    pass


def main(filename: str):
    pass


if __name__=="__main__":
    filename = \
        "lyft_laptop/word_jump_sample_input.txt" \
        if len(sys.argv) < 2 \
        else sys.argv[1]
    main(filename)
