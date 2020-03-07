class Iterable:
    '''
    Class for an iterable object based on a list
    '''
    def __init__(self, lst = None):
        if lst != None:
            self._list = lst
        else:
            self._list = []

    def __setitem__(self, idx, val):
        self._list[idx] = val

    def __getitem__(self, idx):
        return self._list[idx]

    def __delitem__(self, item):
        del self._list[item]

    def __next__(self):
        if self._n < len(self._list): 
            self._n += 1
            return self._list[self._n - 1]
        else:
            raise StopIteration

    def __iter__(self):
        self._n = 0
        return self

    def __repr__(self):
        return str(self._list)

    def __len__(self):
        return len(self._list)

    def __eq__(self, ob):
        if len(self) != len(ob):
            return False
        for i in range(len(ob)):
            if self._list[i] != ob[i]:
                return False
        return True

    def append(self, item):
        self._list.append(item)

def less(a, b):
    return a < b

def sort(lst, cmp = less):
    '''
    Shell sort
    '''
    count = len(lst) // 2
    while count > 0:
        for pos in range(count):
            gapInsertionSort(lst, pos, count, cmp)
        count = count // 2

def gapInsertionSort(lst, start, step, cmp):
    '''
    Insertion sort with gap of dimension step
    '''
    for i in range(start + step, len(lst), step):
        val = lst[i]
        j = i
        while j >= step and cmp(val, lst[j-step]):
            lst[j] = lst[j-step]
            j = j-step

        lst[j] = val

def true(ob, other):
    return True

def filter(lst, prop = true, other = None):
    '''
    A filter function to cut out unwanted elements from a list after a given property function
    '''
    result = []
    for i in lst:
        if prop(i, other):
            result.append(i)
    return result

import unittest 

class test_assig9(unittest.TestCase):
    def setUp(self):
        self.it = Iterable()
        self.it2 = Iterable([1, 2, 3])

    def test_Iterable(self):
        for i in range(len(self.it2)):
            self.assertEqual(i + 1, self.it2[i])

        self.it.append(0)
        self.assertEqual(self.it, [0])
        self.it[0] = -1
        self.assertEqual(self.it[0], -1)
        self.it.append(1)
        del self.it[0]
        self.assertEqual(self.it, [1])

    def test_sort(self):
        self.it2.append(2)
        self.it2.append(4)
        self.it2.append(0)
        sort(self.it2)
        self.assertEqual(self.it2, [0, 1, 2, 2, 3, 4])

    def odd(self, nr):
        return nr % 2 == 1

    def test_filter(self):
        res = filter(self.it2, self.odd)
        self.assertEqual(res, [1, 3])

if __name__ == '__main__':
    unittest.main() 