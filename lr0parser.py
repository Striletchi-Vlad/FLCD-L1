from grammar import Grammar


class LR0Parser:
    def __init__(self, grammar):
        self.grammar = grammar

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


# Example usage
# grammar = Grammar("<program>")
grammar = Grammar("<S>")
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
