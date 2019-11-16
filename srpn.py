import sys
import random
import traceback


class SRPN:

    def __init__(self, overSaturation=None, underSaturation=None, stackOverflow=None):

        self.userInput = []

        self.operands = ['+', '-', '*', '/', '%', '^', 'd', 'r', '#']

        self.stack = []

        self.overSaturation = overSaturation if overSaturation is not None else 2147483647

        self.underSaturation = underSaturation if overSaturation is not None else -2147483647

        self.stackOverflow = stackOverflow if stackOverflow is not None else 23

        self.rNumbers = [1804289383, 846930886, 1681692777,
                         1714636915, 1957747793, 424238335,
                         719885386, 1649760492, 596516649,
                         1189641421, 1025202362, 1350490027,
                         783368690, 1102520059, 2044897763,
                         1967513926, 1365180540, 1540383426,
                         304089172, 1303455736, 35005211,
                         521595368]

        self.stackOverflow = 23

        self.operations = {
            '+': (lambda a, b: a + b),
            '-': (lambda a, b: a - b),
            '*': (lambda a, b: a * b),
            '/': (lambda a, b: a // b),
            '%': (lambda a, b: a % b),
            '^': (lambda a, b: pow(a, b)),
            'r': (lambda a: self.rNumbers[a % len(self.rNumbers)]),
        }

        self.currentR = 0

    def start(self):

        print("You can now start interacting with the SRPN calculator.")

        while True:

            self.getInput()
            self.calculator()

    def getInput(self):

        self.userInput = []

        while True:
            try:
                self.userInput.extend(list(input().split()))
            except Exception as e:
                print(e)
            if self.userInput[-1] == '=':
                del(self.userInput[-1])
                break
            elif self.userInput[-1] == '\n':
                break
            elif self.userInput[-1] == 'd':
                self.printStack()
                del(self.userInput[-1])
            

    def calculator(self):
        try:
            while (any(element in self.userInput for element in self.operands)):
                for i, current in enumerate(self.userInput):
                    if current in self.operands:
                        if current == 'r':
                            self.userInput[i] = self.operations[current](
                                self.currentR)
                            self.currentR += 1
                            continue
                        if current == 'd':
                            self.stack.extend(self.userInput[:i])
                            self.printStack()
                            del(self.userInput[i])
                            break
                        if current == '#':
                            j = i + 1
                            while self.userInput[j] != '#':
                                j += 1
                            self.userInput = self.userInput[:i] + \
                                self.userInput[j+1:]
                            break
                        try:
                            a = int(self.userInput[i-2])
                            b = int(self.userInput[i-1])
                            result = self.operations[current](a, b)
                            if (result >= self.overSaturation):
                                result = self.overSaturation
                            elif (result <= self.underSaturation):
                                result = self.underSaturation
                        except ValueError:
                            print("Stack Overflow.")
                            return

                        self.userInput[i] = result
                        del(self.userInput[i-1])
                        del(self.userInput[i-2])
                        break

                    else:
                        try:
                            int(current)
                        except ValueError:
                            print("Invalid operand {}.".format(current))

        except ZeroDivisionError:
            print("Division by zero.")
            return

        self.stack.extend(self.userInput)

        if len(self.stack) < self.stackOverflow:

            self.printResult()
        else:
            print("Stack Overflow.")

    def printResult(self):
        print(self.stack[-1])

    def printStack(self):
        for entry in self.stack:
            print(entry, '\t')
