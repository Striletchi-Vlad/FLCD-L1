class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = []
        self.start_symbol = None

    def read_grammar_from_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                production = line.strip()
                if production:
                    self.process_production(production)

    def process_production(self, production):
        parts = production.split("::=")
        if len(parts) != 2:
            raise ValueError(f"Invalid production: {production}")

        nonterminal = parts[0].strip()
        self.nonterminals.add(nonterminal)

        rhs_symbols = [symbol.strip() for symbol in parts[1].split("|")]
        for rhs_symbol in rhs_symbols:
            self.process_rhs_symbol(nonterminal, rhs_symbol)

    def process_rhs_symbol(self, nonterminal, rhs_symbol):
        production = (nonterminal, rhs_symbol)
        self.productions.append(production)

        symbols = rhs_symbol.split()
        for symbol in symbols:
            if symbol.isalpha() and symbol.islower():
                self.terminals.add(symbol)

    def print_nonterminals(self):
        print("Nonterminals:", self.nonterminals, "\n")

    def print_terminals(self):
        print("Terminals:", self.terminals, "\n")

    def print_productions(self):
        print("Productions:")
        for production in self.productions:
            print(f"{production[0]} ::= {production[1]}")
        print()

    def productions_for_nonterminal(self, nonterminal):
        matching_productions = [
            prod[1] for prod in self.productions if prod[0] == nonterminal
        ]
        return matching_productions

    def is_cfg(self):
        for production in self.productions:
            if production[0] not in self.nonterminals:
                print("not in nonterminals")
                return False
        return True


# Example usage
grammar = Grammar()
grammar.read_grammar_from_file("Syntax.in")

grammar.print_nonterminals()
grammar.print_terminals()
grammar.print_productions()

nonterminal = "<stmt>"
print(
    f"Productions for {nonterminal}: {grammar.productions_for_nonterminal(nonterminal)}"
)
print("-----------------")
is_cfg = grammar.is_cfg()
print("Is CFG:", is_cfg)
