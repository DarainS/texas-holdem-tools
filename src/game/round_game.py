#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from decimal import Decimal
from deck import Deck
from player import Player
from card import SevenCard

def show(s):
    print(s)

class RoundGame():
    
    """
        pot 算法：记录每个玩家的筹码投入量，然后从高到低计算 value ，玩家获得小于等于其最大筹码数的其他玩家的筹码。
    """
    def __init__(self):
        self.players=[]
        self.livingPlayers=[]
        self.smallBlind=Decimal()
        self.bigBlind=Decimal()
        self.pot={}
        self.buttonIndex=0
        self.deck=Deck()


    def gameBegin(self):
        for p in self.players:
            self.pot[p]=Decimal('0')
        self.livingPlayers=self.players.copy()
        self.activePlayers=self.players.copy()

    def gameEnd(self):
        for p in self.players:
            p.hands=[]

    def dealPlayersHands(self):
        for i in [0,1]:
            for p in self.players:
                p.hands.append(self.deck.dealOne())
        for p in self.players:
            p.sortHands()
        

    def playerBet(self,player,betNum):
        num=Decimal(str(betNum))
        player.currentMoney-=num
        self.pot[player]+=num

    def playerRaise(self,player,betNum):
        self.pot[player]+=Decimal(str(betNum))

    def playerCheck(self,player):
        pass
    
    def playerFold(self,player):
        self.livingPlayers.remove(player)
        self.activePlayers.remove(player)

    def playerAllIn(self,player):
        self.activePlayers.remove(player)


    def askBehaviours(self):
        index=self.buttonIndex
        for i in range(len(self.livingPlayers)):
            index=self.nextLivingPlayerIndex(index)
            if self.players[index].currentMoney<=0:
                continue
            self.askPlayerBehaviour(self.players[index])

        while not self.isThisTurnFinsh():
            index=self.nextActivePlayerIndex(index)
            self.askPlayerBehaviour(self.players[index])

            

    def askPlayerBehaviour(self,player):
        self.playerBet(player,Decimal(1))
        print(str(player)+" "+'checked')
    
    def isThisTurnFinsh(self):
        if len(self.pot.values())<=1:
            return True
        potMax=max(self.pot.values())
        for p in self.livingPlayers:
            if p.currentMoney==0:
                continue
            if self.pot[p]<potMax:
                return False
        return True

    def turnFinish(self):
        pass


    def nextLivingPlayerIndex(self,index):
        id2=index
        while True:
            id2+=1
            if id2>=len(self.players):
                id2=0
            p=self.players[id2]
            if p in self.livingPlayers:
                return id2

    def nextActivePlayerIndex(self,index):
        id2=index
        while True:
            id2+=1
            if id2>=len(self.players):
                index=0
            p=self.players[id2]
            if p in self.livingPlayers and p.currentMoney>0:
                return id2

    def isShowDownTime(self):
        if len(self.deck.showList)>=5:
            return True
        if len(self.activePlayers)<=1:
            return True
        return False

    def goPreFlop(self):
        self.dealPlayersHands()
        self.askBehaviours()

    def goFlop(self):
        for i in range(0,3):
            self.deck.dealAndShow()
        showList=self.deck.showList
        show('flop:'+str(showList[0])+str(showList[1])+str(showList[2]))
        self.askBehaviours()
        
    def goTurn(self):
        self.deck.dealAndShow()
        show('turn:'+str(self.deck.showList[3]))
        self.askBehaviours()

    def goRiver(self):
        self.deck.dealAndShow()
        show('river:'+str(self.deck.showList[4]))
        self.askBehaviours()

    def makePlayersHandsValue(self):
        for p in self.livingPlayers:
            seven=SevenCard.fromCardArray(self.deck.showList,p.hands)
            seven.caculateAll()
            p.handsValue=seven.value

    def makeResult(self):
        self.makePlayersHandsValue()
        while(len(self.livingPlayers)>=1):
            winners=self.getMaxValuePlayers()
            winnerNum=len(winners)
            for player in winners:
                toWinNum=Decimal()
                playPotNum=self.pot[player]
                for key in self.pot.keys():
                    if self.pot[key]>=playPotNum:
                        self.pot[key]-=playPotNum/winnerNum
                        toWinNum+=playPotNum
                    else:
                        toWinNum+=self.pot[key]/winnerNum
                        self.pot[key]=Decimal('0')
                    if self.pot[key]<=0 and key in self.livingPlayers:
                        self.livingPlayers.remove(key)
                player.currentMoney+=toWinNum
        for p in self.players:    
            print(p)

    def getMaxValuePlayers(self):
        result=[]
        maxValue=max(p.handsValue for p in self.livingPlayers)
        for p in self.livingPlayers:
            if p.handsValue==maxValue:
                result.append(p)
        return result