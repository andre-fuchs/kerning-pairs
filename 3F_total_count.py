""" 
This script merge all language specific letter pairs to a global total.
Using the highscores instead of the total sum or an average no relevant 
pair of any language gets lost or ranked down.
"""


import json
import operator
from collections import defaultdict
from pprint import pprint


LANGUAGES = [
    'cs',
    'de',
    'en',
    'es',
    'et',
    'fi',
    'fr',
    'hu',
    'it',
    'nl',
    'no',
    'pl',
    'pt',
    'se',
    'sv',
    'da',
    'hr',
    'sl',
    'lt',
    'tr',
    'lv',
    'ro',
    'sk',
    'sq',
]


QUOTES = ['"', "'", '«', '»', '‘', '’', '‚', '‛', '“', '”', '„', '‟', '‹', '›']


# HIGHSCORES
globalLetterPairs = {}
for LANGUAGE in LANGUAGES:
    # Dictionaries to store all pairs containing quotes
    # To generate all possible stylistic alternates
    leftQuotes = defaultdict(lambda: 1)
    rightQuotes = defaultdict(lambda: 1)
    with open('count/by_language/' + LANGUAGE + '/list.json', 'r') as inputList, \
         open('count/by_language/' + LANGUAGE + '/dictionary.json', 'r') as inputDict:
        letterPairs = dict(json.load(inputList))
        totalValue = letterPairs['total']
        print(LANGUAGE, 'Raw number of pairs:', len(letterPairs))

        # Sum up all quotes
        parentDict = json.load(inputDict)
        for leftLetter, childrenDict in parentDict.items():
            for rightLetter, count in childrenDict.items():
                if leftLetter in QUOTES:
                    leftQuotes[rightLetter] += count
                if rightLetter in QUOTES:
                    rightQuotes[leftLetter] += count
        
        # Remove all keys containing quotes
        letterPairs = {k: v for k, v in letterPairs.items() if not any(QUOTE in k for QUOTE in QUOTES)}
        print(LANGUAGE, 'Without quotes', len(letterPairs))

        # Overwrite/add pairs containing representative quote characters
        for rightLetter, count in leftQuotes.items():
            for QUOTE in ['"', '„', '«', '»']:
                letterPairs[QUOTE + rightLetter] = count
        for leftLetter, count in rightQuotes.items():    
            for QUOTE in ['"', '«', '»']:
                letterPairs[leftLetter + QUOTE] = count
        print(LANGUAGE, 'With all placeholder quotes', len(letterPairs))

        # Clamp below minimum count of 1 per book (100 pages à 3000 characters)    
        letterPairs = {k: v/totalValue * 3000 * 100 for k, v in letterPairs.items()}
        
        # Stores the highest existing value of the given languages
        globalLetterPairs = { key: letterPairs.get(key, 0) \
            if letterPairs.get(key, 0) > globalLetterPairs.get(key, 0) else globalLetterPairs.get(key, 0) \
            for key in set(letterPairs) | set(globalLetterPairs) }


# SORTING
globalLetterPairs = sorted(globalLetterPairs.items(), key=operator.itemgetter(1), reverse=True)
globalLetterPairsDict = {key: value for (key, value) in globalLetterPairs}


# OUTPUT
with open('count/total/list.json', 'w') as output_a, \
     open('count/total/dictionary.json', 'w') as output_b:
    output_a.write(json.dumps(globalLetterPairs, indent=4, ensure_ascii=False))
    output_b.write(json.dumps(globalLetterPairsDict, indent=4, ensure_ascii=False))

