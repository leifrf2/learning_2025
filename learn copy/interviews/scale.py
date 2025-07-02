from typing import List
import random
from functools import cmp_to_key

SUITS = "♣ ♦ ♥ ♠".split(' ')
RANKS = "2 3 4 5 6 7 8 9 10 J K Q A".split(' ')

"""
Card
● A card has two properties: a rank and a suit.
● A card’s rank is an ordered value. There are 13 ranks. From lowest to highest, a
rank can be one of the values: { 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A }
● A card’s suit is an unordered value. A suit can be one of { ♣, ♦, ♥, ♠ }. These
are spoken as “clubs”, “diamonds”, “hearts”, and “spades”.
● A card is defined as a rank and a suit. We display them as rank + suit, f
example, 2♥, 10♦, Q♦, etc.
"""
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return self.__str__()

"""
Deck

● A deck of cards is an ordered collection of cards. It will start with 52 cards, one
card for every combination of rank and suit.
● Players can draw() from a deck. This means that they take the top card from
the deck and add it to their hand.
● You can shuffle() a deck, which randomizes the order of the cards in the
deck.
"""
class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self) -> List[Card]:
        cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        return cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    
    # handle if there are no cards
    # top of deck is index 0
    def draw(self) -> Card:
        return self.cards.pop(0)

"""
Player
● Players have a hand of cards, represented as an ordered collection of cards.
● Players can draw() from a deck. (See definition above
"""
class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand: List[Card] = list()
        self.score = 0
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{self.name}>"

    def add_score(self, score: int) -> None:
        self.score += score

    # handle if there are no cards
    def draw(self, deck: Deck) -> None:
        drawn_card = deck.draw()
        self.hand.append(drawn_card)
        print(f"{self} drew {drawn_card}")

    def __draw_random_card(self) -> Card:
        return self.hand.pop(random.randint(0, len(self.hand) - 1))

    def play_random(self) -> Card:
        card_to_play: Card = self.__draw_random_card()
        print(f"{self} played {card_to_play}")
        return card_to_play

    def play_suit(self, suit: str) -> Card:
        card_to_play: Card = None
        for i in range(0, len(self.hand)):
            if self.hand[i].suit == suit:
                card_to_play = self.hand.pop(i)
                break
        
        if card_to_play is None:
            card_to_play = self.__draw_random_card()
        
        print(f"{self} played {card_to_play}")
        return card_to_play

def print_hand(player: Player) -> None:
    def sort_rank(card1: Card, card2: Card) -> int:
        if RANKS.index(card1.rank) > RANKS.index(card2.rank):
            return 1
        elif RANKS.index(card1.rank) == RANKS.index(card2.rank):
            return 0
        else:
            return -1

    def sort_suit_rank(card1: Card, card2: Card) -> int:
        if SUITS.index(card1.suit) > SUITS.index(card2.suit):
            return 1
        elif SUITS.index(card1.suit) == SUITS.index(card2.suit):
            return sort_rank(card1, card2)
        else:
            return -1

    print(sorted(player.hand, key=cmp_to_key(sort_suit_rank)))

# part 1
# 1. each player takes turns drawing a card
# print player x drew a card
# print out the cards in each player in sorted order
# sort is by by any suit but together
# and then by rank (2->A)

# part 2
# trick taking
# first player plays a card
# each player plays a card in turn of the same suit
# if they don't have a card of that suit they can play any card
# print player x played card
# winner is highest ranked card as starting suit
# winner plays first next
# repeat until no more cards

# part 3
# get points based on cards played fro taht round
# five = 5 pts, 10 = 10 pts, k = 10 pts, all others 0
# at end of round, print points winner took
# end of game, print each player's total points (trick winner X)
# print the name of any player with highest number of fish points
# game winner X


if __name__ == "__main__":
    players = [
        Player("Player 1"),
        Player("Player 2"),
        Player("Player 3"),
        Player("Player 4")
    ]

    deck = Deck()

    deck.shuffle()
    for c in deck.cards:
        print(c)

    while len(deck.cards) > 0:
        for player in players:
            player.draw(deck)
    
    for player in players:
        print_hand(player)

    first_player = random.choice(players)
    while any(len(p.hand) > 0 for p in players):
        highest_card_in_suit: Card = first_player.play_random()
        highest_player = first_player
        trick_value = 0

        for player in [p for p in players if p != first_player]:
            player_card = player.play_suit(highest_card_in_suit.suit)
            if player_card.suit == highest_card_in_suit.suit \
                and RANKS.index(player_card.rank) > RANKS.index(highest_card_in_suit.rank):
                highest_card_in_suit = player_card
                highest_player = player

            if player_card.rank == "5":
                trick_value += 5
            elif player_card.rank == "10":
                trick_value += 10
            elif player_card.rank == "K":
                trick_value += 10

        highest_player.add_score(trick_value)
        first_player = highest_player
        print(f"Trick winner: {player} (Score: {trick_value})")
    
    game_winner = max(players, key=lambda p: p.score)
    print(f"WINNER: {game_winner}")

