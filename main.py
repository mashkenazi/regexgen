# Akiva Ashkenazi

import secrets

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

class Token:

    def __init__(self, tokenstr, modstr):
        self.negate = 0
        self.values = []
        self.modifier = []

        # parse character class
        if tokenstr == '.':
            self.negate = 1
            self.values = []
        else:
            if tokenstr[1] == '^':
                # set negation and skip "^" char
                self.negate = 1
                i = 1
            else:
                i = 0
            # take off the brackets from the token
            tokenstr = tokenstr[1:-1]
            # if token has one char, just add it to values
            if len(tokenstr) == 1:
                self.values = [tokenstr]
            else:
                while i < len(tokenstr):
                    # check if current char is start of a range, and add the range to values if so
                    if i < len(tokenstr) - 2:
                        if tokenstr[i] in letters:
                            if tokenstr[i + 1] == '-':
                                if tokenstr[i + 2] in letters:
                                    start = letters.index(tokenstr[i])
                                    end = letters.index(tokenstr[i + 2])
                                    if start > end:
                                        tmp = start
                                        start = end
                                        end = tmp
                                    for j in range(start, end):
                                        self.values.append(letters[j])
                                    self.values.append(letters[end])
                                    i = i + 3
                                    continue
                        if tokenstr[i] in digits:
                            if tokenstr[i + 1] == '-':
                                if tokenstr[i + 2] in digits:
                                    for j in range(int(tokenstr[i]), int(tokenstr[i + 2])):
                                        self.values.append(str(j))
                                    self.values.append(tokenstr[i + 2])
                                    i = i + 3
                                    continue
                    # will only get here if didn't find a range above, so just add current char to values
                    self.values.append(tokenstr[i])
                    i = i + 1

                # remove repetition in values
                self.values = set(self.values)
                self.values = list(self.values)

        # parse modifier
        if modstr == '+':
            self.modifier = range(1, 99999)
        if modstr == '?':
            self.modifier = [0, 1]
        if modstr == '*':
            self.modifier = range(0, 99999)
        if modstr[0] == '{':
            botrange = ""
            isrange = False
            i = 1
            while i < len(modstr):
                # if we find a "}", then not a range
                if modstr[i] == '}':
                    break
                # if we find a ",', then is a range
                if modstr[i] == ',':
                    isrange = True
                    break
                botrange = botrange + modstr[i]
                i = i + 1
            # parse the range
            if isrange:
                i = i + 1
                toprange = ""
                while i < len(modstr):
                    if modstr[i] == '}':
                        break
                    toprange = toprange + modstr[i]
                    i = i + 1
                self.modifier = range(int(botrange), int(toprange) + 1)
            else:
                self.modifier = [int(botrange)]

        # negate if necessary
        if self.negate == 1:
            # take all possible char values other than newline, and remove values from input regex
            newvalues = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
                         '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                         '{', '|', '}', '~', ' ']
            for x in self.values:
                newvalues.remove(x)
            self.values = newvalues

    # function to produce a string based on data in Token
    def produce(self):
        answer = ""
        modind = secrets.randbelow(len(self.modifier))
        mod = self.modifier[modind]
        for i in range(mod):
            index = secrets.randbelow(len(self.values))
            mychar = self.values[index]
            answer = answer + mychar
        return answer


