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
                if data['num'+str(i)]!=0:
                    data['winRate'+str(i)]=data['winNum'+str(i)]/data['num'+str(i)]
            db.replace_one({'hands':key.simpleString()},data,True)


def updateHandsWinNumForRange(handsList,db,totalNum=1000,toDealNum=5):
    realRange=hands_range.expandRangeToReal(handsList)
    print(time.time(),len(handsList))
    for i in range(0,100):
        dataList=[]
        hands1=HandsCard.fromString(random.choice(realRange))
        hands2=HandsCard.fromString(random.choice(realRange))
        if hands2[0] in hands1 or hands2[1] in hands1:
            continue
        handsList=[hands1,hands2]

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

def updateResultStatisData(handsRange=170,step=5,limit=1000000,target=80,postfix=''):
    ls=hands_range.getRangeHands(handsRange)
    while True:
        db=mongo.generateDB(rangee=str(handsRange),postfix='NoneHigh')
        # print(db)
        r=db.find_one({'hands':'AA'})
        if r and r['totalNum']>=limit:
            ls=hands_range.reduceHands(handsRange)
            handsRange-=step
            continue
        updateHandsWinNumForRange(ls,db)

def main():
    # topHandsResult(k=0.5)
    updateResultStatisData()    
    # cProfile.run('handsWinNumForRange(hands_range.r165)')
    # autoReduceRange()
if __name__ == '__main__':
    main()
