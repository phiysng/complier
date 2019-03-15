# -*-coding=utf-8 -*-

'''
递归下降子程序

固定parser

终结符 ( ) i + *
'''


class ArithParser:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.i = 0
        self.is_valid = True
        self.token = self.get_token()

    def is_legal(self) -> bool:
        self.E()
        return self.is_valid

    def error(self):
        self.is_valid = False
        return

    def get_token(self):
        if self.i < len(self.symbol):
            idx = self.i
            self.i = self.i + 1
            return self.symbol[idx]
        return None

    def match(self, t):
        if self.token == t:
            self.token = self.get_token()
        else:
            self.error()

    def F(self):
        # F->(E)|i
        if (self.token == 'i'):
            self.match('i')
        elif self.token == '(':
            self.match('(')
            self.E()
            self.match(')')
        else:
            self.error()

    def E(self):
        self.T()
        self.E1()

    def T1(self):
        if self.token == '*':
            self.match('*')
            self.F()
            self.T1()
        else:
            pass

    def T(self):
        self.F()
        self.T1()

    def E1(self):
        if self.token == '+':
            self.match('+')
            self.T()
            self.E1()
        else:
            pass


if __name__ == '__main__':
    arith = ArithParser('i+(i*i)')
    print(arith.is_legal())
    arith = ArithParser('(i+(i+(i*i)+i))')
    print(arith.is_legal())

    arith = ArithParser('i+(i*i)+(i+i)*i')
    print(arith.is_legal())
    # 不合法输入
    arith = ArithParser('+i+(i*i)')
    print(arith.is_legal())
    arith = ArithParser('(i+(i+(i*i)+i)')
    print(arith.is_legal())
