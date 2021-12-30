
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 12:46:02 2021

@author: Sam
"""

import sys
import os
from os.path import exists
import random
import time
import signal
from automatons import Automaton
prt = lambda x: list(map(print,x))
class PDA:
    
    '''
    For clarity's sake D is the following:
    {current_state:{input_transition:{out_state:[{'push':stack_symbol,'pop':stack_symbol}...]}}}
    '''
    
    # 6 tuple for a pushdown automaton plus type
    # Q int for number of states from 0 to n
    # E list for input alphabet
    # R list for stack alphabet
    # D dict for state-transition table
    # q int for start state, but its always 0
    # F list for accept states
    # t string for type of pda: 'dpda'/'npda'
    def __init__(self, Q, E, R, D, q, F, t,):
        self.Q = Q
        self.E = E
        self.R = R
        self.D = D
        self.q = q
        self.F = F
        self._t = t
        self.stack = []
        signal.signal(signal.SIGINT, self.end)
        
    def __str__(self):
        s = "Amount of states in {}: {}\n\n".format(self._t, self.Q)\
            + "Input Alphabet: {}\n\n".format(self.E) \
            + "Stack Alphabet: {}\n\n".format(self.R)
        
        d = ""
        for i in range(self.Q):
            d += "Q{}: {}\n".format(i, str(self.D[i]))
        
        s += "Transition Table: \n{}\n".format(d) \
            + "Start State: {}\n\n".format(self.q) \
            + "Accept States: {}\n".format(self.F) 
        
        return s
    
    # w string as the word to check for membership to pda L(w)
    # p list of Q states taken in reverse order
    # t list of Σ* taken in reverse order
    # s stack of Γ* symbols taken in reverse order
    def run(self, w, p, t, s):
        c = p[0] # qi or current state state
        
        if p[0] in self.F and not s and not w: # quick check for membership
                return (True, p, t, s)
        
        
        if not w: # the word is empty
            if p[0] in self.F and not s and not w:
                return (True, p, t, s)
            
            
            if '' in self.D[c].keys(): # check current state for ε transitions
                # for each out state available in ε transitions
                # i is an int representing an out state
                for i in self.D[c][''].keys():
                    
                    # for each possible pop push scenario with ε transitions
                    for j in range(len(self.D[c][''][i])):
                        p0 = self.D[c][''][i][j]['pop']
                        p1 = self.D[c][''][i][j]['push']
                        
                        if p0: # if a pop could happen for jth instance of i
                            if s: # if the stack is not empty
                                if s[0] == p0: # try to pop
                                    new_p = p.copy()
                                    new_t = t.copy()
                                    new_s = s.copy()
                                    
                                    new_p.insert(0, i)
                                    new_t.insert(0, '')
                                    
                                    if p1: # if a push is also available
                                        new_s[0] = p1
                                    else: # guess not so just a pop
                                        new_s.pop(0)
                                    
                                    # recurse with modifications to p, t, s
                                    ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                                    
                                    if ra:
                                        return (ra, rp, rt, rs)
                        
                        elif not p0:
                            new_p = p.copy()
                            new_t = t.copy()
                            new_s = s.copy()
                                    
                            new_p.insert(0, i)
                            new_t.insert(0, '')
                            
                            if p1:
                                new_s.insert(0, p1)
                                
                            ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                            
                            if ra:
                                return (ra, rp, rt, rs)
                    
                    # if we got here, we just went through all outstates
                    # and all possible transitions
                    if i == list(self.D[c][''].keys())[-1]:
                        return (False, p, t, s)        
            
            # no input to parse and no ε transitions in current state - Dead End
            else:
                return (False, p, t, s)
        
        # there is input to parse
        else:
            z = w[0] # current char to parse
            k = self.D[c].keys() # transitions available in current state 
            
            if z in k and '' in k: # current char and ε transitions are available
                for i in self.D[c][z].keys(): # for each state with current char transitions
                    for j in range(len(self.D[c][z][i])): # Ambiguity if more than one state on same transition
                        p0 = self.D[c][z][i][j]['pop']
                        p1 = self.D[c][z][i][j]['push']
                    
                        if p0:
                            if s:
                                if s[0] == p0:
                                    new_p = p.copy()
                                    new_t = t.copy()
                                    new_s = s.copy()
                                    
                                    new_p.insert(0, i)
                                    new_t.insert(0, z)
                                    
                                    # if push 
                                    if p1:
                                        new_s[0] = p1
                                    else:
                                        new_s.pop(0)
                                        
                                    ra, rp, rt, rs = self.run(w[1:], new_p, new_t, new_s)
                                    
                                    if ra:
                                        return (ra, rp, rt, rs)
                                    
                        elif not p0:
                            new_p = p.copy()
                            new_t = t.copy()
                            new_s = s.copy()
                                    
                            new_p.insert(0, i)
                            new_t.insert(0, z)
                            
                            if p1:
                                new_s.insert(0, p1)
                                
                            ra, rp, rt, rs = self.run(w[1:], new_p, new_t, new_s)
                            
                            if ra:
                                return (ra, rp, rt, rs)
                                
                for i in self.D[c][''].keys():
                        # for each possible pop push scenario with ε transitions
                        for j in range(len(self.D[c][''][i])):
                            p0 = self.D[c][''][i][j]['pop']
                            p1 = self.D[c][''][i][j]['push']
                        
                            if p0:
                                if s:
                                    if s[0] == p0:
                                        new_p = p.copy()
                                        new_t = t.copy()
                                        new_s = s.copy()
                                        
                                        new_p.insert(0, i)
                                        new_t.insert(0, '')
                                        
                                        # if push 
                                        if p1:
                                            new_s[0] = p1
                                        else:
                                            new_s.pop(0)
                                            
                                        ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                                        
                                        if ra:
                                            return (ra, rp, rt, rs)
                                        
                                        # not accepted and it was the last pop push for the last state
                                        elif j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra:
                                            return (ra, rp, rt, rs)
                                        
                                # if this is the last pop push of the last state
                                # then return false
                                elif not s and j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra:
                                    return (False, p, t, s)
                                
                            elif not p0:
                                new_p = p.copy()
                                new_t = t.copy()
                                new_s = s.copy()
                                        
                                new_p.insert(0, i)
                                new_t.insert(0, '')
                                
                                if p1:
                                    new_s.insert(0, p1)
                                
                                ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                                
                                if ra:
                                    return (ra, rp, rt, rs)
                                
                                # not accepted and it was the last pop push for the last state
                                elif (j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra):
                                    return (ra, rp, rt, rs)
                                
                        if i == list(self.D[c][''].keys())[-1]:
                            return (False, p, t, s)        
            
            elif z in k and not '' in k:
                for i in self.D[c][z].keys():
                    
                    for j in range(len(self.D[c][z][i])):
                        p0 = self.D[c][z][i][j]['pop']
                        p1 = self.D[c][z][i][j]['push']
                    
                        if p0:
                            if s:
                                if s[0] == p0:
                                    new_p = p.copy()
                                    new_t = t.copy()
                                    new_s = s.copy()
                                    
                                    new_p.insert(0, i)
                                    new_t.insert(0, z)
                                    
                                    # if push 
                                    if p1:
                                        new_s[0] = p1
                                    else:
                                        new_s.pop(0)
                                    
                                    ra, rp, rt, rs = self.run(w[1:], new_p, new_t, new_s)
                                    
                                    if ra:
                                        return (ra, rp, rt, rs)
                        
                        elif not p0:
                            new_p = p.copy()
                            new_t = t.copy()
                            new_s = s.copy()
                                    
                            new_p.insert(0, i)
                            new_t.insert(0, z)
                            
                            if p1:
                                new_s.insert(0, p1)
                            
                            ra, rp, rt, rs = self.run(w[1:], new_p, new_t, new_s)
                            
                            if ra:
                                return (ra, rp, rt, rs)
                    
                    # if we got here, we just went through all outstates
                    # and all possible transitions
                    if i == list(self.D[c][z].keys())[-1]:
                        return (False, p, t, s)
                                
                            
                            
            else:
                if '' in self.D[c].keys():
                    # for each out state available in ε transitions
                    # i is an int representing an out state
                    for i in self.D[c][''].keys():
                        
                        # for each possible pop push scenario with ε transitions
                        for j in range(len(self.D[c][''][i])):
                            p0 = self.D[c][''][i][j]['pop']
                            p1 = self.D[c][''][i][j]['push']
                        
                            if p0:
                                if s:
                                    if s[0] == p0:
                                        new_p = p.copy()
                                        new_t = t.copy()
                                        new_s = s.copy()
                                        
                                        new_p.insert(0, i)
                                        new_t.insert(0, '')
                                        
                                        # if push 
                                        if p1:
                                            new_s[0] = p1
                                        else:
                                            new_s.pop(0)
                                        
                                        ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                                        
                                        if ra:
                                            return (ra, rp, rt, rs)
                                        
                                        # not accepted and it was the last pop push for the last state
                                        elif j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra:
                                            return (ra, rp, rt, rs)
                                        
                                        
                                # stack is empty and pop push is available
                                # if this is the last pop push of the last state
                                # then return false
                                elif not s and j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra:
                                    return (False, p, t, s)
                                            
                                        
                            
                            elif not p0:
                                new_p = p.copy()
                                new_t = t.copy()
                                new_s = s.copy()
                                        
                                new_p.insert(0, i)
                                new_t.insert(0, '')
                                
                                if p1:
                                    new_s.insert(0, p1)
                                
                                ra, rp, rt, rs = self.run(w, new_p, new_t, new_s)
                                
                                if ra:
                                    return (ra, rp, rt, rs)
                                
                                # not accepted and it was the last pop push for the last state
                                elif (j == len(self.D[c][''][i]) - 1 and i == list(self.D[c][''].keys())[-1] and not ra):
                                    return (ra, rp, rt, rs)
                                
                        if i == list(self.D[c][''].keys())[-1]:
                            return (False, p, t, s)        
                else:
                    return (False, p, t, s)
            
    def end(self, signum, f):
        try:
            print("\nUser has hit Ctrl + C to exit!")
            sys.exit(0)
        except Exception as e:
            print(e)
        
        
      
class pda_sim:
    def __init__(self, f):
        self.pda = None
        self.pda = self.read_pda(f)
        print(self.pda)
        
        
    def main(self):
        if __name__ == '__main__':
            if self.pda == None:
                raise TypeError(self.pda, '"self.pda" is not valid')
            else:
                
                word = None
                end = False
    
                while not end:
                    #path always starts at start state state
                    path = [self.pda.q]
                    word = input("Please input a word: ")
    
                    a, p, t, s = self.pda.run(word, path, [], [])
    
                    path = p[::-1]
                    trans = t[::-1]
                    stack = s[::-1]
                    
                    # prt([path,trans,stack])
    
                    if a:
                        print("String Accepted. Path:")
    
    
                    else:
                        print("String Rejected. Path:")
                        
                    for i in range(len(path)):
                        if i != len(path)-1:
                            print("Q{}".format(path[i]),end=' ')
                        else:
                            print("Q{}".format(path[i]),end='\n')
                    
                    print("\nTransitions taken:")
                    for i in range(len(trans)):
                        if i != len(trans)-1:
                            print("{}".format(trans[i]),end=' ')
                        else:
                            print("{}".format(trans[i]),end='\n')
                    
                    print("\nStack:")
                    for i in range(len(stack)):
                        if i != len(stack)-1:
                            print("{}".format(stack[i]),end=' ')
                        else:
                            print("{}".format(stack[i]),end='\n')
                    
        
    
    def read_pda(self, file):
        Q = 0
        E = []
        R = []
        D = {}
        q = 0
        F = []
        t = 'DPDA'
        automaton_t = 'DFA'
        raw = []
        
        all_states = {}
        
        with open(file, 'r') as f:
            for l in f:
                raw.append(l)
            f.close()
            
        
        '''
        HEADER FORMAT for a pda file
        
        HEADER BEGIN
        1. pda type ('dpda' or 'npda')
        2. input alphabet
        3. stack alphabet
        4. amount of states
        5. accept states
        6. '---' 
        HEADER END
        '''
        
        # Extracting Header
        
        # get pda type
        t = raw.pop(0).split()[0]
        
        if t != 'DPDA' and t != 'PDA':
            raise ValueError(t, "Wrong file PDA type")
        
        
        # get input alphabet
        E = raw.pop(0).split()
        if '\n' in E:
            E = E[:E.index('\n')]
        
        # get stack alphabet
        R = raw.pop(0).split()
        if '\n' in R:
            R = R[:R.index('\n')]
        
        # get amount of states
        Q = raw.pop(0).split()[0]
        
        # check if Q is a number
        if not Q.isdigit():
            raise TypeError(Q, 'Number of states is not a number')
            
        # Q is a number. is it valid?
        if int(Q) <= 0:
            raise ValueError(Q, 'Number of states specified is zero or less')
            
        # it is! cast it to int
        Q = int(Q)
        
        # get accept states
        accept_states = raw.pop(0).split()
        
        # check if each accept state is prefixed with 'Q' followed by a valid number
        for i in accept_states:
            # check if string is at least 2 chars
            if len(i) < 2:
                raise ValueError(i, 'Accept state is not valid')
            
            # check if first index is 'Q'
            if i[0] != 'Q':
                raise ValueError(i[0], 'State not prefixed with Q')
            
            # good. Now check if the following chars is an int
            if not i[1:].isdigit():
                raise ValueError(i[1:], 'State number is not valid')
                
            # yay! now cast to int to see if state is between [0, Q)
            a = int(i[1:])
            
            if a < 0 or a >= Q:
                raise ValueError(a, 'State not in range of available states')
                
            # it must be between [0, Q), so add it to F
            F.append(a)
        
        # header extracted, if the next line is not '---'
        # then there must be an file alignment issue
        
        header_break = raw.pop(0).split()[0]
        
        if header_break != '---':
            raise RuntimeError(header_break,'6th line in file should be "---"')
        
        
        # set up transition table
        pda_S = {i:{} for i in range(Q)}
        allS = {i:[] for i in range(Q)}
        
        pda_D = {i:{} for i in range(Q)}
        D = {i:{} for i in range(Q)}
        # Now to extract the rules
        for i in range(len(raw)):
            rule = raw.pop(0).split(' ')
            qi = w = s = qj = p = ''
            
            #print(rule)
            
            # get current state 
            qi = rule.pop(0)
            if qi[0] != 'Q':
                raise TypeError(qi[0], 'State not prefixed with Q')
                
            # good. Now check if state number is a number
            if not qi[1:].isdigit():
                raise ValueError(qi[1:], 'State number is not valid')
                
            # Excellent! I cast magic massile. ahem i mean int()
            qi = int(qi[1:])
            
            # so far so good. Now check if to see if state is between [0, Q)
            if qi < 0 or qi >= Q:
                raise ValueError(qi, "State not in range of available states")
                
            # input symbol could be nil
            w = rule.pop(0)
            
            # it is! it is. pop tha next sucka
            if w == '':
                rule.pop(0)
             
            # stack symbol could be nil
            s = rule.pop(0)
            
            # that junk be nil. you know the drill
            if s == '':
                rule.pop(0)
                
            # get the next state. There has to be one!
            qj = rule.pop(0)
            
            # but is it right. hacha Ctrl + C & Ctrl + V
            if qj[0] != 'Q':
                raise TypeError(qj[0], 'State not prefixed with Q')
                
            # good. Now check if state number is a number
            if not qj[1:].isdigit():
                raise ValueError(qj[1:], 'State number is not valid')
                
            # Excellent! I cast magic massile. ahem i mean int()
            qj = int(qj[1:])
            
            # so far so good. Now check if to see if state is between [0, Q)
            if qj < 0 or qj >= Q:
                raise ValueError(qj, "State not in range of available states")
                
            # stack push symbol could be nil
            p = rule.pop(0)
            
            # it is nil
            if p == '':
                rule.pop(0)
            
            # it is not nil, extract stack push symbol from '\n'
            else:
                p = p[0]
    
            # Thunder! Thunder! Thunder! Thundercats HooooH!
            
            if w not in pda_S[qi].keys():
                pda_S[qi][w] = {qj:[{'pop':s,'push':p}]}
            else:
                
                if qj not in pda_S[qi][w].keys():
                    pda_S[qi][w][qj] = [{'pop':s,'push':p}]
                    
                else:
                    pda_S[qi][w][qj].append({'pop':s,'push':p})
            
        
        return PDA(Q, E, R, pda_S, 0, F, t)
        #print(Q, E, R, D, q, F, t, sep='\n')
            
        
if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            print("No Input File Found")

        else:
            print("Looking for {}".format(sys.argv[1]))
            if exists(sys.argv[1]):
                print("{} Found!".format(sys.argv[1]))
                mainloop = pda_sim((sys.argv[1]))
                mainloop.main()
            else:
                print("{} does not exist!".format(sys.argv[1]))

    except Exception as e:
        print("Found {}. {}.".format(e.args[0], e.args[1]))