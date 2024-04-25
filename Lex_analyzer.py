keyword: list = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
punctuator: list = ['{', '}', '(', ')', '[', ']', ',', ';']
hex: list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']
arithmetic_operator = ['+', '-', '*', '/', '%']
relational_operators = [">", "<", ">=", "<=", "==", "!="]
logic_operator = ["&&", "||", "!"]
ascii_list = [chr(i) for i in range(128)]
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
    if string[0] == '/' and string[1] == '/' and string[len(string) - 1] == '\n':
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

print(staticString_identifier('"annnaa"hfdt"'))
