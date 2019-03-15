# -*- coding: utf-8 -*-


# 将给定程序代码打上token
from _pytest import deprecated

example_code = '''
；
int main(void)
{
    __user asmimage 12_32;
    int a = 010;
    char c = 'x';
    str s = "As you are";
    for(int i = 0 ;i <= 0x10; ++i)
    {
        void *m = i % 11;
        continue;
    }
    return 0;

}

'''

'''
-1  key not exist

'''


# print(example_code)
def parse_space(x):
    if x == '\t' or x == ' ' or x == '\n':
        return True
    return False


def parse_seperator(x):
    seperator_dict = {
        ',': 'comma',
        ':': 'colon',
        ';': 'simcon',
        '(': 'lparen',
        ')': 'rparen',
        '{': 'lbrac',
        '}': 'rbrac'
    }
    print("< '{}'\t:\t'{}'\t >".format(seperator_dict.get(x, -1), x))


def parse_operator(x):
    operator_dict = {
        '++': 'inc',
        '--': 'dec',
        '+': 'add',
        '-': 'minus',
        '*': 'mul',
        '/': 'div',
        '%': 'mod',
        '<=': 'le',
        '<': 'lt',
        '>=': 'ge',
        '>': 'gt',
        '==': 'eq',
        '=': 'assign',
        '!': 'not',
        '!=': 'nequ',
        '&&': 'and',
        '||': 'or'
    }
    if operator_dict.get(x, -1) != -1:
        print("< '{}'\t:\t'{}'\t >".format(operator_dict.get(x, -1), x))
    else:
        return -1
    return 0


def parse_keyword(x):
    key_word_dict = {
        'int': 'kw_int',
        'char': 'kw_char',
        'void': 'kw_void',
        'if': 'kw_if',
        'else': 'kw_else',
        'switch': 'kw_switch',
        'case': 'kw_case',
        'default': 'kw_default',
        'while': 'kw_while',
        'do': 'kw_do',
        'for': 'kw_for',
        'break': 'kw_break',
        'continue': 'kw_continue',
        'return': 'kw_return'

    }
    if key_word_dict.get(x, -1) != -1:
        print("< '{}'\t:\t'{}'\t >".format(key_word_dict.get(x, -1), x))
    else:
        return -1
    return 0


# @deprecated
# def parse_literal(nu):
#     pass
#
#
# @deprecated
# def parse_id(id):
#     pass


def lex_parser(input_str):
    # for i in range(len(input_str)):
    i = 0
    str_len = len(input_str)
    # 主循环
    while i < str_len:
        if parse_space(input_str[i]):
            i = i + 1
            continue
        if input_str[i] in [',', ':', ';', '{', '}', '(', ')']:
            parse_seperator(input_str[i])
            i = i + 1
            continue
        # operator
        if input_str[i] in ['*', '/', '%']:
            parse_operator(input_str[i])
            i = i + 1
            continue
        if input_str[i] in ['<', '>', '=', '!', '+', '-', '&', '|']:
            if parse_operator(input_str[i:i + 2]) != -1:

                i = i + 2
            else:
                parse_operator(input_str[i:i + 1])
                i = i + 1
            continue
        # char
        if input_str[i] == "'":
            assert input_str[i + 2] == "'"
            print("< '{}'\t:\t'{}'\t >".format('char', input_str[i + 1]))
            i = i + 3
            continue
            # str
        if input_str[i] == '"':
            locate = i + 1

            while input_str[locate] != '"':
                locate = locate + 1

            print("< '{}'\t:\t'{}'\t >".format('str', input_str[i + 1:locate]))
            i = locate + 1
            continue
        # 数字
        if '1' <= input_str[i] <= '9':
            locate = i + 1
            while '9' >= input_str[locate] >= '0':
                locate = locate + 1
            print("< '{}'\t:\t'{}'\t >".format('num_literal', input_str[i: locate]))
            i = locate
            continue

        if input_str[i] == '0':
            # oct / hex
            if input_str[i + 1] == 'x' or input_str[i + 1] == 'X':
                locate = i + 2
                while '9' >= input_str[locate] >= '0':
                    locate = locate + 1
                print("< '{}'\t:\t'{}'\t >".format('num_literal', input_str[i: locate]))
                i = locate
            else:
                locate = i + 1
                while '9' >= input_str[locate] >= '0':
                    locate = locate + 1
                print("< '{}'\t:\t'{}'\t >".format('num_literal', input_str[i: locate]))
                i = locate
            continue
        if 'z' >= input_str[i] >= 'a' or 'Z' >= input_str[i] >= 'A' or input_str[i] == '_':
            locate = i + 1
            while ('a' <= input_str[locate] <= 'z' or 'A' <= input_str[locate] <= 'Z' '0' <= input_str[
                locate] <= '9' or input_str[locate] == '_'):
                locate = locate + 1
            lex_str = input_str[i: locate]
            if parse_keyword(lex_str) != 0:
                print("< '{}'\t:\t'{}'\t >".format('var', input_str[i: locate]))
            i = locate
            continue
        print("error in lex")
        i = i + 1


if __name__ == '__main__':
    lex_parser(example_code)
