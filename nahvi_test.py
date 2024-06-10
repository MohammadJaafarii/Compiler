
from prettytable import PrettyTable

def create_table(terminals, data):
    if not data:
        raise ValueError("The provided data array is empty")

    # ایجاد یک جدول با ستون‌های خالی
    table = PrettyTable()

    # تنظیم نام ستون‌ها بر اساس طول اولین سطر
    num_columns = len(data[0])
    columns = terminals
    table.field_names = columns

    # پر کردن جدول با داده‌های آرایه
    for row in data:
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
    # if (nt == 'condition' or nt == 'condition_tail' or nt == 'condition_tail_tail'):
    #     condition_follow:list = ['T_RP', 'T_Semicolon']
    #     return condition_follow
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
                            print(curNT)
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
                            print(curNT)
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

    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")
    print(f"\nAfter elimination of left recursion:\n")

    diction = removeLeftRecursion(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")
    print("\nAfter left factoring:\n")

    diction = LeftFactoring(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")

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

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1


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

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1


# create parse table
def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef
    print("\nFirsts and Follow Result table\n")
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

    print(f"{{:<{10}}} "
          f"{{:<{mx_len_first + 5}}} "
          f"{{:<{mx_len_fol + 5}}}"
          .format("Non-T", "FIRST", "FOLLOW"))
    for u in diction:
        print(f"{{:<{10}}} "
              f"{{:<{mx_len_first + 5}}} "
              f"{{:<{mx_len_fol + 5}}}"
              .format(u, str(firsts[u]), str(follows[u])))

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

    # final state of parse table
    print("\nGenerated parsing table:\n")
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
        # print(f"{ntlist[j]} \t\t{frmt1.format(*y)}")
        j += 1
    print(create_table(terminal_list, rule_with_noneTerminal))
    print(f"Number of Error: {err_count}")
    return (mat, grammar_is_LL, terminals)


def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string, term_userdef ,start_symbol):

    print(f"\nValidate String => {input_string}\n")

    # for more than one entries
    # - in one cell of parsing table
    if grammarll1 == False:
        return f"\nInput String = " \
               f"\"{input_string}\"\n" \
               f"Grammar is not LL(1)"

    # implementing stack buffer

    stack = [start_symbol, '$']
    buffer = []

    # reverse input string store in buffer
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    print("{:>20} {:>20} {:>20}".
          format("Buffer", "Stack" ,"Action"))
    while True:
        # end loop if all symbols matched
        if stack == ['$'] and buffer == ['$']:
            print("{:>20} {:>20} {:>20}"
                  .format(' '.join(buffer),
                          ' '.join(stack),
                          "Valid"))
            return "\nValid String!"
        elif stack[0] not in term_userdef:
            # take font of buffer (y) and tos (x)
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != '':
                # format table entry received
                entry = parsing_table[x][y]
                print("{:>20} {:>20} {:>25}".
                      format(' '.join(buffer),
                             ' '.join(stack),
                             f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                return f"\nInvalid String! No rule at " \
                       f"Table[{stack[0]}][{buffer[-1]}]."
        else:
            # stack top is Terminal
            if stack[0] == buffer[-1]:
                print("{:>20} {:>20} {:>20}"
                      .format(' '.join(buffer),
                              ' '.join(stack),
                              f"Matched:{stack[0]}"))
                buffer = buffer[:-1]
                stack = stack[1:]
            else:
                return "\nInvalid String! " \
                       "Unmatched terminal symbols"


# DRIVER CODE - MAIN

# NOTE: To test any of the sample sets, uncomment ->
# 'rules' list, 'nonterm_userdef' list, 'term_userdef' list
# and for any String validation uncomment following line with
# 'sample_input_String' variable.

sample_input_string = None

# sample set 1 (Result: Not LL(1))
# rules=["A -> S B | B",
#        "S -> a | B c | #",
#        "B -> b | d"]
# nonterm_userdef=['A','S','B']
# term_userdef=['a','c','b','d']
# sample_input_string="b c b"

# sample set 2 (Result: LL(1))
# rules=["S -> A | B C",
#        "A -> a | b",
#        "B -> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="p c"

# sample set 3 (Result: LL(1))
# rules=["S -> A B | C",
#        "A -> a | b | #",
#        "B-> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="a c b"

# sample set 4 (Result: Not LL(1))
# rules = ["S -> A B C | C",
#          "A -> a | b B | #",
#          "B -> p | #",
#         "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="b p p c"

# sample set 5 (With left recursion)
# rules=["A -> B C c | g D B",
#        "B -> b C D E | #",
#        "C -> D a B | c a",
#        "D -> # | d D",
#        "E -> E a f | c"
#       ]
# nonterm_userdef=['A','B','C','D','E']
# term_userdef=["a","b","c","d","f","g"]
# sample_input_string="b a c a c"

# sample set 6
# rules=["E -> T E'",
#        "E' -> + T E' | #",
#        "T -> F T'",
#        "T' -> * F T' | #",
#        "F -> ( E ) | id"
# ]
# nonterm_userdef=['E','E\'','F','T','T\'']
# term_userdef=['id','+','*','(',')']
# sample_input_string="id * * id"
# example string 1
# sample_input_string="( id * id )"
# example string 2
# sample_input_string="( id ) * id + id"

# sample set 7 (left factoring & recursion present)
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
    'number -> T_Decimal | T_Hexadecimal',
    'if_stmt -> T_If T_LP condition T_RP block opt_tail',
    'opt_tail -> T_Else tail | #',
    'tail -> T_If T_LP condition T_RP block tail | block',
    'block -> T_LC stmt_list_tail T_RC ',
    'condition -> or_condition',
    'or_condition -> and_condition or_condition_tail',
    'or_condition_tail -> T_LOp_OR and_condition or_condition_tail | #',
    'and_condition -> not_condition and_condition_tail',
    'and_condition_tail -> T_LOp_AND not_condition and_condition_tail | #',
    'not_condition -> T_LOp_NOT T_Id | expr relop expr',

    'break_stmt -> T_Break T_Semicolon',
    'continue_stmt -> T_Continue T_Semicolon',
    'relop -> T_ROp_LE | T_ROp_GE | T_ROp_NE | T_ROp_E | T_ROp_L | T_LOp_AND | T_LOp_OR',
    'expr_tail_tail -> expr_tail expr_tail_tail | #',
    'term_tail_tail -> term_tail term_tail_tail | #',
    'expr -> term expr_tail_tail',
    'expr_tail -> T_AOp_PL term  | T_AOp_MN term  | T_Assign term ',
    'term -> factor term_tail_tail',
    'term_tail -> T_AOp_DV factor  | T_AOp_RM factor  | T_AOp_ML factor ',
    'factor -> T_Id isarray | T_Decimal | T_Hexadecimal | T_LP expr T_RP',
    'isarray -> T_LB index T_RB | #',
    'index -> T_Hexadecimal | T_Decimal | T_Id',
    'for_stmt -> T_For T_LP for_tail',
    'for_tail -> expr T_Semicolon condition T_Semicolon expr T_RP block | decl T_Semicolon condition T_Semicolon expr T_RP block',
    'func_stmt -> type T_Id T_LP parameter_list T_RP func_body',
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
                   'if_stmt','matched','opt_tail','tail','condition','block','expr','term_tail_tail','expr_tail_tail','expr_tail','term',
                   'term_tail','factor','isarray','index','for_stmt','func_stmt','parameter_list',
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


sample_input_string = (' T_For T_LP T_Int T_Id T_Assign T_Decimal T_Semicolon T_Id T_ROp_L T_Decimal T_Semicolon T_Id T_Assign T_Id T_AOp_PL T_Decimal T_RP T_LC '
                       'T_If T_LP T_Id T_AOp_RM T_Decimal T_ROp_E T_Decimal T_RP T_LC '
                       'T_Id T_Assign T_Id T_Semicolon '
                       'T_RC '
                       'T_Id T_Assign T_Id  T_AOp_PL T_Id T_Semicolon '
                       'T_RC')




function_test = ('T_Int T_Id T_LP T_Int T_Id T_Comma T_Bool T_Id T_Comma T_Char T_Id T_RP T_LC '
                       'T_Int T_Id T_Semicolon '
                       'T_If T_LP T_Id T_LOp_AND T_Id, T_ROp_E T_Character T_RP T_LC '
                       'T_Id T_Assign T_Id T_AOp_ML T_Decimal T_Semicolon '
                       'T_RC T_Else T_LC '
                       'T_Id T_Assign T_Id T_AOp_ML T_Decimal T_Semicolon '
                       'T_RC'
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
# sample set 8 (Multiple char symbols T & NT)
# rules = ["S -> NP VP",
#          "NP -> P | PN | D N",
#          "VP -> V NP",
#          "N -> championship | ball | toss",
#          "V -> is | want | won | played",
#          "P -> me | I | you",
#          "PN -> India | Australia | Steve | John",
#          "D -> the | a | an"]
#
# nonterm_userdef = ['S', 'NP', 'VP', 'N', 'V', 'P', 'PN', 'D']
# term_userdef = ["championship", "ball", "toss", "is", "want",
#                 "won", "played", "me", "I", "you", "India",
#                 "Australia","Steve", "John", "the", "a", "an"]
# sample_input_string = "India won the championship"

# diction - store rules inputted
# firsts - store computed firsts
diction = {}
firsts = {}
follows = {}

# computes all FIRSTs for all non terminals
computeAllFirsts()
# assuming first rule has start_symbol
# start symbol can be modified in below line of code
start_symbol = list(diction.keys())[0]
# computes all FOLLOWs for all occurrences
computeAllFollows()
# generate formatted first and follow table
# then generate parse table

(parsing_table, result, tabTerm) = createParseTable()

# validate string input using stack-buffer concept
if sample_input_string != None:
    validity = validateStringUsingStackBuffer(parsing_table, result,
                                              tabTerm, sample_input_string,
                                              term_userdef ,start_symbol)
    print(validity)
else:
    print("\nNo input String detected")

# Author: Tanmay P. Bisen

