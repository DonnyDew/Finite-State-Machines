# Overview
This project is an implementation of Finite Automata specifically a DFA(Deterministic finite automata) and NFA(Nondeterministic finite automata)

1. Automata.py: Contains the `Automata` class, which serves as a base class for the `NFA` and `DFA` classes. The `Automata` class defines the basic structure and methods of finite automata, including state transitions, accepting states, and alphabet.
2. NFA.py: Contains the `NFA` class, which is a subclass of `Automata`. The `NFA` class defines the behavior of non-deterministic finite automata, which can be in multiple states at once and have multiple transition paths for a given input symbol.
3. DFA.py: Contains the `DFA` class, which is a subclass of `Automata`. The `DFA` class defines the behavior of deterministic finite automata, which have a unique transition for each input symbol and can only be in one state at a time.
4. GUI.py: Contains the `AutomataGUI` class, which provides a graphical user interface for working with finite automata. The GUI allows users to create and manipulate NFAs and DFAs, perform operations on them, and convert NFAs to DFAs.

# How to use
To use the program, simply run the `GUI.py` file. This will open the graphical user interface, where you can create, manipulate, and convert finite automata.

## Creating automata
To create a new automaton, select "Automata1" or "Automata2" from the top bar menu. This will open a tab where you can define the automaton's states, alphabet, transitions, and accepting states. You can create multiple automata on a window by hitting the reset transition button but sometimes that button gets hidden depending on window and screen size so you may to re-reun the program.

## Converting an NFA to a DFA
To convert an NFA to a DFA, select "NFA to DFA" from the top menu. This will open a new tab where you can select the NFA to convert and view the resulting DFA.

## Process Word
To process a word, select "Process Word" from the top menu. This will open a new tab where you can select an automata. You can input an individual word and it will display "accepted" or "rejected". You can also get a list of accepted or rejected words of length n. For number of words select a number. 

## Performing operations
To perform an operation on two automata, select "Union," "Intersection," or "Concatenation" from the top menu. This will open a new tab where you can select the two automata to operate on and view the resulting automaton.

## Performing Kleene star
To perform Kleene star operation on an automaton, select "Kleene Star" from the top menu. This will open a new tab where you can select the automaton to perform Kleene star operation on and view the resulting automaton.

## Example Creation of Automata 
![Example Usage](https://github.com/DonnyDew/Finite-State-Machines/blob/master/example%20usage.PNG?raw=True)
