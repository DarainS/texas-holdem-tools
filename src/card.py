#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bidict import bidict
import random

class Card():
    
    table2={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
    table=bidict(table2)
    tags=['h','d','c','s']

    def __init__(self,num,tag):
        self.num=num
        self.tag=tag
        self.symbol=self.table.inv[num]

    def __gt__(this,that):
        return this.num>that.num

    def __lt__(this,that):
        return this.num<that.num

    def __str__(self):
        return str(self.symbol)+self.tag

    def __repr__(self):
        return str(self.symbol)+self.tag

    def __eq__(self,that):
        if type(that)!=Card:
            return False
        if self.num==that.num and self.tag==that.tag:
            return True
        return False

    def arrayFromString(s):
        arr=[]
        s=s.strip()
        
        if len(s)==2:
            tagList=random.sample(Card.tags,2)
            for i in [0,1]:
                arr.append(Card(Card.table[s[i]],tagList[i]))
            return arr

        if len(s)==3:
            if s[2]=='s':
                tagList=random.sample(Card.tags,1)
                for i in [0,1]:
                    arr.append(Card(Card.table[s[i]],tagList[0]))
                return arr
            elif s[2]=='o':
                tagList=random.sample(Card.tags,2)                
                for i in [0,1]:
                    arr.append(Card(Card.table[s[i]],tagList[i]))
                return arr
            else:
                raise 'Error'
        
        if len(s)==4:
            for i in [0,2]:
                arr.append(Card(Card.table[s[i]],s[i+1]))
        return arr


class HandsCard():
    
    def __init__(self):
        self.hands=[]
        self.value=0

    def fromString(s):
        handsCard=HandsCard()
        handsCard.hands=Card.arrayFromString(s)
        return handsCard

    def __str__(self):
        return str(self.hands[0])+str(self.hands[1])

    def __repr__(self):
        return str(self.hands[0])+str(self.hands[1])
    
    def __getitem__(self,position):
        return self.hands[position]

    def sort(self):
        self.hands.sort(key=lambda card:card.num,reverse=True)

    def simpleString(self):
        assert len(self.hands)==2
        self.sort()
        suit='o'
        if self.hands[0].tag==self.hands[1].tag:
            suit='s'
        if self.hands[0].num==self.hands[1].num:
            suit=''
        return self.hands[0].symbol+self.hands[1].symbol+suit

class SevenCard():

    levelTable={1:'高牌',2:'一对',3:'两对',4:'三条',5:'顺子',6:'同花',7:'葫芦',8:'四条',9:'同花顺'}

    def __init__(self,arr=[]):
        self.arr=arr
        self.maxValue=0
        self.value=0
        self.levelText=self.levelTable[1]
        self.lavel=0
        self.handsList=[]

    def getCardLevelText(self):
        assert self.value>0
        self.level=int(str(self.value)[0])
        self.levelText=self.levelTable[self.cardLevel]
        return self.levelText

    def __str__(self):
        res=''
        for card in self.arr:
            res+=card.__str__()+' '
        return res

    def fromString(s1,s2=''):
        s1=(s1+s2).strip()
        arr=Card.arrayFromString(s1)
        assert len(ls)>=5 and len(ls)<=7
        res=SevenCard()
        res.arr.sort(key=lambda card:card.num)
        
        return res

    def fromHands(hands,showList=[]):
        ls=hands.hands.copy()
        ls.extend(showList)
        assert len(ls)>=5 and len(ls)<=7
        res=SevenCard()
        res.arr=ls
        res.arr.sort(key=lambda card:card.num)
        return res

    def addShowCardAndCaculate(self,card):
        assert len(self.arr)<=6
        self.arr.append(card)
        self.caculateAll()

    def _generateNumNum(self,cards):
        nums={x:0 for x in range(1,15)}
        for card in cards:
            nums[card.num]+=1
            if card.num==14:
                nums[1]+=1
        return nums

    def _generateTagNum(self,cards):
        tags={'h':0,'d':0,'c':0,'s':0}
        for card in cards:
            tags[card.tag]+=1
        return tags

    # 同花顺-9 同花-6
    def _tryResolveStraightFlushAndFlush(self,cards,numNum,tagNum):
        tag=None
        for t in tagNum:
            if tagNum[t]>=5:
                tag=t
                break
        if tag==None:
            return False
        ls=cards.copy()
        for card in ls:
            if card.tag!=tag:
                ls.remove(card)

        r=self._testStraight(ls,self._generateNumNum(ls),[])
        if r:
            lev,mValue=r
            return (9,mValue)
        return(6,ls[-1].num,ls[-2].num,ls[-3].num,ls[-4].num,ls[-5].num)

    # 顺子-5
    def _testStraight(self,cards,numNum,tagNum):
        nums={x:0 for x in range(1,15)}
        for card in cards:
            nums[card.num]+=1
            if card.num==14:
                nums[1]+=1

        for i in range(14,5-1,-1):
            muNum=0
            for j in range(0,5):
                if nums[i-j]>=1:
                    muNum+=1
            if muNum==5:
                return (5,i)
        return False

    def _tryResolveStraight(self,cards,numNum,tagNum):    
        return self._testStraight(cards,numNum,tagNum)

    def _tryResolveFour(self,cards,numNum,tagNum):
        f=0
        for num in range(14,1,-1):
            if numNum[num]>=4:
                f=num
                break
        if f==0:
            return False
        for num in range(14,1,-1):
            if numNum[num]>=1 and num!=f :
                return(8,f,num)

    # 7
    def _tryResolveFullHouse(self,cards,numNum,tagNum):
        f,h=0,0
        for num in range(14,1,-1):
            if numNum[num]>=3:
                if f==0:
                    f=num
                else:
                    h=num
            if numNum[num]>=2:
                if num!=f and num>h:
                    h=num

        if f>0 and h>0:
            return(7,f,h)
        return False

    # 4
    def _tryResolveSet(self,cards,numNum,tagNum):
        f,h1,h2=0,0,0
        for num in range(14,1,-1):
            if numNum[num]>=3:
                f=num
                break
        if f==0:
            return False
        for num in range(14,1,-1):
            if numNum[num]>=1:
                if num!=f:
                    if h1==0:
                        h1=num
                    else:
                        h2=num
                        break
        return(4,f,h1,h2)

     # 
    
    def _tryResolvePair(self,cards,numNum,tagNum):
        p1,p2,t=0,0,0
        ticker=[]
        for num in range(14,1,-1):
            if numNum[num]==2:
                if p1==0:
                    p1=num
                else:
                    p2=num
                    break
        if p1==0:
            return False
        
        if p1!=0 and p2==0:
            for num in range(14,1,-1):
                if len(ticker)==3:
                    break
                if numNum[num]==1:
                    ticker.append(num)
            tup=(2,p1,ticker[0],ticker[1],ticker[2])
            return tup

        if p1!=0 and p2!=0:
            for num in range(14,1,-1):
                if numNum[num]==1:
                    t=num
                    break
            tup=(3,p1,p2,t)
            return tup

    def _tryResolveHigh(self,cards,numNum,tagNum):
        t=(1,cards[-1].num,cards[-2].num,cards[-3].num,cards[-4].num,cards[-5].num)
        return t

    def _caculateValueFromIterator(self,iterator):
        v=[]
        v.extend(iterator)
        toApend=6-len(v)
        v.extend([0 for  i in range(0,toApend)])
        s='%02d%02d%02d%02d%02d%02d'%(v[0],v[1],v[2],v[3],v[4],v[5])
        val=int(s)
        return val

    resolveMethodList=[_tryResolveStraightFlushAndFlush,_tryResolveFour,_tryResolveFullHouse,_tryResolveStraight,_tryResolveSet,_tryResolvePair,_tryResolveHigh]

    def _resolveMaxValue(self):
        cards=self.arr
        numNum=self._generateNumNum(cards)
        tagNum=self._generateTagNum(cards)

        for resolve in self.resolveMethodList:
            t=resolve(self,cards,numNum,tagNum)
            if t:
                return self._caculateValueFromIterator(t)

    def caculateAll(self):
        self.value=self._resolveMaxValue()
        self.levelText=self.getCardLevelText()
        return self

def testAllLevelCards():
    from deck import Deck
    fs=[]
    levelSet=set([i for i  in range(1,10)])
    while len(levelSet)>0:
        deck=Deck()
        deck.shuffle()
        cards=[]
        for i in range(0,7):
            cards.append(deck.dealOne())
        seven=SevenCard.fromHands(cards)
        seven.caculateAll()
        if seven.cardLevel in levelSet:
            fs.append(seven)
            levelSet.remove(seven.cardLevel)

    ls2=sorted(fs,key=lambda seven: seven.value)
    for s in ls2:
        print(s,s.levelText,s.value)


def main():
    print(HandsCard.fromString('AA')[0])

if __name__ == '__main__':
    main()
    
