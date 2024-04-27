# all types in Token
Types = ['T_Bool', 'T_Breal', 'T_Char', 'T_Continue', 'T_Else', 'T_False', 'T_For', 'T_If', 'T_Int',
         'T_Print', 'T_Return', 'T_True', 'T_AOp_PL', 'T_AOp_MN', 'T_AOp_ML', 'T_AOp_DV', 'T_AOp_RM',
         'T_ROp_L', 'T_ROp_G', 'T_ROp_LE', 'T_ROp_GE', 'T_ROp_NE', 'T_ROp_E', 'T_ⅬOp_AND', 'T_LOp_OR', 'T_LOp_NOT'
    , 'T_Assign', 'T_LP', 'T_RP', 'T_LC', 'T_RC', 'T_LB', 'T_RB', 'T_Semicolon', 'T_Comma', 'T_Id', 'T_Decimal'
    , 'T_Hexadecimal', 'T_String', 'T_Character', 'T_Comment', 'T_Whitespace']
id:int = 0

class Token:
    def __init__(self, name, type, location, length, value=None, line=0):
        global id
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        self.length = length
        self.value = value
        self.line = line
        id += 1




# Symbol Table
class SymbolTable:
    def __init__(self,):
        #dic for table
        self.entries = {}

    def insert_entry(self, name, type, value, location, length, line):
        if name in self.entries:
            raise  ValueError(f"this name {name} is in table before")

        token = Token(name,type,location,length,value, line)

        self.entries[token.id] = {
            "name" : token.name,
            "type" :token.type,
            "value" : token.value,
            "location" : token.location,
            "length" : token.length,
            'line' : line
        }

    def get_entry(self, id):
        return self.entries.get(id)


    def update_entry(self, id, value):
        if id not in self.entries:
            raise ValueError(f"this name {id} is not in table ")

        self.entries[id]["value"] = value

    def delete_entry(self,id):
        if id not in self.entries:
            raise ValueError(f"this name {id} is not in table")

        del self.entries[id]

