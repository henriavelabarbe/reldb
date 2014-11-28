'''
 Actions are relops :
     UNION of preceding relation with the one in trans
     MINUS of preceding relation with this one
     RENAME
     EXTEND
     An insert is an union
     A delete is a
     An update is (r1 MINUS r2) UNION s2

'''
import json
import gzip



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

    CRUD = ['C', 'R', 'U', 'D']
    OBJECT = ['D', 'H', 'T', 'R', 'C']

    FUNCS = {'CREL': c_rel, 'DREL': d_rel, 'UREL': u_rel, 'CTYPE': c_type,
             'DTYPE': d_type, 'UTYPE': u_type, 'CTUPLE': c_tuple,
             'DTUPLE': d_tuple, 'UTUPLE': u_tuple}

    ARGS = {'CREL': ('name', 'heading'), 'DREL': d_rel,
            'UREL': u_rel, 'CTYPE': c_type,
            'DTYPE': d_type, 'UTYPE': u_type, 'CTUPLE': c_tuple,
            'DTUPLE': d_tuple, 'UTUPLE': u_tuple}

    def __init__(self, i_crud, i_object, *args):
        'ACTIONS will be used to encode data in journal'
        self.crud = i_crud
        self.object = i_object
        self.args = args


def encode_action(action):
    'Return a list value of the action object'
    return [action.crud, action.object, action.args]

def decode_action(i_list):
    'Return an action object from a list'
    return Action(i_list[0], i_list[1], i_list[2:])


if __name__ == '__main__':
    print('Test start')
