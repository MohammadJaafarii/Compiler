# all types in Token
id:int = 0
from tkinter import filedialog
class Token:
    def __init__(self, name, type, location, length, value=None, line=0, error= None):
        global id
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        self.length = length
        self.value = value
        self.line = line
        self.error = error
        id += 1




# Symbol Table
class SymbolTable:
    def __init__(self,):
        #dic for table
        self.entries = {}
        self.id = {}
    def insert_entry(self, token: Token):
        if token.name in self.entries:
            raise  ValueError(f"this name {token.name} is in table before")

        self.entries[token.id] = {
            "name" : token.name,
            "type" :token.type,
            "value" : token.value,
            "location" : token.location,
            "length" : token.length,
            'line' : token.line,
            'error' : token.error
        }
        if token.type == "T_Id":
            self.check_duplicate_id(token)
    def get_entry(self, id):
        return self.entries.get(id)

    def check_duplicate_id(self, token: Token):

        if not token.name in self.id.keys():
            self.id [token.name] = {
                "type": token.type,
                "value": token.value,
                "location": token.location,
                "length": token.length,
                'line': token.line,
                'error': token.error
            }

    def update_entry(self, id, value):
        if id not in self.entries:
            raise ValueError(f"this name {id} is not in table ")

        self.entries[id]["value"] = value

    def delete_entry(self,id):
        if id not in self.entries:
            raise ValueError(f"this name {id} is not in table")

        del self.entries[id]