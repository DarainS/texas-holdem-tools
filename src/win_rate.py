#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from deck import Deck
from card import Card,SevenCard
from player import Player
import random

def _generateProbabilityGroupResult(cardList,dealNum=None):
    totalResult=[]
    length=len(cardList)
    for n1 in range(0,length):
        for n2 in range(n1+1,length):
            tempList=([cardList[n1],cardList[n2]])
            totalResult.append(tempList)
    return totalResult


def _generateRandomGroupResult(cardList,totalNum,dealNum):
    res=[]
    if dealNum==0:
        return
    for i in range(0,totalNum):
        ls=random.sample(cardList,dealNum)
        res.append(ls)
    return res

def generateAllRegularHands(deck=Deck()):
    l=len(deck.inDeck)
    result=[]
    for i in range(0,l-1):
        for j in range(i+1,l):
            result.append(str(deck.inDeck[i])+str(deck.inDeck[j]))
    return result

def caculcateWinRateBy(deck,players,totalNum=2500,toDealNum=None):
    showList=deck.showList.copy()
    cardList=deck.inDeck.copy()
    winNum=[0 for i in players]

    totalResult=[]

    if toDealNum!=None:
        totalResult=_generateRandomGroupResult(cardList,totalNum,toDealNum)
    elif len(showList)>=3:
        totalResult=_generateProbabilityGroupResult(cardList)
    else:
        dealNum=5-len(showList)
        totalResult=_generateRandomGroupResult(cardList,totalNum,dealNum)

    for cards in totalResult:
        cards.extend(showList)
        pv=[0 for i in players]
        for index,player in enumerate(players):
            temp=SevenCard.fromHands(cards,player.hands)
            temp.caculateAll()
            if temp.value>pv[index]:
                pv[index] = temp.value

        m=max(pv)
        for index,val in enumerate(pv):
            if val==m:
                winNum[index]+=1

    totalPv=0
    for index,num in enumerate(winNum):
        totalPv+=num
    for index,num in enumerate(winNum):
        players[index].winRate=num/totalPv
    return winNum


def testWinRate(list,showCards='',totalNum=1000,toDealNum=None):
    assert len(list)>=2
    deck=Deck()
    ls=[]
    players=[]
    for s in list:
        p1=Player()
        if type(s)==str:            
            p1.hands=Card.arrayFromString(s)
        elif type(s)==Player:
            p1=s
        else:
            raise 'Error'
        players.append(p1)
    deck.removeCardsFromPlayers(players)
    sl=Card.arrayFromString(showCards)
    deck.showList.extend(sl)
    deck.removeCards(sl)
    winNum=caculcateWinRateBy(deck,players,totalNum,toDealNum)
    if __name__ == '__main__':
        for player in players:
            print('%s %.1f'%(str(player.hands[0])+str(player.hands[1]),player.winRate*100)+'%',end='  ')
    return winNum


def main():
    # cProfile.run('testWinRate()')
    # testWinRate(['6s6h','QdQs'])
    testWinRate(['6sJd','AdQs'])

if __name__ == '__main__':
    main()
    
