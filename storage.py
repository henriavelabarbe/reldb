'''
The module manage disk storage of relations.
Here, we are using a json format for tuples and relations.

To avoid overhead, we should store relations in a composable fashion,
so updates and insert are relational ops on unmutable relations

Metadata are stored in a directory .metadata
Transactions are stored in a directory .transaction
 Files are stored in increasing file name
 Transactions are a json dump of a dict with action and param
 Actions are relops :
     UNION of preceding relation with the one in trans
     MINUS of preceding relation with this one
     RENAME
     EXTEND
     An insert is an union
     A delete is a
     An update is (r1 MINUS r2) UNION s2

Objects metadata :
    type : name, from_str, to_str
    attribute : name, type
    heading : attributes
    relvar : name, heading, key

Those metadata should be themselves stored in relation variables.
Maybe using a specific storage server.

A storage server will be used to store the DB actions in transaction logs.
Those should be encoded in a compact structure but efficient for replay,
as it is the standard way to get current relation variable values.

A simple storage server for metadata is used as bootstrap.

A caching mechanim exist for most used result sets
(here a relation variable, really).
Information about cached structure is used to avoid applying all transactions from DB init.
The same caching could be used for metadata.

'''
import json
import gzip


def create_relation(name, heading, values):
    return None


def delete_relation(name, heading, values):
    return None


def update_relation(name, heading, values):
    return None


def read_relation(name, heading, values):
    return None


class Transaction():
    '''
    A transaction is a list of database operations.
    '''
    def __init__(self, actions):
        self.actions = actions

def encode_transaction(transaction):
        return {key: encode_action(action) for key, action in transaction.actions.items()}

class Action():
    '''
    An action on the DB :
        1 - Create a relation
            name
            heading
            key

        2 - Delete a relation
            name

        3 - Update a relation
            name
            update_phrase

        4 - Create a type
            name
            constructor
            string_repesentation

        5 - Delete a type
            name

        6 - Update a type
            name
            update_phrase

        7 - Insert a tuple into a relation
            relation_name
            tuple

        8 - Delete a tuple from a relation
            relation_name
            delete_predicate

        9 - Update a tuple from a relation
            relation_name
            update_phrase
    '''

    def c_rel(self):
        return None

    def d_rel(self):
        return None

    def u_rel(self):
        return None

    def c_type(self):
        return None

    def d_type(self):
        return None

    def u_type(self):
        return None

    def c_tuple(self):
        return None

    def d_tuple(self):
        return None

    def u_tuple(self):
        return None

    ACTIONS = {'CREL': 1, 'DREL': 2, 'UREL': 3, 'CTYPE': 4, 'DTYPE': 5,
               'UTYPE': 6, 'CTUPLE': 7, 'DTUPLE': 8, 'UTUPLE': 9}

    FUNCS = {'CREL': c_rel, 'DREL': d_rel, 'UREL': u_rel, 'CTYPE': c_type,
             'DTYPE': d_type, 'UTYPE': u_type, 'CTUPLE': c_tuple,
             'DTUPLE': d_tuple, 'UTUPLE': u_tuple}

    ARGS = {'CREL': ('name', 'heading'), 'DREL': d_rel, 'UREL': u_rel, 'CTYPE': c_type,
            'DTYPE': d_type, 'UTYPE': u_type, 'CTUPLE': c_tuple,
            'DTUPLE': d_tuple, 'UTUPLE': u_tuple}

    def __init__(self, action, *args):
        'ACTIONS will be used to encode data in journal'
        self.action = Action.ACTIONS[action]
        self.args = args

def encode_action(action):
        #return [self.action, self.args]
        return [action.action, action.args]



class StorageServer():
    '''
    A storage server manage all the persistence of a database.
    '''
    def __init__(self, database='default'):
        '''
        TODO : add a check for existing storage for database
        '''
        self.database = database
        self.transaction_id = 0
        try:
            with open(self.database + '_last_transaction_id', 'r') as lstrfile:
                self.transaction_id = json.load(lstrfile)
                print('Storage found, last transaction id = ' + str(self.transaction_id))
        except:
            with open(self.database + '_last_transaction_id', 'w') as lstrfile:
                json.dump(self.transaction_id, lstrfile)
                print('Storage not found, initating.')

    def store_transaction(self, transaction):
        '''
        Transactions are stored in transaction log files.
        Those log files can be replayed to construct a database object.
        ? : should we express transactions as relops ?
            insert, update, .. are shorthand for relops.
        '''
        current_transaction = self.transaction_id + 1
        with open(self.database + '.' + str(current_transaction)
                  + '.trans', 'w') as transaction_file:
            json.dump(transaction, transaction_file, default=encode_transaction)
            self.transaction_id = current_transaction
            with open(self.database + '_last_transaction_id', 'w') as lstrfile:
                json.dump(self.transaction_id, lstrfile)

    def load_transactions(self, transaction_from=1, transaction_to=None):
        '''
        Load transactions from file into a dict.
        TODO : use yield to avoid loading all in memory
        TODO : add an accumulator, so an existing db cache can be updated
        '''
        if transaction_to is None:
            transaction_to = self.transaction_id
        dbdict = dict()
        for i in range(transaction_from, transaction_to):
            with open(self.database + '.' + str(i) + '.trans', 'r') as curfile:
                dbdict[i] = json.load(curfile)
                print('LOAD TRANS:', dbdict)

    def last_transaction_id(self):
        return self.transaction_id


