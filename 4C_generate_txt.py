""" 
This script generates a TXT file to be used for kerning with your favorite font editor.
Feel free to customize the padding to the left and right sides of the kerning pairs to your liking.
"""

import json

# TO DO:
# add stylistic alternates for QUOATES and en-/em-DASHES (maybe for (false) apostrophes, too)
# QUOTES = [ '‚', '„', '“', '”', '‘', '’', '«', '»', '‹', '›', '"', "'", ]
# Kombinatorik; Alle Ziffern + mathematische Zeichen + Klammern


with open("count/fonts/googleFontsKernVectorList.json", "r") as input_json, open(
    "result/relevant_kerning_with_padding.txt", "w"
) as outputPadded, open(
    "result/relevant_kerning_raw.txt", "w"
) as outputRaw:
    relevantGlobalKerningPairs = json.load(input_json)
    kerningPadded = ["nonu" + v[0] + "nuou\n" for v in relevantGlobalKerningPairs]
    kerningList =  [v[0] + " " for v in relevantGlobalKerningPairs]  # better .join() instead?
    outputPadded.writelines(kerningPadded)
    outputRaw.writelines(kerningList)
