# -*- coding: utf-8 -*-

from collections import deque
from queue import Queue

"""

需要一个计算闭包的函数
DFA需要能够添加键值对/状态点


q0<-closure(n0)  #q0是一个状态 是等价的开始点
Q<-{q0}
work_list <-q0
while worklist !=[]:
    q <- pop worklist
    for_each c in  alphabet:    #获得所有新的状态
        t <- closure(get_status(q,c) #获得一个新的状态
        D[q,c]<-t   #将新的状态和其键值对添加到DFA中
        if t not in Q:
            add t to Q and worklist  #如果这是一个新的状态的话添加到新的确定状态机中
"""


class DFA:
    def __init__(self, state_automaton: dict, alphabet: set, start_status: set, terminal_status: set):
        self.state_automaton = state_automaton
        self.start_status = start_status
        # if (len(self.start_status) != 1):
        #     print("start_status should be ")
        self.terminal_status = terminal_status
        self.alphabet = alphabet

    # def closure(self,status):


class NFA:
    def __init__(self, state_automaton: dict, alphabet: set, start_status: set, terminal_status: set):
        self.state_automaton = state_automaton
        self.start_status = start_status
        # if (len(self.start_status) != 1):
        #     print("start_status should be ")
        self.terminal_status = terminal_status
        self.alphabet = alphabet
    # def closure(self,status):


# def transform(dfa:DFA,nfa:NFA):
#     q0

'''
TODO not implemented 
'''


def work_list(nfa: NFA, start_status: str) -> DFA:
    # dfa = DFA()  # type:DFA
    nfa_automation = nfa.state_automaton
    q0 = epsilon_closure(nfa_automation, start_status)
    Q = set(q0)  # type:set
    dfa_states = set()  # type:set

    dfa_alphabet = nfa.alphabet  # type:set
    dfa_transitions = {}
    # equivalent DFA states states
    nfa_initial_states = epsilon_closure(nfa_automation, start_status)  # type:set
    print('nfa_initial_states {}'.format(type(nfa_initial_states)))
    # 将初始的NFA闭包转换为DFA的开始点

    dfa_final_states = set()  # type:set
    status_list = Queue()  # type:Queue
    status_list.put(nfa_initial_states)
    while not status_list.empty():
        curr_status = status_list.get()  # type:set

        print("当前的状态")
        print(curr_status)

        # current_state_name = _stringify_states(curr_status)#type:str
        tmpset = set()
        for one_input in dfa_alphabet:
            # 用于存储一个原状态一种输入下的转移出的状态
            tmpset = set()  # type:set
            for one_status in curr_status:
                if one_input in nfa_automation[one_status]:
                    t = nfa_automation[one_status][one_input]
                    # if (len(t) >= 2):
                    for item in t:
                        for one_epsilon in epsilon_closure(dfa_transitions, item):
                            tmpset.add(one_epsilon)
                        tmpset.add(item)

            frozentmpset = frozenset(tmpset)
            if frozenset(curr_status) not in dfa_transitions:
                dfa_transitions[frozenset(curr_status)] = dict()
            dfa_transitions[frozenset(curr_status)][one_input] = frozentmpset
            '''TODO:终结状态与初始状态'''
            if frozentmpset not in dfa_states:
                dfa_states.add(frozentmpset)
                status_list.put(tmpset)
    print(dfa_states)
    print('-' * 10)
    print(dfa_transitions)
    # nfa.terminal_status
    for one_status in dfa_states:
        if one_status & nfa.terminal_status:
            dfa_final_states.add(one_status)
    print(dfa_final_states)
    dfa = DFA(alphabet=dfa_alphabet, start_status=nfa_initial_states, state_automaton=dfa_transitions,
              terminal_status=dfa_final_states)
    print(dfa.alphabet)
    return dfa

'''
Moore DFA最小化
将DFA划分为接收状态与非接受状态
`|` 运算
while set is still changing :
    for s in set:
        split(s)
    

def split():
    for i in alphabet:
        if i can split s:
            split s => T1,T2,...Tk

            
'''

def minimize(dfa: DFA) -> DFA:
    pass


def epsilon_closure(nfa: dict, start_status: str) -> set:
    queue = deque(start_status)  # type:deque
    closure = set()  # type:set
    while queue:
        state = queue.popleft()  # type:str
        if state not in closure:
            closure.add(state)
            if state in nfa:
                if 'ε' in nfa[str(state)]:
                    for t in nfa[str(state)]['ε']:
                        queue.append(t)
    return closure


if __name__ == '__main__':
    pass
    delta = {'A': {'0': {'C', 'B'}, '1': {'A'}, 'ε': {'B'}}, 'B': {'1': {'B'}, 'ε': {'C'}},
             'C': {'0': 'C', '1': 'C'}}  # type:dict
    nfa = NFA(state_automaton=delta, start_status={'A'}, terminal_status={'C'}, alphabet={'0', '1'}, )
    work_list(nfa=nfa, start_status='A')
