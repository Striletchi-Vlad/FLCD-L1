class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def read_from_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                line = line.strip().split()
                if line[0] == "states":
                    self.states = set(line[1:])
                elif line[0] == "alphabet":
                    self.alphabet = set(line[1:])
                elif line[0] == "transitions":
                    for transition in line[1:]:
                        start, symbol, end = transition.split(",")
                        self.transitions[(start, symbol)] = end
                elif line[0] == "initial_state":
                    self.initial_state = line[1]
                elif line[0] == "final_states":
                    self.final_states = set(line[1:])

    def display_elements(self):
        print("1. Set of States:", self.states)
        print("2. Alphabet:", self.alphabet)
        print("3. Transitions:")
        for transition, end_state in self.transitions.items():
            print(f"   ({transition[0]}, {transition[1]}) -> {end_state}")
        print("4. Initial State:", self.initial_state)
        print("5. Set of Final States:", self.final_states)

    def is_accepted(self, sequence):
        current_state = self.initial_state
        for symbol in sequence:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.final_states


if __name__ == "__main__":
    fa = FiniteAutomaton()
    # filename = "fa.txt"  # Replace with the actual filename
    filename = "fa_identifier.txt"  # Replace with the actual filename
    fa.read_from_file(filename)

    while True:
        print("\n------ Menu ------")
        print("1. Display Elements")
        print("2. Verify Sequence")
        print("3. Exit")
        print()

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            fa.display_elements()
        elif choice == "2":
            sequence = input("Enter the sequence to verify: ")
            if fa.is_accepted(sequence):
                print("Sequence is accepted by the FA.")
            else:
                print("Sequence is not accepted by the FA.")
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
