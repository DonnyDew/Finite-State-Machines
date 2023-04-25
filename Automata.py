import itertools
from abc import ABC, abstractmethod

class Automata(ABC):
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q # list of states
        self.Sigma = Sigma # list of alphabet
        self.delta = delta
        self.q0 = q0 # start state
        self.F = F # list of final state(s)
    
    @abstractmethod
    def print_info(self):
        pass

    def generate_words(self, n):
        combinations = list(itertools.product(self.Sigma, repeat=n))
        return [''.join(c) for c in combinations]

    @abstractmethod
    def process_word(self, word):
        pass
    
    def get_accept_words(self, n, rejected=False):
        words = self.generate_words(n)
        if rejected:
            accept_words = list(filter(lambda x: not self.process_word(x), words))
        else:
            accept_words = list(filter(self.process_word, words))
        return accept_words
    
