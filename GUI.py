import tkinter as tk
from tkinter import ttk
from NFA import NFA
from DFA import DFA
import io
from PIL import Image, ImageTk
import tkinter.messagebox


class AutomataGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automata GUI")
        self.geometry("800x600")

        self.main_menu = ttk.Notebook(self)
        self.main_menu.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.automata_select_combobox = ttk.Combobox()  # Initialize the combobox

        self.automata_select_comboboxes = []
        self.automata_list = []

        self.automata_counts = {"DFA": 0, "NFA": 0, "UnionNFA": 0, "IntersectionNFA": 0, "ConcatenationNFA": 0,"KleeneNFA":0}

        self.create_automata_page(text="Automata 1")
        self.create_automata_page(text="Automata 2")
        self.create_to_dfa_page()
        self.create_process_word_page()
        self.create_operation_page("Union")
        self.create_operation_page("Intersection")
        self.create_operation_page("Concatenation")
        self.create_kleene_star_page()
    
    def create_automata_page(self, text):
        automata_page = ttk.Frame(self.main_menu)
        self.main_menu.add(automata_page, text=text)

        automata_type_label = ttk.Label(automata_page, text="Automata Type:")
        automata_type_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        automata_type_var = tk.StringVar()
        automata_type_combobox = ttk.Combobox(automata_page, textvariable=automata_type_var)
        automata_type_combobox["values"] = ("DFA", "NFA")
        automata_type_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        q_entry = self.create_q_inputs(automata_page)
        sigma_entry = self.create_sigma_inputs(automata_page)
        current_state_entry, input_symbol_entry, next_state_entry, transitions_listbox = self.create_delta_inputs(automata_page)
        q0_entry = self.create_q0_inputs(automata_page)
        f_entry = self.create_f_inputs(automata_page)

        output_frame = ttk.Frame(automata_page)
        output_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        output_text = tk.Text(output_frame, wrap=tk.WORD, width=40, height=20)
        output_text.grid(row=0, column=0, padx=10, pady=10)
        output_text.config(state=tk.DISABLED)
        
        create_button = ttk.Button(automata_page, text="Create Automata",
                           command=lambda: self.create_automata(automata_type_var, q_entry, sigma_entry,
                                                                transitions_listbox, q0_entry, f_entry,
                                                                output_text,output_frame))
        create_button.grid(row=6, column=1, sticky=tk.E, padx=10, pady=10)

    def create_q_inputs(self, parent):
        q_label = ttk.Label(parent, text="State names (comma-separated):")
        q_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        q_entry = ttk.Entry(parent)
        q_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        return q_entry
    
    def create_sigma_inputs(self, parent):
        sigma_label = ttk.Label(parent, text="Alphabet (comma-separated):")
        sigma_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

        sigma_entry = ttk.Entry(parent)
        sigma_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        return sigma_entry
    
    def create_delta_inputs(self, parent):
        delta_label = ttk.Label(parent, text="Transitions:")
        delta_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)

        current_state_label = ttk.Label(parent, text="Current State:")
        current_state_label.grid(row=3, column=1, sticky=tk.W, padx=0, pady=10)
        current_state_entry = ttk.Entry(parent)
        current_state_entry.grid(row=3, column=2, sticky=tk.W, padx=2, pady=10)
        
        input_symbol_label = ttk.Label(parent, text="Input Symbol:")
        input_symbol_label.grid(row=3, column=3, sticky=tk.W, padx=2, pady=10)
        input_symbol_entry = ttk.Entry(parent)
        input_symbol_entry.grid(row=3, column=4, sticky=tk.W, padx=2, pady=10)
        
        next_state_label = ttk.Label(parent, text="Next State(s):")
        next_state_label.grid(row=3, column=5, sticky=tk.W, padx=2, pady=10)
        next_state_entry = ttk.Entry(parent)
        next_state_entry.grid(row=3, column=6, sticky=tk.W, padx=2, pady=10)

        add_transition_button = ttk.Button(parent, text="Add Transition",
                                       command=lambda: self.add_transition(current_state_entry, input_symbol_entry,
                                                                           next_state_entry, transitions_listbox))
        add_transition_button.grid(row=3, column=7, sticky=tk.W, padx=2, pady=10)

        transitions_listbox = tk.Listbox(parent)
        transitions_listbox.grid(row=3, column=8, padx=10, pady=10, rowspan=3)

        reset_transitions_button = ttk.Button(parent, text="Reset Transitions",
                                 command=lambda: self.reset_transitions(current_state_entry, input_symbol_entry,
                                                                       next_state_entry, transitions_listbox))
        reset_transitions_button.grid(row=6, column=8, sticky=tk.W, padx=2, pady=10)

        return current_state_entry, input_symbol_entry, next_state_entry, transitions_listbox
        
    def create_q0_inputs(self, parent):
        q0_label = ttk.Label(parent, text="Initial state:")
        q0_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)

        q0_entry = ttk.Entry(parent)
        q0_entry.grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)
        return q0_entry
    
    def create_f_inputs(self, parent):
        f_label = ttk.Label(parent, text="Final states (comma-separated):")
        f_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)

        f_entry = ttk.Entry(parent)
        f_entry.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)
        return f_entry
    
    def add_transition(self, current_state_entry, input_symbol_entry, next_state_entry, transitions_listbox):
        current_state = current_state_entry.get()
        input_symbol = input_symbol_entry.get()
        next_state = next_state_entry.get()
        transition = f"{current_state},{input_symbol},{next_state}"

        transitions_listbox.insert(tk.END, transition)

    def reset_transitions(self, current_state_entry, input_symbol_entry, next_state_entry, transitions_listbox):
        # Clear the listbox
        transitions_listbox.delete(0, tk.END)

        # Clear the entries
        current_state_entry.delete(0, tk.END)
        input_symbol_entry.delete(0, tk.END)
        next_state_entry.delete(0, tk.END)
    
    def display_diagram(self, graph, output_frame):
        # Clear the frame's contents
        for child in output_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.destroy()

        img_data = graph.pipe(format='png')
        image = Image.open(io.BytesIO(img_data))

        photo = ImageTk.PhotoImage(image)

        diagram_label = ttk.Label(output_frame, image=photo)
        diagram_label.image = photo
        diagram_label.grid(row=0, column=1, padx=10, pady=10)

        return diagram_label

    def create_automata(self, automata_type_var, q_entry, sigma_entry, transitions_listbox, q0_entry, f_entry, output_text,output_frame):
        automata_type = automata_type_var.get()

        Q = q_entry.get().split(',')
        
        Sigma = sigma_entry.get().split(',')

        delta = []
        for i in range(transitions_listbox.size()):
            d = transitions_listbox.get(i)
            if automata_type_var.get() == "NFA":
                next_states = d.split(',')[-1].split(' ')
                delta.append(tuple(d.split(',')[:-1] + [next_states]))
            else:
                delta.append(tuple(d.split(',')))

        q0 = q0_entry.get()

        F = f_entry.get().split(',')

        if automata_type == "DFA":
            automata = DFA(Q, Sigma, delta, q0, F)
            
        elif automata_type == "NFA":
            automata = NFA(Q, Sigma, delta, q0, F)
            
        self.add_automaton(automata, automata_type)
        self.update_universal_automata_select_combobox()  # Add this line to update the combobox

        graph = automata.diagram()
        self.display_diagram(graph,output_frame)

        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)

        output_text.insert(tk.END, f"{automata_type} created.\n")
        output_text.insert(tk.END, "Information:\n")
        output_text.insert(tk.END, f"Q: {', '.join(Q)}\n")
        output_text.insert(tk.END, f"Sigma: {', '.join(Sigma)}\n")
        output_text.insert(tk.END, f"delta:\n")

        if automata_type == "NFA":
            for d in delta:
                output_text.insert(tk.END, f" {d[0]}, {d[1]}, {' '.join(d[2])}\n")
        else:
            for d in delta:
                output_text.insert(tk.END, f" {', '.join(d)}\n")

        output_text.insert(tk.END, f"q0: {q0}\n")
        output_text.insert(tk.END, f"F: {', '.join(F)}\n")
        output_text.config(state=tk.DISABLED)


    def update_q0_combobox(self, *args):
        num_states = int(self.q_entry.get())
        Q = [f'q{i}' for i in range(num_states)]
        self.q0_combobox["values"] = Q
    
    def create_process_word_page(self):
        process_word_page = ttk.Frame(self.main_menu)
        self.main_menu.add(process_word_page, text="Process Word")
        
        automata_select_label = ttk.Label(process_word_page, text="Select Automaton:")
        automata_select_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.process_word_combobox = ttk.Combobox(process_word_page)
        self.process_word_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        self.automata_select_comboboxes.append( self.process_word_combobox)
        
        process_single_word_title = ttk.Label(process_word_page, text="Process Single Word", font=("Helvetica", 10, "bold"))
        process_single_word_title.grid(row=1, column=0, columnspan=2, pady=5)
        
        word_label = ttk.Label(process_word_page, text="Input Word:")
        word_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

        word_entry = ttk.Entry(process_word_page)
        word_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)

        process_word_button = ttk.Button(process_word_page, text="Process Word",
                                command=lambda: self.process_word_result(word_entry))
        process_word_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)

        result_label = ttk.Label(process_word_page, text="Result:")
        result_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)

        self.result_text = ttk.Label(process_word_page, text="")
        self.result_text.grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)
        
        # New input for n
        show_words_title = ttk.Label(process_word_page, text="Show Accepted/Rejected Words", font=("Helvetica", 10, "bold"))
        show_words_title.grid(row=5, column=0, columnspan=2, pady=5)
        
        n_label = ttk.Label(process_word_page, text="Number of words to display:")
        n_label.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)

        n_entry = ttk.Entry(process_word_page)
        n_entry.grid(row=6, column=1, sticky=tk.W, padx=10, pady=10)

        # New combobox for selecting accepted or rejected words
        word_type_label = ttk.Label(process_word_page, text="Accepted/Rejected:")
        word_type_label.grid(row=7, column=0, sticky=tk.W, padx=10, pady=10)

        word_type_combobox = ttk.Combobox(process_word_page)
        word_type_combobox["values"] = ("Accepted", "Rejected")
        word_type_combobox.grid(row=7, column=1, sticky=tk.W, padx=10, pady=10)

        # New button for displaying words
        display_words_button = ttk.Button(process_word_page, text="Display Words",
                                command=lambda: self.display_words(word_type_combobox, n_entry))
        display_words_button.grid(row=8, column=1, sticky=tk.E, padx=10, pady=10)

        # New label to display the result
        self.displayed_words_text = tk.Text(process_word_page, wrap=tk.WORD, width=40, height=5)
        self.displayed_words_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        self.displayed_words_text.config(state=tk.DISABLED)

        self.automaton_diagram_frame = ttk.Frame(process_word_page)
        self.automaton_diagram_frame.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Bind the Combobox event to the new method
        self.process_word_combobox.bind("<<ComboboxSelected>>", self.display_selected_automaton_diagram)
        
    
    def process_word_result(self, word_entry):
        automata_index = int(self.process_word_combobox.current())
        word = word_entry.get()
        
        if automata_index < len(self.automata_list):
            automata = self.automata_list[automata_index][0]
            result = automata.process_word(word)
            self.result_text.config(text="Accepted" if result else "Rejected")
        else:
            self.result_text.config(text="Invalid Automaton")
    
    def display_words(self, word_type_combobox, n_entry):
        automata_index = int(self.process_word_combobox.current())
        word_type = word_type_combobox.get()
        rejected = (word_type == "Rejected")
        n = int(n_entry.get())

        if automata_index < len(self.automata_list):
            automata = self.automata_list[automata_index][0]
            words = automata.get_accept_words(n, rejected)

            self.displayed_words_text.config(state=tk.NORMAL)
            self.displayed_words_text.delete(1.0, tk.END)

            for word in words:
                self.displayed_words_text.insert(tk.END, f"{word}\n")

            self.displayed_words_text.config(state=tk.DISABLED)
        else:
            self.displayed_words_text.config(state=tk.NORMAL)
            self.displayed_words_text.delete(1.0, tk.END)
            self.displayed_words_text.insert(tk.END, f"Invalid Automaton\n")
            self.displayed_words_text.config(state=tk.DISABLED)
    
    def display_selected_automaton_diagram(self, event):
        automata_index = int(self.process_word_combobox.current())
        if automata_index < len(self.automata_list):
            automata = self.automata_list[automata_index][0]
            graph = automata.diagram()
            self.display_diagram(graph, self.automaton_diagram_frame)
        else:
            tkinter.messagebox.showerror("Error", "Invalid Automaton")
    
    def convert_nfa_to_dfa(self, automata_select_combobox):
        automata_index = int(automata_select_combobox.current())

        if automata_index < len(self.automata_list):
            automata = self.automata_list[automata_index][0]

            if isinstance(automata, NFA):
                dfa = automata.to_dfa()
                self.add_automaton(dfa, "DFA")  # Pass "DFA" as the automaton type
                self.update_universal_automata_select_combobox()
                # Display DFA information
                self.dfa_info_text.config(state=tk.NORMAL)
                self.dfa_info_text.delete(1.0, tk.END)

                self.dfa_info_text.insert(tk.END, "DFA created from NFA.\n")
                self.dfa_info_text.insert(tk.END, "Information:\n")
                self.dfa_info_text.insert(tk.END, f"Q: {', '.join(dfa.Q)}\n")
                self.dfa_info_text.insert(tk.END, f"Sigma: {', '.join(dfa.Sigma)}\n")
                self.dfa_info_text.insert(tk.END, f"delta:\n")

                for d in dfa.delta:
                    self.dfa_info_text.insert(tk.END, f" {', '.join(d)}\n")

                self.dfa_info_text.insert(tk.END, f"q0: {dfa.q0}\n")
                self.dfa_info_text.insert(tk.END, f"F: {', '.join(dfa.F)}\n")
                self.dfa_info_text.config(state=tk.DISABLED)

                # Display DFA diagram
                graph = dfa.diagram()
                self.display_diagram(graph, self.dfa_diagram_container)

            else:
                tkinter.messagebox.showerror("Error", "The selected automaton is not an NFA.")
        else:
            tkinter.messagebox.showerror("Error", "Invalid Automaton")

    def add_automaton(self, automaton, automaton_type=None):
        self.automata_list.append((automaton, automaton_type))
        self.update_universal_automata_select_combobox()


    def update_universal_automata_select_combobox(self):
        automata_names = []
        dfa_count = 1
        nfa_count = 1
        union_nfa_count = 1
        intersec_nfa_count = 1
        concat_nfa_count = 1
        kleene_nfa_count = 1
        for automaton, automaton_type in self.automata_list:
            if automaton_type == "DFA":
                name = f'DFA{dfa_count}'
                dfa_count += 1
            elif automaton_type == "NFA":
                name = f'NFA{nfa_count}'
                nfa_count += 1
            elif automaton_type == "UnionNFA":
                name = f'UnionNFA{union_nfa_count}'
                union_nfa_count += 1
            elif automaton_type == "IntersectionNFA":
                name = f'IntersectionNFA{intersec_nfa_count}'
                intersec_nfa_count += 1
            elif automaton_type == "ConcatenationNFA":
                name = f'ConcatenationNFA{concat_nfa_count}'
                concat_nfa_count += 1
            elif automaton_type == "KleeneNFA":
                name = f'KleeneNFA{kleene_nfa_count}'
                kleene_nfa_count += 1
            else:
                name = f'Automata {len(automata_names) + 1}'
            automata_names.append(name)

        for automata_select_combobox in self.automata_select_comboboxes:
            automata_select_combobox["values"] = automata_names
    
    def create_to_dfa_page(self):
        to_dfa_page = ttk.Frame(self.main_menu)
        self.main_menu.add(to_dfa_page, text="NFA to DFA")
        
        automata_select_label = ttk.Label(to_dfa_page, text="Select Automaton:")
        automata_select_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.to_dfa_combobox = ttk.Combobox(to_dfa_page)
        self.to_dfa_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        self.automata_select_comboboxes.append(self.to_dfa_combobox)
        
        # Bold title for "Convert to DFA"
        convert_dfa_title = ttk.Label(to_dfa_page, text="Convert to DFA", font=("Helvetica", 10, "bold"))
        convert_dfa_title.grid(row=1, column=0, columnspan=2, pady=5)

        # Button for converting NFA to DFA
        convert_dfa_button = ttk.Button(to_dfa_page, text="Convert NFA to DFA",
                                        command=lambda: self.convert_nfa_to_dfa(self.automata_select_combobox))
        convert_dfa_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Label for displaying DFA information
        self.dfa_info_text = tk.Text(to_dfa_page, wrap=tk.WORD, width=40, height=20)
        self.dfa_info_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.dfa_info_text.config(state=tk.DISABLED)
        
        # Diagram container for the DFA
        self.dfa_diagram_container = ttk.Label(to_dfa_page)
        self.dfa_diagram_container.grid(row=3, column=2, columnspan=2)

    def create_automata_select_combobox(self, parent):
        combobox = ttk.Combobox(parent)
        combobox["values"] = ()
        return combobox

    def create_operation_page(self, operation):
        operation_page = ttk.Frame(self.main_menu)
        self.main_menu.add(operation_page, text=operation.capitalize())

        automata1_select_label = ttk.Label(operation_page, text="Select Automaton 1:")
        automata1_select_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        automata1_select_combobox = ttk.Combobox(operation_page)
        automata1_select_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        self.automata_select_comboboxes.append(automata1_select_combobox)

        automata2_select_label = ttk.Label(operation_page, text="Select Automaton 2:")
        automata2_select_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        automata2_select_combobox = ttk.Combobox(operation_page)
        automata2_select_combobox.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        self.automata_select_comboboxes.append(automata2_select_combobox)

        operation_button = ttk.Button(operation_page, text=f"Perform {operation.capitalize()}",
                                    command=lambda: self.perform_operation(operation, automata1_select_combobox, automata2_select_combobox, operation_output_frame))
        operation_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10)

        # Output frame for displaying operation automaton
        operation_output_frame = ttk.Frame(operation_page)
        operation_output_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        return operation_output_frame
    
    def perform_operation(self, operation, automata_select_combobox1, automata_select_combobox2, operation_output_frame):
        automata_index1 = int(automata_select_combobox1.current())
        automata_index2 = int(automata_select_combobox2.current())

        if automata_index1 < len(self.automata_list) and automata_index2 < len(self.automata_list):
            automata1 = self.automata_list[automata_index1][0]
            automata2 = self.automata_list[automata_index2][0]

            automata1_graph = automata1.diagram()
            automata2_graph = automata2.diagram()
            self.display_diagram_with_position(automata1_graph, operation_output_frame, row=1, column=0)
            self.display_diagram_with_position(automata2_graph, operation_output_frame, row=1, column=1)

            
            if operation == "Union":
                result_nfa = automata1.union(automata2)
            elif operation == "Intersection":
                result_nfa = automata1.intersection(automata2)
                if result_nfa is None:
                    tkinter.messagebox.showinfo("No Intersection", "There is no intersection between the selected NFAs.")
                    return
            elif operation == "Concatenation":
                result_nfa = automata1.concatenation(automata2)

            # Add the new NFA with the appropriate name
            self.add_automaton(result_nfa, f"{operation}NFA")
            self.update_universal_automata_select_combobox()

            # Display the operation NFA diagram
            operation_graph = result_nfa.diagram()
            self.display_diagram_with_position(operation_graph, operation_output_frame, row=2, column=0)

            
        else:
            tkinter.messagebox.showerror("Error", "Invalid Automaton")

    
    def display_diagram_with_position(self, graph, output_frame, row=0, column=0, max_width=400, max_height=300):
        img_data = graph.pipe(format='png')
        image = Image.open(io.BytesIO(img_data))

        # Resize the image proportionally if it exceeds max_width or max_height
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)

        diagram_label = ttk.Label(output_frame, image=photo)
        diagram_label.image = photo
        diagram_label.grid(row=row, column=column, padx=10, pady=10)

        return diagram_label
    
    def create_kleene_star_page(self):
        kleene_star_page = ttk.Frame(self.main_menu)
        self.main_menu.add(kleene_star_page, text="Kleene Star")

        automata_select_label = ttk.Label(kleene_star_page, text="Select Automaton:")
        automata_select_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        automata_select_combobox = ttk.Combobox(kleene_star_page)
        automata_select_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        self.automata_select_comboboxes.append(automata_select_combobox)

        kleene_star_button = ttk.Button(kleene_star_page, text="Perform Kleene Star",
                                        command=lambda: self.perform_kleene_star(automata_select_combobox, kleene_star_output_frame))
        kleene_star_button.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

        # Output frame for displaying Kleene Star automaton
        kleene_star_output_frame = ttk.Frame(kleene_star_page)
        kleene_star_output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        return kleene_star_output_frame
    
    def perform_kleene_star(self, automata_select_combobox, kleene_star_output_frame):
        automata_index = int(automata_select_combobox.current())

        if automata_index < len(self.automata_list):
            automata = self.automata_list[automata_index][0]

            automata_graph = automata.diagram()
            self.display_diagram_with_position(automata_graph, kleene_star_output_frame, row=0, column=0)

            
            result_nfa = automata.kleene_star()

            # Add the new NFA with the appropriate name
            self.add_automaton(result_nfa, "KleeneNFA")
            self.update_universal_automata_select_combobox()

            # Display the Kleene Star NFA diagram
            kleene_star_graph = result_nfa.diagram()
            self.display_diagram_with_position(kleene_star_graph, kleene_star_output_frame, row=0, column=1)

            
        else:
            tkinter.messagebox.showerror("Error", "Invalid Automaton")

    

if __name__ == "__main__":
    app = AutomataGUI()
    app.mainloop()