#!/usr/bin/python
import sys
from plistlib import writePlist
from defcon import Font


__doc__ = '''
Subset kerning and groups in a UFO given a list of glyphs provided.
Will export new plist files that can be swapped into the UFO.

Usage:
python subsetUFOKerningAndGroups.py subsetList font.ufo
'''


class SubsetKerning(object):
    def __init__(self, font, subsetFile):
        self.font = Font(font)
        self.subsetFile = subsetFile

        with open(self.subsetFile, 'r') as ssfile:
            rawData = ssfile.read()
            self.subsetGlyphList = [line.split()[0] for line in rawData.splitlines()]
        

    def subsetGroups(self):

        newGroups = {}
        for groupName, glyphList in self.font.groups.items():
            combinedGlyphs = set(self.subsetGlyphList) & set(glyphList)
            newGlyphList = sorted(list(combinedGlyphs))

            if len(newGlyphList):
                newGroups[groupName] = newGlyphList
        return newGroups



    def subsetKerning(self):
        newGroups = self.subsetGroups()
        newKerning = {}
        plistStyleKerning = {}

        # All allowed items for kerning, which are our subset glyphs, 
        # plus the groups filtered earlier:
        allowedItems = set(newGroups) | set(self.subsetGlyphList)

        for [left, right], value in self.font.kerning.items():
            if set([left, right]) <= allowedItems:
                newKerning[left, right] = value

        # Since the kerning paradigm stored in the plist differs from the  
        # in the kerning object, the data structure needs some modification:

        for [left, right], value in newKerning.items():
            partnerDict = plistStyleKerning.setdefault(left, {})
            partnerDict[right] = value

        return plistStyleKerning


def run():
    sk = SubsetKerning(sys.argv[-1], sys.argv[-2])

    writePlist(sk.subsetGroups(), 'subset_groups.plist')
    writePlist(sk.subsetKerning(), 'subset_kerning.plist')
    print 'done'


if len(sys.argv) == 3:
    run()
else:
    print __doc__

