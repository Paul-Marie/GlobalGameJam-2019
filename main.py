#!/usr/bin/env python3

from sys import argv, stderr, exit
from math import factorial

# Do not modify this class, his default comportement is necessary for the program
class   BadArgumentError(Exception):
    def __init__(self, message, errors = "BadArgumentError"):
        super().__init__(message)
        self.errors = errors

# Default object class
class   People():
    """ Definition of People class """
    def __init__(self, argument, total=0):
        """ Initialise Separation's instance and check little errors """
        pass

# Do not put more information in this function, it's must be clearer as possible
def     main():
    """ Main function who perform program's core action like arguments resolution """
    pass

# Don't touch at this except if u don't worry of problems
if __name__ == "__main__":
    #try:
    main()
    #except BaseException as error:
    #    stderr.write(str(type(error).__name__) + ": {}\n".format(error))
    #    exit(84)
