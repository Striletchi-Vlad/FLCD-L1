from grammar import Grammar
import time


class LR0Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.working_stack = []  # Initialize the working stack as an empty list
        self.input_stack = []  # Initialize the input stack as an empty list
        self.output = []  # Initialize the output as an empty list

    def closure(self, items):
        closure_items = set(items)
        changed = True

        while changed:
            changed = False
            for item in list(closure_items):
                # print("BBBB")
                dot_position = item[1].index(".")
                if dot_position < len(item[1]) - 1:
                    # next_space = item[1].index(" ", dot_position)
                    try:
                        next_space = item[1].index(" ", dot_position)
                    except Exception:
                        next_space = len(item[1])
                    next_word = item[1][dot_position + 1 : next_space]
                    if next_word not in self.grammar.nonterminals:
                        # print(next_word)
                        continue
                    # print("AAAA")
                    # nonterminal_to_expand = item[1][dot_position + 1 :]
                    nonterminal_to_expand = next_word
                    # print(nonterminal_to_expand)
                    for production in self.grammar.productions_for_nonterminal(
                        nonterminal_to_expand
                    ):
                        new_item = (nonterminal_to_expand, " ." + production)
                        if new_item not in closure_items:
                            closure_items.add(new_item)
                            changed = True

        return closure_items

    def goto(self, items, symbol):
        goto_items = set()

        for item in items:
            dot_position = item[1].index(".")
            if dot_position < len(item[1]) - 1:
                try:
                    next_space = item[1].index(" ", dot_position)
                except Exception:
                    next_space = len(item[1])
                next_word = item[1][dot_position + 1 : next_space]
                if next_word != symbol:
                    # print(next_word, "!=", symbol, ", aborting.")
                    continue

                new_item = (
                    item[0],
                    item[1][:dot_position]
                    + symbol
                    + " ."
                    # + item[1][dot_position + 2 :],
                    + item[1][next_space + 1 :],
                    # + item[1][dot_position + 1 :],
                )
                goto_items.add(new_item)

        return self.closure(goto_items)

    def canonical_collection(self):
        # start_production = (self.grammar.start_symbol, f"{self.grammar.start_symbol}.")
        start_production = (self.grammar.start_symbol, f".{self.grammar.start_symbol}")
        initial_set = self.closure([start_production])
        # print(initial_set)
        # exit()

        sets = [initial_set]
        pending_sets = [initial_set]

        while pending_sets:
            current_set = pending_sets.pop(0)
            # print(current_set)
            # exit()

            for symbol in self.grammar.terminals.union(self.grammar.nonterminals):
                print("Current set: ", current_set, " Attempting with ", symbol)
                goto_set = self.goto(current_set, symbol)
                print("Goto set: ", goto_set)
                goto_set = self.closure(goto_set)
                print("\tResulting closure: ", goto_set)
                if goto_set and goto_set not in sets:
                    sets.append(goto_set)
                    pending_sets.append(goto_set)

        return sets

    def build_parsing_table(self, canonical_collection):
        self.parsing_table = {}
        for i, state in enumerate(canonical_collection):
            self.parsing_table[i] = {"action": None}
            for production in state:
                # print("Production: ", production)
                rhs = production[1].replace(" ", "")
                # print(f"RHS: '{rhs}'")
                # Case 1: A -> a.B
                if rhs.index(".") != len(rhs) - 1:
                    # print("Case 1")
                    # next_symbol = rhs[rhs.index(".") + 1:]
                    self.parsing_table[i]["action"] = "shift"
                # Case 2 or 3
                elif rhs.index(".") == len(rhs) - 1:
                    # print("Case 2")
                    # Case 2: S' -> S.
                    if production[0] == self.grammar.start_symbol:
                        self.parsing_table[i]["action"] = "accept"
                    # Case 3: A -> B.
                    else:
                        # production_in_file_format = (
                        #     production[0] + " ::= " + production[1].replace(".", "")
                        # )
                        nonterminal = production[0]
                        rhs = production[1].replace(".", "")
                        # print("Production in file format: ", production_in_file_format)
                        k = self.grammar.find_production_index(nonterminal, rhs)
                        self.parsing_table[i]["action"] = f"reduce{k}"
            # Case 4: goto
            # for j in self.grammar.nonterminals:
            for j in self.grammar.terminals:
                # print(f"i: {i}, j: {j}")
                goto_result = self.goto(state, j)
                # print("Goto result: ", goto_result)
                # print("Canonical collection: ", canonical_collection)
                # goto_index = canonical_collection.index(goto_result)
                if goto_result:
                    # self.parsing_table[i][j] = goto_result
                    goto_index = canonical_collection.index(goto_result)
                    self.parsing_table[i][j] = goto_index
            for j in self.grammar.nonterminals:
                # print(f"i: {i}, j: {j}")
                goto_result = self.goto(state, j)
                # print("Goto result: ", goto_result)
                # print("Canonical collection: ", canonical_collection)
                # goto_index = canonical_collection.index(goto_result)
                if goto_result:
                    # self.parsing_table[i][j] = goto_result
                    goto_index = canonical_collection.index(goto_result)
                    self.parsing_table[i][j] = goto_index

    def print_parsing_table(self):
        print("Parsing table:")
        for i in range(len(self.parsing_table)):
            print(i, self.parsing_table[i])

    def shift(self, config, state):
        alpha, beta, phi = config

        # Move the next symbol from beta to alpha
        symbol, rest_beta = beta[0], beta[1:]
        # new_alpha = alpha + symbol
        # new_alpha = symbol

        # Update the state based on the parsing table
        # new_state = self.parsing_table[state]["goto"][symbol]
        new_state = self.parsing_table[state][symbol]

        # if rest_beta != "$":
        new_alpha = alpha + symbol + str(new_state)
        # else:
        #     new_alpha = alpha + symbol

        # Update the configuration
        new_config = (new_alpha, rest_beta, phi)
        return new_config, new_state

    def reduce(self, config, state, reduce_index):
        alpha, beta, phi = config

        # Get the production rule
        production_rule = self.grammar.getProductions()[reduce_index]
        print("Production rule: ", production_rule)

        # Get the left hand side of the production rule
        lhs = production_rule[0]

        # Get the right hand side of the production rule
        rhs = production_rule[1].replace(" ", "")
        print("lenRHS:", len(rhs))
        print("RHS: ", rhs)

        alpha = alpha[: -(len(rhs) + 1)]
        alpha += lhs

        print("Alpha: ", alpha)

        # Find the next state
        for i in range(len(alpha), 0, -1):
            if alpha[i - 1].isnumeric():
                temp_state = int(alpha[i - 1])
                symbol = alpha[i:]
                print("State: ", temp_state)
                print("Symbol: ", symbol)
                print("Alpha: ", alpha)
                next_state = self.parsing_table[temp_state][symbol]
                alpha = alpha[: i - 1] + symbol + str(next_state)
                # exit()
                break

        # Update the configuration
        new_config = (alpha, beta, phi)
        return new_config, next_state

    def parse(self, input_string):
        alpha = "$0"
        state = 0
        beta = input_string.replace(" ", "") + "$"
        phi = ""
        end = False
        config = (alpha, beta, phi)
        while not end:
            if beta == "$":
                print("Accepted")
                end = True
                break
            time.sleep(1)
            if "reduce" in self.parsing_table[state]["action"]:
                reduce_index = int(
                    self.parsing_table[state]["action"].replace("reduce", "")
                )
                print("reduce with ", config, state)
                config, state = self.reduce(config, state, reduce_index)
            elif self.parsing_table[state]["action"] == "shift":
                print("shift with ", config, state)
                config, state = self.shift(config, state)
            elif self.parsing_table[state]["action"] == "accept":
                print("Accepted")
                end = True
            else:
                print("Error")
                end = True


# Example usage
# grammar = Grammar("<program>")
grammar = Grammar("<S'>")
# grammar = Grammar("<S>")
# grammar.read_grammar_from_file("Syntax.in")
grammar.read_grammar_from_file("Sem9syntax.in")
grammar.print_productions()
grammar.print_nonterminals()
grammar.print_terminals()


lr0_parser = LR0Parser(grammar)

canonical_sets = lr0_parser.canonical_collection()

# Print the canonical sets
for i, canonical_set in enumerate(canonical_sets):
    print(f"I{i}:", canonical_set)

lr0_parser.build_parsing_table(canonical_sets)
# print(lr0_parser.parsing_table)
lr0_parser.print_parsing_table()
lr0_parser.parse("a b c")
