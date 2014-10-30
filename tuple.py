"""
Module for heading, tuple, relation

"""


class Heading:
    'A Heading is a set of atttibute : (attribute name, attribute type)'
    def __init__(self, attributes):
        'Attributes are passed as dictionary'
        self.attributes = attributes

    def __repr__(self):
        return '[Heading: %s]' % self.attributes

    def filter(self, attname):
        'return a dictionary of attributes matching name'
#       return list(name for name in self.attributes if name == attname)
        return {name: val for name, val in self.attributes.items()
                if name == attname}

    def degree(self):
        'return the number of attributes'
        return len(self.attributes)

    def rename(self, rename_dict):
        'rename attribute from dict mapping'
        return Heading(renamedict(self.attributes, rename_dict))


class Tuple:
    'A Tuple is a Heading + a dict of name -> values'
    def __init__(self, heading, values):
        self.heading = heading
        self.values = values

    def __str__(self):
        return '[Tuple: %s %s]' % (self.heading, self.values)

    def filterheading(self, attname):
        return self.heading.filter(attname)

    def filtervalues(self, attname):
        return {name: val for name, val in self.values.items()
                if name == attname}

    def rename(self, rename_dict):
        renamed_head = self.heading.rename(rename_dict)
        renamed_values = renamedict(self.values, rename_dict)
        return Tuple(renamed_head, renamed_values)


class Relation:
    'A Relation is a heading, a key and a dict of simplified Tuples'
    def __init__(self, heading, tuples, key):
        self.heading = heading
        self.body = {t.values[key]: t.values for t in tuples}
        self.key = key

    def __repr__(self):
        return '[Relation:\n %s PK: %s \n %s]' % \
            (self.heading, self.key, str(self.body))

    def rename(self, rename_dict):
        'return a relation with renamed attributes from dict'
        renamed_head = self.heading.rename(rename_dict)
        if self.key in rename_dict:
            renamed_key = rename_dict[self.key]
        else:
            renamed_key = self.key
        renamed_body = {}
        for name, val in self.body.items():
            renamed_body[name] = renamedict(val, rename_dict)
#       return Relation(renamed_head, renamed_body.values(), renamed_key)
        return Relation(renamed_head,
                        [Tuple(renamed_head, x)
                         for x in renamed_body.values()],
                        renamed_key)


def renamedict(i_dict, i_rename_dict):
    'return dict with renamed keys'
    renamed_dict = {}
    for name, val in i_dict.items():
        if name in i_rename_dict:
            renamed_dict[i_rename_dict[name]] = val
        else:
            renamed_dict[name] = val
    return renamed_dict


def tupletodict(i_tuple):
    'Extract dict from Tuple'
    return i_tuple.values


if __name__ == '__main__':
    HEAD2 = Heading({'id': 'number', 'name': 'varchar'})
    HEAD3 = HEAD2.rename({'name': 'lastname', 'id': 'pid'})
    print('HEAD3: ' + str(HEAD3))
#   print('rename', HEAD2.rename('name', 'lastname'))
#   print({'id':'number'} == HEAD2.filter('id'))
#   print(HEAD2.filter('name'))
#   print(2  == HEAD2.degree())
    TUPLE4 = Tuple(HEAD2, {'id': 1, 'name': 'toto'})
    TUPLE5 = Tuple(HEAD2, {'id': 2, 'name': 'tutu'})
    TUPLE6 = Tuple(HEAD2, {'id': 3, 'name': 'tata'})
    TUPLE7 = TUPLE4.rename({'name': 'lastname', 'id': 'pid'})
    print('TUPLE7: ' + str(TUPLE7))
#   print('rename tuple', str(TUPLE4.rename('name', 'lastname')))
    RELVAR2 = Relation(HEAD2, [TUPLE4, TUPLE5, TUPLE6], 'id')
    RELVAR3 = RELVAR2.rename({'name': 'lastname', 'id': 'pid'})
    print('HEAD2: ' + str(HEAD2))
#   print('HEAD2 attr' +  str(HEAD2.attributes))
    print('TUPLE4: ' + str(TUPLE4))
#   print('TUPLE4 heading : ', TUPLE4.heading)
#   print('TUPLE4 heading name : ', TUPLE4.filterHeading('name'))
#   print('TUPLE4 values name : ', TUPLE4.filterValues('name'))
    print('relvar2:' + str(RELVAR2))
    print('relvar3:' + str(RELVAR3))
#   print('relvar2 tuples', relvar2.body)
#   print('rlevar rename', relvar2.rename('name', 'lastname'))
