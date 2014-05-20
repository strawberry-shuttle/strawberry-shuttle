from collections import deque as dq

__author__ = 'Vijay Ganesan'


class MedianBuffer:
    """
    A buffer meant to hold a small (n < 10) number of values and efficiently calculate and return data
    """
    def __init__(self,__max=10):
        self.__internallist = dq()
        self.__sortedlist = []
        self.count = 0
        self.median = 0.0
        self.mean = 0.0
        self.sum = 0.0
        self.__max = __max
        return

    def insert(self, num):
        #TODO: Add try-catch for int TypeError
        self.sum += num
        if self.count == self.__max:
            self.sum -= self.__internallist[self.count-1]
            self.__internallist.pop()
        else:
            self.count += 1
        self.mean = self.sum/self.count
        self.__internallist.appendleft(num)
        self.__sortedlist = list(self.__internallist)
        self.__sortedlist.sort()
        self.median = self.__sortedlist[self.count/2]
        return




