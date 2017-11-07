#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from deck import Deck
from card import Card, HandsCard, SevenCard
import random


class Board():

    def __init__(self):
        self.deck = Deck()
        self.handsList = []

    def fromHandsList(handsList):
        b = Board()
        b.handsList = handsList
        for hand in handsList:
            b.deck.removeCards(hand)
        return b

    def generateFakeResultMap(self, dealToNum=5):
        valueMap = {}
        showList = self.deck.showList
        toDeal = dealToNum - len(showList)
        fakeDealList = random.sample(self.deck.inDeck, toDeal)
        mvalue = 0
        for hands in self.handsList:
            sev = SevenCard.fromHands(hands, fakeDealList)
            sev.caculateAll()
            valueMap[hands] = sev
            if sev.value > mvalue:
                mvalue = sev.value
        for hands in self.handsList:
            if valueMap[hands].value == mvalue:
                valueMap[hands].win = True
        return valueMap

    def generateFakeResultList(self, dealToNum=5):
        valueMap = []
        showList = self.deck.showList
        toDeal = dealToNum - len(showList)
        fakeDealList = random.sample(self.deck.inDeck, toDeal)
        for hands in self.handsList:
            sev = SevenCard.fromHands(hands, fakeDealList)
            sev.caculateAll()
            valueMap.append(sev)
        return valueMap


class ResultStatis():
    dataTemplete = {
        'name': '',
        'level': 0,
        'num': 1,
        'winNum': 0,
        'winRate': .0,
    }

    resultTemplete = {'0': {'name': '非高牌', 'level': 0, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '1': {'name': '高牌', 'level': 1, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '2': {'name': '一对', 'level': 2, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '3': {'name': '两对', 'level': 3, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '4': {'name': '三条', 'level': 4, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '5': {'name': '顺子', 'level': 5, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '6': {'name': '同花', 'level': 6, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '7': {'name': '葫芦', 'level': 7, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '8': {'name': '四条', 'level': 8, 'num': 0, 'winNum': 0, 'winRate': 0.0},
                      '9': {'name': '同花顺', 'level': 9, 'num': 0, 'winNum': 0, 'winRate': 0.0}}

    resultTemplete = {
        'hands': None, 'totalNum': 0, 'winNum': 0, 'winRate': 0.0,
        'name0': '非高牌', 'num0': 0, 'rate0': .0, 'winNum0': 0, 'winRate0': 0.0,
        'name1': '高牌', 'num1': 0, 'rate1': .0, 'winNum1': 0, 'winRate1': 0.0,
        'name2': '一对', 'num2': 0, 'rate2': .0, 'winNum2': 0, 'winRate2': 0.0,
        'name3': '两对', 'num3': 0, 'rate3': .0, 'winNum3': 0, 'winRate3': 0.0,
        'name4': '三条', 'num4': 0, 'rate4': .0, 'winNum4': 0, 'winRate4': 0.0,
        'name5': '顺子', 'num5': 0, 'rate5': .0, 'winNum5': 0, 'winRate5': 0.0,
        'name6': '同花', 'num6': 0, 'rate6': .0, 'winNum6': 0, 'winRate6': 0.0,
        'name7': '葫芦', 'num7': 0, 'rate7': .0, 'winNum7': 0, 'winRate7': 0.0,
        'name8': '四条', 'num8': 0, 'rate8': .0, 'winNum8': 0, 'winRate8': 0.0,
        'name9': '同花顺', 'num9': 0, 'rate9': .0, 'winNum9': 0, 'winRate9': 0.0,
    }

    def __init__(self):
        self.resultMap = {}
        self.handsList = []

    def fromHandsList(handsList):
        r = ResultStatis()
        r.handsList = handsList
        for h in handsList:
            r.resultMap[h] = ResultStatis.resultTemplete.copy()
            r.resultMap[h]['hands'] = h.simpleString()
        return r

    def fromHandsAndGenerateResultMap(handsList, totalNum=1000):
        r = ResultStatis.fromHandsList(handsList)
        r.generateRandomResults(totalNum=1000)
        return r.resultMap

    def _makeResultFromResults(self, results):
        for hands in self.handsList:
            resultTemp = self.resultMap[hands]
            for sev in results[hands]:
                level = sev.level
                dataTemp = resultTemp
                dataTemp['num' + str(level)] += 1
                dataTemp['totalNum'] += 1
                if sev.win:
                    dataTemp['winNum' + str(level)] += 1
                    dataTemp['winNum'] += 1
                if level > 1:
                    dataTemp['num0'] += 1
                    if sev.win:
                        dataTemp['winNum0'] += 1

    def generateRandomResults(self, totalNum=1000, dealToNum=5):
        results = {}
        for h in self.handsList:
            results[h] = []
        for i in range(0, totalNum):
            board = Board.fromHandsList(self.handsList)
            m = board.generateFakeResultMap(dealToNum=dealToNum)
            for hands in self.handsList:
                results[hands].append(m[hands])
        self._makeResultFromResults(results)


def main():
    handsList = [HandsCard.fromString('QsJs'), HandsCard.fromString('Ad9c')]
    r = ResultStatis.fromHandsList(handsList)
    r.generateRandomResults()
    print(r.resultMap)


if __name__ == '__main__':
    main()
