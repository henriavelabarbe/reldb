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
Information about cached structure is used to avoid applying
all transactions from DB init.
The same caching could be used for metadata.

'''
import json
import gzip
from action import Action, encode_action, decode_action
from transaction import Transaction, encode_transaction, decode_transaction, list_relvar_from_trans_dict


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
                print('Storage found, last transaction id = '
                      + str(self.transaction_id))
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
            json.dump(transaction, transaction_file,
                      default=encode_transaction)
            self.transaction_id = current_transaction
            with open(self.database + '_last_transaction_id', 'w') as lstrfile:
                json.dump(self.transaction_id, lstrfile)

    def load_transactions(self, transaction_from=1, transaction_to=None):
        '''
        Load transactions (dict of actions) from file into a dict.
        TODO : use yield to avoid loading all in memory
        TODO : add an accumulator, so an existing db cache can be updated
        '''
        if transaction_to is None:
            transaction_to = self.transaction_id
        dbdict = dict()
        for i in range(transaction_from, transaction_to):
            with open(self.database + '.' + str(i) + '.trans', 'r') as curfile:
                dbdict[i] = json.load(curfile)
        return dbdict

    def last_transaction_id(self):
        return self.transaction_id


class Database():
    def __init__(self, name):
        self.name = name
        self.storage_server = StorageServer(self.name)


def test_create_transactions():
    'Create some transactions and return them in a list'
    TR1 = Transaction({'1': Action('C', 'R', 'SUPPLIER', 'HEAD1'),
                       '2': Action('C', 'R', 'CLIENT', 'HEAD2')})
    TR2 = Transaction({'1': Action('D', 'R', 'SUPPLIER', 'HEAD1'),
                       '2': Action('D', 'R', 'CLIENT', 'HEAD1')})
    TR3 = Transaction({'1': Action('C', 'R', 'SUPPLIER', 'HEAD1'),
                       '2': Action('D', 'R', 'SUPPLIER', 'HEAD1')})
    return [TR1, TR2, TR3]


def test_init_metadata():
    'Create transactions related to metadata'
    ACTIONS = [ Action('C', 'T', 'CHAR'),
                Action('C', 'T', 'DATE'),
                Action('C', 'T', 'NUMERIC'),
                Action('C', 'R', 'DATATYPE', 'HEADDATATYPE')]
    TR = { k: v for k, v in enumerate(ACTIONS)}
    return  [Transaction(TR)]


def test_store_transactions(storage_server, transactions):
    'Store several transactions in the given storage'
    for transaction in transactions:
        storage_server.store_transaction(transaction)

if __name__ == '__main__':
    STORE1 = StorageServer()
    test_store_transactions(STORE1, test_create_transactions())
    test_store_transactions(STORE1, test_init_metadata())
    data1 = STORE1.load_transactions()
    print(data1)
    list_relvar_from_trans_dict(data1)
