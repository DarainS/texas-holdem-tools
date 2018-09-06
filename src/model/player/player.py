#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from decimal import Decimal

from model.card.card import HandsCard


class Player(object):

    def __init__(self):
        self.hands = HandsCard()
        self.hands_value = 0
        self.win_rate = 0
        self.current_money = Decimal()
        self.name = ''

    def __str__(self):
        return self.name + " " + str(self.hands[0]) + str(self.hands[1]) + " money:" + str(self.current_money)

    def __repr__(self):
        return self.name + " " + str(self.hands[0]) + str(self.hands[1]) + " money:" + str(self.current_money)

    def sort_hands(self):
        self.hands.sort(key=lambda card: card.num, reverse=True)

    def simple_hands_string(self):
        assert len(self.hands) == 2
        self.sort_hands()
        suit = 'o'
        if self.hands[0].tag == self.hands[1].tag:
            suit = 's'
        if self.hands[0].num == self.hands[1].num:
            suit = ''
        return self.hands[0].symbol + self.hands[1].symbol + suit

    def hands_string(self):
        assert len(self.hands) == 2
        self.sort_hands()
        return str(self.hands[0]) + str(self.hands[1])
