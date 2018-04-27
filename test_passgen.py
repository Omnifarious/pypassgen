import unittest, collections
import passgen
from functools import reduce
import operator

class UniqueRandomPicksTestMixin(object):
    def __init__(self, *args, choose=4, bagsize=5, **kargs):
        super().__init__(*args, **kargs)
        self.choose = choose
        self.bagsize = bagsize
        self.permutes = reduce(operator.mul,
                               range(bagsize, bagsize - choose, -1))

    def setUp(self):
        super().setUp()
        self.s = s = collections.defaultdict(list)
        for n in range(0, self.permutes):
           # Replace the regular secrets.randbelow with a lambda that just
           # returns the current element of the sequence
           tval = tuple(passgen.uniqueRandomPicks(self.choose,
                                                  self.bagsize,
                                                  randbelow=lambda x: n))
           s[tval].append(n) # Record which number generated this sequence

    def test_correctCount(self):
        self.assertEqual(len(self.s), self.permutes,
                         "Not all possible unique permutations generated.")

    def test_onlyOne(self):
        for k, v in self.s.items():
            self.assertEqual(len(v), 1,
                             msg=f"Permutation {k!r} shows up for "\
                                  "these values: {v!r}")
 
    def test_validPermutes(self):
        # Always print out v so we know which number to feed in to cause
        # the issue.
        for k, v in self.s.items():
            for k_item in k:
                self.assertIsInstance(k_item, int, msg="For {k}:{v}")
            self.assertTrue(all(0 <= n < self.bagsize for n in k),
                            msg=f"Some value in {k}:{v} is out of range.")
            self.assertEqual(len(set(k)), len(k),
                             msg=f"duplicate values in {k}:{v}")

class UniqueRandomPicks4From5(UniqueRandomPicksTestMixin, unittest.TestCase):
    def __init__(self, *args, **kargs):
        super().__init__(*args, choose=4, bagsize=5, **kargs)

class UniqueRandomPicks5From6(UniqueRandomPicksTestMixin, unittest.TestCase):
    def __init__(self, *args, **kargs):
        super().__init__(*args, choose=5, bagsize=6, **kargs)
