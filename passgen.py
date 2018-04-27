import urllib.request
import secrets
from functools import reduce
import operator
import sys
import math

wordurl = 'https://raw.githubusercontent.com/first20hours/google-10000-english/'\
          'f0a9af2435f416d974da03200dbdd967a258eb78/google-10000-english-usa-no-swears-medium.txt'

def uniqueRandomPicks(n, pickrange, randbelow=secrets.randbelow, verbose=False):
    """Pick n unique items out of a range using a cryptographically secure random
       number generator by default."""
    if n >= pickrange:
        raise RangeError("n must be smaller than pickrange")
    choices = reduce(operator.mul, range(pickrange, pickrange - n, -1))
    if verbose:
        print(f'{choices} possibilities, {math.log2(choices)} bits of entropy.', file=sys.stderr)
    choicelst = randbelow(choices)
    tmp = []
    for idxrange in range(pickrange, pickrange - n, -1):
        tmp.append(choicelst % idxrange)
        choicelst = choicelst // idxrange
    choicelst = tmp
    picked = []
    for choice in choicelst:
        for prevchoice in picked:
            if choice >= prevchoice:
                choice += 1
        picked.append(choice)
        picked.sort()
        yield choice

def createPassword(nwords=4):
    with urllib.request.urlopen(wordurl) as response:
        words = response.read().decode('utf-8').split()
    words = [w.capitalize() for w in words]
    randpicks = uniqueRandomPicks(nwords, len(words), verbose=True)
    return ''.join(words[choice] for choice in randpicks)
