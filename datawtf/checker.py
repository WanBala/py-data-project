import numpy as np
import pandas as pd
import basics

RUN_COLUMN = 0
RUN_ROW = 1

class SelfDefinedError(Exception):
    def __init__(self, arg):
        self.args = arg
        self.index = None
        self.error = None


class Checker():
    def __init__(self):
        self._func = None
        self.content = None
        self.args = None
        self._errorhandler = None

    def loadFile(self, Filename):
        self.content = basics.loadFile(Filename)
    
    def loadFunction(self, func, **args):
        self._func = func
        self.args = args

    def loadErrorHandler(self, func):
        self._errorhandler = func

    def run(self, target=RUN_ROW):
        self.inspection()
        rows, columns = self.getShape()
        if target == RUN_COLUMN:
            go = columns
        else:
            go = rows
        for i in range(go):
            try:
                self._func(self.getContent(i, target),**self.args)
            except SelfDefinedError as e:
                if self._errorhandler:
                    e.index = i
                    self._errorhandler(e)
                else:
                    self.defaultMessage(i)
            except:
                self.defaultMessage(i)

    def inspection(self):
        if not self.content or not self._func:
            raise Exception("Function and file should be loaded.")      

    
    def getShape(self):
        if self.content:
            return self.content.shape
    
    def getContent(self, index, target=RUN_ROW):
        if target == RUN_ROW:
            return self.content.iloc[index, :]
        elif target == RUN_COLUMN:
            return self.content.iloc[:, index]

    def defaultMessage(self, index):
        print("Get Error in Line {0}".format(index + 1))