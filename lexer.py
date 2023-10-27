from symboltable import SymbolTable
import re


class Lexer():
    def __init__(self, filename):
        self.pos = 0
        self.filename = filename
        self.st = SymbolTable()
        self.lines = []
        with open("Token.in", "r") as f:
            self.tokens = f.read().splitlines()
        self.separators = [
            ' ',
            ';',
            '{',
            '}',
            '(',
            ')',
        ]
        self.identifier_regex = r'^[a-zA-Z][a-zA-Z0-9]?$'
        self.constant_regex = r'^[+-]?[0-9]+$'
        self.PIF = []

    def read_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if line[:2] == '//':
                    continue
                # Remove \n
                line = line[:-1]
                self.lines.append(str(line))

        # print(self.lines)
        # for line in self.lines:
        #     print(line)
        #     print(type(line))

    def split_text(self):
        for i in range(len(self.lines)):
            aux = self.lines[i]
            print(aux)
            for separator in self.separators:
                aux = aux.replace(separator, ' ' + separator + ' ')
            aux = aux.split()
            self.lines[i] = aux

    def lex(self):
        for i, line in enumerate(self.lines):
            for item in line:
                if item in self.tokens:
                    self.PIF.append((item, -1))
                elif re.match(self.identifier_regex, item):
                    idx = self.st.insert(item)
                    self.PIF.append(('id', idx))
                elif re.match(self.constant_regex, item):
                    idx = self.st.insert(item)
                    self.PIF.append(('const', idx))
                else:
                    print('Error: ' + item + ', line ' + str(i))
                    return
        print('Lex succesful!')
        with open('PIF.out', 'w') as f:
            for item in self.PIF:
                f.write(str(item) + '\n')
        with open('ST.out', 'w') as f:
            f.write(str(self.st))

    def main(self):
        self.read_file()
        self.split_text()
        self.lex()


if __name__ == '__main__':
    lexer = Lexer('p1err')
    lexer.main()
