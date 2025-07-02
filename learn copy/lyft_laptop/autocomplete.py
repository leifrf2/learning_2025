import sys
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
# lyft question
"""
Overview
Implement a program that performs simple autocompletion, for instance the kind used on a
smartphone keyboard. You will be given a file of words. The first part of the file will be a dictionary of
words, in order of relevance, with the highest relevance words coming first. The next part of the file
will be a list of prefixes to match against the dictionary. For each of those, you will output the 5 most
likely autocompletion suggestions, in order of relevance, along with their rank.
The following describes the format of the input to your program:
1. The first line contains an integer indicating the number of words (N) in the input dictionary
Constraints: 0 < N < 20000
. The second line contains an integer indicating the number of words (M) to process for
autocomplete. Constraints: 0 < M < 1000
. N lines, each containing a single alphanumeric word for the dictionary.
. M lines, each containing a word to check against the autocomplete. This word might not be in the
dictionary (upper/lower case letters, non-ASCII input, and so on). Be sure to handle this gracefully.
"""

"""
Sample Input

14
4
art
zone
zip
arts
date
z
day
articles
data
catch
zoom
article
articulate
articulation
catc
art
da
z
"""

"""
Sample Output

catc:
catch (10)

art:
art (1)
arts (4)
articles (8)
article (12)
articulate (13)

da:
date (5)
day (7)
data (9)

z:
zone (2)
zip (3)
z (6)
zoom (11)
"""


@dataclass
class WordRank:
    word: str
    rank: int


@dataclass
class TrieNode:
    value: str
    children: Dict[str, Any] # Any is a TrieNode
    descendant_words: List[WordRank]


# trusting the first 2 numbers in the file to be correct
# we can do input validation as a further step
def ingest_file(file_path: str) -> Tuple[List[WordRank], List[str]]:
    # first value is number of words
    # second value is number of searches

    word_ranks: List[WordRank] = list()
    word_searches: List[str] = list()

    with open(file_path, 'r') as f:
        num_words = int(f.readline().strip())
        num_searches = int(f.readline().strip())

        # range is not inclusive on upper bound
        for i in range(1, num_words + 1):
            word_ranks.append(WordRank(
                word=f.readline().strip(),
                rank=i
            ))

        for _ in range(num_searches):
            word_searches.append(f.readline().strip())

    return word_ranks, word_searches


# the trie is only ever growing, never shrinking
# the rank of the word is always increasing
def create_trie(trie_entries: List[WordRank]) -> TrieNode:
    root: TrieNode = TrieNode(
        value=".",
        children=dict(),
        descendant_words=list()
    )

    def add_word_to_Trie(trie_entry: WordRank) -> None:
        current = root
        
        for char in trie_entry.word:
            if char not in current.children.keys():
                current.children[char] = TrieNode(
                    value=char,
                    children=dict(),
                    descendant_words=list()
                )
            
            current: TrieNode = current.children[char]
            current.descendant_words.append(trie_entry)
        
    for entry in trie_entries:
        add_word_to_Trie(entry)

    return root



def autocomplete(word: str, trie_root: TrieNode) -> List[WordRank]:
    current: TrieNode = trie_root

    if len(word) == 0:
        # this case should not occur
        raise ValueError(f"word cannot have length zero")

    for char in word:
        if char in current.children.keys():
            current = current.children[char]

    return current.descendant_words


#catc:
#catch (10)
def print_formatted_result(word: str, results: List[WordRank]) -> None:
    print(f"{word}:")
    for result in results:
        print(f"{result.word} ({result.rank})")


def main(filename: str):
    return_limit = 5
    
    word_ranks, word_searches = ingest_file(filename)
    root: TrieNode = create_trie(word_ranks)

    for word in word_searches:
        results = autocomplete(word, root)
        print_formatted_result(word, results[:return_limit])
        print()


if __name__=="__main__":
    filename = \
        "lyft_laptop/autocomplete_sample_input.txt" \
        if len(sys.argv) < 2 \
        else sys.argv[1]
    main(filename)

