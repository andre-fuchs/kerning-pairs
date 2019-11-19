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
    "count/total/relevant_kerning.txt", "w"
) as output:
    relevantGlobalKerningPairs = json.load(input_json)
    kerningTXT = ["nonu" + v[0] + "nuou\n" for v in relevantGlobalKerningPairs]
    output.writelines(kerningTXT)
