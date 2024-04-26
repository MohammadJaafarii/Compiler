import sys
from tkinter import filedialog
import SymbolTable
keyword: list = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
punctuator: list = ['{', '}', '(', ')', '[', ']', ',', ';']
hex: list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']
arithmetic_operator = ['+', '-', '*', '/', '%', '=']
relational_operators = [">", "<", ">=", "<=", "==", "!="]
logic_operator = ["&&", "||", "!"]
ascii_list = [chr(i) for i in range(128)]
line_lists:list = []
functions_list: list = ['keyword_identifier', 'id_identifier', 'punctuator_identifier', 'comment_identifier', 'number_identifier',
                        'staticString_identifier', 'staticChar_identifier', 'operator_identifier', 'whitespace']
Type :dict = {
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
    '(': 'T_LP',
    ')': 'T_RP',
    '{': 'T_LC',
    '}': 'T_RC',
    '[': 'T_LB',
    ']': 'T_RB',
    ';': 'T_Semicolon',
    ',': 'T_Comma',
    '+': "T_AOp_PL",
    '-': "T_AOp_MN",
    '*': "T_AOp_ML",
    '/': "T_AOp_DV",
    '%': "T_AOp_RM",
    '=': "T_Assign",
    '<': 'T_ROp_L',
    '>': 'T_ROp_G',
    '!': 'T_LOp_NOT',
    '<=': 'T_ROp_LE',
    '>=': 'T_ROp_LE',
    '!=': 'T_ROp_NE',
    '==': 'T_ROp_E',
    '&&': 'T_LOp_AND',
    '||': 'T_LOp_OR',
}
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
}

#علامت های نشانه گذاری 3.1
Symbol = {
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
def is_digit(character):
    return '0' <= character <= '9'

def is_alpha(character):
    return 'a' <= character <= 'z' or 'A' <= character <= 'Z'


def keyword_identifier(string:str):
    global keyword
    if string in keyword:
        return True
    return False
def id_identifier(string: str):
    i = 1
    Token = ''
    if is_alpha(string[0]) or string[0] == '_':
        Token += string[0]
        while i < len(string):
            if is_alpha(string[i]) or is_digit(string[i]) or string[i] == '_':
                Token += string[i]
            i += 1
    global keyword
    if Token in keyword:
        return False
    return Token == string

def punctuator_identifier(character: str):
    global punctuator
    if character in punctuator and len(character) == 1:
        return True
    return False
def comment_identifier(string: str):
    if len(string) > 2 and string[0] == '/' and string[1] == '/' and string[len(string) - 1] == '\n':
        return True
    return False
def number_identifier(string:str):
    global hex
    i = 0
    Token = ''
    # hex detector
    if len(string) >= 2 and string[0:2] == '0x' or string[0:2] == '0X':
        Token += string[0:2]
        i = 2
        if string[i] in hex:
            Token += string[i]
            i += 1
            while i < len(string) and string[i] in hex:
                Token += string[i]
                i += 1
            if i < len(string) and string[i] == '.':
                Token += string[i]
                i += 1
                while i < len(string) and string[i] in hex:
                    Token += string[i]
                    i += 1
    # decimal detector
    elif is_digit(string[i]) or string[i] == '+' or string[i] == '-':
        i = 0
        Token = ''
        Token += string[i]
        i += 1
        while i < len(string) and is_digit(string[i]):
            Token += string[i]
            i += 1
        if i < len(string) and string[i] == '.':
            Token += '.'
            i += 1
            while i < len(string) and is_digit(string[i]):
                Token += string[i]
                i += 1
    return Token == string
def staticString_identifier(string:str):
    Token = ''
    i = 0
    if len(string) > 2 and string[0] == '"' and string[len(string) - 1] == '"':
        Token += '"'
        i += 1
        while i < len(string) - 1:
            if string[i] == '"':
                if string[i-1] == '\\':
                    Token += string[i]
                i += 1
                continue
            Token += string[i]
            i += 1
        Token += '"'
        i += 1

    return Token == string
def staticChar_identifier(string:str):
    global ascii_list

    Token = ''
    if string[0] =="'" and string[len(string) - 1] == "'":
        Token += "'"
        if string[1:3] == "\\'" or string[1:3] == "\\\\":
            Token += string[1:3]
        elif string[1] in ascii_list:
            Token += string[1]
        Token += "'"
    return Token == string

def operator_identifier(string: str):
    global arithmetic_operator, logic_operator, relational_operators
    if string in arithmetic_operator or string in logic_operator or string in relational_operators:
        return True
    return False
def whitespace(string: str):
    return string == ' ' or string == '\t' or string == '\n'

def read_file():
    file_path = filedialog.askopenfilename(initialdir='C:\\Users\\User\\PycharmProjects')
    with open(file_path, 'r') as file:
        global line_lists
        while True:
            line = file.readline()
            if not line:
                break
            line_lists.append(line)
def analyzer():
    line_lists = ['	if (c == true){']
    symboleTable = SymbolTable.SymbolTable()
    index: int = 0
    global functions_list
    for line in line_lists:
        iterator_text = ''
        prev_flag = False
        curr_flag = False
        prev_funct = ''
        curr_funct = ''
        i = -1
        x = len(line)
        while i < len(line):
            i += 1
            iterator_text += line[i]
            curr_flag = False
            curr_funct = ''
            for funct in functions_list:
                funct_name = getattr(sys.modules[__name__], funct)
                flag = funct_name(iterator_text)
                if flag:
                    curr_flag = flag
                    curr_funct = funct
                if curr_flag == False and funct == functions_list[len(functions_list) - 1]:
                    curr_flag = False
                    curr_funct = funct
            if curr_flag == False and prev_flag:
                Token = iterator_text[: -1]
                i -= 1
                iterator_text = ''
                type: str = ''
                if prev_funct == 'staticChar_identifier':
                    type = 'T_Character'
                elif prev_funct == 'staticString_identifier':
                    type = 'T_String'
                elif prev_funct == 'number_identifier':
                    type = 'T_Decimal'
                elif prev_funct == 'comment_identifier':
                    type = 'T_Comment'
                elif prev_funct == 'id_identifier':
                    type = 'T_Id'
                else:
                    type = Type[Token]
                symboleTable.insert_entry(name= Token, type= type, location= index, length= len(Token), value= None)
            elif curr_flag and curr_funct == 'whitespace':
                # Fill symbol table by whitespace token
                type = 'T_Whitespace'
                Token = iterator_text
                iterator_text = ''
                symboleTable.insert_entry(name=Token, type=type, value=None, location=index, length=len(Token))
                if iterator_text == '\t':
                    index += 1

            else:
                prev_flag = curr_flag
                prev_funct = curr_funct
            index += 1

    return SymbolTable
#read_file()
st = analyzer()
print('successfully')
