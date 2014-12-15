from pyparsing import *

parse_test = {}

'''
BNF for TutorialD.jj

TOKENS

/*
 *
 * Lexer definitions
 *
 */
<DEFAULT> SKIP : {
" "
| "\t"
| "\n"
| "\r"
| "\f"
}


<DEFAULT> SPECIAL : {
<SINGLE_LINE_COMMENT: "//" (~["\n","\r"])* ("\n" | "\r" | "\r\n")>
| <FORMAL_COMMENT: "/**" (~["*"])* "*" ("*" | ~["*","/"] (~["*"])* "*")* "/">
| <MULTI_LINE_COMMENT: "/*" (~["*"])* "*" ("*" | ~["*","/"] (~["*"])* "*")* "/">
}


<DEFAULT> TOKEN [IGNORE_CASE] : {
<ADD: "ADD">
| <ALL: "ALL">
| <AND: "AND">
| <ANNOUNCE: "ANNOUNCE">
| <ARRAY: "ARRAY">
| <AS: "AS">
| <ASC: "ASC">
| <AVG: "AVG">
| <AVGD: "AVGD">
| <BASE: "BASE">
| <BEGIN: "BEGIN">
| <BUT: "BUT">
| <BY: "BY">
| <CALL: "CALL">
| <CASE: "CASE">
| <COMMIT: "COMMIT">
| <COMPOSE: "COMPOSE">
| <CONSTRAINT: "CONSTRAINT">
| <COUNT: "COUNT">
| <COUNTD: "COUNTD">
| <DELETE: "DELETE">
| <DESC: "DESC">
| <DIVIDEBY: "DIVIDEBY">
| <DO: "DO">
| <DROP: "DROP">
| <D_INSERT: "D_INSERT">
| <D_UNION: "D_UNION">
| <ELSE: "ELSE">
| <END: "END">
| <EOT: "<EOT>">
| <EXACTLYD: "EXACTLYD">
| <EXACTLY: "EXACTLY">
| <EXECUTE: "EXECUTE">
| <EXTEND: "EXTEND">
| <EXTERNAL: "EXTERNAL">
| <FALSE: "FALSE">
| <FOREIGN: "FOREIGN"> : SCRIPT
| <FOR: "FOR">
| <FROM: "FROM">
| <GROUP: "GROUP">
| <I_DELETE: "I_DELETE">
| <I_MINUS: "I_MINUS">
| <IF: "IF">
| <IN: "IN">
| <INIT: "INIT">
| <INSERT: "INSERT">
| <INTERSECT: "INTERSECT">
| <IS: "IS">
| <JOIN: "JOIN">
| <KEY: "KEY">
| <LEAVE: "LEAVE">
| <LOAD: "LOAD">
| <LAMBDA: "~[">
| <LAMBDAEND: "]~">
| <MATCHING: "MATCHING">
| <MAX: "MAX">
| <MIN: "MIN">
| <MINUS: "MINUS">
| <NOT: "NOT">
| <OPERATOR: "OPERATOR">
| <ORDER: "ORDER">
| <ORDERED: "ORDERED">
| <ORDINAL: "ORDINAL">
| <OR: "OR">
| <OUTPUT: "OUTPUT">
| <PER: "PER">
| <POSSREP: "POSSREP">
| <PREFIX: "PREFIX">
| <PRIVATE: "PRIVATE">
| <PUBLIC: "PUBLIC">
| <REAL: "REAL">
| <RELATION: "RELATION" | "REL">
| <RENAME: "RENAME">
| <RETURN: "RETURN">
| <RETURNS: "RETURNS">
| <ROLLBACK: "ROLLBACK">
| <SAME_HEADING_AS: "SAME_HEADING_AS">
| <SAME_TYPE_AS: "SAME_TYPE_AS">
| <SET: "SET">
| <SEMIJOIN: "SEMIJOIN">
| <SEMIMINUS: "SEMIMINUS">
| <SUFFIX: "SUFFIX">
| <SUMD: "SUMD">
| <SUMMARIZE: "SUMMARIZE">
| <SUM: "SUM">
| <SYNONYMS: "SYNONYMS">
| <TABLE_DEE: "DEE" | "TABLE_DEE">
| <TABLE_DUM: "DUM" | "TABLE_DUM">
| <TCLOSE: "TCLOSE">
| <THEN: "THEN">
| <TIMES: "TIMES">
| <TO: "TO">
| <TRANSACTION: "TRANSACTION">
| <TRUE: "TRUE">
| <TUPLE: "TUPLE" | "TUP">
| <TYPE: "TYPE">
| <UNGROUP: "UNGROUP">
| <UNION: "UNION">
| <UNWRAP: "UNWRAP">
| <UPDATES: "UPDATES">
| <UPDATE: "UPDATE">
| <VAR: "VAR">
| <VERSION: "VERSION">
| <VIRTUAL: "VIRTUAL" | "VIEW">
| <WHEN: "WHEN">
| <WHERE: "WHERE">
| <WHILE: "WHILE">
| <WITH: "WITH">
| <WRAP: "WRAP">
| <WRITE: "WRITE">
| <WRITELN: "WRITELN">
| <XOR: "XOR">
| <XUNION: "XUNION">
}


<DEFAULT> TOKEN : {
<INTEGER_LITERAL: <DECIMAL_LITERAL> (["l","L"])? | <HEX_LITERAL> (["l","L"])? | <OCTAL_LITERAL> (["l","L"])?>
| <#DECIMAL_LITERAL: ["1"-"9"] (["0"-"9"])*>
| <#HEX_LITERAL: "0" ["x","X"] (["0"-"9","a"-"f","A"-"F"])+>
| <#OCTAL_LITERAL: "0" (["0"-"7"])*>
| <FLOATING_POINT_LITERAL: (["0"-"9"])+ "." (["0"-"9"])* (<EXPONENT>)? (["f","F","d","D"])? | "." (["0"-"9"])+ (<EXPONENT>)? (["f","F","d","D"])? | (["0"-"9"])+ <EXPONENT> (["f","F","d","D"])? | (["0"-"9"])+ (<EXPONENT>)? ["f","F","d","D"]>
| <#EXPONENT: ["e","E"] (["+","-"])? (["0"-"9"])+>
| <STRING_LITERAL: "\"" (~["\"","\\","\n","\r"] | "\\" (["n","t","b","r","f","\\","\'","\""] | ["0"-"7"] (["0"-"7"])? | ["0"-"3"] ["0"-"7"] ["0"-"7"]))* "\"" | "\'" (~["\'","\\","\n","\r"] | "\\" (["n","t","b","r","f","\\","\'","\""] | ["0"-"7"] (["0"-"7"])? | ["0"-"3"] ["0"-"7"] ["0"-"7"]))* "\'">
}
'''
DECIMAL_LITERAL = Word(nums)
HEX_LITERAL = Word('0') + Word('xX') + Word(nums + 'abcdef' + 'ABCDEF')
OCTAL_LITERAL = Word('0') + Word('01234567')
INTEGER_LITERAL = DECIMAL_LITERAL + Optional(Word('lL')) | HEX_LITERAL + Optional(Word('lL')) + OCTAL_LITERAL + Optional(Word('lL'))
FLOATING_POINT_LITERAL = Word(nums) + '.' + Word(nums) + Optional(Word('eE') + Optional(Word('+-')) + Word(nums)) + Optional(Word('fFdD'))
STRING_LITERAL = '"' + CharsNotIn('"') * (1, None) + '"'

