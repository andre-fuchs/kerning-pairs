""" 
Clean-up all texts.
Removes short lines and empty .TXT files.
This could be improved to remove more redundant parts.
"""

# https://askubuntu.com/a/726242

import os
import glob
from tqdm import tqdm


LANGUAGES = [
    # 'cs',
    # 'cz',
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


def filter_text(line):
    if '==' in line or len(line) < 80:
        return False
    else:
        return True


checked = 0
removed = 0

# https://codereview.stackexchange.com/a/145128
for LANGUAGE in LANGUAGES:
    for path in tqdm(glob.glob('text/' + LANGUAGE + '/*.txt')):

        with open(path, 'r') as file:
            lines = file.readlines()
        with open(path, 'w') as file:
            lines = filter(filter_text, lines)
            file.writelines(lines) 
            checked += 1

        if os.path.getsize(path) == 0:
            try:
                os.remove(path)
                removed += 1
            except OSError:
                print('Error', path)


print('Checked', checked)
print('Removed Total', removed)