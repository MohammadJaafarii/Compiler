from anytree import Node, RenderTree, PostOrderIter
import copy
import IdentifierTable
input_string: list = []
IdTable = IdentifierTable.IdentifierTable()
tree_index:int = 0
def dfs(node, visited=None):
    global tree_index
    if visited is None:
        visited = set()

    # اگر نود قبلاً بازدید شده، از آن عبور کن
    if node in visited:
        return

    # نود جاری را بازدید کن
    visited.add(node)

    if node.name in term_userdef:
        term_node = Node(input_string[tree_index], parent= node)
        tree_index -= 1



    # بازدید از بچه‌های نود جاری
    for child in node.children:
        dfs(child, visited)


class Token:
    def __init__(self, type, name, line):
        self.type: str = type
        self.name: str = name
        self.line: int = line

def read_input(file_name):
    global input_string
    with open (file_name, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.split()

            tk = Token(line[0], line[1], line[2])
            input_string.append(tk)

from prettytable import PrettyTable
error_list: list = []



def create_pretty_table(header: list , pretty_table: list, align = None):

    global nonterm_userdef
    # ایجاد یک جدول با ستون‌های خالی
    table = PrettyTable()
    # تنظیم نام ستون‌ها بر اساس طول اولین سطر
    num_columns = len(header)
    columns = header
    table.field_names = columns
    # پر کردن جدول با داده‌های آرایه
    if align is not None:
        table.align = align

    for row in pretty_table:
        if len(row) != num_columns:
            raise ValueError("All rows in the data array must have the same number of elements")
        table.add_row(row)

    return table

def removeLeftRecursion(rulesDiction):
    # for rule: A->Aa|b
    # result: A->bA',A'->aA'|#

    # 'store' has new rules to be added
    store = {}
    # traverse over rules
    for lhs in rulesDiction:
        # alphaRules stores subrules with left-recursion
        # betaRules stores subrules without left-recursion
        alphaRules = []
        betaRules = []
        # get rhs for current lhs
        allrhs = rulesDiction[lhs]
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        # alpha and beta containing subrules are separated
        # now form two new rules
        if len(alphaRules) != 0:
            # to generate new unique symbol
            # add ' till unique not generated
            lhs_ = lhs + "'"
            while (lhs_ in rulesDiction.keys()) \
                    or (lhs_ in store.keys()):
                lhs_ += "'"
            # make beta rule
            for b in range(0, len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDiction[lhs] = betaRules
            # make alpha rule
            for a in range(0, len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['#'])
            # store in temp dict, append to
            # - rulesDiction at end of traversal
            store[lhs_] = alphaRules
    # add newly generated rules generated
    # - after removing left recursion
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction


def LeftFactoring(rulesDiction):
    # for rule: A->aDF|aCV|k
    # result: A->aA'|k, A'->DF|CV

    # newDict stores newly generated
    # - rules after left factoring
    newDict = {}
    # iterate over all rules of dictionary
    for lhs in rulesDiction:
        # get rhs for given lhs
        allrhs = rulesDiction[lhs]
        # temp dictionary helps detect left factoring
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        # if value list count for any key in temp is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        new_rule = []
        # temp_dict stores new subrules for left factoring
        tempo_dict = {}
        for term_key in temp:
            # get value from temp for term_key
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = lhs + "'"
                while (lhs_ in rulesDiction.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                # append the left factored result
                new_rule.append([term_key, lhs_])
                # add expanded rules to tempo_dict
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                # no left factoring required
                new_rule.append(allStartingWithTermKey[0])
        # add original rule
        newDict[lhs] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict


# calculation of first
# epsilon is denoted by '#' (semi-colon)

# pass rule in first function
def first(rule):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    # recursion base condition
    # (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'

    # condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            # fres temporary list of result
            fres = []
            rhs_rules = diction[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            # if no epsilon in result
            # - received return fres
            if '#' not in fres:
                return fres
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                # if result is not already returned
                # - control reaches here
                # lastly if eplison still persists
                # - keep it in result of first
                fres.append('#')
                return fres


# calculation of follow
# use 'rules' list, and 'diction' dict from above

# follow function input is the split result on
# - Non-Terminal whose Follow we want to compute
def follow(nt):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)
    res = None
    solset = set()
    if nt == start_symbol:
        # return '$'
        solset.add('$')

    # check all occurrences
    # solset - is result of computed 'follow' so far

    # For input, check in all rules
    if (nt == 'opt_tail' or nt == 'opt_tail_tail'):
        opt_follow:list = ['T_Int', '$', 'T_LP', 'T_Break', 'T_Id', 'T_Void',
                            'T_Hexadecimal', 'T_Return', 'T_Print', 'T_For', 'T_Decimal', 'T_If', 'T_Continue', 'T_Bool', 'T_RC', 'T_Char']
        return opt_follow
    for curNT in diction:
        rhs = diction[curNT]
        # go for all productions of NT
        for subrule in rhs:
            if nt in subrule:
                # call for all occurrences on
                # - non-terminal in subrule
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    # empty condition - call follow on LHS
                    if len(subrule) != 0:
                        # compute first if symbols on
                        # - RHS of target Non-Terminal exists
                        res = first(subrule)
                        # if epsilon in result apply rule
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS, go circular
                        # - and take follow of LHS
                        # only if (NT in LHS)!=curNT
                        if nt != curNT:
                            res = follow(curNT)

                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)
def computeAllFirsts():
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        # remove un-necessary spaces
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs

    header = ['Rules']
    rule_list:list = []
    for y in diction:
        rule_list.append([f"{y}->{diction[y]}"])
    print(create_pretty_table(header, rule_list))
    print('\n\n')


    diction = removeLeftRecursion(diction)
    header = ['After elimination of left recursion']
    left_recs_list: list = []
    for y in diction:
        left_recs_list.append([f"{y}->{diction[y]}"])

    print(create_pretty_table(header, left_recs_list))
    print('\n\n')



    diction = LeftFactoring(diction)
    header = ['After left factoring']
    left_fct_list: list = []
    for y in diction:
        left_fct_list.append([f"{y}->{diction[y]}"])

    print(create_pretty_table(header, left_fct_list))
    print('\n\n')


    # calculate first for each rule
    # - (call first() on all RHS)
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        # save result in 'firsts' list
        firsts[y] = t

def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

# create parse table
def createParseTable():
    global diction, firsts, follows, term_userdef
    print('----------------------------------')
    print("  Firsts and Follow Result table")
    print('----------------------------------')
    print('\n\n')
    # find space size
    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2
    header = ['Non Terminal', 'First', 'Follow']
    result_list: list = []
    for u in diction:
        total = [f'{u}', f'{firsts[u]}', f'{follows[u]}']
        result_list.append(total)
    print(create_pretty_table(header, result_list))
    print('\n\n')

    # create matrix of row(NT) x [col(T) + 1($)]
    # create list of non-terminals
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.append('$')

    # create the initial empty state of ,matrix
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

    # rules implementation
    for lhs in diction:
        rhs = diction[lhs]
        res: list = []
        for y in rhs:
            res = first(y)
            # epsilon is present,
            # - take union with follow
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) + \
                          list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] \
                                   + f"{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] \
                                       + f",{lhs}->{' '.join(y)}"
    mat = define_sync(mat)

    # final state of parse table
    print('----------------------------------')
    print("     Generated parsing table")
    print('----------------------------------')
    print('\n\n')

    frmt = "{:>12}" * len(terminals)
    str_terminal = frmt.format(*terminals)
    terminal_list: list = []
    terminal_list.append('NonTerminals/Terminals')
    i = 0
    while (i != len(str_terminal) - 1):
        while (str_terminal[i] == ' '):
            i += 1
        terminal = ''
        a = str_terminal[i]
        if (i != len(str_terminal) - 1):
            if (str_terminal[i:i+2] == 'T_'):
                terminal += 'T_'
                i += 2
                a = str_terminal[i]
                while (str_terminal[i] != ' ' and str_terminal[i:i+2] != 'T_'):
                    terminal += str_terminal[i]
                    i += 1
                terminal_list.append(terminal)
        else:
            terminal_list.append(str_terminal[i])

    j = 0
    err_count = 0
    rule_with_noneTerminal: list = []
    for y in mat:
        rule_list: list = []
        rule_list.append(ntlist[j])
        frmt1 = "{:>12}" * len(y)
        for i in y:
            if (i == ''):
                rule_list.append('---')
            else:
                if ',' in i:
                    rule_list.append(f"\033[91m{i}\033[0m")
                    err_count += 1
                else:
                    rule_list.append(i)

        rule_with_noneTerminal.append(rule_list)
        j += 1
    print(create_pretty_table(terminal_list, rule_with_noneTerminal))
    print('\n\n')
    if err_count != 0:
        print(f"\033[91mNumber of Error: {err_count}\033[91m")

    return (mat, grammar_is_LL, terminals)


