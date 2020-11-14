import json
from tqdm import tqdm
from pprint import pprint


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

# load local counts into memory
localCounts = dict()
for LANGUAGE in LANGUAGES:
    with open("count/by_language/" + LANGUAGE + "/common_kerning_pairs.json", "r") as inputFile_A:
        pairs = dict(json.load(inputFile_A))
        localCounts[LANGUAGE] = pairs

kerningPairs = dict()
with open("count/total/relevant_kerning_pairs.json", "r") as inputFile_B:
    for [key, relevance_score] in tqdm(json.load(inputFile_B)):
        top_local_counts = list()

        for LANGUAGE, pairs in localCounts.items():
            if key in pairs:
                top_local_counts.append((LANGUAGE, pairs[key]))
        top_local_counts.sort(key=lambda x:x[1], reverse=True)
        kerning_words = list()
        i = 0
        for LANGUAGE, count in top_local_counts[:14]:
            with open("count/by_language/" + LANGUAGE + "/words.json", "r") as inputFile_C:
                words = dict(json.load(inputFile_C))
                share = max(1, (4 - i))
                for word in words:
                    if share >= 1:
                        if len(word) <= 16 and word not in kerning_words:
                            if key[0] == ' ':
                                if key[1].lower() == word[0]:
                                    if key[1].isupper():
                                        kerning_words.append(word.upper())
                                        share -= 1
                                    else:
                                        kerning_words.append(word)
                                        share -= 1
                            elif key[1] == ' ':
                                if key[0].lower() == word[-1]:
                                    if key[0].isupper():
                                        kerning_words.append(word.upper())
                                        share -= 1
                                    else:
                                        kerning_words.append(word)
                                        share -= 1
                            else:
                                if key.isupper():
                                    if key.lower() in word:
                                        kerning_words.append(word.upper())
                                        share -= 1
                                else:
                                    if key in word:
                                        kerning_words.append(word)
                                        share -= 1
                            
            i += 1
        kerningPairs[key] = (relevance_score, kerning_words)  # just store Top 5 local Words
        

with open("result/relevant_words.json", "w") as output:
    output.write(json.dumps(kerningPairs, indent=4, sort_keys=False))
