#!/usr/bin/python
import itertools
import os
import re
import sys


__doc__ = '''\

Prints a list of all kerning pairs to be expected from a kern feature file.
The feature file has to be passed to the script as an argument.
This script has the ability to use a GlyphOrderAndAliasDB file for translating
"friendly" glyph names to final glyph names (for comparison with OTF).

Usage:
------
python getKerningPairsFromFeatureFile.py <path to kern feature file>
python getKerningPairsFromFeatureFile.py -go <path to GlyphOrderAndAliasDB file> <path to kern feature file>

'''

# Regular expressions for parsing individual kerning commands:
x_range_range = re.compile(
    r'\s*(enum\s+?)?pos\s+?\[\s*(.+?)\s*\]\s+?\[\s*(.+?)\s*\]\s+?(-?\d+?)\s*;')
x_range_glyph = re.compile(
    r'\s*(enum\s+?)?pos\s+?\[\s*(.+?)\s*\]\s+?(.+?)\s+?(-?\d+?)\s*;')
x_glyph_range = re.compile(
    r'\s*(enum\s+?)?pos\s+?(.+?)\s+?\[\s*(.+?)\s*\]\s+?(-?\d+?)\s*;')
x_item_item = re.compile(
    r'\s*(enum\s+?)?pos\s+?(.+?)\s+?(.+?)\s+?(-?\d+?)\s*;')
expressions = [x_range_range, x_range_glyph, x_glyph_range, x_item_item]


class KerningPair(object):
    'Storing a flattened kerning pair'

    def __init__(self, pair, pairList, value):

        self.pair = pair
        self.value = value
        self.pairList = pairList


class FEAKernReader(object):

    def __init__(self, options):

        self.goadbPath = None
        self.options = options

        if "-go" in self.options:
            self.goadbPath = self.options[self.options.index('-go') + 1]

        self.featureFilePath = self.options[-1]

        self.featureData = self.readFile(self.featureFilePath)
        self.kernClasses = self.readKernClasses()

        self.foundKerningPairs = self.parseKernLines()
        self.flatKerningPairs = self.makeFlatPairs()

        if self.goadbPath:
            self.glyphNameDict = {}
            self.readGOADB()
            self.flatKerningPairs = self.convertNames(self.flatKerningPairs)

        self.output = []
        for (left, right), value in self.flatKerningPairs.items():
            self.output.append('/%s /%s %s' % (left, right, value))
        self.output.sort()

    def readFile(self, filePath):
        # reads raw file, removes commented lines
        lineList = []
        inputfile = open(filePath, 'r')
        data = inputfile.read().splitlines()
        inputfile.close()
        for line in data:
            if '#' in line:
                line = line.split('#')[0]
            if line:
                lineList.append(line)

        lineString = '\n'.join(lineList)
        return lineString

    def convertNames(self, pairDict):
        newPairDict = {}
        for (left, right), value in pairDict.items():
            newLeft = self.glyphNameDict.get(left)
            newRight = self.glyphNameDict.get(right)

            # in case the glyphs are not in the GOADB:
            if not newLeft:
                newLeft = left
            if not newRight:
                newRight = right

            newPair = (newLeft, newRight)
            newPairDict[newPair] = value

        return newPairDict

    def readKernClasses(self):
        allClassesList = re.findall(
            r"(@\S+)\s*=\s*\[([ A-Za-z0-9_.]+)\]\s*;", self.featureData)

        classes = {}
        for name, glyphs in allClassesList:
            classes[name] = glyphs.split()

        return classes

    def allCombinations(self, left, right):
        if len(left.split()) > 1:
            # The left kerning object is an ad-hoc group
            # like [ a b c ] or [ a @MMK_x c ]:
            leftGlyphs = []
            leftItems = left.split()
            for item in leftItems:
                classFound = self.kernClasses.get(item, None)
                if classFound:
                    leftGlyphs.extend(classFound)
                else:
                    leftGlyphs.append(item)

        else:
            # The left kerning object is something like x or @MMK_x:
            leftGlyphs = self.kernClasses.get(left, [left])

        if len(right.split()) > 1:
            # The right kerning object is an ad-hoc group
            # like [ a b c ] or [ a @MMK_x c ]:
            rightGlyphs = []
            rightItems = right.split()
            for item in rightItems:
                classFound = self.kernClasses.get(item, None)
                if classFound:
                    rightGlyphs.extend(classFound)
                else:
                    rightGlyphs.append(item)
        else:
            # The right kerning object is something like x or @MMK_x:
            rightGlyphs = self.kernClasses.get(right, [right])

        combinations = list(itertools.product(leftGlyphs, rightGlyphs))
        return combinations

    def parseKernLines(self):
        featureLines = self.featureData.splitlines()
        foundKerningPairs = []
        for line in featureLines:
            for expression in expressions:
                match = re.match(expression, line)
                if match:
                    enum = match.group(1)
                    pair = (match.group(2), match.group(3))
                    value = match.group(4)
                    foundKerningPairs.append([enum, pair, value])
                    break
                else:
                    continue
        return foundKerningPairs

    def makeFlatPairs(self):
        indexedPairs = {}
        flatKerningPairs = {}

        for pIndex, (enum, pair, value) in enumerate(self.foundKerningPairs):
            left = pair[0]
            right = pair[1]

            if enum:
                # `enum` is shorthand for breaking down a one-line
                # command into multiple single pairs
                pairList = self.allCombinations(left, right)

            elif '@'not in left and '@' not in right:
                # glyph-to-glyph kerning
                pairList = [pair]

            else:
                # class-to-class, class-to-glyph, or glyph-to-class kerning
                pairList = self.allCombinations(left, right)

            indexedPairs[pIndex] = KerningPair(pair, pairList, value)

        # Iterate through the kerning pairs in reverse order to
        # overwrite less specific pairs with more specific ones:
        for pIndex, kerningPair in sorted(indexedPairs.items(), reverse=True):
            for pair in kerningPair.pairList:
                flatKerningPairs[pair] = kerningPair.value

        return flatKerningPairs

    def readGOADB(self):
        goadbList = self.readFile(self.goadbPath).splitlines()

        for line in goadbList:
            splitLine = line.split()
            if len(splitLine) < 2:
                print('Something is wrong with this GOADB line:\n', line)
            else:
                finalName, workingName = splitLine[0], splitLine[1]
                self.glyphNameDict[workingName] = finalName


if __name__ == "__main__":
    if len(sys.argv) > 1:

        options = sys.argv[1:]
        kernFile = options[-1]

        if (
            os.path.exists(kernFile) and
            os.path.splitext(kernFile)[-1] in ['.fea', '.kern']
        ):
            kfr = FEAKernReader(options)

            print('\n'.join(kfr.output))
            print(
                '\nTotal number of kerning pairs:\n',
                len(kfr.flatKerningPairs)
            )

        else:
            print("No valid kern feature file provided.")

    else:
        print("No valid kern feature file provided.")