def tree(root):
    i = 0
    for node in PostOrderIter(root):
        if not node.children:
            if node.name in nonterm_userdef:
                epsilon_leaf = Node('ε', parent=node)


    return root

def define_sync(parser_table):
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    for nt in nonterm_userdef:

        for term in follows[nt]:
            xnt = ntlist.index(nt)
            if term == '$':
                yt = len(term_userdef)
            else:
                yt = terminals.index(term)
            if (parser_table[xnt] [yt] == ''):
                parser_table[xnt][yt] = 'Sync'
    return parser_table

def expected_items(stack):

    first = firsts[stack]
    expected_first = ''
    expected_follow = ''

    for f in first:
        if f != '#':
            expected_first += f + " "
        else:

            follow = follows[stack]
            for fol in follow:
                expected_follow += fol + " "
    return expected_first+" "+expected_follow


def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, term_userdef ,start_symbol):
    global root, input_string

    # for more than one entries
    # - in one cell of parsing table
    if grammarll1 == False:
        inpt_str = ''
        for inpt in input_string:
            inpt_str += f'{inpt} '
        return f"\nInput String = " \
               f"\"{inpt_str}\"\n" \
               f"Grammar is not LL(1)"

    # implementing stack buffer

    stack = [start_symbol, '$']
    buffer = []

    # reverse input string store in buffer
    # input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string


    header = ["Buffer", "Stack" ,"Action"]
    valid_string_list: list = []
    total:list = []
    stack_node = [root]
    top_node = root
    tree_index = len(input_string) - 1
    while True:
        if len(stack_node) > 0:
            top_node = stack_node[0]
            stack_node = stack_node[1:]

        # end loop if all symbols matched
        if stack == ['$'] and buffer !=['$']:
            while buffer != ['$']:
                error_list.append(f"\033[91mUnMatched Token {buffer[-1].type} at line {buffer[-1].line}\033[0m")
                buffer = buffer[:-1]
        if stack == ['$'] and buffer == ['$']:
            if len(error_list) == 0 :
                total = [f'{buffer}',f'{stack}', f'Valid']
                valid_string_list.append(total)
                return "\n\033[92mValid String!\033[0m", valid_string_list, header

            else:

                total = [f'{buffer}', f'{stack}', f'InValid']
                valid_string_list.append(total)
                return '\n\033[91mInvalid String!\033[91m', valid_string_list, header

        elif stack[0] not in term_userdef:

            # take font of buffer (y) and tos (x)
            x = list(diction.keys()).index(stack[0])

            target_buffer: str
            if buffer == ['$']:
                target_buffer = '$'
            else:
                target_buffer = buffer[-1].type
            y = table_term_list.index(target_buffer)
            if parsing_table[x][y] != '' and parsing_table[x][y] != "Sync":
                # format table entry received
                entry = parsing_table[x][y]
                buffer_str: list = []
                if type(buffer) != 'str':
                    buffer_str.append('$')
                    for b in buffer:
                        if b == '$':
                            continue
                        buffer_str.append(b.type)

                if buffer == ['$']:
                    target_buffer = '$'
                else:
                    target_buffer = buffer[-1].type
                total = [f'{buffer_str}',f'{stack}', f'T[{stack[0]}][{target_buffer}] = {entry}']
                valid_string_list.append(total)
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                entryrhs = lhs_rhs[1].split()
                tmp_stack: list = []
                for ent in entryrhs:
                    new_node = Node(ent, parent=top_node)

                    tmp_stack.append(new_node)
                tmp_stack.reverse()
                for tmp in tmp_stack:
                    stack_node.insert(0, tmp)
                stack = entryrhs + stack[1:]
            else:

                error_list.append(f"\033[91m{buffer[-1].type} is error at line {buffer[-1].line} \nExpectation:\n{expected_items(stack[0])}\033[0m\n")
                if parsing_table[x][y]== "Sync":
                    stack = stack[1:]
                elif '#' in firsts[stack[0]]:
                    stack = stack[1:]
                elif parsing_table[x][y] == '':
                    buffer = buffer[:-1]

        else:
            # stack top is Terminal
            if buffer == ['$']:
                target_buffer = '$'
            else:
                target_buffer = buffer[-1].type
            if stack[0] == target_buffer:
                buffer_str: list = []
                for b in buffer:
                    if b == '$':
                        buffer_str.append('$')
                        continue
                    buffer_str.append(b.type)
                total = [f'{buffer_str}',f'{stack}', f'\n\033[92mMatched:{stack[0]}\033[0m']
                valid_string_list.append(total)

                buffer = buffer[:-1]
                stack = stack[1:]
            else:

                error_list.append(f"\033[91m{buffer[-1].type} is error at line {buffer[-1].line} \nExpectation:\n{stack[0]}\033[0m\n")
                stack = stack[1:]



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


