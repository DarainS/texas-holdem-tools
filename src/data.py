# -*- coding=utf-8 -*-

from win_rate import testWinRate
from deck import Deck
from mongo import mongo
from player import Player
import random
from card import Card,SevenCard,HandsCard
import hands_range
import cProfile
from board import Board,ResultStatis
import time

def insertDataList(db,dataList):
    ratedb=db
    # print(dataList)
    for data in dataList:
        r=ratedb.find_one({
            'hands':data['hands']
        })
        if not r:
            for i in range(0,10):
                data['winRate'+str(i)]=data['winNum'+str(i)]/data['totalNum'+str(i)]
            ratedb.insert_one(data)
        else:
            data['totalNum']+=r['totalNum']
            data['winNum']+=r['winNum']
            for i in range(0,10):
                data['winNum'+str(i)]+=r['winNum'+str(i)]
                data['totalNum'+str(i)]+=r['totalNum'+str(i)]
                data['winRate'+str(i)]=data['winNum'+str(i)]/data['totalNum'+str(i)]
            ratedb.replace_one({'hands':data['hands']},data,True)

def insertMapData(db,dataMap):
    for key in dataMap.keys():
        r=db.find_one({
            'hands':key.simpleString(),
        })
        data=dataMap[key]
        if not r:
            for i in range(0,10):
                data['rate'+str(i)]=data['num'+str(i)]/ data['totalNum']
                if data['num'+str(i)]!=0:
                    data['winRate'+str(i)]=data['winNum'+str(i)]/data['num'+str(i)]
            db.insert_one(data)
        else:
            data['totalNum']+=r['totalNum']
            data['winNum']+=r['winNum']
            data['winRate']=data['winNum']/data['totalNum']
            for i in range(0,10):
                data['winNum'+str(i)]+=r['winNum'+str(i)]
                data['num'+str(i)]+=r['num'+str(i)]
                data['rate'+str(i)]=data['num'+str(i)]/ data['totalNum']
                if data['num'+str(i)]!=0:
                    data['winRate'+str(i)]=data['winNum'+str(i)]/data['num'+str(i)]
            db.replace_one({'hands':key.simpleString()},data,True)


def updateHandsWinNumForRange(handsList,playerNum,db,totalNum=1000,toDealNum=5):
    realRange=hands_range.expandRangeToReal(handsList)

    for i in range(0,100):
        handsList=[]
        cards=set()
        dataList=[]
        for n in range(0,playerNum):
            hands=None
            while hands==None or hands[0] in cards or hands[1] in cards:
                hands=HandsCard.fromString(random.choice(realRange))
            cards.add(hands[0])
            cards.add(hands[1])
            handsList.append(hands)

        res=ResultStatis.fromHandsAndGenerateResultMap(handsList,totalNum=1000)

        insertMapData(db,res)


def topHandsResult(k=0.25):
    if type(k)==float:
        k=int(169*k)
    ratedb=mongo.generateDB(rangee='169')
    res=ratedb.find({}).sort([('winRate',-1)])
    handsResult=set()
    for i in range(0,k):
        hands=Card.arrayFromString(res[i]['hands'])
        handsResult.add(hands)
        if __name__ == '__main__':
            print(res[i]['hands'],end=' ')
    return handsResult


def autoReduceRange(cur=170,step=5,limit=300000,target=50,postfix=''):
    ls2=hands_range.getRangeHands(cur)
    while True:
        db=mongo.generateDB(rangee=str(cur))
        r=db.find_one({'hands':'AA'})
        if r and r['totalNum']>=limit:
            ls2=hands_range.reduceHands(cur)
            cur-=step
            continue
        updateHandsWinNumForRange(ls2,db)

def updateResultStatisData(handsRange=170,playerNum=2,step=5,limit=1000000,target=80,postfix='NoneHigh'):
    ls=hands_range.getRangeHands(handsRange)
    t1=time.time()
    while True:
        db=mongo.generateDB(playerNum=playerNum,rangee=str(handsRange),postfix=postfix)
        r=db.find_one({'hands':'AA'})
        if r and r['totalNum']>=limit:
            ls=hands_range.reduceHands(handsRange,postfix=postfix)
            handsRange-=step
            continue
        print('%.1f'%(time.time()-t1),len(ls))
        t1=time.time()
        updateHandsWinNumForRange(ls,playerNum,db)

def main():
    updateResultStatisData(playerNum=3,limit=300000)
    # cProfile.run('handsWinNumForRange(hands_range.r165)')

if __name__ == '__main__':
    main()
