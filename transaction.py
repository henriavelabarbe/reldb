'''
 Files are stored in increasing file name
 Transactions are a json dump of a dict with action and param
'''
from action import Action, encode_action, decode_action


class Transaction():
    '''
    A transaction is a dict of database operations.
    '''
    def __init__(self, actions):
        self.actions = actions

    def __str__(self):
        return 'Transaction : ' + map(str, actions)


def encode_transaction(transaction):
    return {key: encode_action(action)
            for key, action in transaction.actions.items()}


def decode_transaction(db_dict):
    return {key: decode_action(action) for key, action in db_dict.items()}



if __name__ == '__main__':
    print('Test')
