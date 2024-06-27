rules =[ 'program -> stmt stmt_list_tail',
    'stmt_list_tail -> stmt stmt_list_tail| #',
    'stmt -> if_stmt | decl_or_func | for_stmt | return_stmt | expr_stmt | print_stmt | break_stmt | continue_stmt',
    'decl_or_func -> type T_Id decl_or_func_tail',
    'decl_or_func_tail -> init var_list_tail T_Semicolon | T_LP parameter_list T_RP func_body',
    'expr_stmt -> expr T_Semicolon',
    'return_stmt -> T_Return expr T_Semicolon',
    'decl -> type var_list T_Semicolon',
    'var_list -> var_decl var_list_tail',
    'var_list_tail -> T_Comma var_decl var_list_tail | #',
    'type -> T_Bool | T_Char | T_Int | T_Void',
    'var_decl -> T_Id init',
    'init -> var_init | T_LB number T_RB array_init',
    'var_init -> T_Assign value | #',
    'array_init -> T_Assign array_init_tail | #',
    'array_init_tail -> T_LC value_list T_RC | T_String',
    'value_list -> value value_list_tail',
    'value_list_tail -> T_Comma value value_list_tail | #',
    'value -> bool | char | number',
    'bool -> T_False | T_True',
    'char -> T_Character | T_String',
    'number -> T_Decimal | T_Hexadecimal | T_Id',
    'if_stmt -> T_If T_LP condition T_RP block opt_tail',
    'opt_tail -> T_Else opt_tail_tail | #',
    'opt_tail_tail -> T_If T_LP condition T_RP block opt_tail | block opt_tail',
    'block -> T_LC stmt_list_tail T_RC ',
    'condition -> or_condition',
    'or_condition -> and_condition or_condition_tail',
    'or_condition_tail -> T_LOp_OR and_condition or_condition_tail | #',
    'and_condition -> not_condition and_condition_tail',
    'and_condition_tail -> T_LOp_AND not_condition and_condition_tail | #',
    'not_condition -> T_LOp_NOT  factor | factor not_condition_tail',
    'not_condition_tail -> relop factor | #',
    'break_stmt -> T_Break T_Semicolon',
    'continue_stmt -> T_Continue T_Semicolon',
    'relop -> T_ROp_LE | T_ROp_GE | T_ROp_NE | T_ROp_E | T_ROp_L | T_ROp_G',
    'expr_tail_tail -> expr_tail expr_tail_tail | #',
    'term_tail_tail -> term_tail term_tail_tail | #',
    'expr -> term expr_tail_tail',
    'expr_tail -> T_AOp_PL term  | T_AOp_MN term  | T_Assign term ',
    'term -> factor term_tail_tail',
    'term_tail -> T_AOp_DV factor  | T_AOp_RM factor  | T_AOp_ML factor ',
    'factor -> T_Id isarray | T_Decimal | T_Hexadecimal | T_LP expr T_RP | T_False | T_True | T_Character ',
    'isarray -> T_LB index T_RB | #',
    'index -> T_Hexadecimal | T_Decimal | T_Id',
    'for_stmt -> T_For T_LP for_tail',
    'for_tail -> expr T_Semicolon condition T_Semicolon expr T_RP block | decl condition T_Semicolon expr T_RP block',
    'parameter_list -> parameter parameter_list_tail | #',
    'parameter_list_tail -> T_Comma parameter parameter_list_tail | #',
    'parameter -> type T_Id',
    'func_body -> block | T_Semicolon',
    'print_stmt -> T_Print T_LP formatstr argprintopt T_RP T_Semicolon',
    'formatstr -> T_String',
    'argprintopt -> arg argprintopt | #',
    'arg -> T_Comma valid_print',
    'valid_print -> expr'
        ]

