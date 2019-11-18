#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/adobe-type-tools/kern-dump/blob/master/dumpkerning.py

"""
This script extracts kerning tables of any font files in a given directory
including all subdirectories. These kerning tables sum up to a global total one
including the total count of uses in these fonts and the average normalized kern value.
"""

from kernDump.getKerningPairsFromFEA import FEAKernReader
from kernDump.getKerningPairsFromOTF import OTFKernReader
from kernDump.getKerningPairsFromUFO import UFOkernReader
import defcon
import os
from glob import glob
from collections import defaultdict
from pprint import pprint
from collections import defaultdict
import pandas as pd
import json
from fontTools.ttLib import TTFont


# Characterset to translate from font tools’ character names
CHARACTERS = {
    'space': ' ',
    'exclam': '!',
    'quotedbl': '"',
    'numbersign': '#',
    'dollar': '$',
    'percent': '%',
    'ampersand': '&',
    'quotesingle': "'",
    'parenleft': '(',
    'parenright': ')',
    'asterisk': '*',
    'plus': '+',
    'comma': ',',
    'hyphen': '-',
    'period': '.',
    'slash': '/',
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'colon': ':',
    'semicolon': ';',
    'less': '<',
    'equal': '=',
    'greater': '>',
    'question': '?',
    'at': '@',
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 'P',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',
    'bracketleft': '[',
    'backslash': '\\',
    'bracketright': ']',
    'circumflex': 'ˆ',
    'underscore': '_',
    'grave': '`',
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',
    'braceleft': '{',
    'bar': '|',
    'braceright': '}',
    'asciitilde': '~',
    'Agrave': 'À',
    'Aacute': 'Á',
    'Acircumflex': 'Â',
    'Atilde': 'Ã',
    'Adieresis': 'Ä',
    'Aring': 'Å',
    'AE': 'Æ',
    'Ccedilla': 'Ç',
    'Egrave': 'È',
    'Eacute': 'É',
    'Ecircumflex': 'Ê',
    'Edieresis': 'Ë',
    'Igrave': 'Ì',
    'Iacute': 'Í',
    'Icircumflex': 'Î',
    'Idieresis': 'Ï',
    'Eth': 'Ð',
    'Ntilde': 'Ñ',
    'Ograve': 'Ò',
    'Oacute': 'Ó',
    'Ocircumflex': 'Ô',
    'Otilde': 'Õ',
    'Odieresis': 'Ö',
    'multiply': '×',
    'Oslash': 'Ø',
    'Ugrave': 'Ù',
    'Uacute': 'Ú',
    'Ucircumflex': 'Û',
    'Udieresis': 'Ü',
    'Yacute': 'Ý',
    'Thorn': 'Þ',
    'germandbls': 'ß',
    'agrave': 'à',
    'aacute': 'á',
    'acircumflex': 'â',
    'atilde': 'ã',
    'adieresis': 'ä',
    'aring': 'å',
    'ae': 'æ',
    'ccedilla': 'ç',
    'egrave': 'è',
    'eacute': 'é',
    'ecircumflex': 'ê',
    'edieresis': 'ë',
    'igrave': 'ì',
    'iacute': 'í',
    'icircumflex': 'î',
    'idieresis': 'ï',
    'eth': 'ð',
    'ntilde': 'ñ',
    'ograve': 'ò',
    'oacute': 'ó',
    'ocircumflex': 'ô',
    'otilde': 'õ',
    'odieresis': 'ö',
    'divide': '÷',
    'oslash': 'ø',
    'ugrave': 'ù',
    'uacute': 'ú',
    'ucircumflex': 'û',
    'udieresis': 'ü',
    'yacute': 'ý',
    'thorn': 'þ',
    'ydieresis': 'ÿ',
    'Amacron': 'Ā',
    'amacron': 'ā',
    'Abreve': 'Ă',
    'abreve': 'ă',
    'Aogonek': 'Ą',
    'aogonek': 'ą',
    'Cacute': 'Ć',
    'cacute': 'ć',
    'Ccircumflex': 'Ĉ',
    'ccircumflex': 'ĉ',
    'uni010A': 'Ċ',
    'uni010B': 'ċ',
    'Ccaron': 'Č',
    'ccaron': 'č',
    'Dcaron': 'Ď',
    'dcaron': 'ď',
    'uni0110': 'Đ',
    'uni0111': 'đ',
    'Emacron': 'Ē',
    'emacron': 'ē',
    'Ebreve': 'Ĕ',
    'ebreve': 'ĕ',
    'uni0116': 'Ė',
    'uni0117': 'ė',
    'Eogonek': 'Ę',
    'eogonek': 'ę',
    'Ecaron': 'Ě',
    'ecaron': 'ě',
    'Gcircumflex': 'Ĝ',
    'gcircumflex': 'ĝ',
    'Gbreve': 'Ğ',
    'gbreve': 'ğ',
    'uni0120': 'Ġ',
    'uni0121': 'ġ',
    'uni0122': 'Ģ',
    'uni0123': 'ģ',
    'Hcircumflex': 'Ĥ',
    'hcircumflex': 'ĥ',
    'Hbar': 'Ħ',
    'hbar': 'ħ',
    'Itilde': 'Ĩ',
    'itilde': 'ĩ',
    'Imacron': 'Ī',
    'imacron': 'ī',
    'Ibreve': 'Ĭ',
    'ibreve': 'ĭ',
    'Iogonek': 'Į',
    'iogonek': 'į',
    'Idotaccent': 'İ',
    'dotlessi': 'ı',
    'IJ': 'Ĳ',
    'ij': 'ĳ',
    'Jcircumflex': 'Ĵ',
    'jcircumflex': 'ĵ',
    'uni0136': 'Ķ',
    'uni0137': 'ķ',
    'kgreenlandic': 'ĸ',
    'Lacute': 'Ĺ',
    'lacute': 'ĺ',
    'uni013B': 'Ļ',
    'uni013C': 'ļ',
    'Lcaron': 'Ľ',
    'lcaron': 'ľ',
    'Ldot': 'Ŀ',
    'ldot': 'ŀ',
    'Lslash': 'Ł',
    'lslash': 'ł',
    'Nacute': 'Ń',
    'nacute': 'ń',
    'uni0145': 'Ņ',
    'uni0146': 'ņ',
    'Ncaron': 'Ň',
    'ncaron': 'ň',
    'napostrophe': 'ŉ',
    'Eng': 'Ŋ',
    'eng': 'ŋ',
    'Omacron': 'Ō',
    'omacron': 'ō',
    'Obreve': 'Ŏ',
    'obreve': 'ŏ',
    'uni0150': 'Ő',
    'uni0151': 'ő',
    'OE': 'Œ',
    'oe': 'œ',
    'Racute': 'Ŕ',
    'racute': 'ŕ',
    'uni0156': 'Ŗ',
    'uni0157': 'ŗ',
    'Rcaron': 'Ř',
    'rcaron': 'ř',
    'Sacute': 'Ś',
    'sacute': 'ś',
    'Scircumflex': 'Ŝ',
    'scircumflex': 'ŝ',
    'Scedilla': 'Ş',
    'scedilla': 'ş',
    'Scaron': 'Š',
    'scaron': 'š',
    'uni0162': 'Ţ',
    'uni0163': 'ţ',
    'Tcaron': 'Ť',
    'tcaron': 'ť',
    'Tbar': 'Ŧ',
    'tbar': 'ŧ',
    'Utilde': 'Ũ',
    'utilde': 'ũ',
    'Umacron': 'Ū',
    'umacron': 'ū',
    'Ubreve': 'Ŭ',
    'ubreve': 'ŭ',
    'Uring': 'Ů',
    'uring': 'ů',
    'uni0170': 'Ű',
    'uni0171': 'ű',
    'Uogonek': 'Ų',
    'uogonek': 'ų',
    'Wcircumflex': 'Ŵ',
    'wcircumflex': 'ŵ',
    'Ycircumflex': 'Ŷ',
    'ycircumflex': 'ŷ',
    'Ydieresis': 'Ÿ',
    'Zacute': 'Ź',
    'zacute': 'ź',
    'uni017B': 'Ż',
    'uni017C': 'ż',
    'Zcaron': 'Ž',
    'zcaron': 'ž',
    'longs': 'ſ',
    'guillemotleft': '«', 
    'guillemotright': '»', 
    'guilsinglleft': '‹', 
    'guilsinglright': '›',
    'quoteleft': '‘', 
    'quoteright': '’', 
    'quotesinglbase': '‚', 
    'quotereversed': '‛', 
    'quotedblleft': '“', 
    'quotedblright': '”', 
    'quotedblbase': '„', 
    'uni201F': '‟', 
}



