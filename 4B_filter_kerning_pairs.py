#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

CHARACTER_SETS = {
    # 'buchstaben': [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'ā', 'Ă', 'ă', 'Ą', 'ą', 'Ć', 'ć', 'Ĉ', 'ĉ', 'Ċ', 'ċ', 'Č', 'č', 'Ď', 'ď', 'Đ', 'đ', 'Ē', 'ē', 'Ĕ', 'ĕ', 'Ė', 'ė', 'Ę', 'ę', 'Ě', 'ě', 'Ĝ', 'ĝ', 'Ğ', 'ğ', 'Ġ', 'ġ', 'Ģ', 'ģ', 'Ĥ', 'ĥ', 'Ħ', 'ħ', 'Ĩ', 'ĩ', 'Ī', 'ī', 'Ĭ', 'ĭ', 'Į', 'į', 'İ', 'ı', 'Ĳ', 'ĳ', 'Ĵ', 'ĵ', 'Ķ', 'ķ', 'ĸ', 'Ĺ', 'ĺ', 'Ļ', 'ļ', 'Ľ', 'ľ', 'Ŀ', 'ŀ', 'Ł', 'ł', 'Ń', 'ń', 'Ņ', 'ņ', 'Ň', 'ň', 'ŉ', 'Ŋ', 'ŋ', 'Ō', 'ō', 'Ŏ', 'ŏ', 'Ő', 'ő', 'Œ', 'œ', 'Ŕ', 'ŕ', 'Ŗ', 'ŗ', 'Ř', 'ř', 'Ś', 'ś', 'Ŝ', 'ŝ', 'Ş', 'ş', 'Š', 'š', 'Ţ', 'ţ', 'Ť', 'ť', 'Ŧ', 'ŧ', 'Ũ', 'ũ', 'Ū', 'ū', 'Ŭ', 'ŭ', 'Ů', 'ů', 'Ű', 'ű', 'Ų', 'ų', 'Ŵ', 'ŵ', 'Ŷ', 'ŷ', 'Ÿ', 'Ź', 'ź', 'Ż', 'ż', 'Ž', 'ž', 'ſ', ],
    'versalien': [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'Ă', 'Ą', 'Ć', 'Ĉ', 'Ċ', 'Č', 'Ď', 'Đ', 'Ē', 'Ĕ', 'Ė', 'Ę', 'Ě', 'Ĝ', 'Ğ', 'Ġ', 'Ģ', 'Ĥ', 'Ħ', 'Ĩ', 'Ī', 'Ĭ', 'Į', 'İ', 'Ĳ', 'Ĵ', 'Ķ', 'Ĺ', 'Ļ', 'Ľ', 'Ŀ', 'Ł', 'Ń', 'Ņ', 'Ň', 'Ŋ', 'Ō', 'Ŏ', 'Ő', 'Œ', 'Ŕ', 'Ŗ', 'Ř', 'Ś', 'Ŝ', 'Ş', 'Š', 'Ţ', 'Ť', 'Ŧ', 'Ũ', 'Ū', 'Ŭ', 'Ů', 'Ű', 'Ų', 'Ŵ', 'Ŷ', 'Ÿ', 'Ź', 'Ż', 'Ž', ],
    'leerzeichen': [ ' ', ],
    'interpunktion': [ '.', ',', ':', ';', '…', '!', '¡', '?', '¿', '·', '•', '*', '#', '/', '/', '\\', '(', ')', '{', '}', '[', ']', '-', '­', '–', '—', '_', '"', "'", '«', '»', '‘', '’', '‚', '‛', '“', '”', '„', '‟', '‹', '›', ],
    'numbers': [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '½', '¼', '¾', ],
    'sonderzeichen': [ '¢', '¤', '$', '€', 'ƒ', '£', '¥', '+', '−', '×', '÷', '=', '≠', '>', '<', '≥', '≤', '±', '≈', '~', '¬', '^', '∞', '∫', 'Ω', '∆', '∏', '∑', '√', 'µ', '∂', '%', '‰', '◊', '@', '&', '¶', '§', '©', '®', '™', '°', '|', '¦', '†', '‡', '℮', ],
    'non-letters': [ ' ', '.', ',', ':', ';', '…', '!', '¡', '?', '¿', '·', '•', '*', '#', '/', '/', '\\', '(', ')', '{', '}', '[', ']', '-', '­', '–', '—', '_', '"', "'", '«', '»', '‘', '’', '‚', '‛', '“', '”', '„', '‟', '‹', '›', '¢', '¤', '$', '€', 'ƒ', '£', '¥', '+', '−', '×', '÷', '=', '≠', '>', '<', '≥', '≤', '±', '≈', '~', '¬', '^', '∞', '∫', 'Ω', '∆', '∏', '∑', '√', 'µ', '∂', '%', '‰', '◊', '@', '&', '¶', '§', '©', '®', '™', '°', '|', '¦', '†', '‡', '℮', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '½', '¼', '¾', ], 
}

# To Do:
# replace "count/total/relevant_kerning_pairs.json" with "googleFontsKernVectorList.json"
# better file name schema and directory required

for SUFFIX, SET in CHARACTER_SETS.items():
    with open('count/total/relevant_kerning_pairs.json', 'r') as input_json, \
         open('count/total/relevant_kerning_pairs_' + SUFFIX + '.json', 'w') as output_json, \
         open('count/total/relevant_kerning_pairs_' + SUFFIX + '.txt', 'w') as output_txt:
        relevantKerningPairs = json.load(input_json)
        filtered = [k for k in relevantKerningPairs if any(character in k[0] for character in SET)]
        kerningTXT = ['nonu' + k + 'nuou\n' for (k, v) in filtered]
        # pprint(filtered)
        print(SUFFIX, len(filtered), len(relevantKerningPairs))
        output_json.write(json.dumps(filtered, indent=4, ensure_ascii=False))
        output_txt.writelines(kerningTXT)


# Inverse
with open('count/total/relevant_kerning_pairs.json', 'r') as input_json, \
     open('count/total/relevant_kerning_pairs_buchstaben_only.json', 'w') as output_json, \
     open('count/total/relevant_kerning_pairs_buchstaben_only.txt', 'w') as output_txt:
    relevantKerningPairs = json.load(input_json)
    filtered = [k for k in relevantKerningPairs if not any(character in k[0] for character in CHARACTER_SETS['non-letters'])]
    kerningTXT = ['nonu' + k + 'nuou\n' for (k, v) in filtered]
    # pprint(filtered)
    print('Buchstaben only', len(filtered), len(relevantKerningPairs))
    output_json.write(json.dumps(filtered, indent=4, ensure_ascii=False))
    output_txt.writelines(kerningTXT)


# Counts per 1, 10 and 100 pages
for value in [100, 10, 1]:
    with open('count/total/relevant_kerning_pairs.json', 'r') as input_json:
        relevantKerningPairs = json.load(input_json)
        filtered = list(filter(lambda x: x[1] >= value, relevantKerningPairs))
        print(len(filtered))
