HEX: list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']
ASCII_LIST = [chr(i) for i in range(128)]
WHITE_SPACES: list = [' ', '\t', '\n']
#کلمات کلیدی1.1
KEYWORDS = {
    "bool": "T_Bool",
    "break": "T_Break",
    "char": "T_Char",
    "continue": "T_Continue",
    "else": "T_Else",
    "false": "T_False",
    "for": "T_For",
    "if": "T_If",
    "int": "T_Int",
    "print": "T_Print",
    "return": "T_Return",
    "true": "T_True",
    "void": "T_Void",
}

#علامت های نشانه گذاری 3.1
SYMBOL = {
    '(': 'T_LP',
    ')': 'T_RP',
    '{': 'T_LC',
    '}': 'T_RC',
    '[': 'T_LB',
    ']': 'T_RB',
    ';': 'T_Semicolon',
    ',': 'T_Comma',
}

#عملگرهای تک حرفی
SINGLE_CHAR_OPERATORS = {
    '+': "T_AOp_PL",
    '-': "T_AOp_MN",
    '*': "T_AOp_ML",
    '/': "T_AOp_DV",
    '%': "T_AOp_RM",
    '=': "T_Assign",
    '<': 'T_ROp_L',
    '>': 'T_ROp_G',
    '!': 'T_LOp_NOT',
}

#عملگرهای دو حرفی
DOUBLE_CHAR_OPERATORS = {
    '<=': 'T_ROp_LE',
    '>=': 'T_ROp_LE',
    '!=': 'T_ROp_NE',
    '==': 'T_ROp_E',
    '&&': 'T_LOp_AND',
    '||': 'T_LOp_OR',

}