nonterm_userdef = ['program',
                    'stmt_list_tail',
                    'stmt',
                    'expr_stmt',
                   'return_stmt',
                    'decl',
                   'type',
                   'var_decl',
                   'init',
                   'var_init',
                   'array_init',
                   'value_list',
                   'value_list_tail',
                   'value',
                   'bool',
                   'char',
                   'number',
                    'array_init_tail',
                   'var_list',
                   'var_list_tail',
                   'relop',
                   'decl_or_func',
                   'decl_or_func_tail',
                   'break_stmt',
                   'continue_stmt',
                   'for_tail',
                   'or_condition',
                   'or_condition_tail',
                   'and_condition',
                   'and_condition_tail',
                   'not_condition',
                   'opt_tail_tail',
                   'not_condition_tail',
                   'if_stmt','opt_tail','condition','block','expr','term_tail_tail','expr_tail_tail','expr_tail','term',
                   'term_tail','factor','isarray','index','for_stmt','parameter_list',
                   'parameter_list_tail','parameter','func_body','print_stmt','formatstr','argprintopt','arg','valid_print'


                  ]

term_userdef =['T_LP' ,'T_RP' ,'T_LC' ,'T_RC' ,'T_LB' ,'T_RB',
               'T_Bool',
               'T_Break',
               'T_Char',
               'T_Continue',
               'T_Else',
               'T_False',
               'T_For',
               'T_If',
               'T_Int',
               'T_Print',
               'T_Return',
               'T_True',
               'T_Void',
               'T_Semicolon',
               'T_Comma',
               'T_AOp_PL',
               'T_AOp_MN',
               'T_AOp_ML',
               'T_AOp_DV',
               'T_AOp_RM','T_Assign','T_ROp_L','T_ROp_G','T_LOp_NOT','T_ROp_LE',
               'T_ROp_GE','T_ROp_NE','T_ROp_E','T_LOp_AND','T_LOp_OR','T_Id','T_Decimal','T_Hexadecimal','T_String','T_Character'
               ]




sample_input_string = ('T_If T_LP T_Id T_ROp_GE T_Decimal T_LOp_OR T_Id T_ROp_L T_Id T_LOp_AND T_LOp_NOT T_Id T_RP T_LC '
                       'T_Id T_Assign T_True T_Semicolon T_RC')



function_test = ('T_Int T_Id T_LP T_Int T_Id T_Comma T_Bool T_Id T_Comma T_Char T_Id T_RP T_LC '
                       'T_Int T_Id T_Semicolon '
                       'T_If T_LP T_Id T_LOp_AND T_Id T_ROp_E T_Character T_RP T_LC '
                       'T_Id T_Assign T_Id T_AOp_ML T_Decimal T_Semicolon '
                       'T_RC T_Else T_LC '
                       'T_Id T_Assign T_Id T_AOp_ML T_Decimal T_Semicolon '
                       'T_RC '
                       'T_Return T_Id T_Semicolon '
                       'T_RC')

for_test = (' T_For T_LP T_Id T_Assign T_Decimal T_Semicolon T_Id T_ROp_L T_Decimal T_Semicolon T_Id T_Assign T_Id T_AOp_PL T_Decimal T_RP T_LC '
                       'T_If T_LP T_Id T_AOp_RM T_Decimal T_ROp_E T_Decimal T_RP T_LC '
                       'T_Id T_Assign T_Id T_Semicolon '
                       'T_RC '
                       'T_Id T_Assign T_Id  T_AOp_PL T_Id T_Semicolon '
                       'T_RC') # Continue, Break and variable declaration

b = ('T_If T_LP T_Id T_ROp_GE T_Decimal T_LOp_OR T_Id T_ROp_L T_Id T_LOp_AND T_LOp_NOT T_Id T_RP T_LC'
                       'T_Id T_Assign T_True T_Semicolon T_RC')

a = ('T_If T_LP T_Id T_ROp_E T_Decimal T_RP T_LC '
                       'T_Id T_Assign T_Decimal T_Semicolon '
                       'T_Id T_Assign T_Decimal T_Semicolon '
                       'T_RC')