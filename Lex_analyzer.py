
digit: list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def keyword_identifier(string:str):
    lst:list = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
    if string in lst:
        return True
    return False
def id_identifier(string: str):
    i = 1
    Token = ''
    lst:list = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
    global letters, digit
    if string[0] in letters or string[0] == '_':
        Token += string[0]
        while i < len(string):
            if string[i] in letters or string[i] in digit or string[i] == '_':
                Token += string[i]
            i += 1
    if Token in lst:
        return False
    return Token == string
