"""
Module for relational operators

"""
import relvar


def rename(irelvar, rename_dict):
    'Return a relvar with renamed attributes'
    return irelvar.rename(rename_dict)


def restrict(relvar, predicate):
    'Return a relvar responding to predicate expr'
    return relvar

def project(relvar, attributes):
    return relvar

def join(relvar1, relvar2):
    return relvar1

def union(relvar1, relvar2):
    return relvar1

def intersect(relvar1, relvar2):
    return relvar1

def difference(relvar1, relvar2):
    return relvar1

def extend(relvar1, expression, attribute):
    return relvar1

def summarize():
    return set()


if __name__ == '__main__':
    print("Empty test")
