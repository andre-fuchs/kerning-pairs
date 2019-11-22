""" 
This script generates a TXT file to be used for kerning with your favorite font editor.
Feel free to customize the padding to the left and right sides of the kerning pairs to your liking.
"""

import json

# TO DO:
# Generate all combinations of numbers, math characters and brackets


CHARACTER_SETS = {
    "uppercase": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "Á",
        "Â",
        "Ã",
        "Ä",
        "Å",
        "Æ",
        "Ç",
        "È",
        "É",
        "Ê",
        "Ë",
        "Ì",
        "Í",
        "Î",
        "Ï",
        "Ð",
        "Ñ",
        "Ò",
        "Ó",
        "Ô",
        "Õ",
        "Ö",
        "Ø",
        "Ù",
        "Ú",
        "Û",
        "Ü",
        "Ý",
        "Þ",
        "Ă",
        "Ą",
        "Ć",
        "Ĉ",
        "Ċ",
        "Č",
        "Ď",
        "Đ",
        "Ē",
        "Ĕ",
        "Ė",
        "Ę",
        "Ě",
        "Ĝ",
        "Ğ",
        "Ġ",
        "Ģ",
        "Ĥ",
        "Ħ",
        "Ĩ",
        "Ī",
        "Ĭ",
        "Į",
        "İ",
        "Ĳ",
        "Ĵ",
        "Ķ",
        "Ĺ",
        "Ļ",
        "Ľ",
        "Ŀ",
        "Ł",
        "Ń",
        "Ņ",
        "Ň",
        "Ŋ",
        "Ō",
        "Ŏ",
        "Ő",
        "Œ",
        "Ŕ",
        "Ŗ",
        "Ř",
        "Ś",
        "Ŝ",
        "Ş",
        "Š",
        "Ţ",
        "Ť",
        "Ŧ",
        "Ũ",
        "Ū",
        "Ŭ",
        "Ů",
        "Ű",
        "Ų",
        "Ŵ",
        "Ŷ",
        "Ÿ",
        "Ź",
        "Ż",
        "Ž",
    ],
    "punctuation": [
        ".",
        ",",
        ":",
        ";",
        "…",
        "!",
        "¡",
        "?",
        "¿",
        "·",
        "•",
        "*",
        "#",
        "/",
        "/",
        "\\",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "-",
        "­",
        "–",
        "—",
        "_",
        '"',
        "'",
        "«",
        "»",
        "‘",
        "’",
        "‚",
        "‛",
        "“",
        "”",
        "„",
        "‟",
        "‹",
        "›",
        "¢",
        "¤",
        "$",
        "€",
        "ƒ",
        "£",
        "¥",
        "+",
        "−",
        "×",
        "÷",
        "=",
        "≠",
        ">",
        "<",
        "≥",
        "≤",
        "±",
        "≈",
        "~",
        "¬",
        "^",
        "∞",
        "∫",
        "Ω",
        "∆",
        "∏",
        "∑",
        "√",
        "µ",
        "∂",
        "%",
        "‰",
        "◊",
        "@",
        "&",
        "¶",
        "§",
        "©",
        "®",
        "™",
        "°",
        "|",
        "¦",
        "†",
        "‡",
        "℮",
    ],
    "numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "½", "¼", "¾",],
}

clusters = {
    "uppercase": [],
    "punctuation": [],
    "numbers": [],
    "other": [],  # fallback
}

with open(
    "count/fonts/googleFontsKernVectorList.json", "r"
) as input_json, open(
    "result/relevant_kerning_with_padding.txt", "w"
) as outputPadded, open(
    "result/relevant_kerning_raw.json", "w", encoding="utf8"
) as outputRaw, open(
    "result/relevant_kerning_clustered.txt", "w", encoding="utf8"
) as outputClustered:
    relevantGlobalKerningPairs = json.load(input_json)
    kerningPadded = ["nonu" + v[0] + "nuou\n" for v in relevantGlobalKerningPairs]
    kerningList =  [v[0] for v in relevantGlobalKerningPairs]
    # Cluster kerning pairs
    kerningClustered = ''
    for pair in kerningList:
        found = False
        for SUFFIX, SET in CHARACTER_SETS.items():
            if any(character in pair for character in SET):
                found = True
                clusters[SUFFIX].append(pair)
                if len(clusters[SUFFIX]) > 30:
                    # Dump
                    kerningClustered += ' '.join(clusters[SUFFIX]) + '\n \n'
                    # Reset
                    clusters[SUFFIX] = []
                break
        if not found:
            # Store it in fallback cluster for all lowercase characters etc.
            clusters['other'].append(pair)
            if len(clusters['other']) > 30:
                    kerningClustered += ' '.join(clusters['other']) + '\n \n'
                    # Reset
                    clusters['other'] = []

    outputPadded.writelines(kerningPadded)
    outputClustered.writelines(kerningClustered)
    outputRaw.write(json.dumps(kerningList, indent=4, ensure_ascii=False))