diction = {}
firsts = {}
follows = {}
start_symbol = None
root = None
# For Phase 3
func_return: list = []

def starting_SyntaxAnalyzer():
    global start_symbol, root, input_string, tree_index, func_return
    computeAllFirsts()
    # assuming first rule has start_symbol
    # start symbol can be modified in below line of code
    start_symbol = list(diction.keys())[0]
    # computes all FOLLOWs for all occurrences
    computeAllFollows()
    # generate formatted first and follow table
    # then generate parse table
    root = Node(start_symbol)


    read_input('SyntaxInput.txt')
    (parsing_table, result, tabTerm) = createParseTable()

    # validate string input using stack-buffer concept
    if input_string != None:
        validity, valid_string_list, header = validateStringUsingStackBuffer(parsing_table, result,
                                                                             tabTerm,
                                                                             term_userdef, start_symbol)
        print(create_pretty_table(header, valid_string_list, 'l'))

        print('\n\n')
        print(validity)
        print('\n\n')

        for err in error_list:
            print(err)

        # print(root)
        root = tree(root)
        tree_index = len(input_string)-1
        dfs(root)
        for pre, fill, node in RenderTree(root):
            tmp_node: Node = None
            if type(node.name) == type(input_string[0]):
                tmp_node = node.name.name
            else:
                tmp_node = node.name
            print(f"{pre}{tmp_node}")
        travesr_parse_tree(root)
        try:
            if IdTable.func['main'].retVal != 'T_Int' or IdTable.func['main'].paramType != None:
                raise Exception('error in declare main function')
        except:
            raise Exception('program most have main function')

    else:
        print("\nNo input String detected")

