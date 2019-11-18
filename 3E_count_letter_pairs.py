""" 
Counting letter pairs of a batch of texts.
Using defaultdicts for the counting itself is about 300 times faster 
than using pandas’ dataframe, I had to find out. 
The dataframe will be created from the resulting dict at the end 
... in case you need it, I did not use so far.
"""


import os
import glob
import timeit
from collections import defaultdict
import pandas as pd
import json
from tqdm import tqdm


LANGUAGES = [
    'cs',
    # 'de',
    # 'en',
    # 'es',
    # 'et',
    # 'fi',
    # 'fr',
    # 'hu',
    # 'it',
    # 'nl',
    # 'no',
    # 'pl',
    # 'pt',
    # 'se',
    # 'sv',
    # 'da',
    # 'hr',
    # 'sl',
    # 'lt',
    # 'tr',
    # 'lv',
    # 'ro',
    # 'sk',
    # 'sq',
]

LANGUAGES.sort()

LETTERS = [ ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', 'ˆ', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'Ā', 'ā', 'Ă', 'ă', 'Ą', 'ą', 'Ć', 'ć', 'Ĉ', 'ĉ', 'Ċ', 'ċ', 'Č', 'č', 'Ď', 'ď', 'Đ', 'đ', 'Ē', 'ē', 'Ĕ', 'ĕ', 'Ė', 'ė', 'Ę', 'ę', 'Ě', 'ě', 'Ĝ', 'ĝ', 'Ğ', 'ğ', 'Ġ', 'ġ', 'Ģ', 'ģ', 'Ĥ', 'ĥ', 'Ħ', 'ħ', 'Ĩ', 'ĩ', 'Ī', 'ī', 'Ĭ', 'ĭ', 'Į', 'į', 'İ', 'ı', 'Ĳ', 'ĳ', 'Ĵ', 'ĵ', 'Ķ', 'ķ', 'ĸ', 'Ĺ', 'ĺ', 'Ļ', 'ļ', 'Ľ', 'ľ', 'Ŀ', 'ŀ', 'Ł', 'ł', 'Ń', 'ń', 'Ņ', 'ņ', 'Ň', 'ň', 'ŉ', 'Ŋ', 'ŋ', 'Ō', 'ō', 'Ŏ', 'ŏ', 'Ő', 'ő', 'Œ', 'œ', 'Ŕ', 'ŕ', 'Ŗ', 'ŗ', 'Ř', 'ř', 'Ś', 'ś', 'Ŝ', 'ŝ', 'Ş', 'ş', 'Š', 'š', 'Ţ', 'ţ', 'Ť', 'ť', 'Ŧ', 'ŧ', 'Ũ', 'ũ', 'Ū', 'ū', 'Ŭ', 'ŭ', 'Ů', 'ů', 'Ű', 'ű', 'Ų', 'ų', 'Ŵ', 'ŵ', 'Ŷ', 'ŷ', 'Ÿ', 'Ź', 'ź', 'Ż', 'ż', 'Ž', 'ž', 'ſ', '«', '»', '‘', '’', '‚', '‛', '“', '”', '„', '‟', '‹', '›']


start = timeit.default_timer()


# Parse text and count letter pairs
for LANGUAGE in LANGUAGES:
    dictionary = defaultdict(lambda: defaultdict(lambda: 1))
    total = 0
    for path in tqdm(glob.glob('text/' + LANGUAGE + '/*.txt')):
        with open(path, 'r') as file:
            text = file.read().replace('\n', ' ')
            letterCache = text[:1]
            for letter in text[1:]:
                # Uncomment this if statement to get unfiltered results
                # REDUNDANT: LETTERS OUTSIDE THE SET WON'T BE MARKED AS RELEVANT LATER ON, SEE SCRIPT 3G_MARK_POTENTIAL_PAIRS
                if all (key in LETTERS for key in (letter, letterCache)):
                    dictionary[letterCache][letter] += 1
                    total += 1
                letterCache = letter

    print(LANGUAGE, 'total:', total)
    # Convert dictionary to list and dataframe
    list = [('total', total)]
    for left_letter in dictionary:
        for right_letter in dictionary[left_letter]:
            list.append((left_letter + right_letter, dictionary[left_letter][right_letter]))
    list = sorted(list, key=lambda x: x[1], reverse=True)
    dataframe = pd.DataFrame.from_dict(dictionary, orient='index')

    # Write out
    directory = 'count/by_language/' + LANGUAGE + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file = open(directory + 'dictionary.json', 'w')
    file.write(json.dumps(dictionary, indent=4, sort_keys=True))
    file.close()
    file = open(directory + 'list.json', 'w')
    file.write(json.dumps(dict(list), indent=4))
    file.close()
    dataframe.to_pickle(directory + 'dataframe.pkl')
    # dataframe.to_hdf(directory + 'dataframe.h5', key='dataframe', mode='w')  # expensive


stop = timeit.default_timer()
print('Execution Time: ', stop - start)

