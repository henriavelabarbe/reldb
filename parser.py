"""
Example of valid syntax to parse :
TUPLE { S# S#('S1'), SNAME NAME('Smith'), STATUS 20, CITY 'London' }
S WHERE NOT ( CITY = 'Athens' ) ;
DELETE S WHERE CITY = 'Athens' ;
RELATION {
        TUPLE { S# S#('S1'), SNAME NAME('Smith'),
                 STATUS 20, CITY 'London' } ,
        TUPLE { S# S#('S2'), SNAME NAME('Jones'),
                 STATUS 10, CITY 'Paris' } ,
        TUPLE { S# S#('S3'), SNAME NAME('Blake'),
                 STATUS 30, CITY 'Paris' } ,
        TUPLE { S# S#('S4'), SNAME NAME('Clark'),
                 STATUS 20, CITY 'London' } ,
        TUPLE { S# S#('S5'), SNAME NAME('Adams'),
                 STATUS 30, CITY 'Athens' } }
TUPLE { S# S#('S1'), SNAME NAME('Smith'), STATUS 20, CITY 'London' }

a projection :
S { S#, SNAME, STATUS }
"""

def parse(text):
    "Simply parse input and return AST"
    words = text.split()
    if words[0] == 'relvar':
        newRelvar(words[1], 'jj', 'kk')
    elif words[0] == 'insert':
        insRelvar(words[1], 'jjj')
    else :
        errorParsing()

def newRelvar(name, attributes, values):
    print('newrelvar', name)

def insRelvar(name, values):
    print('ins', name)

def errorParsing():
    print('Error Parsing')