#----------------------------------------------------------------------------------------------
#---------------------------------------phase three--------------------------------------------
#----------------------------------------------------------------------------------------------


counter: int = 0
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
            if c.name.name == '=':
                check_assign(rt)


    elif node.name == 'index' or node.name=='number':
        for child in node.children:
            if child.name == 'T_Decimal':
                if int(child.children[0].name.name ) < 1:
                    raise Exception(f'Index must be greater than 0 at line {child.children[0].name.line}')
            if child.name == 'T_Id':
                try:
                    if IdTable.lookup(child.children[0].name.name).type != 'T_Int':
                        raise Exception(f'Index most be integer at line {child.children[0].name.line}')
                except :
                    raise Exception(f'{child.children[0].name.name} must be declared at line {child.children[0].name.line}')

    elif node.name == 'factor':
        for child in node.children:
            if child.name == 'T_Id':

               IdTable.lookup(child.children[0].name)

    if node.name == 'return_stmt':
        check_assign(node=func_return[counter].ItsReturn[0], type_org=func_return[counter].expected_return_type)
        counter += 1

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
                name = child.children[0].name.name
        paramType = []

        function(node=node,paramType=paramType,type=type, name= name)
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
        tp = None
        nm = None
        for child in node.children:
            if child.name == 'type':
                paramType.append(child.children[0].name)
                tp = child.children[0].name
            if child.name == 'T_Id':
                nm = child.children[0].name
        IdTable.declare(name=nm,var_type=tp)



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
        IdTable.declare(node.children[0].name.name,return_value['type'], node.children[0].name.line)
    elif node.name == 'value':
        for c in node.children:

            if c.name == 'bool':
                if not (return_value['type'] == 'T_Bool'):
                    raise Exception(f'Value declaretion is not match')
            if c.name == 'number':
                for ch in c.children:
                    if ch.name == 'T_Hexadecimal' or ch.name == 'T_Decimal':
                        if not (return_value['type'] == 'T_Int'):
                            raise Exception('Value declaretion is not match')
                    elif ch.name == 'T_Id':
                        if IdTable.lookup(ch.children[0].name).type != return_value['type']:
                            raise Exception(f'Value declaretion is not match at line {ch.children[0].name.line}')



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

        if node.children[i].name.name in ['&&','||']:
            if node.children[i-1].name.name not in  ['true', 'false']:
                if IdTable.lookup(node.children[i-1].name).type != 'T_Bool':
                    raise Exception(f'Operand is not bool at line {node.children[i-1].name.line}')
            if node.children[i + 1].name.name not in ['true', 'false']:
                if IdTable.lookup(node.children[i+1].name).type != 'T_Bool':
                    raise Exception(f'Operand is not bool at line {node.children[i+1].name.line}')

        elif node.children[i].name.name in ['!']:
            if node.children[i + 1].name.name not in ['true', 'false']:
                if IdTable.lookup(node.children[i+1].name).type != 'T_Bool':
                    raise Exception(f'Operand is not bool at line {node.children[i+1].name.line}')

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
        if node.children[i].name.name in ['+','-','*','/']:
            a = node.children[i-1].name.name
            if not (a.isdigit() and a not in ['(',')']):
                if IdTable.lookup(node.children[i-1].name).type != 'T_Int':
                    raise Exception(f'Operand is not int at line {node.children[i - 1].name.line}')
            b = node.children[i + 1].name.name
            if not (b.isdigit() and b not in ['(',')']):
                if IdTable.lookup(node.children[i+1].name).type != 'T_Int':
                    raise Exception(f'Operand is not int at line {node.children[i+1].name.line}')


