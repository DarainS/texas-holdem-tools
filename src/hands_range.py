# -*- coding=utf-8 -*-

from mongo import mongo
from card import Card

pair={'AA':0.5,'KK':0.9,'QQ':1.7,'JJ':3.0,'TT':3.8,'99':5.1,'88':5.9,'77':7.5,'66':8.0,'55':9.7,'44':10.7,'33':14.5,'22':22.5}

Axs={'AKs':1.2,'AQs':3.3,'AJs':5.4,'ATs':6.2,'A9s':9.2,'A8s':10.0,'A7s':11.9,'A6s':13.4,'A5s':12.5,'A4s':14.0,'A3s':16.0,'A2s':17.2}
Axo={'AKo':2.6,'AQo':4.7,'AJo':7.1,'ATo':8.9,'A9o':11.6,'A8o':13.4,'A7o':15.7,'A6o':19.0,'A5o':18.1,'A4o':19.9,'A3o':22,'A2o':23.7}
Axo2=['AKo','AQo','AJo','ATo','A9o','A8o','A7o','A6o','A5o','A4o','A3o','A2o']
Kxs={'KQs':10.3,'KJs':12.2,'KTs':14.8,'K9s':22/8,'K8s':25.2,'K7s':25.5,'K6s':27,'K5s':28.5,'K4s':29.7,'K3s':31.8,'K2s':32.1}
Kxo={'KQo':16.9,'KJo':20.8,'KTo':24.6,'K9o':26.7,'K8o':29.4,'K7o':31.5,'K6o':33.3,'K5o':34.5,'K4o':37.3,'K3o':39.1,'K2o':40.6}
Qxs={'QJs':21.1,'QTs':24.9,'Q9s':28.2,'Q8s':32.4,'Q7s':37.6,'Q6s':38.2,'Q5s':39.7,'Q4s':41.8,'Q3s':43.0,'Q2s':44.8}
Qxo={}

Jxs={'JTs':25.8,'J9s':33.6,'J8s':39.4,'J7s':43.6,'J6s':49,'J5s':49.6,'J4s':50.8,'J3s':54.1,'J2s':55.7}
Jxo={'JTo':36.3,'J9o':42.7,'J8o':47.8,'J7o':51.7,'J6o':56.9,'J5o':59.9,'J4o':61.7,'J3o':65.3,'J2o':69.5}

Txs={'T9s':37.9,'T8s':43.3,'T7s':49.3,'T6s':54.4,'T5s':60.2,'T4s':60.5,'T3s':63.8,'T2s':65.6}
Txo={'T9o':48.7,'T8o':53.8,'T7o':58.7,'T6o':62.6,'T5o':68.6,'T4o':71.0,'T3o':74.7,'T2o':77.4}
x9s={'98s':46,'97s':52.9,'96s':59,'95s':64.4,'94s':70.1,'93s':72.5,'92s':75.9}
x9o={'98o':57.8,'97o':63.5,'96o':67.7,'95o':73.8,'94o':79.8,'93o':82.2,'92o':85.5}
x8s={'87s':56,'86s':60.8,'85s':66.8,'84s':72.9,'83s':78.9,'82s':81}
x8o={'87o':66.5,'86o':72.2,'85o':78.3,'84o':84.6,'83o':90.3,'82o':91.6}


x7s={'76s':64.1,'75s':69.8,'74s':76.2,'73s':81.3,'72s':87}
x7o={'76o':75.6,'75o':80.7,'74o':86.7,'73o':92.9,'72o':96.4}

x6s={'65s':71.3,'64s':78.6,'63s':83.7,'62s':89.4}
x6o={'65o':83.1,'64o':88.8,'63o':94.3,'62o':98.2}

x5s={'54s':76.5,'53s':83.4,'52s':89.1}
x5o={'54o':87.9,'53o':93.4,'52o':97.3}

x4s={'43s':85.8,'42s':90.6}
x4o={'43o':95.5,'42o':99.1}

x3s={'32s':94.6}
x3o={'32o':100}

sc1=['AKs','KQs','QJs','JTs','T9s','98s','87s','76s','65s','54s','43s','32s']

sc2=['AQs','KJs','QTs','J9s','T8s','97s','86s','75s','64s','53s','42s']

allHands=[pair,Axs,Axo,Kxs,Kxo,Qxs,Qxo,Jxs,Jxo,Txs,Txo,x9s,x9o,x8s,x8o,x7s,x7o,x6s,x6o,x5s,x5o,x4s,x4o,x3s,x3o]



def updateHandsRank(db=mongo.c5p2r169db,allHands=allHands):
    for type in allHands:
        for key in type:
            data=db.find_one(
                {'hands':key},
            )
            data['percent']=type[key]
            db.replace_one(
                {'hands':key},
                data,
                upsert=True
            )
    res=db.find({}).sort([('percent',1)])
    for index,data in enumerate(res):
        data['index']=index
        db.replace_one(
            {'hands':data['hands']},
            data,
            upsert=True
        )


def getRangeHands(l=160):
    db=mongo.generateDB(rangee=str(l))
    res=db.find({}).sort([('winRate',-1)])
    return res


def _expandPair(s):
    result=[]
    s1=s[0]
    tags=Card.tags
    for c1 in range(0,3):
        for c2 in range(c1+1,4):
            result.append(s1+tags[c1]+s1+tags[c2])
    return result

def _expandSuited(s):
    result=[]
    tags=Card.tags
    for c1 in range(0,4):
        result.append(s[0]+tags[c1]+s[1]+tags[c1])
    return result

def _expandOffsuit(s):
    result=[]
    tags=Card.tags
    for c1 in range(0,4):
        for c2 in range(0,4):
            if c1!=c2:
                result.append(s[0]+tags[c1]+s[1]+tags[c2])
    return result

def expandRangeToReal(handsList):
    result=[]
    for s in handsList:
        if len(s)==2:
            result.extend(_expandPair(s))
        elif s.endswith('s'):
            result.extend(_expandSuited(s))
        elif s.endswith('o'):
            result.extend(_expandOffsuit(s))
        else:
            raise 'Error'
    return result

def reduceHands(fromRange=165,step=5):
    length=fromRange-step
    dbfrom=mongo.generateDB(playerNum=2,rangee=str(fromRange))
    res=mongo.getSortedData(dbfrom,'winRate',-1)
    result=[]
    for data in res:
        result.append(data['hands'])
    if __name__ == '__main__':
        print(result[0:length])
    return result[0:length]

def main():
    # print(getRangeHands(30))
    reduceHands(fromRange=165)


if __name__ == '__main__':
    main()
