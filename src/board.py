#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from deck import Deck
from card import Card,HandsCard,SevenCard
import random

class Board():

    def __init__(self):
        self.deck=Deck()
        self.handsList=[]

    def fromHandsList(handsList):
        b=Board()
        b.handsList=handsList
        return b

    def generateFakeResultMap(self,dealToNum=5):
        valueMap={}
        showList=self.deck.showList
        toDeal=dealToNum-len(showList)
        fakeDealList=random.sample(self.deck.inDeck,toDeal)
        mvalue=0
        for hands in self.handsList:
            sev=SevenCard.fromHands(hands,fakeDealList)
            sev.caculateAll()
            valueMap[hands]=sev
            if sev.value>mvalue:
                mvalue=sev.value
        for hands in self.handsList:
            if valueMap[hands].value==mvalue:
                valueMap[hands].win=True
        return valueMap

    def generateFakeResultList(self,dealToNum=5):
        valueMap=[]
        showList=self.deck.showList
        toDeal=dealToNum-len(showList)
        fakeDealList=random.sample(self.deck.inDeck,toDeal)
        for hands in self.handsList:
            sev=SevenCard.fromHands(hands,fakeDealList)
            sev.caculateAll()
            valueMap.append(sev)
        return valueMap

class ResultStatis():

    dataTemplete={
            'name':'',
            'level':0,
            'num':1,
            'winNum':0,
            'winRate':.0,
        }

    resultTemplete={1:None,2:None,3:None,4:None,5:None,6:None,7:None,8:None,9:None}

    def __init__(self):
        self.resultMap={}
        self.handsList=[]

    def fromHandsList(handsList):
        r=ResultStatis()
        r.handsList=handsList
        for h in handsList:
            r.resultMap[h]=ResultStatis.resultTemplete.copy()
        return r

    def _makeResultFromResults(self,results):
        for hands in self.handsList:
            resultTemp=self.resultMap[hands]
            for sev in results[hands]:
                level=sev.level
                dataTemp=resultTemp[level]
                if not dataTemp:
                    dataTemp=ResultStatis.dataTemplete.copy()
                    dataTemp['level']=sev.level
                    dataTemp['name']=sev.levelText
                    if sev.win:
                        dataTemp['winNum']=1
                    else:
                        dataTemp['winNum']=0
                    resultTemp[level]=dataTemp
                else:
                    if sev.win:
                        dataTemp['winNum']+=1
                    dataTemp['num']+=1
         
        

    def generateRandomResults(self,totalNum=1000,dealToNum=5):
        results={}
        for h in self.handsList:
            results[h]=[]
        for i in range(0,totalNum):
            board=Board.fromHandsList(self.handsList)
            m=board.generateFakeResultMap(dealToNum=dealToNum)
            for hands in self.handsList:
                results[hands].append(m[hands])
        self._makeResultFromResults(results)

def main():
    handsList=[HandsCard.fromString('QsJs'),HandsCard.fromString('Ad9c')]
    r=ResultStatis.fromHandsList(handsList)
    r.generateRandomResults()
    print(r.resultMap)

if __name__ == '__main__':
    main()



