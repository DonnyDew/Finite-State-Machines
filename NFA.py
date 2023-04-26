from Automata import Automata
import importlib
from graphviz import Digraph

class NFA(Automata):
    def __init__(self, Q, Sigma, delta, q0, F):
        delta_dict = dict() #ex: [['q0','a',['q0','q1']],[...]]
        for transition in delta:
            current_state = transition[0]
            input_symbol = transition[1]
            next_states = transition[2]
            if (current_state, input_symbol) not in delta_dict:
                delta_dict[(current_state, input_symbol)] = set()
            for next_state in next_states:
                delta_dict[(current_state, input_symbol)].add(next_state)

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
        for transition, next_states in self.delta.items():
            current_state, input_symbol = transition
            if input_symbol == '':
                input_symbol = '\u03B5'
            print("  -", current_state, " --", input_symbol, "-->", ", ".join(next_states))

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

        for transition, next_states in self.delta.items():
            current_state, input_symbol = transition
            if input_symbol == '':
                input_symbol = 'ε'
            for next_state in next_states:
                dot.edge(current_state, next_state, label=input_symbol)

        return dot
    
    # Helper function to find states that can be reached by following only an epsilon
    def epsilon_closure(self, state_set):
        closure = set(state_set)
        stack = list(state_set)

        while stack:
            state = stack.pop()
            if (state, '') in self.delta:
                for next_state in self.delta[(state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure
    
    def reachable_states(self, current_state, input_symbol=None):
        #Helper function for process_word that returns the possible states given a current state and letter
        #This is a micro view of a DFA
        
        # Compute the epsilon closure of the current state
        reachable = self.epsilon_closure({current_state}) # Add the reachable states by following 0 or more epsilons
        
        # If input_symbol is provided, find the reachable states using that symbol 
        if input_symbol is not None:
            symbol_reachable = set()
            for state in reachable:
                if (state, input_symbol) in self.delta:
                    for next_state in self.delta[(state, input_symbol)]:
                        symbol_reachable.add(next_state)
            
            final_reachable = set()
            for state in symbol_reachable:
                if (state, '') in self.delta: # handles case for when there is an input then an epsilon
                    for next_state in self.delta[(state, '')]: 
                        final_reachable |= self.reachable_states(next_state)
                final_reachable.add(state)
            return final_reachable #return when letter specified

        return reachable #returns for when no letter (intialized part)

    def process_word(self, word):
        #Run through NFA to determine if the word is in the lanugage
        current_states = set([self.q0])  # current states are self.qo and where an epislon can take q0
        for letter in word:
            next_states = set()
            for state in current_states: #Multiple universes
                next_states |= self.reachable_states(state, letter)
            current_states = next_states

        #Current states represents all the possible final states at this point
        for state in current_states:
            if state in self.F:
                return True

        return False
    
    def to_dfa(self):
    # Steps taken from geeksforgeeks site https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/

        # Step 1: Create the DFA's start state
        q0_dfa = frozenset(self.epsilon_closure({self.q0})) #can't be modifed
        
        # Step 2: Create the DFA's transition table
        Q_dfa = [q0_dfa] #Sets of states like {q0,q1} , {q2,q3}, {q1,q2,q3}
        delta_dfa = []

        i = 0
        while i < len(Q_dfa):
            current_state_set = Q_dfa[i]
            for symbol in self.Sigma:
                next_state_set = set()
                for state in current_state_set:
                    if (state, symbol) in self.delta:
                        next_state_set |= self.delta[(state, symbol)]
                
                # Compute the epsilon closure of the set of next states
                next_state_set = frozenset(self.epsilon_closure(next_state_set))

                if next_state_set not in Q_dfa:
                    Q_dfa.append(next_state_set)

                delta_dfa.append([current_state_set, symbol, next_state_set])
            i += 1

        # Step 3: Create the DFA's final states
        # Each set of states that has at least one final state becomes a final state
        F_dfa = [state_set for state_set in Q_dfa if any(q in self.F for q in state_set)]
        
        # Rename states
        state_map = {}
        for i, q in enumerate(Q_dfa):
            state_map[q] = f'q{i}'  # use simple name

        Q_dfa_renamed = [state_map[q] for q in Q_dfa]
        q0_dfa_renamed = state_map[q0_dfa]

        delta_dfa_renamed = []
        for transition in delta_dfa:
            q_from = state_map[transition[0]]
            symbol = transition[1]
            q_to = state_map[transition[2]]
            delta_dfa_renamed.append([q_from, symbol, q_to])

        F_dfa_renamed = [state_map[q] for q in F_dfa]
        
        DFA = importlib.import_module("DFA").DFA #workaround to avoid circular import
        #return the DFA
        return DFA(Q_dfa_renamed, self.Sigma, delta_dfa_renamed, q0_dfa_renamed, F_dfa_renamed)
    

    def union(self, nfa2):
        # Step 1: Create a new start state
        new_start_state = 'q_new_start'

        # Step 2: Connect the new start state to the start states of both input NFA's using epsilon transitions
        new_delta = [transition for transition in self.delta.items()] + [transition for transition in nfa2.delta.items()]
        new_delta.append([(new_start_state, ''), {self.q0}])
        new_delta.append([(new_start_state, ''), {nfa2.q0}])

        # Convert new_delta to the original format
        new_delta_formatted = []
        for transition in new_delta:
            current_state, input_symbol = transition[0]
            next_states = transition[1]
            new_delta_formatted.append([current_state, input_symbol, list(next_states)])

        # Step 3: Combine the state sets, input alphabets,and final state sets of the input NFA's
        new_Q = self.Q + nfa2.Q + [new_start_state]
        new_Sigma = list(set(self.Sigma) | set(nfa2.Sigma))
        new_F = self.F + nfa2.F

        # Step 4: Create a new NFA using the combined data
        return NFA(new_Q, new_Sigma, new_delta_formatted, new_start_state, new_F)
  
    
    def intersection(self, nfa2):
        Q1, Q2 = self.Q, nfa2.Q
        Sigma1, Sigma2 = self.Sigma, nfa2.Sigma
        q0_1, q0_2 = self.q0, nfa2.q0
        F1, F2 = self.F, nfa2.F
        
        #Reachable from start means any number of epsilon transitions and 1 non epsilon from start
        def reachable_states_from_start(nfa, start_state): #This function is to cut down on states
            reachable = set()
            # Create a stack to hold the states that need to be checked for reachability
            stack = [start_state]

            while stack:
                state = stack.pop()
                if state not in reachable:
                    reachable.add(state)
                    for symbol in nfa.Sigma:
                        # Get the set of states that can be reached from the current state on the current symbol
                        next_states = nfa.reachable_states(state, symbol)
                        # Add the next states to the stack to be checked for reachability
                        stack.extend(next_states)

            return reachable
        
        reachable1 = reachable_states_from_start(self, q0_1)
        reachable2 = reachable_states_from_start(nfa2, q0_2)
        
        # Create the new NFA's states by taking the Cartesian product of Q1 and Q2
        Q_new = [f"{q1}_{q2}" for q1 in reachable1 for q2 in reachable2] 

        # Start state of the new NFA is the pair of start states from the input NFAs
        q0_new = f"{q0_1}_{q0_2}"  

        # Accept states are pairs where both states are accept states in their respective NFAs
        F_new = [f"{q1}_{q2}" for q1 in F1 for q2 in F2 if f"{q1}_{q2}" in Q_new]  

        # Transitions of the new NFA are pairs of transitions from the input NFAs for each symbol
        delta_new = []
        for q1_q2_str in Q_new:
            q1, q2 = q1_q2_str.split('_')  # Add this line to split the state names
            for symbol in Sigma1:
                if symbol in Sigma2:
                    next_states1 = self.reachable_states(q1, symbol)
                    next_states2 = nfa2.reachable_states(q2, symbol)
                    next_states_new = [f"{next_q1}_{next_q2}" for next_q1 in next_states1 for next_q2 in next_states2]  
                    if next_states_new:
                        delta_new.append([q1_q2_str, symbol, next_states_new])  

        # Combine the alphabets of the input NFAs
        Sigma_new = list(set(Sigma1).union(Sigma2))

        # Create the new NFA using the generated components
        intersection_nfa = NFA(Q_new, Sigma_new, delta_new, q0_new, F_new)

        # If there are no final states in the intersection NFA, return None
        if not F_new:
            return None

        # Check if the start state can reach any final state
        reachable_from_start = reachable_states_from_start(intersection_nfa, q0_new)
        if not any(final_state in reachable_from_start for final_state in F_new):
            return None

        return intersection_nfa
    
    def concatenation(self, nfa2):
        # Step 1: Create new states by combining the state sets of both input NFAs
        new_Q = self.Q + nfa2.Q
        
        # Step 2: Combine the input alphabets of both NFAs
        new_Sigma = list(set(self.Sigma) | set(nfa2.Sigma))
        
        # Step 3: The start state of the resulting NFA remains the same as the start state of the first NFA
        new_q0 = self.q0
        
        # Step 4: Create new transitions by combining the transitions of both input NFAs
        new_delta = [transition for transition in self.delta.items()] + [transition for transition in nfa2.delta.items()]
        
        # Step 5: Add epsilon transitions from every final state of the first NFA to the start state of the second NFA
        for final_state in self.F:
            if (final_state, '') in self.delta:
                new_delta.append([(final_state, ''), self.delta[(final_state, '')].union({nfa2.q0})])
            else:
                new_delta.append([(final_state, ''), {nfa2.q0}])
        
        # Convert new_delta to the original format
        new_delta_formatted = []
        for transition in new_delta:
            current_state, input_symbol = transition[0]
            next_states = transition[1]
            new_delta_formatted.append([current_state, input_symbol, list(next_states)])
        
        # Step 6: The final states of the resulting NFA are the same as the final states of the second NFA
        new_F = nfa2.F
        
        # Step 7: Create a new NFA using the combined data
        return NFA(new_Q, new_Sigma, new_delta_formatted, new_q0, new_F)
    
    def kleene_star(self):
        # Step 1: Create a new start state for the resulting NFA
        new_start_state = 'q_new_start'

        # Step 2: Add epsilon transitions from the new start state to the original start state
        new_delta = [transition for transition in self.delta.items()]
        new_delta.append([(new_start_state, ''), {self.q0}])

        # Step 3: Add epsilon transitions from each of the final states back to the original start state
        for final_state in self.F:
            if (final_state, '') in self.delta:
                new_delta[(final_state, '')].add(self.q0)
            else:
                new_delta.append([(final_state, ''), {self.q0}])

        # Convert new_delta to the original format
        new_delta_formatted = []
        for transition in new_delta:
            current_state, input_symbol = transition[0]
            next_states = transition[1]
            new_delta_formatted.append([current_state, input_symbol, list(next_states)])

        # Step 4: Make the new start state an accept state
        new_F = self.F + [new_start_state]

        # Step 5: Preserve the other states, input alphabet, and transition function from the original NFA
        new_Q = self.Q + [new_start_state]
        new_Sigma = self.Sigma

        # Create the new NFA with the Kleene star applied
        kleene_star_nfa = NFA(new_Q, new_Sigma, new_delta_formatted, new_start_state, new_F)

        return kleene_star_nfa