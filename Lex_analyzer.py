import sys
from tkinter import filedialog
from SymbolTable import SymbolTable, Token
from prettytable import PrettyTable
from element_lists import *
line_lists:list = []
invalid_tokens: Token = []
start_index: int = 0
line_index: int = 1
line_start_index: int = 0
functions_list: list = ['keyword_identifier', 'id_identifier', 'punctuator_identifier', 'comment_identifier', 'numberhex_identifier', 'numberdecimal_identifier',
                        'staticString_identifier', 'staticChar_identifier', 'operator_identifier', 'whitespace_identifier']

symboleTable = SymbolTable()
def is_digit(character):
    return '0' <= character <= '9'

def is_alpha(character):
    return 'a' <= character <= 'z' or 'A' <= character <= 'Z'


def keyword_identifier(line: str, iterator: int):
    global start_index, line_start_index, line_index, KEYWORDS
    token = ''
    while iterator < len(line) and is_alpha(line[iterator]):
        token += line[iterator]
        iterator += 1

    if token in KEYWORDS:
        tk = Token(name=token, type=KEYWORDS[token], value=None,location=start_index,
                                                     length=len(token), line=line_index)
        return tk
    return None
def id_identifier(line: str, iterator: int):
    token = ''
    if not (is_alpha(line[iterator]) or line[iterator] == '_'): # Valid char for starting ID
        return None

    while iterator < len(line) and (is_alpha(line[iterator]) or is_alpha(line[iterator]) or line[iterator] == '_'):
        token += line[iterator]
        iterator += 1

    global KEYWORDS
    if not token in KEYWORDS:
        tk = Token(name=token, type='T_Id', value=None,location=start_index,
                                             length=len(token), line=line_index)
        return tk
    return None

def punctuator_identifier(line: str, iterator: int):
    global SYMBOL
    token = ''
    if line[iterator] in SYMBOL:
        token += line[iterator]
        tk = Token(name=token, type= SYMBOL[token], value=None, location=start_index, length=len(token), line=line_index)
        return tk
    return None
def comment_identifier(line: str, iterator: int):
    if not line[iterator: iterator+2] == '//':
        return None
    token = ''
    while iterator < len(line) and line[iterator] != '\n':
        token += line[iterator]
        iterator += 1
    if token and line[iterator] == '\n':
        tk = Token(name=token, type= 'T_Comment', value=None, location=start_index,
                     length=len(token), line=line_index)
        return tk
    return None

# hex detector
def numberhex_identifier(line: str, iterator: int):
    global HEX
    token = ''
    if not line [iterator: iterator+2].lower() =='0x':
        return None
    else:
        token += line [iterator: iterator+2]
        iterator += 2
    while iterator < len(line):
        if line[iterator] in HEX:
            token += line[iterator]
            iterator += 1
        elif line[iterator] =='.':
            token += line[iterator]
            iterator += 1
        else:
            break
    if not token:
        return None
    tk = Token(name=token, type= 'T_Hexadecimal', value=None, location=start_index,
                     length=len(token), line=line_index)
    return tk

# decimal detector
def numberdecimal_identifier(line: str, iterator: int):
    token = ''
    if line[iterator] == '-' or line[iterator] =='+':
        if (iterator+1 < len(line) and not is_digit(line[iterator+1])) or iterator + 1 == len(line):
            return None
    if line[iterator] == '+' or line[iterator] == '-':
        token += line[iterator]
        iterator += 1
    while iterator < len(line):
        if is_digit(line[iterator]):
            token += line[iterator]
            iterator += 1
        elif line[iterator] == '.':
            token += line[iterator]
            iterator += 1
        else:
            break
    if not token:
        return None
    else:
        tk = Token(name=token, type= 'T_Decimal', value=None, location=start_index,
                     length=len(token), line=line_index)
        return tk

def staticString_identifier(line: str, iterator: int):
    token = ''
    if line[iterator] != '"':
        return None
    token += '"'
    iterator += 1
    while iterator < len(line) and line[iterator] != '"':
        token += line[iterator]
        if line[iterator] == '\\':
            iterator += 1
            token += line[iterator]
        iterator += 1
    if iterator < len(line) and line[iterator] == '"':
        token += '"'
        tk = Token(name=token, type= 'T_String', value=None, location=start_index,
                     length=len(token), line=line_index)
        return tk
    return None

def staticChar_identifier(line: str, iterator: int):

    token = ''
    if line[iterator] != "'":
        return None
    token += "'"
    iterator += 1
    while iterator < len(line) and line [iterator] != "'" and line[iterator] in ASCII_LIST:
        token += line[iterator]
        if line[iterator] == '\\':
            iterator += 1
            token += line[iterator]
        iterator += 1
    if iterator < len(line) and line[iterator] == "'" and (len(token) in [2,3] or (len(token) == 4 and token[0] == '\\')):
        token += "'"
        tk = Token(name=token, type='T_Character', value=None, location=start_index,
                     length=len(token), line=line_index)
        return tk
    return None
