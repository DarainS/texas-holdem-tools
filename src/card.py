#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bidict import bidict
import random

class Card():
    
    table2={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
    table=bidict(table2)
    tags=['h','d','c','s']

    cardDict={}


    def __init__(self,num,tag):
        self.num=num
        self.tag=tag
        self.symbol=self.table.inv[num]
        self.isActive=False

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

    def __hash__(self):
        return self.__str__().__hash__()

    def arrayFromString(s):
        if len(Card.cardDict.items)==0:
            for key in table2.keys():
                for tag in tags:
                    card=Card(key,tag)
                    cardDict[str(card)]=card

        arr=[]
        s=s.strip()
        
        if len(s)==2:
            tagList=random.sample(Card.tags,2)
            for i in [0,1]:
                arr.append(Card.cardDict(s[i]+tagList[i]))
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
                arr.append(Card.cardDict[s[i]+s[i+1]])
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
        return self.simpleString()
    
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

    levelTable={0:'非高牌',1:'高牌',2:'一对',3:'两对',4:'三条',5:'顺子',6:'同花',7:'葫芦',8:'四条',9:'同花顺'}

    def __init__(self,arr=[]):
        self.arr=arr
        self.maxValue=0
        self.value=0
        self.levelText=self.levelTable[1]
        self.level=0
        self.win=False
        self.handsList=[]

    def getCardLevelText(self):
        assert self.value>0
        self.level=int(str(self.value)[0])
        self.levelText=self.levelTable[self.level]
        return self.levelText

    def __str__(self):
        res=''
        for card in self.arr:
            res+=card.__str__()+' '
        return res


    def fromHands(hands,showList=[]):
        ls=hands.copy()
        ls.extend(showList)
        assert len(ls)>=5 and len(ls)<=7
        res=SevenCard()
        for card in ls:
            card.isActive=False
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
        for card in ls[-5:]:
            card.isActive=True
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
                for n in range(i,i-5,-1):
                    for card in cards:
                        if card.num==n:
                            card.isActive=True
                            break
                        if n==1 and card.num==14:
                            card.isActive=True
                            break
                return (5,i)
        return False

    def _tryResolveStraight(self,cards,numNum,tagNum):    
        r = self._testStraight(cards,numNum,tagNum)
        if not r:
            return False
        _,n=r

        return r

    def _tryResolveQuads(self,cards,numNum,tagNum):
        f=0
        for num in range(14,1,-1):
            if numNum[num]>=4:
                f=num
                break
        if f==0:
            return False
        for card in cards:
            if card.num==f:
                card.isActive=True
        for num in range(14,1,-1):
            if numNum[num]>=1 and num!=f :
                for card in cards:
                    if card.num==num:
                        card.isActive=True
                        break
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
            t=5
            for card in cards:
                if card.num==f:
                    t-=1
                    card.isActive=True
            for card in cards:
                if card.num==h and t>0:
                    t-=1
                    card.isActive=True
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
        for card in cards:
            if card.num==f or card.num==h1 or card.num==h2:
                card.isActive=True
        return(4,f,h1,h2)

    # 2
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
            for card in cards:
                if card.num==p1 or card.num==ticker[0] or card.num==ticker[1] or card.num==ticker[2]:
                    card.isActive=True
                                    
            tup=(2,p1,ticker[0],ticker[1],ticker[2])
            return tup

        if p1!=0 and p2!=0:
            for num in range(14,1,-1):
                if numNum[num]==1:
                    t=num
                    break
            mt=True
            for card in cards:
                if card.num==p1 or card.num==p2:
                    card.isActive=True
                if mt and card.num==t:
                    card.isActive=True
                    mt=False
            tup=(3,p1,p2,t)
            return tup

    def _tryResolveHigh(self,cards,numNum,tagNum):
        t=(1,cards[-1].num,cards[-2].num,cards[-3].num,cards[-4].num,cards[-5].num)
        for card in cards[-5:]:
            card.isActive=True
        return t

    def _caculateValueFromIterator(self,iterator):
        v=[]
        v.extend(iterator)
        toApend=6-len(v)
        v.extend([0 for  i in range(0,toApend)])
        s='%02d%02d%02d%02d%02d%02d'%(v[0],v[1],v[2],v[3],v[4],v[5])
        val=int(s)
        return val

    resolveMethodList=[_tryResolveStraightFlushAndFlush,_tryResolveQuads,_tryResolveFullHouse,_tryResolveStraight,_tryResolveSet,_tryResolvePair,_tryResolveHigh]

    def _resolveMaxValue(self):
        cards=self.arr
        numNum=self._generateNumNum(cards)
        tagNum=self._generateTagNum(cards)

        for resolve in self.resolveMethodList:
            t=resolve(self,cards,numNum,tagNum)
            if t:
                sum=0
                for card in cards:
                    if card.isActive:
                        sum+=1
                if sum != 5:    
                    print(sum,t)
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
        cards=[]
        for i in range(0,7):
            cards.append(deck.dealOne())
        seven=SevenCard.fromHands(cards)
        seven.caculateAll()
        if seven.level in levelSet:
            fs.append(seven)
            levelSet.remove(seven.level)

    ls2=sorted(fs,key=lambda seven: seven.value)
    for s in ls2:
        print(s,s.levelText,s.value)


def main():
    testAllLevelCards()

if __name__ == '__main__':
    main()
    
