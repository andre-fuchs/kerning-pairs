"""
Create a dictionary of all words occuring in the text samples including their count. This will be used to generate a text including the relevant kerning pairs.
"""

import os
import glob
import timeit
from collections import defaultdict, OrderedDict
import json
from tqdm import tqdm


LANGUAGES = [
    "cs",
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

LANGUAGES.sort()


start = timeit.default_timer()

# Parse text and count words
for LANGUAGE in LANGUAGES:
    dictionary = defaultdict(lambda: 1)
    for path in tqdm(glob.glob("text/" + LANGUAGE + "/*.txt")):
        with open(path, "r") as file:
            text = file.read().replace("\n", " ")
            words = text.split()
            for word in words:
                dictionary[word] += 1                    

    print(LANGUAGE, len(dictionary), 'uncleaned "words" collected')

    # Sort
    sorted_dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
    
    # Write out
    directory = "count/by_language/" + LANGUAGE + "/"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    file = open(directory + "words.json", "w")
    file.write(json.dumps(sorted_dictionary, indent=4, sort_keys=False))
    file.close()

stop = timeit.default_timer()
print("Execution Time: ", stop - start)
