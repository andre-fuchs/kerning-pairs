import itertools
from FL import fl
f = fl.font
fl.output = ''


class VFBkernReader(object):
    # basically a copy of UFOKernReader

    def __init__(self, groups, kerning, includeZero=False):
        self.groups = groups
        self.kerning = kerning
        self.group_group_pairs = {}
        self.group_glyph_pairs = {}
        self.glyph_group_pairs = {}
        self.glyph_glyph_pairs = {}

        self.allKerningPairs = self.makePairDicts(includeZero)
        self.output = self.makeOutput(self.allKerningPairs)

    def makeOutput(self, kerningDict):
        output = []
        for (left, right), value in kerningDict.items():
            output.append('/%s /%s %s' % (left, right, value))
        output.sort()
        return output

    def allCombinations(self, left, right):
        leftGlyphs = self.groups.get(left, [left])
        rightGlyphs = self.groups.get(right, [right])
        combinations = list(itertools.product(leftGlyphs, rightGlyphs))
        return combinations

    def makePairDicts(self, includeZero):
        kerningPairs = {}

        for (left, right), value in self.kerning.items():

            if '@' in left and '@' in right:
                # group-to-group-pair
                for combo in self.allCombinations(left, right):
                    self.group_group_pairs[combo] = value

            elif '@' in left and '@' not in right:
                # group-to-glyph-pair
                for combo in self.allCombinations(left, right):
                    self.group_glyph_pairs[combo] = value

            elif '@' not in left and '@' in right:
                # glyph-to-group-pair
                for combo in self.allCombinations(left, right):
                    self.glyph_group_pairs[combo] = value

            else:
                # glyph-to-glyph-pair a.k.a. single pair
                self.glyph_glyph_pairs[(left, right)] = value

        # The updates occur from the most general pairs to the most specific.
        # This means that any given class kerning values are overwritten with
        # the intended exceptions.
        kerningPairs.update(self.group_group_pairs)
        kerningPairs.update(self.group_glyph_pairs)
        kerningPairs.update(self.glyph_group_pairs)
        kerningPairs.update(self.glyph_glyph_pairs)

        if includeZero is False:
            # delete any kerning values == 0.
            # This cannot be done in the previous loop, since exceptions
            # might set a previously established kerning pair to be 0.
            cleanKerningPairs = dict(kerningPairs)
            for pair in kerningPairs:
                if kerningPairs[pair] == 0:
                    del cleanKerningPairs[pair]
            return cleanKerningPairs

        else:
            return kerningPairs


class FLKerningData(object):

    def __init__(self, font):
        self.f = font
        self._readFLGroups()
        self._splitFLGroups()
        self.leftKeyGlyphs = self._filterKeyGlyphs(self.leftGroups)
        self.rightKeyGlyphs = self._filterKeyGlyphs(self.rightGroups)
        self._readFLKerning()

    def _isMMfont(self, font):
        'Checks if the FontLab font is a Multiple Master font.'
        if font[0].layers_number > 1:
            return True
        else:
            return False

    def _readFLGroups(self, *args):
        self.groupToKeyglyph = {}
        self.groups = {}
        self.groupOrder = []

        flClassStrings = [cString for cString in self.f.classes if cString[0] == '_']

        for cString in flClassStrings:

            FLclassName = cString.split(":")[0] #  FL class name, e.g. _L_LC_LEFT
            OTgroupName = '@%s' % FLclassName[1:] #  OT group name, e.g. @L_LC_LEFT
            markedGlyphList = cString.split(":")[1].split()
            cleanGlyphList = [gName.strip("'") for gName in markedGlyphList]
            # strips out the keyglyph marker

            for gName in markedGlyphList:
                if gName[-1] == "'":  # finds keyglyph
                    keyGlyphName = gName.strip("'")
                    break
                else:
                    keyGlyphName = markedGlyphList[0]
                    print "\tWARNING: Kerning class %s has no explicit key glyph.\n\tUsing first glyph found (%s)." % (cString, keyGlyphName)

            self.groupOrder.append(OTgroupName)
            self.groupToKeyglyph[OTgroupName] = keyGlyphName
            self.groups[OTgroupName] = cleanGlyphList

    def _splitFLGroups(self):
        '''
        Splits FontLab kerning classes into left and right sides; based on
        the class name. Both sides are assigned to classes without an explicit
        side-flag.'
        '''

        leftTagsList = ['_LEFT', '_1ST', '_L_']
        rightTagsList = ['_RIGHT', '_2ND', '_R_']

        self.leftGroups = []
        self.rightGroups = []

        for groupName in self.groups:
            if any([tag in groupName for tag in leftTagsList]):
                self.leftGroups.append(groupName)
            elif any([tag in groupName for tag in rightTagsList]):
                self.rightGroups.append(groupName)
            else:
                self.leftGroups.append(groupName)
                self.rightGroups.append(groupName)

    def _filterKeyGlyphs(self, groupList):
        '''
        Returns a dictionary {keyGlyph: FLClassName}
        for a given list of classNames.
        '''

        filteredKeyGlyphs = {}

        for groupName in groupList:
            keyGlyphName = self.groupToKeyglyph[groupName]
            filteredKeyGlyphs[keyGlyphName] = groupName

        return filteredKeyGlyphs

    def _readFLKerning(self):
        'Reads FontLab kerning and converts it into a UFO-style kerning dict.'

        self.kerning = {}
        glyphs = self.f.glyphs

        for gIndexLeft, glyphLeft in enumerate(glyphs):
            gNameLeft = glyphLeft.name
            flKerningArray = glyphs[gIndexLeft].kerning

            for flKerningPair in flKerningArray:
                gIndexRight = flKerningPair.key
                gNameRight = glyphs[gIndexRight].name

                if self._isMMfont(self.f):
                    kernValue = '<%s>' % ' '.join(map(str, flKerningPair.values))
                    # gl.kerning[p].values is an array holding kern values for each master
                else:
                    kernValue = int(flKerningPair.value)

                pair = self.leftKeyGlyphs.get(gNameLeft, gNameLeft), self.rightKeyGlyphs.get(gNameRight, gNameRight)
                self.kerning[pair] = kernValue


def run():
    kD = FLKerningData(f)
    vkr = VFBkernReader(kD.groups, kD.kerning)
    # vkr = VFBkernReader(kD.groups, kD.kerning, includeZero=True)

    print '\n'.join(vkr.output), '\n'
    print 'Total amount of kerning pairs:', len(vkr.output)

    dumpFileName = f.file_name + '.kerndump'
    dumpFile = open(dumpFileName, 'w')
    for (g1, g2), v in sorted(vkr.allKerningPairs.items()):
        dumpFile.write("%s %s %s\n" % (g1, g2, v))
    dumpFile.close()

    print '\nList of kerning pairs written to\n{}'.format(dumpFileName)

if __name__ == '__main__':
    run()