parse_test['FLOATING_POINT_LITERAL'] = FLOATING_POINT_LITERAL.parseString('45.56e+23f')
parse_test['STRING_LITERAL'] = STRING_LITERAL.parseString('"toto est Venu ici !!!"')
parse_test['INTEGER_LITERAL'] = INTEGER_LITERAL.parseString('44556677')

'''
<DEFAULT> TOKEN : {
<IDENTIFIER: <LETTER> (<LETTER> | <DIGIT> | "." | "#")*>
| <#LETTER: ["$","A"-"Z","_","a"-"z","\u00c0"-"\u00d6","\u00d8"-"\u00f6","\u00f8"-"\u00ff","\u0100"-"\u1fff","\u3040"-"\u318f","\u3300"-"\u337f","\u3400"-"\u3d2d","\u4e00"-"\u9fff","\uf900"-"\ufaff"]>
| <#DIGIT: ["0"-"9","\u0660"-"\u0669","\u06f0"-"\u06f9","\u0966"-"\u096f","\u09e6"-"\u09ef","\u0a66"-"\u0a6f","\u0ae6"-"\u0aef","\u0b66"-"\u0b6f","\u0be7"-"\u0bef","\u0c66"-"\u0c6f","\u0ce6"-"\u0cef","\u0d66"-"\u0d6f","\u0e50"-"\u0e59","\u0ed0"-"\u0ed9","\u1040"-"\u1049"]>
}
'''

IDENTIFIER = Word(alphanums)