def operator_identifier(line: str, iterator: int):
    global DOUBLE_CHAR_OPERATORS, SINGLE_CHAR_OPERATORS
    token = ''
    if line[iterator: iterator+2] in DOUBLE_CHAR_OPERATORS:
        token += line[iterator: iterator+2]
        return Token(name= token, type= DOUBLE_CHAR_OPERATORS[token], value=None, location=start_index,
                     length=len(token), line=line_index)
    elif line[iterator] in SINGLE_CHAR_OPERATORS:
        token += line[iterator]
        tk = Token(name=token, type=SINGLE_CHAR_OPERATORS[token], value=None, location=start_index,
                     length=len(token), line=line_index)
        return tk
    return None
def whitespace_identifier(line: str, iterator: int):
    if line[iterator] in WHITE_SPACES:
        return True
    return None



def read_file():
    file_path = filedialog.askopenfilename(initialdir='C:\\Users\\User\\PycharmProjects\\Compiler')
    with open(file_path, 'r') as file:
        global line_lists
        while True:
            line = file.readline()
            if not line:
                break
            line_lists.append(line)
def display_and_save():
    prettytable_list = []
    table = PrettyTable(['Location', 'Name', 'Type', 'line'])
    file = open('output.txt', 'w')
    for key in symboleTable.entries:
        # Valid Tokens except WhiteSpaces
        if not (symboleTable.entries[key]['name'] == ' ' or symboleTable.entries[key]['name'] == '\t' or
                symboleTable.entries[key]['name'] == '\n') and not symboleTable.entries[key]['error']:
            str = f"{symboleTable.entries[key]['location']}: {symboleTable.entries[key]['name']} -> {symboleTable.entries[key]['type']} | line -> {symboleTable.entries[key]['line']}\n"
            file.write(str)
            prettytable_list.append([symboleTable.entries[key]['location'], symboleTable.entries[key]['name'],
                                     symboleTable.entries[key]['type'], symboleTable.entries[key]['line']])
        # WhiteSpaces
        elif not symboleTable.entries[key]['error']:
            str = f"{symboleTable.entries[key]['location']}: whitespace -> {symboleTable.entries[key]['type']} | line -> {symboleTable.entries[key]['line']}\n"
            file.write(str)
            prettytable_list.append(
                [symboleTable.entries[key]['location'], 'whitespace', symboleTable.entries[key]['type'],
                 symboleTable.entries[key]['line']])
        # Invalid Tokens
        else:
            red_color = "\033[31m"
            reset_color = "\033[0m"
            str = f"{symboleTable.entries[key]['location']}: Error -> {symboleTable.entries[key]['type']}\nName: {symboleTable.entries[key]['name']}  | line -> {symboleTable.entries[key]['line']}\n"
            file.write(str)
            prettytable_list.append([f'{red_color}{symboleTable.entries[key]['location']}{reset_color}', f'{red_color}{symboleTable.entries[key]['name']}{reset_color}', f'{red_color}{symboleTable.entries[key]['type']}{reset_color}',
                                     f'{red_color}{symboleTable.entries[key]['line']}{reset_color}'])
    file.close()
    for row in prettytable_list:
        table.add_row(row)
    print(table)
def analyzer():
    global functions_list, start_index, line_index, line_start_index
    start_index = 0
    line_index = 1
    current_token: Token = None
    previous_token: Token = None
    token_founded = False
    for line in line_lists:
        line_start_index = 0
        while line_start_index < len(line):
            token_founded = False
            for funct in functions_list:
                funct_name = getattr(sys.modules[__name__], funct)
                token = funct_name(line, line_start_index)
                if token == True:
                    tk = Token(name=line[line_start_index], type='T_Whitespace', value=None, location=start_index,
                     length=len(line[line_start_index]), line=line_index)
                    current_token = tk
                    symboleTable.insert_entry(tk)
                    token_founded = True
                    start_index += tk.length
                    line_start_index += tk.length
                    break
                elif token is not None:
                    current_token = token
                    if previous_token is not None and((previous_token.type == 'T_Decimal' or previous_token.type == 'T_Hexadecimal') and current_token.type == 'T_Id'):
                        symboleTable.delete_entry(previous_token.id)
                        token.name = previous_token.name + current_token.name
                        token.type = 'Invalid Token'
                        token.length = previous_token.length + current_token.length
                        token.location = previous_token.location
                        token.error = True


                    symboleTable.insert_entry(token)
                    token_founded = True
                    start_index += token.length
                    line_start_index += token.length
                    break



            if not token_founded:
                tk = Token(name=line[line_start_index], type='Invalid Token', value=None, location=start_index,
                     length=len(line[line_start_index]), line=line_index, error=True)
                current_token = tk
                symboleTable.insert_entry(tk)
                start_index += 1
                line_start_index += 1
            previous_token = current_token
        line_index += 1




if __name__ == '__main__':
    read_file()
    analyzer()
    display_and_save()




    'stmt': 'for_stmt',
    'for_stmt': 'T_For T_LP opt_expr T_Semicolan opt_expr T_Semicolan opt_expr T_RP block',
    'opt_expr': ['expr', 'epsilon'],
    'expr': ['assignment', 'condition'],
    'assignment': 'T_ID T_Assign expr',