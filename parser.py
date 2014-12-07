"""
Example of valid syntax to parse :
TUPLE { S# S#('S1'), SNAME NAME('Smith'), STATUS 20, CITY 'London' }
S WHERE NOT ( CITY = 'Athens' ) ;
DELETE S WHERE CITY = 'Athens' ;

SUPPLIER := RELATION {
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

T1 := TUPLE { S# S#('S1'), SNAME NAME('Smith'), STATUS 20, CITY 'London' }

a projection :
S { S#, SNAME, STATUS }

"""

from pyparsing import *

SIMPLETUPLE = "TUPLE { S# S#('S1'), SNAME NAME('Smith'),TATUS 20, CITY 'London' }"

SUPPLIER = '''
SUPPLIER := RELATION {
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
'''

'''
; identifier
    = '<identifier>'
; string
    = '<string literal>'
; integer
    = '<integer literal>'
; decimal
    = '<decimal literal>'
; float
    = '<float literal>'
'''

identifier = Word(alphanums)

'''
attribute_name
    = identifier
    ;
'''
attribute_name = identifier
'''
type_name
= identifier
    ;
'''
type_name = identifier

'''
rel_expression
    = add_expression
    | add_expression compop add_expression
    ;
'''
rel_expression = Keyword('TOTO')

'''
not_expression
    = rel_expression
    | NOT rel_expression
    ;
'''
not_expression = Group((Keyword('NOT') + rel_expression)) | rel_expression

'''
and_expression
    = not_expression
    | and_expression AND not_expression
    ;
'''
#and_expression = not_expression | and_expression + Keyword('AND') + not_expression
and_expression = Forward()
and_expression << (not_expression + ZeroOrMore(Keyword('AND') + not_expression)).setResultsName('AND')

'''
xor_expression
    = and_expression
    | xor_expression XOR and_expression
    ;
'''
xor_expression = Forward()
xor_expression << (and_expression + ZeroOrMore(Keyword('XOR') + and_expression)).setResultsName('XOR')

'''
or_expression
    = xor_expression
    | or_expression OR xor_expression
    ;
'''
or_expression = Forward()
#or_expression = xor_expression | or_expression + Keyword('OR') + xor_expression
or_expression << (xor_expression + ZeroOrMore(Keyword('OR') + xor_expression)).setResultsName('OR')
print('or_expression:')
print(or_expression.parseString('TOTO'))
print(or_expression.parseString('TOTO OR TOTO'))
print(or_expression.parseString('NOT TOTO XOR TOTO OR TOTO'))
print(or_expression.parseString('NOT TOTO XOR TOTO OR TOTO').__dict__)
print(or_expression.parseString('NOT TOTO XOR TOTO OR TOTO')['AND'])

'''
simple_expression
    = or_expression
    ;
'''
simple_expression = or_expression

'''
relation
    = simple_expression
    | project
    | where
    | rename
    | wrap
    | unwrap
    | group
    | ungroup
    | divide
    ;
'''
relation = simple_expression

'''
relation_exp
    = relation
    | relation_exp relop relation
    ;
'''
relation_exp = relation

'''
expression
    = relation_exp
    | tuple_extractor_inv
    | attribute_extractor_inv
    | with_expression
    | extend
    | summarize
￼   | tclose
    ;
'''
expression = relation_exp

'''
type
￼    = type_name
    | SAME_TYPE_AS '(' expression ')'
    | RELATION heading
    | RELATION SAME_HEADING_AS '(' expression ')'
    | TUPLE heading
    | TUPLE SAME_HEADING_AS '(' expression ')'
    | CHAR
    | CHARACTER
    | INTEGER
    | DECIMAL
    | RATIONAL
    | BOOLEAN
    ;
'''
atype = type_name \
    | Keyword('SAME_TYPE_AS') + '(' + expression + ')' \
    | Keyword('RELATION') + Keyword('SAME_HEADING_AS') + '(' + expression + ')' \
    | Keyword('CHAR') \
    | Keyword('CHARACTER') \
    | Keyword('INTEGER') \
    | Keyword('DECIMAL') \
    | Keyword('RATIONAL') \
    | Keyword('BOOLEAN')

'''
attribute
    = attribute_name type
    ;
'''
attribute = attribute_name + atype + Optional(',')
print('attribute:')
print(attribute.parseString('label CHAR'))
print(attribute.parseString('label SAME_TYPE_AS(toto)'))

'''
attribute_commalist
    = attribute
    | attribute_commalist ',' attribute
    ;
'''
attribute_commalist = attribute * (1, None)

'''
opt_attribute_commalist
    =
    | attribute_commalist
    ;
'''
opt_attribute_commalist = attribute_commalist