'''
<DEFAULT> TOKEN : {
<LPAREN: "(">
| <RPAREN: ")">
| <LBRACE: "{">
| <RBRACE: "}">
| <SEMICOLON: ";">
| <COMMA: ",">
| <COLON: ":">
}


<DEFAULT> TOKEN : {
<ASSIGN: ":=">
| <EQ: "=">
| <GT: ">">
| <LT: "<">
| <LTE: "<=">
| <GTE: ">=">
| <NEQ: "<>">
| <PLUS: "+">
| <SUBT: "-">
| <STAR: "*">
| <SLASH: "/">
}


<SCRIPT> TOKEN : {
<ENDFOREIGN: "\nEND"> : DEFAULT
| <TEXT: ~[]>
}
'''

'''

NON-TERMINALS

evaluate
evaluate        ::=     ( compound_statement_body ";" )? expression ( <EOT> | <EOF> )
'''
compound_statement_body = Forward()
expression = Forward()
evaluate = expression
'''
code
code    ::=     statement ( statement )* ( <EOT> | <EOF> )
'''

'''
statement
statement       ::=     statement_body ";"
'''
statement_body = Forward()
statement = statement_body + ';'

'''
op_before_returns
op_before_returns       ::=     <OPERATOR> identifier "(" ( identifier type_ref ( "," identifier type_ref )* )? ")"
op_after_returns
op_after_returns        ::=     op_updates op_synonym op_version ";" op_body <END> <OPERATOR>
|       identifier <FOREIGN> ( <TEXT> )* <ENDFOREIGN> <OPERATOR>
getoperatorreturntype
getoperatorreturntype   ::=     op_before_returns op_returns op_after_returns
getheading
getheading      ::=     heading
getsignature
getsignature    ::=     op_signature op_returns
'''

'''
statement_body
statement_body  ::=     assignment
|       loop
|       op_def
|       type_def
|       drop
|       var_def
|       db_constraint_def
|       relation_array_load
|       begin_transaction
|       compound_statement_body
|       commit
|       rollback
|       call
|       return_statement
|       case_statement
|       if_statement
|       leave
|       write
|       writeln
|       output
|       announce
|       execute
|       set
'''
assignment = Forward()
statement_body = assignment