# def subpattern(inputexp, index):
#     exp = ""
#     i = 1
#     while i < len(inputexp) - 1:
#         if inputexp[i] == '.':
#             i = i + 1
#             modstr = ""
#             while True:
#                 if inputexp[i] == ')':
#                     break
#                 elif inputexp[i] == '.' or inputexp[i] == '[' or inputexp[i] == '/':
#                     break
#                 else:
#                     modstr = modstr + inputexp[i]
#                 i = i + 1
#             if modstr == "":
#                 modstr = "{1}"
#             newtoken = Token(".", modstr)
#             exp = exp + newtoken.produce()
#         elif inputexp[i] == '[':
#             tokenstr = ""
#             while True:
#                 if inputexp[i] == ']':
#                     tokenstr = tokenstr + inputexp[i]
#                     break
#                 tokenstr = tokenstr + inputexp[i]
#                 i = i + 1
#             i = i + 1
#             modstr = ""
#             if inputexp[i] == '?' or inputexp[i] == '*' or inputexp[i] == '+' or inputexp[i] == '{':
#                 while True:
#                     if inputexp[i] == '}':
#                         modstr = modstr + inputexp[i]
#                         i = i + 1
#                         break
#                     elif inputexp[i] == '.' or inputexp[i] == '[' or inputexp[i] == '/':
#                         break
#                     else:
#                         modstr = modstr + inputexp[i]
#                     i = i + 1
#             if modstr == "":
#                 modstr = "{1}"
#             newtoken = Token(tokenstr, modstr)
#             exp = exp + newtoken.produce()
#         else:
#             literalstr = ""
#             while True:
#                 literalstr = literalstr + inputexp[i]
#                 i = i + 1
#                 if inputexp[i] == '[' or inputexp[i] == '.':
#                     exp = exp + literalstr
#                     break
#     return [i, exp]


def generate(inputexp, times):
    output = []
    if inputexp[0] != '/':
        print("Wrong format.")
        return
    for x in range(0, times):
        exp = ""
        i = 1
        while i < len(inputexp) - 1:
            if inputexp[i] == '.':
                i = i + 1
                modstr = ""
                while True:
                    if inputexp[i] == '.' or inputexp[i] == '[' or inputexp[i] == '/':
                        break
                    else:
                        modstr = modstr + inputexp[i]
                    i = i + 1
                if modstr == "":
                    modstr = "{1}"
                newtoken = Token(".", modstr)
                exp = exp + newtoken.produce()
            elif inputexp[i] == '[':
                tokenstr = ""
                while True:
                    if inputexp[i] == ']':
                        tokenstr = tokenstr + inputexp[i]
                        break
                    tokenstr = tokenstr + inputexp[i]
                    i = i + 1
                i = i + 1
                modstr = ""
                if inputexp[i] == '?' or inputexp[i] == '*' or inputexp[i] == '+' or inputexp[i] == '{':
                    while True:
                        if inputexp[i] == '}':
                            modstr = modstr + inputexp[i]
                            i = i + 1
                            break
                        elif inputexp[i] == '.' or inputexp[i] == '[' or inputexp[i] == '/':
                            break
                        else:
                            modstr = modstr + inputexp[i]
                        i = i + 1
                if modstr == "":
                    modstr = "{1}"
                newtoken = Token(tokenstr, modstr)
                exp = exp + newtoken.produce()
            else:
                literalstr = ""
                while True:
                    literalstr = literalstr + inputexp[i]
                    i = i + 1
                    if inputexp[i] == '[' or inputexp[i] == '.':
                        exp = exp + literalstr
                        break
        output.append(exp)
    return output


if __name__ == '__main__':

    test11 = "/[-+]?[0-9]{1,16}[.][0-9]{1,6}/"
    test12 = 2

    test21 = "/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{8}/"
    test22 = 5

    test31 = "/.{8,12}/"
    test32 = 4

    test41 = "/[^aeiouAEIOU0-9]{5}/"
    test42 = 10

    test51 = "/[a-f-]{5}/"
    test52 = 3

    test1 = generate(test11, test12)
    test2 = generate(test21, test22)
    test3 = generate(test31, test32)
    test4 = generate(test41, test42)
    test5 = generate(test51, test52)

    print("Test 1:")
    for i in test1:
        print(i)

    print("Test 2:")
    for i in test2:
        print(i)

    print("Test 3:")
    for i in test3:
        print(i)

    print("Test 4:")
    for i in test4:
        print(i)

    print("Test 5:")
    for i in test5:
        print(i)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
