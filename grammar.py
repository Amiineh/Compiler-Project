LHS = [
'program_prime',
'program',
'declaration_list',
'declaration_list',
'declaration',
'declaration',
'var_declaration',
'var_declaration',
'type_specifier',
'type_specifier',
'fun_declaration',
'params',
'params',
'param_list',
'param_list',
'param',
'param',
'compound_stmt',
'local_declarations',
'local_declarations',
'statement_list',
'statement_list',
'statement',
'statement',
'statement',
'statement',
'statement',
'expression_stmt',
'expression_stmt',
'selection_stmt',
'iteration_stmt',
'return_stmt',
'return_stmt',
'expression',
'expression',
'var',
'var',
'simple_expression',
'simple_expression',
'relop',
'relop',
'additive_expression',
'additive_expression',
'addop',
'addop',
'term',
'term',
'factor',
'factor',
'factor',
'factor',
'call',
'args',
'args',
'arg_list',
'arg_list',
]

RHS = [
['program'],
['declaration_list','EOF'],
['declaration_list','declaration'],
['declaration'],
['var_declaration'],
['fun_declaration'],
['type_specifier','ID', ';'],
['type_specifier','ID', '[', 'NUM', ']', ';'],
['int'],
['void'],
['type_specifier','ID','(', 'params', ')', 'compound_stmt'],
['param_list'],
['void'],
['param_list',',','param'],
['param'],
['type_specifier', 'ID'],
['type_specifier','ID', '[', ']'],
['{', 'local_declarations','statement_list', '}'],
['local_declarations','var_declaration'],
[],
['statement_list','statement'],
[],
['expression_stmt'],
['compound_stmt'],
['selection_stmt'],
['iteration_stmt'],
['return_stmt'],
['expression',';'],
[';'],
['if','(','expression',')','statement','else','statement'],
['while','(','expression',')','statement'],
['return', ';'],
['return', 'expression', ';'],
['var', '=', 'expression'],
['simple_expression'],
['ID'],
['ID', '[', 'expression', ']'],
['additive_expression','relop','additive_expression'],
['additive_expression'],
['<'],
['=='],
['additive_expression','addop','term'],
['term'],
['+'],
['-'],
['term', '*', 'factor'],
['factor'],
['(','expression',')'],
['var'],
['call'],
['NUM'],
['ID', '(', 'args', ')'],
['arg_list'],
[],
['arg_list',',','expression'],
['expression']
]

follow = {
'declaration': ['EOF', 'void', 'int'],
'params': [')'],
'compound_stmt': ['ID', 'EOF', 'if', '(', 'int', 'NUM', 'return', 'else', 'void', 'while', '{', ';', '}'],
'declaration_list': ['EOF', 'void', 'int'],
'expression_stmt': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], # rsdfw({;}n
'fun_declaration': ['EOF', 'void', 'int'], # evi
'statement': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], # rsdfw({;}n
'selection_stmt': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], # rsdfw({;}n
'iteration_stmt': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], # rsdfw({;}n
'var': ['==', ')', '*', ';', '+', '<', ',', '=', '-', ']'], # q)*;+<,=-]
'simple_expression': [')', ';', ',', ']'], # );,]
'local_declarations': ['return', 'ID', 'if', 'void', 'while', '(', 'int', '{', ';', '}', 'NUM'], # rdfvw(i{;}n
'term': ['==', ')', '*', ';', '+', '<', ',', '-', ']'], # q)*;+<,-]
'addop': ['ID', '(', 'NUM'], # d(n
'relop': ['ID', '(', 'NUM'], # d(n
'program': ['$'], # $
'additive_expression': ['==', ')', ';', '+', '<', ',', '-', ']'], # q);+<,-]
'return_stmt': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], # rsdfw({;}n
'statement_list': ['return', 'else', 'ID', 'if', 'while', '(', '{', ';', '}', 'NUM'], #rdfw({;}n
'type_specifier': ['ID'], # d
'factor': ['==', ')', '*', ';', '+', '<', ',', '-', ']'], # q)*;+<,-]
'var_declaration': ['return', 'ID', 'EOF', 'void', 'if', 'while', '(', 'int', '{', ';', '}', 'NUM'], # rdevfw(i{;}n
'param': [')', ','], # ),
'expression': [')', ';', ',', ']'], # );,]
'param_list': [')', ','], # ),
'call': ['==', ')', '*', ';', '+', '<', ',', '-', ']'], # q)*;+<,-]
'args': ['('], # )
'arg_list': ['(', ','] # ),
}