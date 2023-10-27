class SymbolTable:
    def __init__(self, size=100):
        """
        Initialize a symbol table with an optional specified size.

        :param size: The size of the hash table. Default is 100.
        """
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        """
        A simple hash function that returns the index for a given key.

        :param key: The key to be hashed.
        :return: The hash index for the key.
        """
        return hash(key) % self.size

    def insert(self, value):
        """
        Insert a value into the symbol table using its hash as the key.

        :param value: The value to be inserted.
        """
        key = hash(value)
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i in range(len(self.table[index])):
                if self.table[index][i][0] == key:
                    self.table[index][i] = (key, value)
                    return index
            self.table[index].append((key, value))
        return index

    def lookup(self, value):
        """
        Look up a value in the symbol table and return the key if found

        :param value: The value to be looked up.
        :return: The key for the value if found, None otherwise.
        """
        key = hash(value)
        index = self.hash_function(key)
        if self.table[index] is not None:
            for i in range(len(self.table[index])):
                if self.table[index][i] == value:
                    return index
        return None

    def delete(self, value):
        """
        Delete a value from the symbol table.

        :param value: The value to be deleted.
        """
        key = hash(value)
        index = self.hash_function(key)
        if self.table[index] is not None:
            for i in range(len(self.table[index])):
                if self.table[index][i][0] == key:
                    del self.table[index][i]
                    return

    def display(self):
        """
        Display the contents of the symbol table.
        """
        for index, entry in enumerate(self.table):
            if entry is not None:
                print(f'Index {index}: {entry}')

    def __str__(self):
        """
        Return a string representation of the symbol table.

        :return: A string representation of the symbol table.
        """
        result = ''
        for index, entry in enumerate(self.table):
            if entry is not None:
                result += f'Index {index}: {entry} \n'
        return result


if __name__ == "__main__":
    # Example usage:
    symbol_table = SymbolTable()
    symbol_table.insert('a')
    symbol_table.insert(42)
    symbol_table.insert(19)
    symbol_table.insert(42)  # Overwrites the previous value
    symbol_table.display()
    print('Lookup 42:', symbol_table.lookup(42))
    symbol_table.delete(19)
    symbol_table.display()