'''
/* Rel extension - non-TTM */
write
write   ::=     <WRITE> expression
/* Rel extension - non-TTM */
writeln
writeln ::=     <WRITELN> ( expression )?
/* Rel extension - non-TTM */
output
output  ::=     <OUTPUT> expression
/* Rel extension - non-TTM */
announce
announce        ::=     <ANNOUNCE> string_literal
/* Rel extension - non-TTM */
execute
execute ::=     <EXECUTE> expression
/* Rel extension - non-TTM */
set
set     ::=     <SET> identifier identifier
compound_statement_body
compound_statement_body ::=     <BEGIN> ";" ( statement )* <END>
'''
compound_statement_body << Keyword('BEGIN') + ';' + ZeroOrMore(statement) + Keyword('END')
'''
op_def
op_def  ::=     <OPERATOR> identifier "(" parameter_def_commalist ")" op_returns ( rel_op_def | external_op_def )
lambda
lambda  ::=     <OPERATOR> lambda_definition <END> <OPERATOR>
|       <LAMBDA> lambda_definition <LAMBDAEND>
lambda_definition
lambda_definition       ::=     "(" parameter_def_commalist ")" <RETURNS> type_ref ";" op_body
external_op_def
external_op_def ::=     identifier <FOREIGN> ( <TEXT> )* <ENDFOREIGN> <OPERATOR>
rel_op_def
rel_op_def      ::=     op_updates op_synonym op_version ";" op_body <END> <OPERATOR>
/* Note: op_returns() and op_updates()
should be mutually exclusive. */
op_returns
op_returns      ::=     ( <RETURNS> type_ref )?
op_updates
op_updates      ::=     ( <UPDATES> "{" ( <ALL> <BUT> parameter_name_commalist )? "}" )?
op_synonym
op_synonym      ::=     ( synonym_def )?
op_version
op_version      ::=     ( <VERSION> identifier )?
op_body
op_body ::=     ( statement )?
return_statement
return_statement        ::=     <RETURN> ( expression )?
/* Not explicitly defined in TTM3 */
parameter_def_commalist
parameter_def_commalist ::=     ( parameter_def ( "," parameter_def )* )?
parameter_def
parameter_def   ::=     identifier type_ref
/* Not explicitly defined in TTM3 */
parameter_name_commalist
parameter_name_commalist        ::=     ( identifier ( "," identifier )* )?
synonym_def
synonym_def     ::=     <SYNONYMS> "{" user_op_name_commalist "}"
/* Not explicitly defined in TTM3 */
user_op_name_commalist
user_op_name_commalist  ::=     identifier ( "," identifier )*
/* Inclusion of type_ref_commalist() in
OPERATOR DROP is not per TTM3,
but necessary to
disambiguate operators. */
drop
drop    ::=     <DROP> ( <OPERATOR> op_signature | <VAR> identifier | <CONSTRAINT> identifier | <TYPE> identifier )
op_signature
op_signature    ::=     identifier "(" type_ref_commalist ")"
op_type
op_type ::=     <OPERATOR> "(" type_ref_commalist ")" ( <RETURNS> type_ref )?
type_ref_commalist
type_ref_commalist      ::=     ( type_ref ( "," type_ref )* )?
/* Was user_scalar_type_def */
type_def
type_def        ::=     <TYPE> identifier type_def_kind
type_def_kind
type_def_kind   ::=     type_def_external
|       type_def_internal
type_def_external
type_def_external       ::=     identifier <FOREIGN> ( <TEXT> )* <ENDFOREIGN> <TYPE>
/* User-defined (internal) types start here */
type_def_internal
type_def_internal       ::=     type_def_internal_ordinal type_def_internal_union type_def_internal_is_or_possrep
type_def_internal_is_or_possrep
type_def_internal_is_or_possrep ::=     is_def
|       possrep_def_list
type_def_internal_ordinal
type_def_internal_ordinal       ::=     ( type_def_internal_opt_ordinal )?
type_def_internal_opt_ordinal
type_def_internal_opt_ordinal   ::=     ( <ORDINAL> | <ORDERED> )
type_def_internal_union
type_def_internal_union ::=     ( type_def_internal_opt_union )?
type_def_internal_opt_union
type_def_internal_opt_union     ::=     <UNION>
is_def
is_def  ::=     <IS> "{" ( single_inheritance_is_def | multiple_inheritance_is_def ) "}"
single_inheritance_is_def
single_inheritance_is_def       ::=     identifier possrep_or_specialization_details
possrep_or_specialization_details
possrep_or_specialization_details       ::=     specialisation_constraint_def ( derived_possrep_def_list )?
|       possrep_def_list
multiple_inheritance_is_def
multiple_inheritance_is_def     ::=     scalar_type_name_commalist derived_possrep_def_list
/* Not explicitly defined in TTM3 */
scalar_type_name_commalist
scalar_type_name_commalist      ::=     scalar_type_name ( "," scalar_type_name )*
scalar_type_name
scalar_type_name        ::=     identifier
/* Not explicitly defined in TTM3 */
possrep_def_list
possrep_def_list        ::=     ( possrep_def )* possrep_opt_initialiser
/* Not defined in TTM3.  For explicitly setting
values of components not in the current possrep.
Only required by types with multiple possreps.
Takes the place of "highly protected
operators not part of D". (pg 382, etc.) */
possrep_opt_initialiser
possrep_opt_initialiser ::=     ( <INIT> possrep_initialiser_assignments ( possrep_initialiser_assignments )* )?
/* Not defined in TTM3, as per above.
Identifier should be existing POSSREP name. */
possrep_initialiser_assignments
possrep_initialiser_assignments ::=     identifier "(" assignment ")"
possrep_def
possrep_def     ::=     <POSSREP> possrep_def_identifier "{" possrep_component_def_commalist possrep_opt_constraint_def "}"
possrep_def_identifier
possrep_def_identifier  ::=     ( identifier )?
possrep_opt_constraint_def
possrep_opt_constraint_def      ::=     ( constraint_def )?
/* Not explicitly defined in TTM3 */
possrep_component_def_commalist
possrep_component_def_commalist ::=     ( possrep_component_def ( "," possrep_component_def )* )?
possrep_component_def
possrep_component_def   ::=     identifier type_ref
/* Expression must be boolean */
constraint_def
constraint_def  ::=     <CONSTRAINT> expression
/* Expression must be boolean */
specialisation_constraint_def
specialisation_constraint_def   ::=     <CONSTRAINT> expression
/* Not explicitly defined in TTM3 */
derived_possrep_def_list
derived_possrep_def_list        ::=     derived_possrep_def ( derived_possrep_def )*
derived_possrep_def
derived_possrep_def     ::=     <POSSREP> derived_possrep_def_opt_identifier "{" derived_possrep_component_def_commalist "}"
derived_possrep_def_opt_identifier
derived_possrep_def_opt_identifier      ::=     ( identifier )?
/* Not explicitly defined in TTM3 */
derived_possrep_component_def_commalist
derived_possrep_component_def_commalist ::=     derived_possrep_component_def ( "," derived_possrep_component_def )*
derived_possrep_component_def
derived_possrep_component_def   ::=     identifier "=" identifier "(" identifier ")"
/* End user-defined types (internal) */

/* Includes scalar_var_def,
relation_var_def,
array_var_def and
tuple_var_def */
var_def
var_def ::=     <VAR> identifier ( var_scalar_or_tuple | var_array | var_relvar )
var_relvar
var_relvar      ::=     ( <REAL> | <BASE> ) var_type_or_init_value var_keydeflist
|       <PRIVATE> var_type_or_init_value var_keydeflist
|       <PUBLIC> type_ref var_keydeflist
|       <VIRTUAL> expression var_keydeflistoptional
|       var_relvar_external
var_relvar_external
var_relvar_external     ::=     <EXTERNAL> identifier string_literal ( identifier )?
var_keydeflist
var_keydeflist  ::=     var_keydef ( var_keydef )*
var_keydeflistoptional
var_keydeflistoptional  ::=     ( var_keydef )*
var_keydef
var_keydef      ::=     <KEY> "{" attribute_name_list "}"
var_scalar_or_tuple
var_scalar_or_tuple     ::=     var_type_or_init_value
var_type_or_init_value
var_type_or_init_value  ::=     var_type_and_optional_init
|       var_init
var_type_and_optional_init
var_type_and_optional_init      ::=     type_ref ( <INIT> "(" expression ")" )?
var_init
var_init        ::=     <INIT> "(" expression ")"
var_array
var_array       ::=     <ARRAY> type_ref
db_constraint_def
db_constraint_def       ::=     <CONSTRAINT> identifier expression
'''

