from Automata import Automata
from NFA import NFA
from graphviz import Digraph

class DFA(Automata):
    def __init__(self, Q, Sigma, delta, q0, F):
        delta_dict = dict()
        for transition in delta: # nested list ex: [[qstart, letter, qend], […, …, …]]
            delta_dict[(transition[0], transition[1])] = transition[2]

        super().__init__(Q, Sigma, delta_dict, q0, F)

    def print_info(self):
        print("States (Q):")
        for state in self.Q:
            print("  -", state)
        
        print("\nStart state (q0): ",self.q0)

        print("\nInput Alphabet (Sigma):")
        for symbol in self.Sigma:
            print("  -", symbol)
        
        print("\nTransition Function (delta):")
        for transition, next_state in self.delta.items():
            current_state, input_symbol = transition
            print("  -", current_state, " --", input_symbol, "-->", next_state)

        print("\nStart State (q0):")
        print("  -", self.q0)

        print("\nFinal States (F):")
        for final_state in self.F:
            print("  -", final_state)
    
    def diagram(self):
        dot = Digraph()
        dot.graph_attr['rankdir'] = 'LR'

        dot.node('start', shape='plaintext', label='')

        for state in self.Q:
            if state in self.F:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        dot.edge('start', self.q0)

        for transition, next_state in self.delta.items():
            current_state, input_symbol = transition
            dot.edge(current_state, next_state, label=input_symbol)

        return dot
    
    def process_word(self,word): #word has to be string
        curr_state = self.q0
        for l in word:
            curr_state = self.delta[(curr_state,l)]
            #print(f"DFA read {l} and is now at {curr_state}")
        if curr_state in self.F:
            return True
        else:
            return False
    
    def to_nfa(self):
        Q = self.Q
        Sigma = self.Sigma
        delta = [[k[0], k[1], [v]] for k, v in self.delta.items()]
        q0 = self.q0
        F = self.F
        return NFA(Q, Sigma, delta, q0, F)

    def union(self, dfa2):
        nfa1 = self.to_nfa()
        nfa2 = dfa2.to_nfa()

        new_start_state = 'q_new_start'

        new_delta = [transition for transition in nfa1.delta.items()] + [transition for transition in nfa2.delta.items()] + [((new_start_state, ''), {nfa1.q0, nfa2.q0})]

        new_delta_formatted = []
        for t in new_delta:
            current_state, input_symbol = t[0]
            next_states = list(t[1])
            new_delta_formatted.append([current_state, input_symbol, next_states])

        new_Q = nfa1.Q + nfa2.Q + [new_start_state]
        new_Sigma = list(set(nfa1.Sigma) | set(nfa2.Sigma))
        new_F = nfa1.F + nfa2.F

        return NFA(new_Q, new_Sigma, new_delta_formatted, new_start_state, new_F)

    def intersection(self, dfa2):
        nfa1 = self.to_nfa()
        nfa2 = dfa2.to_nfa()

        # Perform the intersection of the two NFAs
        intersection_nfa = nfa1.intersection(nfa2)

        return intersection_nfa
    
    def concatenation(self, dfa2):
        nfa1 = self.to_nfa()
        nfa2 = dfa2.to_nfa()

        # Perform the concatenation of the two NFAs
        concatenation_nfa = nfa1.concatenation(nfa2)
        
        return concatenation_nfa
    
    def kleene_star(self):
        nfa = self.to_nfa()
        return nfa.kleene_star()
    





    
    
    
