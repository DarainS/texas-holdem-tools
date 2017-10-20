#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sys
sys.path.append("..")
from round_game import RoundGame
from decimal import Decimal
from deck import Deck
from player import Player
from card import SevenCard

class GameManager():

    def __init__(self):
        self.deck=Deck()
        self.deck.shuffle()
        self.roundGame=RoundGame()
        self.players=[]
        self.livingPlayers=[]
        self.buttonIndex=0

    def testRoundGame(self,playerNum=3):
        players=[]
        for i in range(0,playerNum):
            p=Player()
            p.name=str(i)
            p.currentMoney=Decimal('100')+i
            players.append(p)
        game=RoundGame()
        game.sb=Decimal('1')
        game.bb=Decimal('2')
        game.players=players
        game.gameBegin()

        game.goPreFlop()
        if not game.isShowDownTime():
            game.goFlop()
        game.goTurn()
        game.goRiver()
        game.makeResult()

    def nextRoundGame(self):
        self.roundGame=RoundGame()
        self.roundGame.dealPlayersHands()
        self.roundGame.askBehaviours()



def test1():
    game=GameManager()
    game.testRoundGame()


def main():
    test1()

if __name__ == '__main__':
    main()