'''
/* type -- scalar_type, tuple_type, relation_type */
type_ref
type_ref        ::=     identifier
|       type_same_type_as
|       tuple_type
|       relation_type
|       op_type
'''
identifier = Forward()
relation_type = Forward()
tuple_type = Forward()
type_same_type_as = Forward()
op_type = Forward()
type_ref = identifier | type_same_type_as | tuple_type | relation_type | op_type
'''
type_same_type_as
type_same_type_as       ::=     <SAME_TYPE_AS> "(" expression ")"
'''

'''
tuple_type
tuple_type      ::=     <TUPLE> heading_type
'''
heading_type = Forward()
tuple_type << Keyword('TUPLE') + heading_type
'''
relation_type
relation_type   ::=     <RELATION> heading_type
'''
relation_type = Keyword('RELATION') + heading_type
'''
heading_type
heading_type    ::=     heading
|       same_heading_as
'''

heading = Forward()
same_heading_as = Forward()
heading_type = heading | same_heading_as
'''
same_heading_as
same_heading_as ::=     <SAME_HEADING_AS> "(" expression ")"
relation_array_load
relation_array_load     ::=     <LOAD> identifier <FROM> expression
begin_transaction
begin_transaction       ::=     <BEGIN> <TRANSACTION>
commit
commit  ::=     <COMMIT>
rollback
rollback        ::=     <ROLLBACK>
case_statement
case_statement  ::=     <CASE> ";" when_def_list case_else <END> <CASE>
when_def_list
when_def_list   ::=     when_def ( when_def )*
when_def
when_def        ::=     <WHEN> expression <THEN> statement
case_else
case_else       ::=     ( <ELSE> statement )?
/* Note that THEN and ELSE are not
followed by semicolons, but maybe should be? */
if_statement
if_statement    ::=     <IF> expression <THEN> statement if_statement_else <END> <IF>
if_statement_else
if_statement_else       ::=     ( <ELSE> statement )?
loop
loop    ::=     ( identifier ":" )? ( do_statement | while_statement | for_statement )
do_statement
do_statement    ::=     <DO> identifier ":=" expression <TO> expression ";" statement <END> <DO>
while_statement
while_statement ::=     <WHILE> expression ";" statement <END> <WHILE>
for_statement
for_statement   ::=     <FOR> expression ";" statement <END> <FOR>
leave
leave   ::=     <LEAVE> identifier
call
call    ::=     <CALL> identifier "(" arglist ")"
'''

'''
assignment
assignment      ::=     assign ( "," assign )*
'''
assign = Forward()
assignment = assign + ZeroOrMore(',' + assign)
'''
assign
assign  ::=     identifier ":=" expression
|       <INSERT> identifier expression
|       <D_INSERT> identifier expression
|       <DELETE> identifier delete_parameter
|       <I_DELETE> identifier expression
|       <UPDATE> identifier update_where ":" update_assignment
'''
expression = Forward()
assign = identifier + ':=' + expression | 'INSERT' + identifier + expression
'''
delete_parameter
delete_parameter        ::=     ( ( <WHERE> )? expression )?
update_where
update_where    ::=     ( <WHERE> expression )?
update_assignment
update_assignment       ::=     "{" assignment "}"
'''