def extractKerning(path):
    path = os.path.normpath(path)  # remove trailing slash for .ufo
    base, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext in [".ttf", ".otf"]:
        otfKern = OTFKernReader(path)
        return otfKern.kerningPairs
    elif ext == ".ufo":
        ufoKern = UFOkernReader(defcon.Font(path), includeZero=True)
        return ufoKern.allKerningPairs
    else:
        # assume .fea
        feaOrgKern = FEAKernReader([path])
        return feaOrgKern.flatKerningPairs


# Fonts Source: 
# https://github.com/google/fonts/archive/master.zip
PATH = 'fonts/google-webfonts/fonts-master'
counts = defaultdict(lambda: defaultdict(lambda: 0))
values = defaultdict(lambda: defaultdict(lambda: 0))
paths = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.ttf'))]
countTotal = len(paths)

for index, path in enumerate(paths):
    print(str(index + 1) + '/' + str(countTotal), path)
    fontKernDump = extractKerning(path)
    if len(fontKernDump):
        font = TTFont(path)
        try:
            nLeftSideBearing = font['hmtx'].metrics['n'][1]
            spaceWidth = font['hmtx'].metrics['space'][0]
            referenceSpace = (nLeftSideBearing + spaceWidth/4) / 2
            for pair, value in fontKernDump.items():
                # Filtering character set
                if all (key in CHARACTERS for key in (pair[0], pair[1])):
                    normalizedValue = value / referenceSpace
                    counts[CHARACTERS[pair[0]]][CHARACTERS[pair[1]]] += 1
                    values[CHARACTERS[pair[0]]][CHARACTERS[pair[1]]] += normalizedValue
        except:
            print('At least we tried.')


# Convert dictionary to list and dataframe
list = []
for left_letter in counts:
    for right_letter in counts[left_letter]:
        averageValue = values[left_letter][right_letter] / counts[left_letter][right_letter]
        list.append((left_letter + right_letter, (counts[left_letter][right_letter], averageValue)))
list = sorted(list, key=lambda x: x[1][0], reverse=True)
# dataframe = pd.DataFrame.from_dict(dictionary, orient='index')


# Write out
with open('count/fonts/googleFontsKernDumpCounts.json', 'w', encoding='utf8') as file:
    file.write(json.dumps(counts, indent=4, sort_keys=True, ensure_ascii=False))
with open('count/fonts/googleFontsKernDumpValues.json', 'w', encoding='utf8') as file:
    file.write(json.dumps(values, indent=4, sort_keys=True, ensure_ascii=False))
with open('count/fonts/googleFontsKernDumpList.json', 'w', encoding='utf8') as file:
    file.write(json.dumps(dict(list), indent=4, ensure_ascii=False))
# dataframe.to_pickle('googleFontsKernDumpDataframe.pkl')