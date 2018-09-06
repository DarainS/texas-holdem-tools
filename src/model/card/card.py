#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import copy

from bidict import bidict
import random

_table2 = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
           'A': 14}
TAG_INT_TABLE = bidict(_table2)
_tags = ['h', 'd', 'c', 's']





class Card(object):

    CACHE_TABLE={}

    def __init__(self, num, tag):
        self.num = num
        self.tag = tag
        self.symbol = TAG_INT_TABLE.inv[num]
        self.is_active = False

    def __gt__(self, that):
        return self.num > that.num

    def __lt__(self, that):
        return self.num < that.num

    def __str__(self):
        return str(self.symbol) + self.tag

    def __repr__(self):
        return str(self.symbol) + self.tag

    def __eq__(self, that):
        if type(that) != Card:
            return False
        if self.num == that.num and self.tag == that.tag:
            return True
        return False

    def __hash__(self):
        return self.__str__().__hash__()

    @staticmethod
    def try_init_cache():
        card_list = [Card(n, t) for n in _table2.values() for t in _tags]
        Card.CACHE_TABLE = {c.__repr__():c for c in card_list}

    @staticmethod
    def array_from_string(s):

        Card.try_init_cache()

        arr = []
        s = s.strip()

        if len(s) == 2:
            tag_list = random.sample(_tags, 2)
            for i in [0, 1]:
                arr.append(Card.cache(s[i] + tag_list[i]))
            return arr

        if len(s) == 3:
            if s[2] == 's':
                tag_list = random.sample(Card.tags, 1)
                for i in [0, 1]:
                    arr.append(Card(Card.table[s[i]], tag_list[0]))
                return arr
            elif s[2] == 'o':
                tag_list = random.sample(Card.tags, 2)
                for i in [0, 1]:
                    arr.append(Card(Card.table[s[i]], tag_list[i]))
                return arr
            else:
                raise RuntimeError

        if len(s) == 4:
            for i in [0, 2]:
                arr.append(Card.cache[s[i] + s[i + 1]])

        return arr


class HandsCard(object):

    def __init__(self):
        self.hands = []
        self.value = 0

    @staticmethod
    def from_string(s):
        hands_card = HandsCard()
        hands_card.hands = Card.array_from_string(s)
        return hands_card

    def __str__(self):
        return str(self.hands[0]) + str(self.hands[1])

    def __repr__(self):
        return self.simple_string()

    def __getitem__(self, position):
        return self.hands[position]

    def __len__(self):
        return len(self.hands)

    def sort(self):
        self.hands.sort(key=lambda card: card.num, reverse=True)

    def simple_string(self):
        assert len(self.hands) == 2
        self.sort()
        suit = 'o'
        if self.hands[0].tag == self.hands[1].tag:
            suit = 's'
        if self.hands[0].num == self.hands[1].num:
            suit = ''
        return self.hands[0].symbol + self.hands[1].symbol + suit
