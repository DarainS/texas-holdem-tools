# -*- coding=utf-8 -*-

from win_rate import testWinRate
from deck import Deck
from mongo import mongo
from player import Player
import random
from card import Card,SevenCard,HandsCard
import hands_range
import cProfile


def insertDate(db,dataList):
    ratedb=db
    for data in dataList:
        r=ratedb.find_one({
            'hands':data['hands']
        })
        if not r:
            data['winRate']=data['winNum']/data['totalNum']
            ratedb.insert_one(data)
        else:
            data['winNum']+=r['winNum']
            data['totalNum']+=r['totalNum']
            data['winRate']=data['winNum']/data['totalNum']
            ratedb.replace_one({'hands':data['hands']},data,True)


def updateHandsWinNumForRange(handsRange,totalNum=1000,toDealNum=5):
    realRange=hands_range.expandRangeToReal(handsRange)
    print(len(handsRange))
    for i in range(0,totalNum):
        dataList=[]
        hands1=HandsCard.fromString(random.choice(realRange))
        hands2=HandsCard.fromString(random.choice(realRange))
        if hands2[0] in hands1 or hands2[1] in hands1:
            continue
        handsList=[hands1,hands2]
        # print(len(handsRange),hands1,hands2)
        deck=Deck.fromHandsList(handsList)
        winNum=deck.generateWinNum(totalNum=totalNum,toDealNum=5)
        for index,p in enumerate(handsList):
            dataList.append({
                'hands':handsList[index].simpleString(),
                'winNum':winNum[index],
                'totalNum':totalNum,
            })
        insertDate(mongo.generateDB(toDealNum=toDealNum,playerNum=2,rangee=len(handsRange)),dataList)


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


def autoReduceRange(cur=160,step=5,limit=300000,target=50):
    ls2=hands_range.getRangeHands(cur)
    while True:
        db=mongo.generateDB(rangee=str(cur))
        r=db.find_one({'hands':'AA'})
        if r['totalNum']>=limit:
            ls2=hands_range.reduceHands(cur)
            cur-=step
            continue
        updateHandsWinNumForRange(ls2)

def main():
    # topHandsResult(k=0.5)
    autoReduceRange()    
    # cProfile.run('handsWinNumForRange(hands_range.r165)')

if __name__ == '__main__':
    main()
