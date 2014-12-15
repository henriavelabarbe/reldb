'''
A simple parser for TUPLE, RELATION, VAR (based on tutoriald.bnf)
'''
from pyparsing import *

identifier = Word(alphanums)
#type_ref = Keyword('CHAR') | Keyword('BOOL') | Keyword('NUMERIC')
heading = Forward()
expression = Forward()
same_heading_as = Keyword('SAME HEADING AS') + '(' + expression + ')'
heading_type = heading | same_heading_as
tuple_type = Keyword('TUPLE') + heading_type
relation_type = Keyword('RELATION') + heading_type
#type_ref = identifier | tuple_type | relation_type
type_ref = Keyword('CHAR') | Keyword('BOOL') | Keyword('NUMERIC') | tuple_type | relation_type
attribute_spec = identifier + type_ref
attribute_spec_commalist = attribute_spec + ZeroOrMore(',' + attribute_spec)
heading << '{' + Optional(attribute_spec_commalist) + '}'
relation_heading = Optional(heading)
tuple_exp_commalist = Optional(expression + ZeroOrMore(',' + expression))
relation = Keyword('RELATION') + relation_heading + '{' + tuple_exp_commalist + '}' | Keyword('TABLE_DEE') | Keyword('TABLE_DUM')
bool_ = Keyword('TRUE') | Keyword('FALSE')
tuple_ = Forward()
integer = Word(nums)
character = '"' + Word(alphanums) + '"'
literal = tuple_ | relation | integer | character | bool_
primary_expression = literal
unary_expression = primary_expression
mul_expression = unary_expression
add_expression = mul_expression
attribute_name_commalist = Optional(identifier + ZeroOrMore(',' + identifier))
optional_all_but = Optional(Keyword('ALL') + Keyword('BUT'))
attribute_name_list = optional_all_but + attribute_name_commalist
rel_project = add_expression + Optional('{' + attribute_name_list + '}')
rel_monadic = rel_project
compare_expression = rel_monadic
basic_expression = compare_expression
expression << basic_expression
tuple_component = identifier + expression
tuple_component_commalist = tuple_component + ZeroOrMore(',' + tuple_component)
tuple_ << Keyword('TUPLE') + '{' + Optional(tuple_component_commalist) + '}'
var_type_and_optional_init = type_ref + Keyword('INIT') + '(' + expression + ')'
var_type_or_init_value = var_type_and_optional_init
var_scalar_or_tuple = var_type_or_init_value
var_keydef = Keyword('KEY') + '{' + attribute_name_list + '}'
var_keydeflist = var_keydef + ZeroOrMore(var_keydef)
var_relvar = Keyword('BASE') + var_type_or_init_value + var_keydeflist
var_def = Keyword('VAR') + identifier + (var_scalar_or_tuple | var_relvar)
assign = identifier + Keyword(':=') + expression
assignment = assign + ZeroOrMore(',' + assign)
drop = Keyword('DROP') + Keyword('VAR') + identifier
statement_body = assignment | var_def | drop
#statement_body = var_def
statement = statement_body + ';'


if __name__ == '__main__':
    print(tuple_.parseString('TUPLE { id 345, label "RTITITI"}'))
    print(relation.parseString('RELATION {id NUMERIC, label CHAR} {TUPLE { id 345, label "RTITITI"}, TUPLE { id 347, label "RTI"}}'))
    print(var_def.parseString('VAR toto RELATION {id NUMERIC, label CHAR} INIT(RELATION {id NUMERIC, label CHAR} {TUPLE { id 345, label "RTITITI"}, TUPLE { id 347, label "RTI"}})'))
    print(var_def.parseString('VAR toto BASE RELATION {id NUMERIC, label CHAR} INIT(RELATION {id NUMERIC, label CHAR} {TUPLE { id 345, label "RTITITI"}, TUPLE { id 347, label "RTI"}}) KEY {id})'))
    print(assignment.parseString('''
mytoto := RELATION {id NUMERIC, label CHAR} {TUPLE { id 345, label "RTITITI"}, TUPLE { id 347, label "RTI"}}
'''))
    print(statement.parseString('''
VAR toto BASE RELATION {id NUMERIC, label CHAR} INIT(RELATION {id NUMERIC, label CHAR} {TUPLE { id 345, label "RTITITI"}, TUPLE { id 347, label "RTI"}}) KEY {id};
'''))
    print(statement.parseString('''
DROP VAR toto;
'''))

