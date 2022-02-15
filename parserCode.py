from anytree import Node,dotexport
from scannerCode import Scanner
from copy import deepcopy
from re import compile, search
from PIL import Image
# from matplotlib.pyplot import show ,close,imshow
# from  matplotlib.image import imread

class Error(Exception):
    pass

class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.node_names = {}

    def create_node(self, name):
        for node, value in self.node_names.items():
            if node == name:
                new_name = value * ' ' + str(name)
                created_node = Node(new_name)
                self.node_names[name] += 1
                return created_node

        created_node = Node(name)
        self.node_names[name] = 1
        return created_node

    def get_tree(self):
        self.node_names = {}
        return self.stmt_seq()

    def match(self, token):

        if self.scanner.current_token()[0] == token:
            self.scanner.next_token()
        else:
            raise Error(f"ERROR MATCHING ({token})")

    def stmt_seq(self):

        temp = self.create_node('stmt_seq')
        self.statement().parent = temp
        while self.scanner.current_token()[0] == 'SEMICOLON':
            self.match('SEMICOLON')
            self.statement().parent = temp

        return temp

    def statement(self):
        if self.scanner.current_token()[0] == 'IF':
            return self.if_stmt()
        elif self.scanner.current_token()[0] == 'REPEAT':
            return self.repeat_stmt()
        elif self.scanner.current_token()[0] == 'IDENTIFIER':
            return self.assign_stmt()
        elif self.scanner.current_token()[0] == 'READ':
            return self.read_stmt()
        elif self.scanner.current_token()[0] == 'WRITE':
            return self.write_stmt()
        else:
            raise Error("CANNOT RESOLVE STATMENT")

    def if_stmt(self):
        self.match('IF')

        temp = self.create_node('if')
        if self.scanner.current_token()[0] == 'OPENBRACKET':
            self.match('OPENBRACKET')
            self.exp().parent = temp
            self.match('CLOSEDBRACKET')
        else:
            self.exp().parent = temp
        self.match('THEN')
        self.stmt_seq().parent = temp
        if self.scanner.current_token()[0] == 'ELSE':
            self.match('ELSE')
            self.stmt_seq().parent = temp
        self.match('END')

        return temp

    def repeat_stmt(self):

        self.match('REPEAT')
        temp = self.create_node('repeat')
        self.stmt_seq().parent = temp
        self.match('UNTIL')
        self.exp().parent = temp

        return temp

    def assign_stmt(self):

        temp = self.create_node(f'assign ({self.scanner.current_token()[1]})')
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.exp().parent = temp

        return temp

    def read_stmt(self):

        self.match('READ')
        temp = self.create_node(f'read ({self.scanner.current_token()[1]})')
        self.match('IDENTIFIER')

        return temp

    def write_stmt(self):

        self.match('WRITE')
        temp = self.create_node(f'write ({self.scanner.current_token()[1]})')
        self.exp().parent = temp

        return temp

    def exp(self):
        temp = self.simple_exp()
        while (self.scanner.current_token()[0] in ['EQUAL', 'LESSTHAN', 'GREATERTHAN']):

            new_temp = self.create_node(f'op ({self.scanner.current_token()[1]})')
            self.match(self.scanner.current_token()[0])

            temp.parent = new_temp
            self.simple_exp().parent = new_temp

            temp = deepcopy(new_temp)

        return temp

    def simple_exp(self):
        temp = self.term()
        while (self.scanner.current_token()[0] in ['PLUS', 'MINUS']):

            new_temp = self.create_node(f'op ({self.scanner.current_token()[1]})')
            self.match(self.scanner.current_token()[0])

            temp.parent = new_temp
            self.term().parent = new_temp

            temp = deepcopy(new_temp)

        return temp

    def term(self):
        temp = self.factor()
        while (self.scanner.current_token()[0] == 'MULT' or self.scanner.current_token()[0] == 'DIV'):
            new_temp = self.create_node(f'op ({self.scanner.current_token()[1]})')
            self.match(self.scanner.current_token()[0])

            temp.parent = new_temp
            self.factor().parent = new_temp

            temp = deepcopy(new_temp)

        return temp

    def factor(self):
        temp = None
        if (self.scanner.current_token()[0] == 'OPENBRACKET'):
            self.match('OPENBRACKET')
            temp = self.exp()
            self.match('CLOSEDBRACKET')

        elif (self.scanner.current_token()[0] == 'NUMBER'):
            temp = self.create_node(f'const ({self.scanner.current_token()[1]})')
            self.match('NUMBER')

        elif (self.scanner.current_token()[0] == 'IDENTIFIER'):
            temp = self.create_node(f'id ({self.scanner.current_token()[1]})')
            self.match('IDENTIFIER')
        else:
            raise Error("ERROR MATCHING [(IDENTIFIER), (NUMBER), (OPENBRACKET)]")

        return temp

    @staticmethod
    def nodeattrfunc(node):
        pattern = compile(r'(if\b)|(assign\b)|(read\b)|(write\b)|(repeat\b)')
        is_stmt = bool(search(pattern, node.name))
        if is_stmt:
            return "shape=polygon"
        else:
            return "shape=ellipse"

    @staticmethod
    def edgeattrfunc(node, child):
        pattern1 = compile(r'(repeat\b)')
        pattern2 = compile(r'(stmt_seq\b)')
        is_optional = bool(search(pattern1, node.name)) and bool (search(pattern2, child.name))
        if is_optional:
            return "style=dashed,dir=none"
        else:
            return "dir=none"

    # @staticmethod
    # def nodenamefunc(node):
    #     if (node.name.find('.') != -1):
    #         return node.name.split(".", 1)[1]
    #     else :
    #         return node.name

if __name__ == '__main__':
    with open("test3.txt") as f:  # open file
        lines = f.read()
    S = Scanner(lines)
    P = Parser(S)
    if not S.check():

        syntax_tree = P.get_tree()
        dotexport.DotExporter(syntax_tree, nodeattrfunc=P.nodeattrfunc,
                              edgeattrfunc=P.edgeattrfunc).to_dotfile("tree.dot")

        from graphviz import Source

        Source.from_file('tree.dot')
        from graphviz import render

        render('dot', 'png', 'tree.dot')
        im = Image.open("Tree.dot.png")
        im.show()
        # close()
            # reading the image
            # testImage = imread("Tree.png")

            # displaying the image
            # imshow(testImage)
            # show()
