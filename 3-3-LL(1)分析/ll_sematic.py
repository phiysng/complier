# -*- coding=utf-8 -*-

'''
LL1语法分析

'''
from typing import Optional, Dict, Tuple, Any


def get_first(target, grammar):
    '''
    返回
    :param target: 右部 如 A->Bc 种的 Bc
    :param grammar: 语法规则
    :return: first集
    '''
    c = target[0]
    one_first = set()  # one_first:set
    if c.isupper():
        # 非终结符
        for st in grammar[c]:
            if st == '#':
                # 可以推出空且空后面还有符号的情况
                if len(target) != 1:
                    # 递归求解
                    one_first = one_first.union(get_first(target[1:], grammar))
                else:  # A->#
                    one_first = one_first.union('#')
            else:
                # 非终结符递归调用
                recursive_first = get_first(st, grammar)
                one_first = one_first.union(x for x in recursive_first)
    else:
        # 终结符
        one_first = one_first.union(c)
    return one_first


def get_ll1_table(follow, grammar: dict) -> Optional[Dict[Tuple[Any, Any], Any]]:
    M = {}  # 语法分析表
    for left_part in grammar:
        for each_right in grammar[left_part]:
            if each_right != '#':
                # 对于First(a)中的每个终结符号 将推导式的右部加入table[A,a]
                for i in get_first(each_right, grammar):
                    if (left_part, i) in M:
                        print("No LL1 Grammar")
                        return None
                    M[left_part, i] = each_right

            else:
                # #的时候 Follow集
                for i in follow[left_part]:
                    if (left_part, i) in M:
                        print("Not a Legal Grammar")
                        return None
                    M[left_part, i] = each_right
    return M


def process(user_input, start_symbol, parsingTable):
    flag = 0

    # 把$加到输入串的最后
    user_input = user_input + "$"

    stack = ["$", start_symbol]

    index = 0
    print("开始")
    while len(stack) > 0:  # 栈不为空的时候

        top = stack[len(stack) - 1]  # 获得栈顶元素

        current_input = user_input[index]

        if top == current_input:  # 栈顶的元素与待输入的相等 则弹出 输入也被读掉
            stack.pop()
            index = index + 1
        else:

            #  不能读掉的时候就需要看LL1转换表
            key = top, current_input
            # print(key)

            # 如果转换表没有栈顶元素与 最新的输入元素对应的转换 就出错了
            if key not in parsingTable:
                flag = 1
                break

            value = parsingTable[key]
            if value != '#':
                '''
                # 逆置字符串 将value压入栈中 因为需要最左推导 所以最左边的符号要在栈顶 也就是 value需要逆序
                如 (A)在 栈中排布
                (
                A
                )
                xxx
                $
                '''
                value = value[::-1]
                value = list(value)

                # 弹掉原本的栈顶 并压入新的产生式右部
                stack.pop()

                # 将获得的产生式压栈
                for element in value:
                    stack.append(element)
            else:
                stack.pop()
        print(stack[::-1])

    if flag == 0:
        print("Legal!")
    else:
        print("Illegal!")


def all_follow(S: str, Non_terminal: set, grammar):
    follow_set = dict()
    for i in Non_terminal:
        follow_set[i] = set()

    follow_now = dict(follow_set)
    print(follow_now)
    follow_now[S] = follow_now[S].union('$')  # 开始符号

    print(follow_set)
    print(follow_now)

    while follow_set != follow_now:
        print("循环开始时")
        print(follow_set)
        print(follow_now)
        print('------')
        follow_set = dict(follow_now)
        for i in Non_terminal:
            follow_now = get_follow_set_of_one_nonterminal(S, i, grammar, Non_terminal, follow_now)
            print(follow_now)
    print(follow_now)
    return follow_now


def get_follow_set_of_one_nonterminal(S: str, B: str, grammar: dict, Non_terminal: set, follow_set: dict):
    '''
    dict 键为 str且(len(str) == 1    值为 set set内为str
    '''
    for left_part in grammar:
        for each_right in grammar[left_part]:  # each_right:str
            index = each_right.find(B)
            if index != -1:  # 看这个表达式右部是否存在A
                if index == (len(each_right) - 1):  # 在最右边 A->aB
                    follow_set[B] = follow_set[B].union(follow_set[left_part])

                else:  # 存在但是不在最右边
                    # follow集右边串的first集
                    first_after_follow = get_first(each_right[index + 1], grammar)
                    if '#' in first_after_follow:  # A->aBβ
                        follow_set[B] = follow_set[B].union(follow_set[left_part])
                    follow_set[B] = follow_set[B].union(first_after_follow) - {'#'}
    return follow_set


def get_grammar() -> dict:
    file = "./sample.txt"
    grammer = dict()
    with open(file, encoding='utf-8', mode='r') as fd:
        for line in fd.readlines():
            print(line.replace('\n', ''))
            l, r = line.replace('\n', '').split('::')
            print(l, r)
            if l not in grammer:
                grammer[l] = set()

            grammer[l].add(r)

    print(grammer)
    return grammer


if __name__ == '__main__':
    # 测试一
    grammar = get_grammar()
    # grammar = {'S': {'a', '^', '(T)'}, 'T': {'SM'}, 'M': {',SM', '#'}}
    first_set = dict()
    for i in grammar:
        first_set[i] = get_first(i, grammar)
    print("First集")
    print(first_set)
    print("First集结束")
    S = 'S'
    follow_set = all_follow(S, {'S', 'T', 'M'}, grammar)
    print(len(get_ll1_table(follow_set, grammar)))
    M = get_ll1_table(follow_set, grammar)
    print(get_ll1_table(follow_set, grammar))
    process('(a,a)', S, M)
    print("*" * 10)
    process('(a,a))', S, M)

    # 测试二
    # grammar = {'A': {'a=E;'}, 'E': {'FT'}, 'F': {'a', 'r', '(E)'}, 'P': {'bSe'}, 'S': {'AR'},
    #            'R': {'#', 'AR'}, 'T': {'#', '+FT'}}
    grammar = {'D':{'TV'},'T':{'i','f'},'V':{'cW'},'W':{',V','#'}}
    first_set = dict()
    for i in grammar:
        first_set[i] = get_first(i, grammar)
    print(first_set)
    S = 'D'
    follow_set = all_follow(S, {'D','T','V','W'}, grammar)
    print(len(get_ll1_table(follow_set, grammar)))
    M = get_ll1_table(follow_set, grammar)
    print(get_ll1_table(follow_set, grammar))
    # parse('a*(a+a)', S, M)
    process('ic,c,c', S, M)
    process('icc', S, M)