def check_assign(node,type_org=None):
    if type_org == None:
        type_org = IdTable.lookup(node.children[0].name).type
    index = 0
    for i in range(len(node.children)):
        if node.children[i].name.name == '=':
            index = i + 1
            break

    for i in range(index,len(node.children)):
        a = node.children[i].name.name
        if (not a in ['+','-','*','/']) and (not a.isdigit()) and (not a in ['true','false']):
            if IdTable.lookup(node.children[i].name).type != type_org:
                raise Exception(f"Not Matching type for variable '{a}' at line {node.children[i].name.line}\n<{a}>'s type: {IdTable.lookup(node.children[i].name).type}"
                                f"\nExpected type: {type_org}")

        elif a in ['true','false']:
            if type_org!= 'T_Bool':
                raise Exception(f"'{a}' is Bool but {type_org} is expected at line {node.children[i].name.line}")
        elif a.isdigit():
            if type_org == 'T_Bool':
                raise Exception(f"'{a}' is {node.children[i].name.type} but Boolean variable is expected at line {node.children[i].name.line}")




class Func_Return:
    def __init__(self, name, expected_type):
        self.function = name
        self.expected_return_type = expected_type
        self.ItsReturn = []
    def add_return(self, returnn):
        self.ItsReturn.append(returnn)
