# -*- coding: utf-8 -*-
#
# Decontractors - A Design by Contract(tm) implementation using Decorators
# Copyright (c) 2011 Thomas Perl <m@thp.io>
# http://thp.io/2011/decontractors/
#

from decontractors import *


@Precondition(lambda: x > 0 and y > 0)
@Postcondition(lambda: __return__ == (x + y))
def positive_nonzero_addition(x, y):
    return x + y

print positive_nonzero_addition(4, 1)

class ShoppingList:
    def __init__(self):
        self.total = 0
        self.limit = 10
        self.items = []

    upper_limit = Invariant(lambda: self.total < self.limit)

    @upper_limit
    def add(self, item, costs):
        self.total += costs
        self.items.append(item)


list = ShoppingList()
list.add('Bananas', 4.3)

try:
    list.add('Milk', 7)
except DecontractorException, de:
    print 'add failed. content now:', list.total, 'with', list.items

def mean(a, b):
    print 'called: mean(%d, %d)' % (a, b)
    a0, b0 = a, b

    precondition = lambda: (b >= a) and ((a+b) % 2 == 0)
    invariant = lambda: (b >= a) and ((a + b) == (a0 + b0))
    postcondition = lambda: (a == b) and (a == (a0 + b0)/2)

    with Contract(precondition, invariant, postcondition) as contract:
        while a != b:
            contract()
            a += 1
            b -= 1
            contract()

    print 'mean calculated:', a, b


mean(2, 20)

try:
    mean(20, 2)
except DecontractorException, de:
    print 'exception:', de.__class__

try:
    mean(5, 15)
except DecontractorException, de:
    print 'exception:', de.__class__

try:
    mean(2, 7)
except DecontractorException, de:
    print 'exception:', de.__class__

