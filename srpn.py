import re


class SRPN:

    def __init__(self, overSaturation=None, underSaturation=None, stackOverflow=None):

        self.userInput = []

        self.operators = ['+', '-', '*', '/', '%', '^', 'd', 'r', '#','=']

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
            '=': (lambda a: a)
        }

        self.currentR = 0

        self.previous = 0

    def start(self):

        print("You can now start interacting with the SRPN calculator.")

        while True:

            self.getInput()


    def getInput(self):

        while True:
            self.userInput = []
            try:
                self.userInput.extend(list(input().split(' ')))
                if(len(self.userInput) > 1):
                    if self.userInput[-1] == '=':
                        del(self.userInput[-1])
                        self.createStack()
                        self.printResult()
                        break
            except Exception as e:
                print(e)
            if self.userInput[-1] == '=':
                self.printResult()
                break
            self.createStack()


    def createStack(self):

        while self.userInput:
         
            for i, element in enumerate(self.userInput):
                try:
                    number = int(element)
                    del(self.userInput[i])
                    if len(self.stack) + 1 > self.stackOverflow:
                        print("Stack Overflow!")
                        continue
                    else:
                        self.stack.append(number)
                        break
                except ValueError:
                    if element in self.operators:
                        if element == '#':
                            j = i + 1
                            while self.userInput[j] != '#':
                                j += 1
                            self.userInput = self.userInput[:i] + self.userInput[j+1:]
                            break
                        elif element == 'r':
                            if len(self.stack) + 1 > self.stackOverflow:
                                del(self.userInput[i])
                                print("Stack Overflow!")
                                break
                            else:
                                self.stack.append(self.operations[element](self.currentR))
                                self.currentR += 1
                                del(self.userInput[i])
                                break
                        elif element == 'd':
                            self.printStack()
                            del(self.userInput[i])
                            continue
                        else:
                            self.calculator(element)
                            del(self.userInput[i])
                            break
                    else:
                        string = self.userInput[-1]
                        del(self.userInput[-1])
                        self.userInput.extend(self.separateConcatenantedStrings(string))
                        break
                        #print("Unrecognized operator or opernad {}".format(element))



    def calculator(self, operator):

        try:
            if operator == '=':
                print(self.previous)
                return

            a = int(self.stack[-2])
            b = int(self.stack[-1])
            self.previous = b
            result = self.operations[operator](a, b)

            if (result >= self.overSaturation):
                result = self.overSaturation
            elif (result <= self.underSaturation):
                result = self.underSaturation

            self.stack[-1] = result
            del(self.stack[-2])

        except ValueError:
            print("Stack Underflow.")
            return

        except ZeroDivisionError:
            print("Divison by zero.")
            return

        except IndexError:
            print(self.stack, operator)
            print("Stack Underflow!")
            return

    def separateConcatenantedStrings(self, concatString):

        numbers = []
        operators = []

        stringList = re.split('(\D)', concatString)
        stringList = list(filter(lambda a: a != '', stringList))

        for string in stringList:
            try:
                numbers.append(int(string))
            except ValueError:
                if string in self.operators:
                    operators.append(string)
                else:
                    print("Unrecognized operator or operand {}.".format(string))
        
        numbers.extend(operators)

        return numbers        

    def printResult(self):
        print(self.stack[-1])

    def printStack(self):
        for entry in self.stack:
            print(entry, '\t')
