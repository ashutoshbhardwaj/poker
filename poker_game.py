# -----------
# User Instructions
#
# Modify the hand_rank function so that it returns the
# correct output for the remaining hand types, which are:
# full house, flush, straight, three of a kind, two pair,
# pair, and high card hands.
#
# Do this by completing each return statement below.
#
# You may assume the following behavior of each function:
#
# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function
#                  returns their corresponding ranks as a
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks
#                  in a hand (where the order goes from
#                  highest to lowest rank).
#
# Since we are assuming that some functions are already
# written, this code will not RUN. Clicking SUBMIT will
# tell you if you are correct.
from collections import Counter


def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return allmax_v2(hands, key=hand_rank)


def card_ranks(hand):
    "Return a list of the ranks, sorted on highest rank"
    rank_weight = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    ranks = [int(rank_weight.get(r, r)) for r, s in hand]
    # Alternative to above -
    # ranks = ['--123456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks


def allmax(iterable, key=lambda x: x):
    "Returns a list of all items equal to the max of iterable"
    result, maxval = [], None
    for item in iterable:
        item_val = key(item)
        if not result or item_val > maxval:
            result, maxval = [item], item_val
        elif item_val == maxval:
            result.append(item)
    return result


# Alternative approach by me
def allmax_v2(iterable, key=lambda x: x):
    max_item = max(iterable, key=hand_rank)
    return [max_item] * iterable.count(max_item)


def straight(ranks):
    "Retun True if the ordered ranks form a 5 card straight"
    return (max(ranks) - min(ranks) == 4) and len(ranks) == 5


def flush(hand):
    "Returns True if all the cards have same suit"
    suits = [s for r, s in hand]
    return len(set(suits)) == 1


def two_pair(ranks):
    "Return 2 pairs if the ranks list has 2 pairs else None"
    # ranks = card_ranks(hand)
    n_of_a_kind = n_of_a_kind_tup(2, ranks)
    if n_of_a_kind and len(n_of_a_kind) == 2:
        return tuple(n_of_a_kind)
    return None


def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):  # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):  # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):  # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):  # flush
        return (5, ranks)
    elif straight(ranks):  # straight
        return (4, ranks)
    elif kind(3, ranks):  # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):  # 2 pair
        return (2, kind(2, ranks), ranks)
    elif kind(2, ranks):  # kind
        return (1, kind(2, ranks), ranks)
    else:  # high card
        return (1, ranks)


def kind(n, ranks):
    n_of_a_kind = n_of_a_kind_tup(n, ranks)
    if n_of_a_kind:
        return max(n_of_a_kind)
    else:
        return None


def n_of_a_kind_tup(n, ranks):
    counts = Counter(ranks)
    # n_of_a_kind = [rank for rank, frequency in counts.items() if frequency == n]
    return (
        n_of_a_kind
        if (
            n_of_a_kind := [
                rank for rank, frequency in counts.items() if frequency == n
            ]
        )
        else None
    )
    print(n_of_a_kind)
    # if n_of_a_kind:
    #     return n_of_a_kind
    # else:
    #     return None


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split()  # Straight Flush
    fk = "9D 9H 9S 9C 7D".split()  # Four of a Kind
    fh = "TD TC TH 7C 7D".split()  # Full House
    tp = "5S 5D 9H 9C 6S".split()  # Two pair

    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)
    assert straight([10, 9, 8, 7, 6]) == True
    # assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    # assert poker([sf] + 99 * [fh]) == [sf]
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    return "tests pass"


print(test())