'''
/* Expressions */
expression
expression      ::=     ( attribute_from | basic_expression | tuple_from | with | tclose )
'''
attribute_from = Forward()
basic_expression = Forward()
with_ = Forward()
tclose = Forward()
tuple_from = Forward()
expression << (attribute_from | tuple_from)
'''
attribute_from
attribute_from  ::=     identifier <FROM> expression
'''
attribute_from = identifier + Keyword('FROM') + expression
'''
tuple_from
tuple_from      ::=     <TUPLE> <FROM> expression
'''
tuple_from << Keyword('TUPLE') + Keyword('FROM') + expression
'''
with
with    ::=     <WITH> "(" name_intro_commalist ")" ":" expression
'''
name_intro_commalist = Forward()
with_ = Keyword('WITH') + '(' + name_intro_commalist + ')' + ':' + expression
'''
name_intro_commalist
name_intro_commalist    ::=     name_intro ( "," name_intro )*
'''
name_intro = Forward()
name_intro_commalist << (name_intro + ZeroOrMore(',' + name_intro))
'''
name_intro
name_intro      ::=     identifier ":=" expression
'''
name_intro << (identifier + ':=' + expression)
'''
tclose
tclose  ::=     <TCLOSE> expression
'''
tclose << (Keyword('TCLOSE') + expression)
'''
basic_expression
basic_expression        ::=     order_expression ( "[" expression "]" | "(" arglist ")" )?
'''
order_expression = Forward()
where_expression = Forward()
or_expression = Forward()
xor_expression = Forward()
and_expression = Forward()
compare_expression = Forward()
basic_expression = order_expression + Optional('[' + expression + ']')
'''
order_expression
order_expression        ::=     where_expression ( <ORDER> "(" order_item_commalist ")" )?
'''
order_item_commalist = Forward()
order_expression << where_expression + Optional(Keyword('ORDER') + '(' + order_item_commalist + ')')
'''
where_expression
where_expression        ::=     or_expression ( <WHERE> or_expression )?
'''
where_expression << or_expression + Optional(Keyword('WHERE') + or_expression)
'''
or_expression
or_expression   ::=     xor_expression ( <OR> xor_expression )*
'''
or_expression << xor_expression + ZeroOrMore(Keyword('OR') + xor_expression)
'''
xor_expression
xor_expression  ::=     and_expression ( <XOR> and_expression )*
'''
xor_expression << and_expression + ZeroOrMore(Keyword('XOR') + and_expression)
'''
and_expression
and_expression  ::=     compare_expression ( <AND> compare_expression )*
'''
and_expression << compare_expression + ZeroOrMore(Keyword('AND') + compare_expression)
'''
compare_expression
compare_expression      ::=     rel_diadic ( "=" rel_diadic | "<>" rel_diadic | ">=" rel_diadic | "<=" rel_diadic | ">" rel_diadic | "<" rel_diadic | <IN> rel_diadic )?
'''

