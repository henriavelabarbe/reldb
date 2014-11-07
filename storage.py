'''
The module manage disk storage of relations.
We are using a json format for tuples and relations.
To avoid overhead, we should store relations in a composable fashion.
'''
#from relvar import Relation, Tuple, Body, Heading, RELA, HEADA
import json
import gzip


def store_rel(rel, database='default'):
    'Store a relation in a database'
    with open(database, 'w') as dbfile:
        json.dump(rel, dbfile)


def simple_tuple(i_tuple):
    'Return a tuple without heading'
    return i_tuple['values']


def tuples2dict(i_tuples, key):
    'Return a dict of tuples on key, from a list of tuples'
    return {t[key]: t for t in i_tuples}


def gentuples(number):
    'Return a list of number tuples'
    return [dict(id=str(i), name=str(i)+'TTTT') for i in range(number)]


def gentuplesz(number):
    'Return a list of number tuples'
    return [dict(id=str(i), lastname=str(i)+'TTTTFFGJGJGJSKKSKSKSKDKDK', firstname=str(i)+'YIYYIYIYIYIYIYI', hiredate='20141001', salary='56000') for i in range(number)]

if __name__ == '__main__':
    HEADB = dict(id='number', name='varchar')
    HEADZ = dict(id='number', lastname='varchar', firstname='varchar', hiredate='date', salary='number')
#   The json.dumps doesn't respect id being a numeric, so we use string
    TUPLEB = dict(head=HEADB, values=dict(id='1', name='toto'))
    TUPLEC = dict(head=HEADB, values=dict(id='2', name='tutu'))
    TUPLED = dict(head=HEADB, values=dict(id='3', name='tata'))
    print('toto', simple_tuple(TUPLEB))
    BODYB = map(simple_tuple, [TUPLEB, TUPLEC, TUPLED])
    BODYB2 = tuples2dict(BODYB, 'id')
    print(BODYB2)
    RELB = dict(head=HEADB, body=BODYB2, key='id')
    print(RELB)
    print(json.dumps(HEADB))
    print(json.dumps(TUPLEB))
    print(json.dumps(TUPLEC))
    print(json.dumps(TUPLED))
    print(json.dumps(RELB))
    json.dump(RELB, fp=open('RELB.dat', 'w'), indent=4)
    RELC = json.load(open('RELB.dat'))
    print(RELB == RELC)
    print('RELC', RELC)
    print('RELB', RELB)
    RELD = dict(head=HEADB, body=tuples2dict(gentuples(1000000), key='id'), key='id')
    RELZ = dict(head=HEADZ, body=tuples2dict(gentuplesz(1000000), key='id'), key='id')
    json.dump(RELD, fp=gzip.open('RELD.dat', 'wt'), indent=4)
    RELE = json.load(gzip.open('RELD.dat', 'rt'))
    json.dump(RELZ, fp=gzip.open('RELZ.dat', 'wt'), indent=4)
    RELEZ = json.load(gzip.open('RELZ.dat', 'rt'))
    print(RELD == RELE)
