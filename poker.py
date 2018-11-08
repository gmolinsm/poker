import random
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)

    def __lt__(self, other):
        if ranks.index(self.get_rank()) < ranks.index((other.get_rank())):
            return True
        return False


class Deck(object):
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        deck = ""
        for i in range(0, 52):
            deck += str(self.cards[i]) + " "
        return deck

    def take_one(self):
        return self.cards.pop(0)


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        for i in range(5):
            self.cards.append(deck.take_one())

    def __str__(self):
        hand = ""
        for i in range(5):
            hand += str(self.cards[i]) + " "
        return hand

    def is_pair(self):
        for i in range(5):
            for j in range(i+1, 5):
                if self.cards[i].get_rank() == self.cards[j].get_rank():
                    if not self.is_twopair() and not self.is_threeofakind():
                        return True
        return False

    def is_twopair(self):
        ranks = []
        for i in range(4):
            if self.cards[i].get_rank() == self.cards[i+1].get_rank():
                if not ranks.__contains__(self.cards[i].get_rank()):
                    ranks.append(self.cards[i].get_rank())
        if len(ranks) == 2:
            if not self.is_fullhouse() and not self.is_flush():
                return True
        return False

    def is_threeofakind(self):
        for i in range(5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    if self.cards[i].get_rank() == self.cards[j].get_rank() \
                            and self.cards[i].get_rank() == self.cards[k].get_rank():
                        if not self.is_flush() and not self.is_fullhouse():
                            return True
        return False

    def is_straight(self):
        self.cards.sort()
        for i in range(4):
            if ranks.index(self.cards[i].get_rank())+1 != ranks.index(self.cards[i+1].get_rank()):
                return False
        if not self.is_flush():
            return True

    def is_fullhouse(self):
        count = 0
        for i in range(4):
            if self.cards[i].get_rank() != self.cards[i + 1].get_rank():
                count += 1
                if count > 1:
                    return False
        if not self.is_fourofakind():
            return True

    def is_flush(self):
        for i in range(4):
            if self.cards[i].get_suit() != self.cards[i+1].get_suit():
                return False
        if not self.is_fullhouse() and not self.is_straightflush() and not self.is_royalflush():
            return True

    def is_fourofakind(self):
        for i in range(5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    for l in range(k+1, 5):
                        if self.cards[i].get_rank() == self.cards[j].get_rank() \
                                and self.cards[i].get_rank() == self.cards[k].get_rank() \
                                and self.cards[i].get_rank() == self.cards[l].get_rank():
                                    return True
        return False

    def is_straightflush(self):
        self.cards.sort()
        for i in range(4):
            if ranks.index(self.cards[i].get_rank()) + 1 != ranks.index(self.cards[i + 1].get_rank()):
                return False
            if self.cards[i].get_suit() != self.cards[i+1].get_suit():
                return False
        if not self.is_royalflush():
            return True
        return False

    def is_royalflush(self):
        self.cards.sort()
        if self.cards[0].get_rank() != "10":
            return False
        for i in range(4):
            if ranks.index(self.cards[i].get_rank()) + 1 != ranks.index(self.cards[i + 1].get_rank()):
                return False
            if self.cards[i].get_suit() != self.cards[i+1].get_suit():
                return False
        return True

    def is_highcard(self):
        if self.is_pair():
            return False
        if self.is_straight():
            return False
        return True

    def royalhand(self):
        self.cards = [Card("♠", "10"), Card("♠", "J"), Card("♠", "Q"), Card("♠", "K"), Card("♠", "A")]


hands = {"High card": 0, "Pair": 0, "Two pairs": 0, "Three of a kind": 0, "Straight": 0,
         "Flush": 0, "Fullhouse": 0, "Four of a kind": 0, "Straight flush": 0}

for i in range(10000):
    new_deck = Deck()
    new_deck.shuffle()
    hand = Hand(new_deck)

    if hand.is_highcard():
        hands["High card"] += 1
    if hand.is_pair():
        hands["Pair"] += 1
    if hand.is_twopair():
        hands["Two pairs"] += 1
    if hand.is_threeofakind():
        hands["Three of a kind"] += 1
    if hand.is_straight():
        hands["Straight"] += 1
    if hand.is_flush():
        hands["Flush"] += 1
    if hand.is_fullhouse():
        hands["Fullhouse"] += 1
    if hand.is_fourofakind():
        hands["Four of a kind"] += 1
    if hand.is_straightflush():
        hands["Straight flush"] += 1

print(hands)
for i in hands:
    print(hands[i]/100, "%")
command = input("Would you like to compute the royal flush? (Might take a while)(y/n):")
if command == "y":
    royalflush = 0
    while True:
        new_deck = Deck()
        new_deck.shuffle()
        hand = Hand(new_deck)
        if hand.is_royalflush():
            print(hand, "It took", royalflush, "draws in order to get one royal flush,")
            print("which means there is about:", (1/royalflush)*100,
                  "% chances you get one in a real game")
            break
        royalflush += 1
else:
    print("Done")
    exit(0)