'''
rel_diadic
rel_diadic      ::=     rel_monadic ( <UNION> rel_monadic | <XUNION> rel_monadic | <D_UNION> rel_monadic | <INTERSECT> rel_monadic | <MINUS> rel_monadic | <I_MINUS> rel_monadic | <JOIN> rel_monadic | <TIMES> rel_monadic | <COMPOSE> rel_monadic | ( <SEMIJOIN> | <MATCHING> ) rel_monadic | ( <SEMIMINUS> | <NOT> <MATCHING> ) rel_monadic )*
rel_monadic
rel_monadic     ::=     rel_project ( <RENAME> "{" renaming_commalist "}" | <WRAP> wrapping | <UNWRAP> identifier | <GROUP> grouping | <UNGROUP> identifier | <DIVIDEBY> expression <PER> "(" expression divide_per_optional ")" )?
/* Not explicitly defined in TTM3 */
'''
'''
order_item_commalist
order_item_commalist    ::=     ( order_item ( "," order_item )* )?
'''
order_item = Forward()
order_item_commalist << Optional(order_item + ZeroOrMore(',' + order_item))
'''
order_item
order_item      ::=     <ASC> identifier
|       <DESC> identifier
'''
order_item << (Keyword('ASC') | Keyword('DESC')) + identifier
#parse_test['order_item'] = order_item.parseString('ASC toto')
'''
divide_per_optional
divide_per_optional     ::=     ( "," expression )?
rel_project
rel_project     ::=     add_expression ( "{" attribute_name_list "}" )?
grouping
grouping        ::=     "{" attribute_name_list "}" <AS> identifier
wrapping
wrapping        ::=     "{" attribute_name_list "}" <AS> identifier
renaming_commalist
renaming_commalist      ::=     ( renaming ( "," renaming )* )?
renaming
renaming        ::=     renaming_simple
|       renaming_prefix
|       renaming_suffix
renaming_simple
renaming_simple ::=     identifier <AS> identifier
renaming_prefix
renaming_prefix ::=     <PREFIX> string_literal <AS> string_literal
renaming_suffix
renaming_suffix ::=     <SUFFIX> string_literal <AS> string_literal
attribute_name_list
attribute_name_list     ::=     optional_all_but attribute_name_commalist
optional_all_but
optional_all_but        ::=     ( <ALL> <BUT> )?
attribute_name_commalist
attribute_name_commalist        ::=     ( identifier ( "," identifier )* )?
add_expression
add_expression  ::=     mul_expression ( "+" mul_expression | "-" mul_expression | "||" mul_expression )*
mul_expression
mul_expression  ::=     unary_expression ( "*" unary_expression | "/" unary_expression )*
unary_expression
unary_expression        ::=     <NOT> unary_expression
|       "+" unary_expression
|       "-" unary_expression
|       primary_expression
primary_expression
primary_expression      ::=     literal
|       aggregate_operator
|       exactly
|       nadic_or
|       nadic_xor
|       nadic_and
|       nadic_union
|       nadic_xunion
|       nadic_disjoint_union
|       nadic_intersect
|       nadic_join
|       nadic_times
|       nadic_compose
|       nadic_count
|       nadic_sum
|       nadic_avg
|       nadic_max
|       nadic_min
|       extend
|       summarize
|       substitute
|       case_expression
|       if_expression
|       fn_invoke
|       dereference
|       "(" expression ")"
case_expression
case_expression ::=     <CASE> when_def_list_expr <ELSE> expression <END> <CASE>
when_def_list_expr
when_def_list_expr      ::=     when_def_expr ( when_def_expr )*
when_def_expr
when_def_expr   ::=     <WHEN> expression <THEN> expression
if_expression
if_expression   ::=     <IF> expression <THEN> expression <ELSE> expression <END> <IF>
/* Update expression, *not* assignment.
Contents of expression() does not change! */
substitute
substitute      ::=     <UPDATE> expression ":" update_assignment
nadic_optional_heading
nadic_optional_heading  ::=     heading "{" heading_exp_commalist "}"
|       "{" heading_exp_commalist "}"
nadic_union
nadic_union     ::=     <UNION> nadic_optional_heading
nadic_xunion
nadic_xunion    ::=     <XUNION> nadic_optional_heading
nadic_disjoint_union
nadic_disjoint_union    ::=     <D_UNION> nadic_optional_heading
nadic_intersect
nadic_intersect ::=     <INTERSECT> nadic_optional_heading
nadic_join
nadic_join      ::=     <JOIN> "{" heading_exp_commalist "}"
nadic_times
nadic_times     ::=     <TIMES> "{" heading_exp_commalist "}"
nadic_compose
nadic_compose   ::=     <COMPOSE> "{" heading_exp_commalist "}"
nadic_or
nadic_or        ::=     <OR> "{" bool_exp_commalist "}"
nadic_xor
nadic_xor       ::=     <XOR> "{" bool_exp_commalist "}"
nadic_and
nadic_and       ::=     <AND> "{" bool_exp_commalist "}"
nadic_count
nadic_count     ::=     <COUNT> "{" exp_commalist "}"
nadic_sum
nadic_sum       ::=     <SUM> "{" exp_commalist "}"
nadic_avg
nadic_avg       ::=     <AVG> "{" exp_commalist "}"
nadic_max
nadic_max       ::=     <MAX> "{" exp_commalist "}"
nadic_min
nadic_min       ::=     <MIN> "{" exp_commalist "}"
exactly
exactly ::=     <EXACTLY> "(" expression ( "," expression ( "," expression )* )? ")"
exp_commalist
exp_commalist   ::=     ( expression ( "," expression )* )?
bool_exp_commalist
bool_exp_commalist      ::=     ( expression ( "," expression )* )?
heading_exp_commalist
heading_exp_commalist   ::=     ( expression ( "," expression )* )?
extend
extend  ::=     <EXTEND> expression ":" "{" extend_add_commalist "}"
extend_add_commalist
extend_add_commalist    ::=     extend_add ( "," extend_add )*
extend_add
extend_add      ::=     identifier ":=" expression
summarize
summarize       ::=     <SUMMARIZE> expression per_or_by ":" "{" summarize_add_commalist "}"
per_or_by
per_or_by       ::=     ( <PER> "(" expression ")" | <BY> "{" attribute_name_list "}" )?
summarize_add_commalist
summarize_add_commalist ::=     summarize_add ( "," summarize_add )*
summarize_add
summarize_add   ::=     identifier ":=" summary
summary
summary ::=     <COUNT> "(" ")"
|       <COUNTD> "(" expression ")"
|       <SUM> "(" expression ")"
|       <SUMD> "(" expression ")"
|       <AVG> "(" expression ")"
|       <AVGD> "(" expression ")"
|       <MAX> "(" expression ")"
|       <MIN> "(" expression ")"
|       <AND> "(" expression ")"
|       <OR> "(" expression ")"
|       <XOR> "(" expression ")"
|       <EXACTLY> "(" expression "," expression ")"
|       <EXACTLYD> "(" expression "," expression ")"
|       <UNION> "(" expression ")"
|       <XUNION> "(" expression ")"
|       <D_UNION> "(" expression ")"
|       <INTERSECT> "(" expression ")"
fn_invoke
fn_invoke       ::=     identifier "(" arglist ")"
arglist
arglist ::=     ( expression ( "," expression )* )?
aggregate_operator
aggregate_operator      ::=     <COUNT> "(" expression ")"
|       <SUM> "(" expression "," expression ")"
|       <AVG> "(" expression "," expression ")"
|       <MAX> "(" expression "," expression ")"
|       <MIN> "(" expression "," expression ")"
|       <AND> "(" expression "," expression ")"
|       <OR> "(" expression "," expression ")"
|       <XOR> "(" expression "," expression ")"
|       <UNION> "(" expression "," expression ")"
|       <XUNION> "(" expression "," expression ")"
|       <D_UNION> "(" expression "," expression ")"
|       <INTERSECT> "(" expression "," expression ")"
'''

