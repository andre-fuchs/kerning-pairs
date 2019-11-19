"""
This script filters all kerning pairs from all counted letter pairs 
and lists them sorted by count.
"""


import json
import operator
from collections import defaultdict
from tqdm import tqdm


LANGUAGES = [
    "cs",
    "de",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "hu",
    "it",
    "nl",
    "no",
    "pl",
    "pt",
    "se",
    "sv",
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

LANGUAGES.sort()

# Theory
file1 = open("shapes/01_potential_kerning_pairs.json", "r")
# file1 = open('shapes/01_test.json', 'r')
potentialKerningPairs = json.load(file1)
file1.close()
print("Potential Kerning Pairs", len(potentialKerningPairs))  # 20554

# Praxis
file2 = open("count/fonts/googleFontsKernDumpList.json", "r")
# file2 = open('count/fonts/test.json', 'r')
realWorldKerningPairs = json.load(file2)
useCounts = [value[0] for value in realWorldKerningPairs.values()]
minimum = (
    max(useCounts) * 0.2
)  # Clamp at 20 % ... removes unusual pairs in a pragmatic way
print("Clamp Minimum", minimum)
realWorldKerningPairs = {
    k: v for k, v in realWorldKerningPairs.items() if v[0] > minimum
}
realWorldKerningPairs = list(realWorldKerningPairs.keys())
print("Real World Kerning Pairs", len(realWorldKerningPairs))  # 58569
file2.close()
# realWorldKerningPairs = []

# Merge the two lists without duplicates
difference = [
    x for x in tqdm(potentialKerningPairs) if x not in set(realWorldKerningPairs)
]
potentialKerningPairs = realWorldKerningPairs + difference
print("Difference", len(difference))  # 4356
print("Total", len(potentialKerningPairs))  # 62925


for LANGUAGE in LANGUAGES:
    with open("count/by_language/" + LANGUAGE + "/list.json", "r") as input:
        letterPairs = json.load(input)
        totalValue = letterPairs["total"]

        # Convert to uppercase and SUM UP duplicate values (for example formly known as "Va", "va" and "VA" )
        uppercaseTemp = list((k.upper(), v) for k, v in letterPairs.items())
        uppercaseLetterPairs = defaultdict(int)
        for (key, value) in uppercaseTemp:
            uppercaseLetterPairs[key] += value
        # Merge letterPair Dictionaries
        for (key, value) in uppercaseLetterPairs.items():
            if key in letterPairs:
                letterPairs[key] = max(letterPairs[key], value)
            else:
                letterPairs[key] = value

        print(
            LANGUAGE,
            "Letter Pairs",
            len(letterPairs),
            "Total Count",
            "{:,}".format(totalValue),
        )
        with open(
            "count/by_language/" + LANGUAGE + "/common_kerning_pairs.json",
            "w",
            encoding="utf8",
        ) as output:
            commonKerningPairs = {
                key: letterPairs[key]
                for key in potentialKerningPairs
                if key in letterPairs
            }  # Filter potential kerning pairs
            commonKerningPairs = {
                k: v / totalValue * 3000 * 100 for k, v in commonKerningPairs.items()
            }  # Normalize 1 in 100 pages a 3000 characters
            commonKerningPairs = sorted(
                commonKerningPairs.items(), key=operator.itemgetter(1), reverse=True
            )  # Sort by count
            # print(commonKerningPairs)
            output.write(
                json.dumps(commonKerningPairs, indent=4, ensure_ascii=True)
            )  # Output
            print(LANGUAGE, "Common Kerning Pairs", len(commonKerningPairs))
            if "AN" in commonKerningPairs:
                print("AN", LANGUAGE)
            if "AR" in commonKerningPairs:
                print("AR", LANGUAGE)

# Merge all language specific kerning pairs to a global total
globalKerningPairs = {}
for LANGUAGE in LANGUAGES:
    with open(
        "count/by_language/" + LANGUAGE + "/common_kerning_pairs.json", "r"
    ) as input_a:
        kerningPairs = dict(json.load(input_a))
        # Stores the highest existing value of the given languages
        globalKerningPairs = {
            key: kerningPairs.get(key, 0)
            if kerningPairs.get(key, 0) > globalKerningPairs.get(key, 0)
            else globalKerningPairs.get(key, 0)
            for key in set(kerningPairs) | set(globalKerningPairs)
        }


# Filtering the relevant pairs by count value above a minimum
minimum = 1  # in 100 pages or 30,000 characters
relevantGlobalKerningPairs = {
    k: v for k, v in globalKerningPairs.items() if v >= minimum
}


# Sorting
globalKerningPairs = sorted(
    globalKerningPairs.items(), key=operator.itemgetter(1), reverse=True
)
relevantGlobalKerningPairs = sorted(
    relevantGlobalKerningPairs.items(), key=operator.itemgetter(1), reverse=True
)


# Output
with open("count/total/common_kerning_pairs.json", "w") as output_a, open(
    "count/total/relevant_kerning_pairs.json", "w"
) as output_c:
    output_a.write(json.dumps(globalKerningPairs, indent=4, ensure_ascii=False))
    output_c.write(json.dumps(relevantGlobalKerningPairs, indent=4, ensure_ascii=False))


print("Total")
print("Total", "Kerning Pairs", len(globalKerningPairs))
print("Total", "Relevant Kerning Pairs", len(relevantGlobalKerningPairs))
