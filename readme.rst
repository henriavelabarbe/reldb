Relational database in Python

============
Introduction
============
A relational database management system is a set of components managing a relational database.
A relational database is a container for relational structures that can be operated using relation operators.

Elements :

* datatype : define the domain of a type, for instance char, date, numeric, integer, employerid,..

* heading : a set of attribute name, datatype pair

* tuple : a set of attribute name, value corresponding to a heading

* relation variable : a set of tuple responding to a predicate at a given time

* key : a set of attribute that uniquely determine a tuple in a relation variable

* constraint : a predicate that should evaluate to true

* transaction : a list of actions on database components that is atomic

* action : a change on the database

The information stored in the database can be of 2 types : metadata and relvar data.
Metadata is used by the system to manage user data.
Exemple of metadata : datatypes and their repr, definition of relations, ..

It is questionable how this distinction is usefull as some information is difficult to place in a context.


.. table:: Relational operators

======
  op
======

===========
components
===========

client : software that interface an application to the database
         receive api calls and send data trough socket
         maybe increased with a parser 

parser : transform a string of char to an AST

pool manager : handle connections from client
               pass communication to transaction managers

transaction manager : handle transactions
                      serialize or parallel calls to storage managers
storage manager : persist db changes to disk and memory
                  retrieve db changes from disk and memory
resultset manager : provide a instant view of database elements from db changes
                    
replication manager : manage replication between storage managers



=======
diagram
=======

client <-->         pool manager        <--> db server
   reld transactions            reld transactions

client:
parser : so we can offload parsing
metadata : result cache, so we can offload metadata query for parsing
data : result cache, so we can offload data query for parsing

db server :
parser <--> metadata <--> storage manager
parser --> AST

DB Action --> transaction log

=======
Transactions and actions
=======

A transaction is an ordered list of actions.
An action is an operation (CRUD) on metadata or on user data.

Examples:
CRUD a datatype
CRUD a relation variable (so a heading, key, tuples)
CRUD a database constraint
CRUD a tuple in a relation variable
update the heading of relation variable
reading a relation variable and returning the result to a client

We can bootstrap those in a limited RDBMS for metadata. 

relvar datatype : type_name: char, type_create:(char -> type_name)
relvar datatype_repr : type_name: char, type_repr : (datatype -> char)
relvar datatype_store : type_name: char, type_store : (datatype -> bitfield)

relvar heading : heading_id: uniqueid
relvar relation : relation_id: uniqueid, relation_name: char, heading_id: headingid, comment: varchar
relvar relation_tuples : 

relvar action : action_name: char, action_object:

How do we manage changes in that context ?

==========
scenario 1
==========

client send some reld commands in a transaction to pool manager
pool manager send reld command to db server
db server parse reld commands, send AST to db server transaction manager and return result
transaction manager checks all constraints and persists changes in transaction logs
AST is stored in the transaction log

