import json
from tqdm import tqdm
from pprint import pprint
from random import randrange, randint
from fuzzywuzzy import fuzz

# # Custom shuffle function to mix up the beginning of the text with its more frequently repeating words
def fuzzy_knuth_shuffle(l):
    end = (len(l) - 1)
    i = 0
    while i < end:
        fuzzyness = max(1, int(10 - 10 * ((i/end)**2)))  # Less shuffling necessary for less relevant (fewer) words
        if any(letter in l[i] for letter in ['.', ',', ';', '_', '-']):
            fuzzyness += 10
        stop = min(i + fuzzyness, end)
        idx = randrange(i, stop)
        l[i], l[idx] = l[idx], l[i]
        i += 1


word_cache = list()
word_scores = list()
with open("result/relevant_words.json", "r") as inputFile:
    collected_words = json.load(inputFile)
    for [key, [score, words]] in tqdm(collected_words.items()):
        for word in words:
            word_score = 0
            for [key, [score, words]] in collected_words.items():
                if key in word:
                    word_score += int(score)
            word_score = int(word_score / len(word))
            if not word in word_cache and word_score > 950:
                if len(word) > 3 and not any(fuzz.partial_ratio(word, w) == 100 for w in word_cache):
                    word_cache.append(word)
                    word_scores.append((word_score, word))
                
word_scores = sorted(word_scores, reverse=True)

selected_words = dict()
selected_words['lower'] = list()
selected_words['upper'] = list()
for word_score, word in word_scores[:500]:
    case = 'upper' if word.isupper() else 'lower'
    selected_words[case].append(word)


# Loosen up the list of words to avoid obvious repetitions
fuzzy_knuth_shuffle(selected_words['lower'])
fuzzy_knuth_shuffle(selected_words['upper'])


with open("result/relevant_words.json", "r") as inputFile:
    for [key, [score, words]] in json.load(inputFile).items():
        share = int(max(min((score / 1000), 10), 1))  # scale score value to a number between 0 and 9
        case = 'upper' if key.isupper() else 'lower'
        # Count occurances of key in selected words
        n = 0
        for word in selected_words[case]:
            if key in word:
                share -= 1
        share = max(0, min(len(words), share))  # make sure that this share limit is not larger then the number of words
        for word in words[:share]:        
            if not word in selected_words[case] and not any(letter in word for letter in ['{', '}', '[', ']', '\\', '_', '<', '>', ]):
                # Mix the more relevant words with the existing text (made of the most relevant words)
                if score > 700:
                    selected_words[case].insert(randint(0, len(selected_words[case])), word)
                else:
                    selected_words[case].append(word)
        

text = ''
for case, words in selected_words.items():
    # knuth_shuffle(words)
    text += ' '.join(words) + '\n\n'
    print(case, len(words))

with open("result/relevant_words.txt", "w") as output:
    output.write(text)