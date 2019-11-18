"""
Computes a Kern Score for each kerning pair
depening on FREQUENCY (text count), POPULARITY (use count) and NECESSITY (kern value).
Popularity and necessity determine a kern vector. The larger the kern value and "use count", 
the greater the kern vector. The score is the sum of the frequency and this kern vector.
All values normalized.
"""
# To Do: Rename all file names containing "vector" into "score"

import json
import operator
from math import sqrt
from tqdm import tqdm
from statistics import mean


QUOTES = ['"', "'", '«', '»', '‘', '’', '‚', '‛', '“', '”', '„', '‟', '‹', '›']


# Praxis
with open('count/fonts/googleFontsKernDumpList.json', 'r') as input_a, \
     open('count/total/relevant_kerning_pairs.json', 'r') as input_b, \
     open('count/fonts/googleFontsKernVectorDictionary.json', 'w') as output_a, \
     open('count/fonts/googleFontsKernVectorList.json', 'w') as output_b:

    kernDump = json.load(input_a)
    pairs = json.load(input_b)

    print('Raw Count:', len(kernDump.values()))
    useCounts = [value[0] for value in kernDump.values()]
    minimum = max(useCounts) * 0.02
    useCountsClamped = [value[0] for value in kernDump.values() if value[0] > minimum]  ## clamp at > 2 %
    print('Clamped Count', len(useCountsClamped))
    averageUseCount = mean(useCountsClamped)
    textCounts = [value for (key, value) in pairs if value > 1]
    averageTextCount = mean(textCounts)

    kerningPairs = {}
    for (key, textCount) in tqdm(pairs):
        if key in kernDump:
            value = kernDump[key]
        else:
            value = [0, 0, 0, 0, 0, 0]  # fallback values
        useCountNormalized = (value[0] / averageUseCount) * 0.25
        # kernValueNormalized = min(1.5, abs(sqrt(value[1] ** 2 + useCountNormalized ** 2)))
        kernValueNormalized = min(1.5, abs(value[1]))
        textCountNormalized = textCount / averageTextCount
        # Ignore all kerning values used less than 5 % of average
        if useCountNormalized <= 0.05:
            useCountNormalized = 0
            kernValueNormalized = 0 
        # kernVector = sqrt(useCountNormalized ** 2 + kernValueNormalized ** 2) if value[0] > 100 else 0
        # print(key, useCountNormalized, kernValueNormalized, textCountNormalized)

        if useCountNormalized > 0.05:
            score = useCountNormalized + kernValueNormalized + textCountNormalized
        else: 
            score = textCountNormalized

        # Whitelist Bonus
        bonus = 0.5 if any(letter in key for letter in QUOTES) else 0  
        score += bonus

        # differenz = score - textCountNormalized  # only necessary for charts
        kerningPairs[key] = (value[0], value[1], score, textCountNormalized, useCountNormalized, kernValueNormalized, bonus) 
    
    kerningPairsList = [(key, value[0], value[1], value[2], value[3], value[4], value[5], value[6]) for key, value in kerningPairs.items()]
    kerningPairsList.sort(key=operator.itemgetter(3), reverse=True)
    output_a.write(json.dumps(kerningPairs, indent=4, ensure_ascii=False))
    output_b.write(json.dumps(kerningPairsList, indent=4, ensure_ascii=False))