'''
literal
literal ::=     lambda
|       tuple
|       relation
|       integer
|       character
|       rational
|       bool
'''
tuple_ = Forward()
literal = tuple_
'''
tuple
tuple   ::=     <TUPLE> "{" ( tuple_component_commalist )? "}"
tuple_component_commalist
tuple_component_commalist       ::=     tuple_component ( "," tuple_component )*
tuple_component
tuple_component ::=     identifier expression
'''
#tuple_component = identifier + expression
tuple_component = identifier + 'xx'
tuple_component_commalist = tuple_component + ZeroOrMore(',' + tuple_component)
tuple_ << Keyword('TUPLE') + '{' + ZeroOrMore(tuple_component_commalist) + '}'
parse_test['tuple_'] = tuple_.parseString('TUPLE {}')
parse_test['tuple_1'] = tuple_.parseString('TUPLE {toto xx}')
'''
relation
relation        ::=     <RELATION> relation_heading "{" tuple_exp_commalist "}"
|       <TABLE_DUM>
|       <TABLE_DEE>
relation_heading
relation_heading        ::=     ( heading )?
'''
tuple_exp_commalist= Forward()
relation_heading = Optional(heading)
relation = Keyword('RELATION') + relation_heading + '{' + tuple_exp_commalist + '}'
'''
heading
heading ::=     "{" ( attribute_spec_commalist )? "}"
'''
attribute_spec_commalist = Forward()
heading << '{' + ZeroOrMore(attribute_spec_commalist) + '}'
'''
tuple_exp_commalist
tuple_exp_commalist     ::=     ( expression ( "," expression )* )?
'''
tuple_exp_commalist << Optional(expression + ZeroOrMore(',' + expression))
'''
attribute_spec_commalist
attribute_spec_commalist        ::=     attribute_spec ( "," attribute_spec )*
'''
attribute_spec = Forward()
attribute_spec_commalist << attribute_spec + ZeroOrMore(',' + attribute_spec)
'''
attribute_spec
attribute_spec  ::=     identifier type_ref
'''
attribute_spec << identifier + type_ref
'''
identifier
identifier      ::=     <IDENTIFIER>
dereference
dereference     ::=     <IDENTIFIER>
character
character       ::=     <STRING_LITERAL>
string_literal
string_literal  ::=     <STRING_LITERAL>
integer
integer ::=     <INTEGER_LITERAL>
rational
rational        ::=     <FLOATING_POINT_LITERAL>
bool
bool    ::=     <TRUE>
|       <FALSE>
'''
identifier << IDENTIFIER
parse_test['identifier'] = identifier.parseString('toto')
INTEGER = INTEGER_LITERAL
RATIONAL = FLOATING_POINT_LITERAL
BOOL = Keyword('TRUE') | Keyword('FALSE')

if __name__ == '__main__':
    for akey, atest in parse_test.items():
        print(akey, ':', atest)
