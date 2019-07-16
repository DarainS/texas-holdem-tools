#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from card import Card,SevenCard,HandsCard
import random

class Deck():
    
    numList=[2,3,4,5,6,7,8,9,10,11,12,13,14]
    tagList=['d','h','c','s']
    initCardList=[]

    for num in numList:
        for tag in tagList:
            initCardList.append(Card(num,tag))

    def __init__(self):
        self.inDeck=Deck.initCardList.copy()
        self.showList=[]
        self.handsList=[]
        self.handsValues={}
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.inDeck)
        self.showList=[]

    def fromHandsList(handsList):
        deck=Deck()
        deck.handsList.extend(handsList)
        for hands in handsList:
            deck.handsValues[hands]=[]
            deck.removeCards(hands)
        return deck


    def fromSampleHandsStrings(strList):
        deck=Deck()
        for s in strList:
            h=HandsCard.fromString(s)
            deck.removeCards(h)
        return deck

    def dealOne(self,index=0):
        assert len(self.inDeck)>0
        r=self.inDeck[index]
        self.inDeck.remove(r)
        return r

    def dealAndShow(self,index=0):
        assert len(self.inDeck)>0
        r=self.inDeck[index]
        self.showList.append(r)
        self.inDeck.remove(r)
        return r

    def removeCards(self,cards):
        for card in cards:
            self.inDeck.remove(card)

    def removeCardsFromPlayers(self,players):
        for player in players:
            self.removeCards(player.hands)

    def generateWinNum(self,totalNum,toDealNum=5):
        winNum=[0 for i in self.handsList]
        for n in range(0,totalNum):
            showList=random.sample(self.inDeck,toDealNum)
            pv=[0 for i in self.handsList]
            for index,hands in enumerate(self.handsList):
                temp=SevenCard.fromHands(hands,showList=showList).caculateAll()
                if temp.value>pv[index]:
                    pv[index] = temp.value
            m=max(pv)
            for index,val in enumerate(pv):
                if val==m:
                    winNum[index]+=1
        return winNum

    def generateResultForRandomNumber(self,randomNum):
        for toDealNum in [3,4,5]:
            self.showList=random.sample(self.inDeck,toDealNum)
            for index,hands in enumerate(self.handsList):
                temp=SevenCard.fromHands(hands,self.showList).caculateAll()
                self.handsValues[hands].append(temp.value)

