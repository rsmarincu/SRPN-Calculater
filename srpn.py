"""
I decided to use an object oriente approach for this courswork because it allows for easier data storage and manipulation.
It also helps with code organization and allows for customisation and for features to be added in the future.
An additional python package that I used is the regular expressions package for some string manipulation.
"""

import re

#Creating the SRPN class.
class SRPN:

    # Defining the init method that allows for class instantiation with either custom under saturation, over saturation and maximum stack length 
    # or provides in-built ones. 

    
    def __init__(self, overSaturation=None, underSaturation=None, stackOverflow=None):

        # The user input will be stored as an array in this variable.
        self.userInput = []

        # All the operators that the class uses.
        self.operators = ['+', '-', '*', '/', '%', '^', 'd', 'r', '#', '=']

        # The result stack will be stored here.
        self.stack = []

        # Initializing the over saturation in case a custom one is not provided.
        self.overSaturation = overSaturation if overSaturation is not None else 2147483647

        # Initializing the under saturation in case a custom one is not provided.
        self.underSaturation = underSaturation if overSaturation is not None else -2147483647

        # Initializing the maximum stack length in case a custom one is not provided.
        self.stackOverflow = stackOverflow if stackOverflow is not None else 23

        #The pseudo-random values that ar accesed by the 'r' operator.
        self.rNumbers = [1804289383, 846930886, 1681692777,
                         1714636915, 1957747793, 424238335,
                         719885386, 1649760492, 596516649,
                         1189641421, 1025202362, 1350490027,
                         783368690, 1102520059, 2044897763,
                         1967513926, 1365180540, 1540383426,
                         304089172, 1303455736, 35005211,
                         521595368]
        
        # The lambda functions used to perform calculations are stored in a dictionary with the correspding operator ar a key.
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

        # A variable that keeps track of the current pseudo-random number.
        self.currentR = 0

        # Avariable that always stores the last value a calculation was performed on.
        self.previous = 0

    # This method is used to start the SRPN calculator. It prints a message that informs the user he can interact with it.
    # The calculator can be terminated by pressing Ctrl + C in the terminal.
    def start(self):

        print("You can now start interacting with the SRPN calculator.")

        while True:
            self.getInput()

    # This method is used to get the user input. It also peforms list manipulations on the input and calls the createStack function.
    def getInput(self):

        # This function should be repeated until the user terminates the run.
        while True:

            # The user input variable is initialised as an empty list every loop.
            self.userInput = []

            # Used exception handling for unexpected input.
            try:
                # The input is stored as a list, spliting it with and empty space.
                self.userInput.extend(list(input().split(' ')))

                # Removing all strings which are formed of empty spaces, including tabs.
                self.userInput = list(filter(None, self.userInput))

                # We check if the user used a one line input.
                if(len(self.userInput) > 1):
                    
                    # If the last item in the list is the '=' operator, we can start performing calculations.
                    if self.userInput[-1] == '=':

                        # Removing the '=' operator from the list and calling createStack and printResult then breaking the while loop.
                        del(self.userInput[-1])
                        self.createStack()
                        self.printResult()
                        break

            # Handle unexpected exception
            except Exception as e:
                print(e)
            
            # If the user use new line separated values, check if the last one is the '=' operator, print the result and break the loop.
            if self.userInput[-1] == '=':
                self.printResult()
                break

            # If not, we can call createStack.
            self.createStack()


    # Defining the createStack function. This method processes the user input and updates the stack with the results.
    def createStack(self):

        # Do the follwing while the userInput does not evaluate to False (while it has values).
        while self.userInput:

            # For the element at index i in userInput, perform the follwing.
            for i, element in enumerate(self.userInput):

                # Used exception handling the check if the current string can be converted into a integer.
                try:

                    # Store the current element into a number variable and delete it from the user input list.
                    number = int(element)
                    del(self.userInput[i])

                    # Check if there is an empty space in the stack. If not, print Stack Overflow and continue, else add the current number to the stack and break the for loop.
                    if len(self.stack) + 1 > self.stackOverflow:
                        print("Stack Overflow!")
                        continue
                    else:
                        self.stack.append(number)
                        break
                
                # If we get a ValueError, it means the current element might be an operator.
                except ValueError:

                    # If the current element is in our operator list, we can perform calculations. 
                    if element in self.operators:

                        # First we check if the current element is a '#', we can skip the elements in the user input list until another '#' is found. 
                        # After we found the next '#', we can remove the comment from the user input and break the for loop.
                        if element == '#':
                            j = i + 1
                            while self.userInput[j] != '#':
                                j += 1
                            self.userInput = self.userInput[:i] + \
                                self.userInput[j+1:]
                            break

                        # If the current element is 'r', check for stack overflow. If there is space in the stack, get the current random value,
                        # add it to the stack and increase the current random value index.
                        elif element == 'r':
                            if len(self.stack) + 1 > self.stackOverflow:
                                del(self.userInput[i])
                                print("Stack Overflow!")
                                break
                            else:
                                self.stack.append(
                                    self.operations[element](self.currentR))
                                self.currentR += 1
                                del(self.userInput[i])
                                break

                        # If the current element is 'd', delete it from the user input list and print the current stack.
                        # Else, it means that the current element can perform an operation. Call the calculator function.
                        elif element == 'd':
                            self.printStack()
                            del(self.userInput[i])
                            continue
                        else:
                            self.calculator(element)
                            del(self.userInput[i])
                            break
                    
                    # If the current element is not a number and an operand, store it into a variable to perform string maniulation on it.
                    else:
                        string = self.userInput[-1]
                        del(self.userInput[-1])
                        self.userInput.extend(self.separateConcatenantedStrings(string))
                        break


    # Defining the calculator method which takes an operator variable as an argument.
    def calculator(self, operator):

        # Used try: except: to handle stack underflow and division by zero error.
        try:
            # If the operator is '=' print the previous value.
            if operator == '=':
                print(self.previous)
                return

            # If not, then perform the coresponding operation from the operations dictionary on the last two values in the stack
            a = int(self.stack[-2])
            b = int(self.stack[-1])
            self.previous = b
            result = self.operations[operator](a, b)

            # Check if the result is smaller that under saturation or bigger than over saturation. If yes, the result gets the according value.
            if (result >= self.overSaturation):
                result = self.overSaturation
            elif (result <= self.underSaturation):
                result = self.underSaturation

            # Set the last value in the stack as the result and remove the second last from the stack.
            self.stack[-1] = result
            del(self.stack[-2])

        # If there is a value error it means that there is a number missing, hence a stack underflow.
        except ValueError:
            print("Stack Underflow.")
            return

        # Dividion by zero handling.
        except ZeroDivisionError:
            print("Divison by zero.")
            return

        # If there is no elements left in the stack, print stack underflow.
        except IndexError:
            print("Stack Underflow!")
            return

    # Defininf the method that separates concatenated strings, which takes the string as an argument.
    def separateConcatenantedStrings(self, concatString):

        # Initialize a numbers and operators array.
        numbers = []
        operators = []

        # Using regular expressions we can separate the string using anything that is not a number as a separator, storing the results as well as the separators.
        stringList = re.split('(\D)', concatString)

        # Remove the empty strings from the list using the filter method.
        stringList = list(filter(None, stringList))

        # Separate the numbers from the strings. If the string is not an operator, then print a message alerting the user.
        for string in stringList:
            try:
                numbers.append(int(string))
            except ValueError:
                if string in self.operators:
                    operators.append(string)
                else:
                    print("Unrecognized operator or operand {}.".format(string))

        # Add the operators list at the end of the numbers list.
        numbers.extend(operators)

        return numbers

    # Helper functions that print the last item in the stack and the entire stack.
    def printResult(self):
        print(self.stack[-1])

    def printStack(self):
        for entry in self.stack:
            print(entry, '\t')
