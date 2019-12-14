""" 
Concatenate smaller text files to work around GitHub‘s limit of maximum 1000 files per directory.
"""


import os
import glob
from tqdm import tqdm
from shutil import move


LANGUAGES = [
    'cs',
    'cz',
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
    "da",
    "hr",
    "sl",
    "lt",
    "tr",
    "lv",
    "ro",
    "sk",
    "sq",
]


for LANGUAGE in LANGUAGES:
    print(LANGUAGE)
    outputCount = 0
    fileSize = 0
    text = ''
    for path in tqdm(glob.glob("text/" + LANGUAGE + "/*.txt")):            
        with open(path, "r") as inputFile:
            fileSize += os.fstat(inputFile.fileno()).st_size
            text += '\n' + inputFile.read()
            if fileSize > 200000:
                outputCount += 1
                fileSize = 0
                with open("text/" + LANGUAGE + "/grouped-" + str(outputCount) + ".txt", "w") as outputFile: 
                    outputFile.write(text)  # write file content
                text = ''
        os.remove(path)