'''
heading
    = '{' opt_attribute_commalist '}'
    ;
'''
heading = '{' + opt_attribute_commalist + '}'

def test_heading():
    print('heading:')
    print(heading.parseString('{sid INTEGER, label CHAR, hiredate DATE}'))

'''
constraint_name
= identifier
    ;
introduced_name
    = identifier
    ;
parameter_name
    = identifier
    ;
possrep_name
= identifier
    ;
possrep_component_name
= identifier
    ;
statement_name
= identifier
;
'''


''''
user_op_name
= identifier
    ;
variable_name
= identifier
'''


'''
; boolean
    = TRUE
    | FALSE
    ;
'''
aboolean = Keyword('TRUE') | Keyword('FALSE')
print('boolean:')
print(aboolean.parseString('TRUE'))
print(aboolean.parseString('FALSE'))


'''
expression_commalist
    = expression
    | expression_commalist ',' expression
    ;
'''
expression_commalist = expression * (1,None)

'''
opt_expression_commalist
    =
    | expression_commalist
    ;
'''
opt_expression_commalist = expression_commalist

'''
literal
    = RELATION '{' expression_commalist '}'
    | RELATION heading '{' opt_expression_commalist '}'
| TUPLE
| TABLE_DEE
| TABLE_DUM
| string
| integer
| decimal
| float
| boolean
;
'''
literal = Keyword('RELATION') + '{' + expression_commalist + '}' \
    | Keyword('RELATION') + heading + '{' + opt_expression_commalist + '}' \
    | Keyword('TUPLE') \
    | Keyword('TABLE_DEE') \
    | Keyword('TABLE_DUM') \
    | Word(alphanums) \
    | Word(nums) \
    | aboolean
print('literal:')
print(literal.parseString('TABLE_DEE'))
print(literal.parseString('TABLE_DUM'))


'''
target
    = variable_name
    | THE_ variable_name '(' target ')'
    ;
'''
target = Word(alphanums)
'''
￼opt_where_condition
    =
    | WHERE simple_expression
    ;
'''
opt_where_condition = Keyword('WHERE') + simple_expression

'''
insert
    = INSERT target expression
    ;
'''
insert = Keyword('INSERT') + target + expression
'''
delete
    = DELETE target opt_where_condition
    ;
'''
delete = Keyword('DELETE') + target + opt_where_condition
'''
update
    = UPDATE target opt_where_condition
      SET '(' attribute_assign_commalist ')'
    ;
'''
update = Keyword('UPDATE') + target + opt_where_condition
'''
assign
    = target ':=' expression
    | insert
    | delete
    | update
;
'''

assign = insert \
       | delete \
       | update \
       | target + ':=' + expression
'''
assign_commalist
    = assign
    | assign_commalist ',' assign
;
'''

assign_commalist = assign + Optional(',')

'''
assignment
    = assign_commalist
    ;
'''
assignment = assign_commalist * (1, None)

'''
statement_body
    = -- noop
    | assignment
    | user_op_def
    | user_op_drop
    | user_scalar_type_def
    | user_scalar_type_drop
    | scalar_or_tuple_var_def
    | relation_var_def
    | relation_var_drop
    | constraint_def
    | constraint_drop
    | array_var_def
    | relation_get
    | relation_set
    | transaction_statement
    | call
    | return
    | case
    | if
    | do
    | while
    | leave
    | compound_statement_body
    ;
'''
statement_body = assignment

'''
statement
    = statement_body ';'
    ;
'''
statement = statement_body + ';'

'''
statement_list
    = statement
    | statement_list statement
    ;
'''
statement_list = statement

