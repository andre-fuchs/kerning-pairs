#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import html
from decimal import Decimal
from pprint import pprint


keys = []
totalValues = []
vectors = []
colors = []
outputJS = ""
LANGUAGES = [
    "cs",
    "da",
    "de",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "hr",
    "hu",
    "it",
    "lt",
    "lv",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "se",
    "sk",
    "sl",
    "sq",
    "sv",
    "tr",
]

# blacklist = {
#     '1&#x27;': "\'",
#     'l&#x27;': "\'",
# }

# Get labels and first dataset from TOTAL
with open("count/total/relevant_kerning_pairs.json", "r") as input_a, open(
    "count/fonts/googleFontsKernVectorDictionary.json", "r"
) as input_b:
    kerningPairs = json.load(input_a)
    kernVectors = json.load(input_b)
    keyMaximum = max(
        kernVectors, key=kernVectors.get
    )  # Just use 'min' instead of 'max' for minimum.
    maxUseCount = kernVectors[keyMaximum][0]
    for pair in kerningPairs:
        key = html.escape(pair[0])
        value = pair[1]
        keys.append(key)
        totalValues.append(round((value / 100), 2))
        if key in kernVectors:
            vector = min(2, abs(kernVectors[key][1])) * -1
            color = "rgba(255, 0, 0, {})".format(kernVectors[key][0] / maxUseCount)
        else:
            vector = 0
            color = "#ccc"
        vectors.append(vector)
        colors.append(color)
    keys = [key.replace("\\", "\\\\") for key in keys]
    outputJS = "labels = ['" + "', '".join(keys) + "']; \n"
    outputJS += "dataset_total = ['" + "', '".join(map(str, totalValues)) + "']; \n"
    outputJS += "dataset_colors = ['" + "', '".join(map(str, colors)) + "']; \n"
    outputJS += "dataset_vectors = ['" + "', '".join(map(str, vectors)) + "']; \n"


# Local datasets
for LANGUAGE in LANGUAGES:
    with open(
        "count/by_language/" + LANGUAGE + "/common_kerning_pairs.json", "r"
    ) as input:
        kerningPairs = dict(json.load(input))
        localValues = []
        for key in keys:
            normalizedValue = kerningPairs[key] if key in kerningPairs else 0
            localValues.append(round(normalizedValue, 2))
        outputJS += (
            "dataset_"
            + LANGUAGE
            + " = ['"
            + "', '".join(map(str, localValues))
            + "']; \n"
        )
        # print(localValues[:100])

# Counting
countTotal = len(keys)
outputJS += "countTotal = " + str(countTotal) + "; \n"
with open("count/total/relevant_kerning_pairs_interpunktion.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countInterpunktion = " + str(count) + "; \n"
with open("count/total/relevant_kerning_pairs_leerzeichen.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countLeerzeichen = " + str(count) + "; \n"
with open("count/total/relevant_kerning_pairs_sonderzeichen.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countSonderzeichen = " + str(count) + "; \n"
with open("count/total/relevant_kerning_pairs_numbers.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countNumbers = " + str(count) + "; \n"
with open("count/total/relevant_kerning_pairs_buchstaben_only.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countBuchstabenOnly = " + str(count) + "; \n"
with open("count/total/relevant_kerning_pairs_versalien.json", "r") as input:
    count = len(json.load(input))
    outputJS += "countVersalien = " + str(count) + "; \n"

# Counts per 1, 10 and 100 pages
for value in [100, 10, 1]:
    with open("count/total/relevant_kerning_pairs.json", "r") as input_json:
        relevantKerningPairs = json.load(input_json)
        filtered = list(filter(lambda x: x[1] >= value, relevantKerningPairs))
        outputJS += "countGreater" + str(value) + " = " + str(len(filtered)) + "; \n"

# Google Fonts Kern Dump
with open("count/fonts/googleFontsKernDumpList.json", "r") as input:
    kerningPairs = json.load(input)
    k = []
    v = []
    for key, value in kerningPairs.items():
        k.append(html.escape(key))
        v.append(value[0])
    k = [x.replace("\\", "\\\\") for x in k]
    outputJS += "labelsKernDump = ['" + "', '".join(k) + "']; \n"
    outputJS += "datasetKernDump = ['" + "', '".join(map(str, v)) + "']; \n"
    print(len(k))

# Google Fonts Kern Vectors
# TO BE UPDATED: kerningPairs.keys should be the relevant ones, not the Google Fonts ones
with open("count/fonts/googleFontsKernVectorList.json", "r") as input:
    kernDumpList = json.load(input)
    # kernDump = {value[0]: (value[1], value[2], value[3], value[4], value[5], value[6]) for value in kernDumpList}
    k = []
    scores = []
    countsNormalized = []
    usesNormalized = []
    valuesNormalized = []
    boni = []
    uses = []
    values = []
    # vectors = []
    differences = []
    for dataset in kernDumpList:
        k.append(html.escape(dataset[0]))
        # if key in kernDump:
        use = dataset[1]
        kernValue = dataset[2]
        # vector = dataset[3]
        countNormalized = dataset[4]
        useNormalized = dataset[5]
        valueNormalized = dataset[6]
        bonus = dataset[7]
        score = dataset[3]

        uses.append("{:4}".format(use))
        values.append("{:4.2f}".format(kernValue).rjust(5))
        # vectors.append(str(vector).rjust(5))
        countsNormalized.append("{:4.2f}".format(countNormalized).rjust(5))
        usesNormalized.append("{:4.2f}".format(useNormalized).rjust(5))
        valuesNormalized.append("{:4.2f}".format(valueNormalized).rjust(5))
        boni.append("{:4}".format(bonus).rjust(2))
        scores.append("{:4.2f}".format(score).rjust(5))
    k = [key.replace("\\", "\\\\") for key in k]
    outputJS += "labels_kernVector = ['" + "', '".join(k) + "']; \n"
    outputJS += "dataset_kernVectorUses = ['" + "', '".join(map(str, uses)) + "']; \n"
    outputJS += (
        "dataset_kernVectorValues = ['" + "', '".join(map(str, values)) + "']; \n"
    )
    outputJS += (
        "dataset_kernVectorCounts = ['"
        + "', '".join(map(str, countsNormalized))
        + "']; \n"
    )
    # outputJS += "dataset_kernVectorVectors = ['" + "', '".join(map(str, vectors)) + "']; \n"
    outputJS += (
        "dataset_kernVectorUses = ['" + "', '".join(map(str, usesNormalized)) + "']; \n"
    )
    outputJS += (
        "dataset_kernVectorValuesNormalized = ['"
        + "', '".join(map(str, valuesNormalized))
        + "']; \n"
    )
    outputJS += "dataset_kernVectorBonus = ['" + "', '".join(map(str, boni)) + "']; \n"
    outputJS += "dataset_kernVector = ['" + "', '".join(map(str, scores)) + "']; \n"


with open("charts/datasets/count_comparison.js", "w") as output:
    output.write(outputJS)
    # print(keys[:20], totalValues[:20])
