#!/usr/bin/env python3
import itertools
import os
import sys


class UFOkernReader(object):

    def __init__(self, font, includeZero=False):
        self.f = font

        try:
            format_version = self.f.ufoFormatVersion
        except AttributeError:
            format_version = self.f.naked().ufoFormatVersion
        if format_version >= 3:
            self.group_indicator = 'public.'
        else:
            self.group_indicator = '@'

        self.group_group_pairs = {}
        self.group_glyph_pairs = {}
        self.glyph_group_pairs = {}
        self.glyph_glyph_pairs = {}

        self.allKerningPairs = self.makePairDicts(includeZero)
        self.output = self.makeOutput(self.allKerningPairs)

        self.totalKerning = sum(self.allKerningPairs.values())
        self.absoluteKerning = sum(
            [abs(value) for value in self.allKerningPairs.values()])

    def makeOutput(self, kerningDict):
        output = []
        for (left, right), value in kerningDict.items():
            output.append('/%s /%s %s' % (left, right, value))
        output.sort()
        return output

    def allCombinations(self, left, right):
        leftGlyphs = self.f.groups.get(left, [left])
        rightGlyphs = self.f.groups.get(right, [right])
        combinations = list(itertools.product(leftGlyphs, rightGlyphs))
        return combinations

    def makePairDicts(self, includeZero):
        kerningPairs = {}

        for (left, right), value in self.f.kerning.items():

            if (
                self.group_indicator in left and
                self.group_indicator in right
            ):
                # group-to-group-pair
                for combo in self.allCombinations(left, right):
                    self.group_group_pairs[combo] = value

            elif (
                self.group_indicator in left and
                self.group_indicator not in right
            ):
                # group-to-glyph-pair
                for combo in self.allCombinations(left, right):
                    self.group_glyph_pairs[combo] = value

            elif (
                self.group_indicator not in left and
                self.group_indicator in right
            ):
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


def run(font):
    ukr = UFOkernReader(font, includeZero=True)
    scrap = os.popen('pbcopy', 'w')
    output = '\n'.join(ukr.output)
    scrap.write(output)
    scrap.close()

    if inRF:
        pass
        # print('Total length of kerning:', ukr.totalKerning)

    if inCL:
        print('\n'.join(ukr.output), '\n')

    print('Total amount of kerning pairs:', len(ukr.output))
    print('List of kerning pairs copied to clipboard.')


if __name__ == '__main__':
    inRF = False
    inCL = False

    try:
        import mojo
        inRF = True
        f = CurrentFont()
        if f:
            run(f)
        else:
            print(u'You need to open a font first. \U0001F625')

    except ImportError:
        try:
            import defcon
            inCL = True
            path = os.path.normpath(sys.argv[-1])
            if os.path.splitext(path)[-1] in ['.ufo', '.UFO']:
                f = defcon.Font(path)
                run(f)
            else:
                print('No UFO file given.')
        except ImportError:
            print(u'You don’t have Defcon installed. \U0001F625')