'''
attribute_assign_commalist
    = attribute_assign
    | attribute_assign_commalist ',' attribute_assign
    ;
attribute_assign
    = attribute_name ':=' expression
    ;
transaction_statement
    = START  opt_transaction
    | COMMIT opt_transaction
    | ABORT  opt_transaction
    ;
opt_transaction
    =
    | TRANSACTION
; call
    = CALL user_op_inv
; return
    = RETURN opt_expression
    ;
opt_expression
    =
    | expression
    ;
case
    = CASE ';' when_def_list opt_else_def END CASE
    ;
when_def_list
    = when_def
    | when_def_list when_def
; when_def
    = WHEN expression THEN statement
; if
    = IF expression THEN statement opt_else_def END IF
    ;
opt_else_def
    =
    | ELSE statement
    ;
do
    = opt_statement_name
      DO identifier ':=' expression TO expression ';'
      statement END DO
    ;
while
    = opt_statement_name
      WHILE expression ';' statement END WHILE
    ;
opt_statement_name
    =
    | statement_name ':'
; leave
    = LEAVE statement_name
    ;
compound_statement_body
= BEGIN ';' statement_list END
￼    ;
user_scalar_type_def
    = TYPE type_name opt_ordinal possrep_def_list
    ;
opt_ordinal
=
| ORDINAL ;
user_scalar_type_drop
    = DROP TYPE type_name
    ;
possrep_def_list
    = possrep_def
    | possrep_def_list possrep_def
    ;
possrep_def
    = POSSREP opt_possrep_name
        '{' possrep_component_def_commalist opt_possrep_constraint_def '}'
    ;
opt_possrep_name
    =
    | possrep_name
    ;
possrep_component_def_commalist
    = possrep_component_def
    | possrep_component_def_commalist ',' possrep_component_def
    ;
possrep_component_def
    = possrep_component_name type
    ;
opt_possrep_constraint_def
    =
    | possrep_constraint_def
    ;
possrep_constraint_def
    = CONSTRAINT expression
    ;
user_op_def
    = user_update_op_def
    | user_readonly_op_def
    ;
user_update_op_def
    = OPERATOR identifier '(' parameter_def_commalist ')'
        UPDATES '{' parameter_name_commalist '}' ';' statement END OPERATOR
    ;
user_readonly_op_def
    = OPERATOR identifier '(' parameter_def_commalist ')'
        RETURNS type ';' statement END OPERATOR
    ;
user_op_drop
    = DROP OPERATOR user_op_name
    ;
parameter_def_commalist
    = parameter_def
    | parameter_def_commalist ',' parameter_def
    ;
parameter_def
    = parameter_name type
    ;
parameter_name_commalist
    = parameter_name
    | parameter_name_commalist ',' parameter_name
    ;
scalar_or_tuple_var_def
    = VAR variable_name type_or_init_value
￼    ;
array_var_def
    = VAR variable_name ARRAY OF type
    ;
relation_var_def
    = database_relation_var_def
    | application_relation_var_def
    ;
database_relation_var_def
    = real_relation_var_def
    | virtual_relation_var_def
    ;
real_relation_var_def
    = VAR variable_name REAL type_or_init_value candidate_key_def_list
    ;
virtual_relation_var_def
    = VAR variable_name VIRTUAL '(' expression ')' candidate_key_def_list
    ;
application_relation_var_def
    = VAR variable_name private_or_public
        type_or_init_value candidate_key_def_list
    ;
private_or_public
    = PRIVATE
| PUBLIC
    ;
relation_var_drop
    = DROP VAR variable_name
    ;
type_or_init_value
    = type
    | INIT '(' expression ')'
    | type INIT '(' expression ')'
    ;
candidate_key_def_list
    = candidate_key_def
    | candidate_key_def_list candidate_key_def
    ;
candidate_key_def
    = KEY '{' attribute_name_commalist '}'
    ;
constraint_def
    = CONSTRAINT constraint_name expression
    ;
constraint_drop
    = DROP CONSTRAINT constraint_name
    ;
relation_get
    = LOAD identifier FROM expression ORDER '(' order_item_commalist ')'
    ;
order_item_commalist
    = order_item
    | order_item_commalist ',' order_item
; order_item
    = direction attribute_name
; direction
= ASC | DESC ;
relation_set
    = LOAD identifier FROM identifier
    ;
'''



'''
opt_tuple_component_commalist
    =
    | tuple_component_commalist
    ;
tuple_component_commalist
    = tuple_component
    | tuple_component_commalist ',' tuple_component
    ;
tuple_component
    = attribute_name expression
    ;
'''


'''
relop
= UNION
    | INTERSECT
    | MINUS
    | JOIN
    | COMPOSE
    | SEMIJOIN
    | MATCHING
    | SEMIMINUS
    | NOT MATCHING
    ;
'''


