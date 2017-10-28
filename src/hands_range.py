# -*- coding=utf-8 -*-

from mongo import mongo
from card import Card

pair=['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22', ]
Axs=['AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s']
Axo=['AKo','AQo','AJo','ATo','A9o','A8o','A7o','A6o','A5o','A4o','A3o','A2o']

Kxs=['KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s''KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s']
Kxo=['KQo', 'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o', 'K5o', 'K4o', 'K3o', 'K2o',]

Qxs=['QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s']
Qxo=['QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o', 'Q6o', 'Q5o', 'Q4o', 'Q3o', 'Q2o', ]

Jxs=['JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',]
Jxo=['JTo', 'J9o', 'J8o', 'J7o', 'J6o', 'J5o', 'J4o', 'J3o', 'J2o',]
Txs=['T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s',]
Txo=['T9o', 'T8o', 'T7o', 'T6o', 'T5o', 'T4o', 'T3o', 'T2o', ]
x9s=['98s', '97s', '96s', '95s', '94s', '93s', '92s',]
x9o=['98o', '97o', '96o', '95o', '94o', '93o', '92o', ]
x8s=['87s', '86s', '85s', '84s', '83s', '82s',]
x8o=['87o', '86o', '85o', '84o', '83o', '82o',]


x7s=['76s', '75s', '74s', '73s', '72s',]
x7o=['76o', '75o', '74o', '73o', '72o']

x6s=['65s', '64s', '63s', '62s']
x6o=['65o', '64o', '63o', '62o',]

x5s=['54s', '53s', '52s',]
x5o=['54o', '53o', '52o',]

x4s=['43s', '42s',]
x4o=['43o', '42o',]

x3s=['32s']
x3o=['32o']

sc1=['AKs','KQs','QJs','JTs','T9s','98s','87s','76s','65s','54s','43s','32s']
sc2=['AQs','KJs','QTs','J9s','T8s','97s','86s','75s','64s','53s','42s']

oc1=['AKo','KQo','QJo','JTo','T9o','98o','87o','76o','65o','54o','43o','32o']
oc2=['AQo','KJo','QTo','J9o','T8o','97o','86o','75o','64o','53o','42o']


allHandsType=[pair,Axs,Axo,Kxs,Kxo,sc1,sc2,oc1,oc2,Qxs,Qxo,Jxs,Jxo,Txs,Txo,x9s,x9s,x8s,x8o,x7s,x7o,x6s,x6o,x5s,x5o,x4s,x4o,x3s,x3o,]

r169=['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'AKo', 'AQo', 'AJo', 'ATo', 'A9o', 'A8o', 'A7o', 'A6o', 'A5o', 'A4o', 'A3o', 'A2o', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s', 'KQo', 'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o', 'K5o', 'K4o', 'K3o', 'K2o', 'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s', 'QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o', 'Q6o', 'Q5o', 'Q4o', 'Q3o', 'Q2o', 'JTs','J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s', 'JTo', 'J9o','J8o', 'J7o', 'J6o', 'J5o', 'J4o', 'J3o', 'J2o', 'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s', 'T9o', 'T8o', 'T7o', 'T6o', 'T5o', 'T4o', 'T3o', 'T2o', '98s', '97s', '96s', '95s', '94s', '93s', '92s', '98o', '97o', '96o', '95o', '94o', '93o', '92o', '87s', '86s', '85s', '84s', '83s', '82s', '87o', '86o', '85o', '84o', '83o', '82o', '76s', '75s', '74s', '73s', '72s', '76o', '75o', '74o', '73o', '72o','65s', '64s', '63s', '62s', '65o', '64o', '63o', '62o', '54s', '53s', '52s', '54o', '53o', '52o', '43s', '42s', '43o', '42o', '32s', '32o']

allHands=r169


def getDefault169HandsRange():
    return r169

def getRangeHands(l=165):
    if l>=166:
        l=169
        return getDefault169HandsRange()
    db=mongo.generateDB(rangee=str(l))
    res=db.find({}).sort([('winRate',-1)])
    result=[]
    for data in res:
        result.append(data['hands'])
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

def reduceHands(fromRange=165,step=5,winRate='winRate0',postfix=''):
    length=fromRange-step
    dbfrom=mongo.generateDB(playerNum=2,rangee=str(fromRange),postfix=postfix)
    res=mongo.getSortedData(dbfrom,winRate,-1)
    result=[]
    for data in res:
        result.append(data['hands'])
    if __name__ == '__main__':
        print(result[0:length])
    return result[0:length]

    # 22+,AJs+,AQo,87s+,QTo+
def makeRanges(s='22+'):
    result=[]
    s=s.replace(' ','')
    if not ',' in s:
        s+=','
    for s1 in s.split(','):
        s1=s1.replace('+','')
        for type in allHandsType:
            if s1 in type:
                index=type.index(s1)
                for hands in type[0:index+1]:
                    if hands not in result:
                        result.append(hands)
    return result


def main():
    # ls=getRangeHands(169)
    print(makeRanges('33+,AJs+,65s+'))


if __name__ == '__main__':
    main()

c5p2r90=['AA','KK','QQ','JJ','AKs','TT','AKo','AQs','AQo','AJs','99','AJo','ATs','88','A8s','A9s','ATo','A7s','KQs','A9o','KJs','A5s','77','A6s','KQo','66','A8o','A4s','KTs','KJo','A3s','A7o','A2s','A5o','55','KTo','K8s',
'44','A4o','A2o','K9s','K9o','K6s','QJs','33','QTs','K8o','QJo','QTo','K7s','JTs','Q9s','22','Q8s','Q9o','J9s','JTo','T9s','Q8o','J8s','J9o','98s','Q7o','87s','Q6o','J7s','76s','T8s','Q3s','T9o','T7s',]


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