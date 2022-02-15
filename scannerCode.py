import string


class Scanner():

    def __init__(self, text):
        self.text = text
        self.tokens, self.errors = self.scan(text)
        self.num_tokens = len(self.tokens)
        if len(self.errors)>0:
            self.error = True
        else:
            self.error = False
        if self.num_tokens > 0:
            self.current_i = 0
            self.finished = False
        else:
            self.finished = True

    def next_token(self):
        if self.current_i < (self.num_tokens - 1):
            self.current_i += 1
        else:
            self.finished = True

    def current_token(self):
        if self.finished:
            return ('FINISHED')
        else:
            return self.tokens[self.current_i]

    def reset_i(self):
        self.current_i =0

    def get_length(self):
        return self.num_tokens

    def get_errors(self):
        return self.errors

    def get_tokens(self):
        return self.tokens

    def get_token(self):
        if self.current_i <= (self.num_tokens - 1):
            token = self.tokens[self.current_i]
            self.current_i+=1
            return token
        else:
            self.finished =True
            return ('FINISHED')

    def is_finished (self) :
        if self.num_tokens > 0:
            self.current_i = 0
            self.finished = False
        else:
            self.finished = True
        return self.finished

    def check(self):
        return self.error

    def scan(self,file1):
        if str(type(file1)) == "<class 'str'>":
            plain = file1.splitlines(True)

        elif str(type(file1)) == "<class 'list'>":
            plain = file1
        reserved_names = {
            'if': 'IF',
            'repeat': 'REPEAT',
            'until': 'UNTIL',
            "then": "THEN",
            "else": "ELSE",
            "end": "END",
            "read": "READ",
            "write": "WRITE"
        }
        idx=0
        special_names = {"+": "PLUS",
                         "-": "MINUS",
                         "/": "DIV",
                         "*": "MULT",
                         "<": "LESSTHAN",
                         "(": "OPENBRACKET",
                         ")": "CLOSEDBRACKET",
                         ';': 'SEMICOLON',
                         ':=': "ASSIGN",
                         '=': "EQUAL"
                         }

        words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        symbols = ["+", "-", "/", "*", "=", "<", "(", ")", ";", ">"]
        alphapet = list(string.ascii_letters)
        spaces = ['\n', ' ', "	"]
        numbers = [a for a in string.digits]
        tokens = []
        error = []
        state = 'START'
        tokenType = ""
        token = ""
        opFlag = False
        aFlag = False
        for j, line in enumerate(plain):
            for i, ch in enumerate(line):
                if state == 'START':
                    if ch == '{':
                        state = "INCOMMENT"
                        idx =j

                    elif ch == ':':
                        state = "INASSIGN"
                        tokenType = "Assign"

                    elif ch in symbols:

                        state = "DONE"
                        token += ch
                        tokenType = "Special Symbol"

                    elif ch in alphapet:

                        state = "INID"
                        token += ch
                        tokenType = "Identifier"

                    elif ch in numbers:

                        state = "INNUM"
                        token += ch
                        tokenType = "Number"
                    elif ch in spaces:
                        state = "START"
                    else:
                        state = "ERROR"

                elif state == "INCOMMENT":

                    if ch == '}':
                        state = "START"
                        token = ""
                    else:
                        state = "INCOMMENT"

                elif state == "INASSIGN":

                    if ch == '=':
                        token = ":="
                        state = "DONE"

                    else:
                        state = "ERROR"
                        token = ""

                elif state == "INID":

                    if ch in alphapet:
                        token += ch
                        if token in words:
                            tokenType = "Reserved Word"
                            state = "DONE"

                    elif ch in numbers:
                        token += ch

                    elif (ch in spaces) or (ch in symbols):
                        state = "DONE"
                        opFlag = True
                    elif ch == ":":
                        state = "DONE"
                        aFlag = True

                    else:
                        state = "ERROR"

                elif state == "INNUM":

                    if ch in numbers:
                        token += ch

                    elif (ch in spaces) or (ch in symbols):

                        state = "DONE"
                        opFlag = True
                    else:
                        state = "ERROR"
                        token = ""
                if state == "DONE":
                    temp1 = token
                    temp2 = tokenType
                    # temp3=
                    if tokenType == "Reserved Word":
                        temp3 = reserved_names[token]
                    elif tokenType == "Number":
                        temp3 = "NUMBER"
                    elif tokenType == "Special Symbol":
                        temp3 = special_names[token]
                    elif tokenType == "Identifier":
                        temp3 = "IDENTIFIER"
                    elif tokenType == "Assign":
                        temp3 = "ASSIGN"
                    # yield temp1, temp2, temp3
                    tokens.append((temp3, temp1))
                    state = "START"
                    token = ""
                    tokenType = ""
                    if (opFlag == True) and (ch in symbols):

                        temp1 = ch
                        temp2 = "Special Symbol"
                        temp3 = special_names[ch]
                        tokens.append((temp3, temp1))
                    elif aFlag == True:
                        state = "INASSIGN"
                        token = ":"
                        tokenType = "Assign"

                    aFlag = False
                    opFlag = False
                if state == "ERROR":
                    if len(token) > 0:
                        if tokenType == "Reserved Word":
                            temp3 = reserved_names[token]
                        elif tokenType == "Number":
                            temp3 = "NUMBER"
                        elif tokenType == "Special Symbol":
                            temp3 = special_names[token]
                        elif tokenType == "Identifier":
                            temp3 = "IDENTIFIER"
                        elif tokenType == "Assign":
                            temp3 = "ASSIGN"
                        tokens.append((temp3, temp1))
                    error.append([j, i])
                    state = "START"
                    token = ""
                    tokenType = ""

        if state == "INCOMMENT":
            error.append([idx, 0])


        return tokens, error


if __name__ == "__main__":

    with open("test1.txt") as f: #open file
        lines = f.readlines()
    scanner = Scanner(lines)
    # text = adjust(lines)
    # tok,err = scan(lines)
    # print(S.check())
    lst = scanner.get_tokens()
    # print(lst)
    # l = S.get_length()
    # print(l)
    # for i in range(l):
    #     print(S.get_token())
    # print(S.get_token())
    # print(S.get_token())
    count = 0
    for i in range(scanner.num_tokens):
        count += 1
        print(scanner.current_token())
        scanner.next_token()
    print(count)

    textfile = open("out_file.txt", "w")
    for element in lst:
        textfile.write(element[1]+','+element[0] + "\n")
    textfile.close()