class Database():
    def __init__(self, name):
        self.name = name
        self.storage_server = StorageServer(self.name)


def init_db(database='default'):
    '''
    Initialize DB metadata
    Create disk structures for relation, heading
    1 - Check if db exist
    2 - Create metadata dir
    3 - Create type, attribute, heading, relvar structures
    4 - Return created database object
    '''
    with open(database + '.' + 'meta', 'w') as dbfile:
        json.dump({'transaction': ['initdb'],
                   'relvar': {'relation':{},
                              'heading':{}}}, dbfile)


HEAD_TYPE = 'name:string,from_str:func,to_str:func'
TRANS_TYPE = 'CR,_type,' + HEAD_TYPE + '%name'
HEAD_ATT = 'headname:string,name:string,type:string'
TRANS_ATT = 'CR,_attribute,' + HEAD_ATT + '%headname,name'
RELVAR_TYPE = 'name:string,headname:string,key:attribute'

def write_trans(transaction, transaction_number, database='default'):
    'Store a transaction on disk'
    with open(database + '_' + str(transaction_number) + '.tr') as tr_file:
        json.dump(transaction, tr_file)

def open_db(database='default'):
    '''
    Read or init database metadata
    Return the db metadata object
    List of db rel and their properties should be available
    '''
    with open(database + '.' + 'meta', 'r') as dbfile:
        dbmeta = json.load(dbfile)
    return dbmeta


'''
A database metadata should be a journal of transactions.
As we want unmutable data, we should have a structure to manage that.
Same for data, relations should be journaled.
'''


def add_rel(rel, database):
    'Add a relation in a database'
    rdb = database
    rdb['transaction'].append('addrel')
    return rdb


def del_rel(rel, database):
    'Del a relation from database'
    return database


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
    return [dict(id=str(i), lastname=str(i)+'TTTTFFGJGJGJSKKSKSKSKDKDK',
                 firstname=str(i)+'YIYYIYIYIYIYIYI', hiredate='20141001',
                 salary='56000') for i in range(number)]

'The list of possible transactions'

TRANSACTIONS = {
    'initdb': init_db,
    'addrel': add_rel,
    'delrel': del_rel
}

if __name__ == '__main__':
    HEADB = dict(id='number', name='varchar')
    HEADZ = dict(id='number', lastname='varchar', firstname='varchar',
                 hiredate='date', salary='number')
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
#    RELD = dict(head=HEADB, body=tuples2dict(gentuples(100000), key='id'),
    RELD = dict(head=HEADB, body=tuples2dict(gentuples(100), key='id'),
                key='id')
    json.dump(RELD, fp=gzip.open('RELD.dat', 'wt'), indent=4)
    RELE = json.load(gzip.open('RELD.dat', 'rt'))
    print(RELD == RELE)
    init_db()
    metadb = open_db()
    print(metadb)
    metadb2 = add_rel(RELD, metadb)
    print(metadb2)
    STORE1 = StorageServer()
    TR1 = Transaction({'1': Action('CREL', 'SUPPLIER', 'HEAD1'),
           '2':Action('CREL', 'SUPPLIER', 'HEAD1')})
    TR2 = Transaction({'1': Action('CREL', 'SUPPLIER', 'HEAD1'),
           '2':Action('CREL', 'SUPPLIER', 'HEAD1')})
    TR3 = Transaction({'1': Action('CREL', 'SUPPLIER', 'HEAD1'),
           '2':Action('CREL', 'SUPPLIER', 'HEAD1')})
    STORE1.store_transaction(TR1)
    STORE1.store_transaction(TR2)
    STORE1.store_transaction(TR3)
    STORE1.load_transactions()
