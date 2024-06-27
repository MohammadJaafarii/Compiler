import IdentifierTable
from anytree import Node, RenderTree, PostOrderIter
from Rules import nonterm_userdef, term_userdef

IdTable = IdentifierTable.IdentifierTable()

counter: int = 0
func_return: list = []

def tree(root):
    i = 0
    for node in PostOrderIter(root):
        if not node.children:
            if node.name in nonterm_userdef:
                epsilon_leaf = Node('ε', parent=node)


    return root
def travesr_parse_tree(node, visited=None):
    global counter
    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    # نود جاری را بازدید کن
    visited.add(node)
    if node.name == 'decl_or_func':
        arg_node = tree(node)
        decl_or_func(arg_node)

    elif node.name == 'T_LC':
        IdTable.enter_scope()

    elif node.name == 'T_RC':
        IdTable.exit_scope()

    elif node.name == 'condition':
        arg_node = tree(node)
        rt = Node(name='condition')
        condition(arg_node,rt)
        check_bitOp(rt)

    elif node.name == 'expr':
        arg_node = tree(node)
        rt = None
        rt = Node(name='expr')
        expression(arg_node,rt)
        checkOp(rt)
        for c in rt.children:
            if c.name == '=':
                check_assign(rt)


    elif node.name == 'index' or node.name=='number':
        for child in node.children:
            if child.name == 'T_Decimal':
                if child.children[0].name == '0':
                    raise Exception('index most be greater than 0')
            if child.name == 'T_Id':
                try:
                    if IdTable.lookup(child.children[0].name).type != 'T_Int':
                        raise Exception('index most be integer')
                except :
                    raise Exception(f'{child.children[0].name} must declared')

    elif node.name == 'factor':
        for child in node.children:
            if child.name == 'T_Id':
               IdTable.lookup(child.children[0].name)

    if node.name == 'return_stmt':

        check_assign(node=func_return[counter].ItsReturn[0], type_org=func_return[counter].expected_return_type)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        travesr_parse_tree(child, visited)



def decl_or_func(node):
    func_flag = False
    for child in node.children:
        if child.name == 'decl_or_func_tail':
            for ch in child.children:
                if ch.name == 'T_LP':
                    func_flag = True

    if func_flag == True:
        #function
        type = None
        name = None
        for child in node.children:
            if child.name == 'type':
                type = child.children[0].name
            elif child.name == 'T_Id':
                name = child.children[0].name
        paramType = []

        function(node=node,paramType=paramType,type=type, name= name)
        IdTable.exit_scope()
        if paramType == []:
            paramType = None
        IdTable.enter_func(name,type,type,paramType)




    else:
        #variable
        variable(node)


def function(node,type, name,paramType=None, visited=None):
    global func_return
    if visited is None:
        visited = set()
    if paramType is None:
        paramType = []

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    if node.name == 'parameter':
        for child in node.children:
            if child.name == 'type':
                paramType.append(child.children[0].name)



    if node.name == 'return_stmt':
        for child in node.children:
            if child.name == 'expr':
                arg_node = tree(child)
                rt = None
                rt = Node(name='expr')
                expression(arg_node, rt)
                rt = tree(rt)
                fnt_rtrn = Func_Return(name=name, expected_type=type)
                fnt_rtrn.add_return(rt)
                func_return.append(fnt_rtrn)

    visited.add(node)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        function(node=child, type= type, paramType=paramType, visited=visited, name=name)



def variable(node,return_value={} ,visited=None):
    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return
    if node.name == 'type':
        return_value['type'] = node.children[0].name
    elif node.name == 'T_Id':
        IdTable.declare(node.children[0].name,return_value['type'])
    elif node.name == 'value':
        for c in node.children:
            if c.name == 'bool':
                if not (return_value['type'] == 'T_Bool'):
                    raise Exception('value declaretion is not match')
            if c.name == 'number':
                for ch in c.children:
                    if ch.name == 'T_Hexadecimal' or ch.name == 'T_Decimal':
                        if not (return_value['type'] == 'T_Int'):
                            raise Exception('value declaretion is not match')
                    elif ch.name == 'T_Id':
                        if IdTable.lookup(ch.children[0].name).type != return_value['type']:
                            raise Exception('value declaretion is not match')



    visited.add(node)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        variable(child, return_value,visited)


def condition(node,rt,visited=None):

    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    # نود جاری را بازدید کن
    visited.add(node)

    if (node.name not in term_userdef) and (node.name not in nonterm_userdef) and node.name !='ε':
        rt = Node(node.name, parent=rt)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        condition(child, rt,visited)

def check_bitOp(node):

    for i in range(0,len(node.children)):
        if node.children[i].name in ['&&','||']:
            if node.children[i-1].name not in  ['true', 'false']:
                if IdTable.lookup(node.children[i-1].name).type != 'T_Bool':
                    raise Exception('operand is not bool')
            if node.children[i + 1].name not in ['true', 'false']:
                if IdTable.lookup(node.children[i+1].name).type.type != 'T_Bool':
                    raise Exception('operand is not bool')

        elif node.children[i].name in ['!']:
            if node.children[i + 1].name not in ['true', 'false']:
                if IdTable.lookup(node.children[i+1].name).type != 'T_Bool':
                    raise Exception('operand is not bool')

def expression(node,rt,visited=None):
    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    # نود جاری را بازدید کن
    visited.add(node)

    if (node.name not in term_userdef) and (node.name not in nonterm_userdef) and node.name !='ε':
        rt = Node(node.name, parent=rt)

    # بازدید از بچه‌های نود جاری
    for child in node.children:
        expression(child, rt,visited)

def checkOp(node):
    for i in range(0,len(node.children)):
        if node.children[i].name in ['+','-','*','/']:
            a = node.children[i-1].name
            if not (a.isdigit() and a not in ['(',')']):
                if IdTable.lookup(node.children[i-1].name).type != 'T_Int':
                    raise Exception('operand is not int')
            b = node.children[i + 1].name
            if not (b.isdigit() and b not in ['(',')']):
                if IdTable.lookup(node.children[i+1].name).type != 'T_Int':
                    raise Exception('operand is not int')


def check_assign(node,type_org=None):
    if type_org == None:
        type_org = IdTable.lookup(node.children[0].name).type
    index = 0
    for i in range(len(node.children)):
        if node.children[i].name == '=':
            index = i + 1
            break

    for i in range(index,len(node.children)):
        a = node.children[i].name
        if (not a in ['+','-','*','/']) and (not a.isdigit()) and (not a in ['true','false']):
            if IdTable.lookup(a).type != type_org:
                raise Exception('in assaignment type not match')

        elif a in ['true','false']:
            if type_org!= 'T_Bool':
                raise Exception('in assaignment type not match')
        elif a.isdigit():
            if type_org == 'T_Bool':
                raise Exception('in assaignment type not match')




class Func_Return:
    def __init__(self, name, expected_type):
        self.function = name
        self.expected_return_type = expected_type
        self.ItsReturn = []
    def add_return(self, returnn):
        self.ItsReturn.append(returnn)