'''
project
    = relation '{' opt_all_but attribute_name_commalist '}'
    ;
where
    = relation WHERE simple_expression
    ;
rename
    = relation RENAME '(' renaming_commalist ')'
    ;
wrap
    = relation WRAP '(' wrapping_or_grouping_commalist ')'
    ;
unwrap
    = relation UNWRAP '(' attribute_name_commalist ')'
    ;
group
    = relation GROUP '(' wrapping_or_grouping_commalist ')'
    ;
ungroup
    = relation UNGROUP '(' attribute_name_commalist ')'
    ;
divide
    = relation DIVIDEBY expression per
    ;
attribute_name_commalist
    = attribute_name
    | attribute_name_commalist ',' attribute_name
    ;
renaming_commalist
    = renaming
    | renaming_commalist ',' renaming
    ;
renaming
    = attribute_name AS introduced_name
    | PREFIX  string AS string
    | SUFFIX  string AS string
    ;
￼wrapping_or_grouping_commalist
    = wrapping_or_grouping
    | wrapping_or_grouping_commalist ',' wrapping_or_grouping
    ;
wrapping_or_grouping
    = '{' opt_all_but attribute_name_commalist '}' AS introduced_name
    ;
tuple_extractor_inv
    = TUPLE FROM expression
    ;
attribute_extractor_inv
    = identifier FROM expression
    ;
with_expression
    = WITH name_intro_commalist ':' expression
    ;
name_intro_commalist
    = name_intro
    | name_intro_commalist ',' name_intro
; name_intro
    = expression AS introduced_name
; extend
    = EXTEND expression ADD '(' extend_add_commalist ')'
    ;
extend_add_commalist
    = extend_add
    | extend_add_commalist ',' extend_add
    ;
extend_add
    = expression AS introduced_name
    ;
summarize
    = SUMMARIZE expression opt_per_or_by ADD '(' summarize_add_commalist ')'
    ;
opt_per_or_by
    =
    | per
    | BY '{' opt_all_but attribute_name_commalist '}'
    ;
opt_all_but
    =
| ALL BUT
; per
    = PER '(' expression opt_comma_expression ')'
    ;
opt_comma_expression
    =
    | ',' expression
    ;
summarize_add_commalist
    = summarize_add
    | summarize_add_commalist ',' summarize_add
    ;
summarize_add
    = summary AS introduced_name
; summary
    = summary_spec '(' opt_expression_commalist ')'
    ;
summary_spec
    = COUNT
    | COUNTD
    | SUM
    | SUMD
    | AVG
    | AVGD
    | MAX
    | MIN
    | AND
    | OR
    | XOR
    | EXACTLY
    | EXACTLYD
    | UNION
    | D_UNION
    | INTERSECT
    ;
tclose
    = TCLOSE expression
    ;
'''



'''
add_expression
    = mul_expression
    | addop mul_expression
    | add_expression addop mul_expression
    | add_expression '||'  mul_expression
    ;
mul_expression
    = primary_expression
    | mul_expression mulop primary_expression
    ;
primary_expression
    = identifier
    | literal
    | user_op_inv
    | agg_op_inv
    | nadic_op_inv
    | '(' expression ')'
    ;
compop
= '='
    | '/='
    | '>='
    | '<='
    | '>'
    | '<'
    | IN
    | NOT_IN
    | SUBSET OF
    | PROPER SUBSET OF
    | SUPERSET OF
    | PROPER SUPERSET OF
; addop
= '+' | '-' ;
mulop
= '*'
| '/'
    ;
user_op_inv
    = user_op_name '(' opt_argument_commalist ')'
    ;
opt_argument_commalist
    =
    | argument_commalist
    ;
argument_commalist
    = argument
    | argument_commalist ',' argument
; argument
= expression
; agg_op_inv
    = agg_op_name '(' opt_expression_commalist ')'
    ;
agg_op_name
    = COUNT
    | SUM
    | AVG
    | MAX
    | MIN
    | AND
    | OR
    | XOR
    | EXACTLY
    | UNION
    | D_UNION
    | INTERSECT
    ;
nadic_op_inv
    = UNION '{' expression_commalist '}'
    | UNION heading '{' opt_expression_commalist '}'
    | D_UNION '{' expression_commalist '}'
    | D_UNION heading '{' opt_expression_commalist '}'
    | INTERSECT '{' expression_commalist '}'
    | INTERSECT heading '{' opt_expression_commalist '}'
    | JOIN '{' opt_expression_commalist '}'
    ;
    '''
#attribute_name = Word(alphanums+'#')
#datatype_constructor = Word(alphanums+'#')
#datatype = Word(nums) \
 #   | "'" + Word(alphanums) + "'" \
#    | datatype_constructor + '(' + "'" + Word(alphanums) + "'" + ')'
#attribute = attribute_name + datatype + Optional(',')
#atuple = Keyword("TUPLE") + "{" + attribute * (1, None) + "}" + Optional(',')
#relvar = Word(alphas).setResultsName('variable') + ":=" \
#    + Keyword("RELATION") + "{" + atuple * (1, None) + "}"
#print('Relation supplier:')
#print(relvar.parseString(SUPPLIER))
#print('variable:')
#print(relvar.parseString(SUPPLIER)['variable'])


def parse(text):
    "Simply parse input and return AST"
    words = text.split()
    if words[1] == ':=':
        newRelvar(words[0], 'jj', 'kk')
    elif words[0] == 'insert':
        insRelvar(words[1], 'jjj')
    else:
        errorParsing()


def newRelvar(name, attributes, values):
    print('newrelvar', name)


def insRelvar(name, values):
    print('ins', name)


def errorParsing():
    print('Error Parsing')

if __name__ == '__main__':
    test_heading()
