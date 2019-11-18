#!/usr/bin/python
# coding: utf-8

from __future__ import division
import os
import sys
import itertools
import getKerningPairsFromUFO
from collections import defaultdict
from robofab.world import RFont as Font
from robofab import ufoLib
import time

# from defcon import Font
# ufo 3 defcon would write proper glif names,
# but creates a huge kerning plist. (why?)

reload(getKerningPairsFromUFO)

startTime = time.time()

'''
2016/03/11 12:47:07
# XXX This script works, but is not beautiful.
# XXX I consider it to be a work in progress.

2016/09/01
# XXX Big problem: This script changes start points in the target UFO.
# XXX At this point, it seems easier to just revert the change in the
# XXX .glif files via git than re-writing the script.


Transfer group structure from source UFO to (kerned) target UFO.
----------------------------------------------------------------
This script is necessary if the groups change in one of several interpolating
masters -- they need to be re-unified.

If `verbatim` mode is on, the kerning data in the target UFO is absolutely the
same before & after; but there might be a number of new exceptions.

If `verbatim` mode is off, the best available group kerning value is chosen,
which might overwrite some zero-value exceptions. I found that to be the better
option in some cases.


required steps:
1. explode target kerning (handled outside)
2. match pairs to source groups
3. consolidate exploded kerning
4. delete target kerning & groups, replace data
'''


def glyphNameToFileName(glyphName, glyphSet):

    parts = glyphName.split(".")

    for partIndex, part in enumerate(parts):
        part = part.replace('_', '-')
        # substitute ligature markers with hyphens

        if part == '':
            part = '_'
            # rename .notdef to _.notdef

        letterList = list(part)
        for i, letter in enumerate(letterList):
            if letter != letter.lower():
                letter = '%s_' % letter
                letterList[i] = letter
                # marker following every capital letter

        part = '%s' % (''.join(letterList))
        parts[partIndex] = part

    return ".".join(parts) + ".glif"


class CustomWriter(ufoLib.UFOWriter):

    def getGlyphSet(self, glyphNameToFileNameFunc=None):
        glyphNameToFileNameFunc = glyphNameToFileName
        # print "Custom GN2FN active."
        return super(CustomWriter, self).getGlyphSet(glyphNameToFileNameFunc)


class Group(object):
    "Container for storing groups and related information."

    def __init__(self):
        self.glyphs = []
        self.name = ''
        self.side = ''
        self.used = False


class KerningPair(object):
    "Container for storing a kerning pair with attributes."

    def __init__(self):
        self.kerningPair = 0
        self.variations = 0
        self.recordedVariations = 0
        self.flatPairValueDict = {}


loggedProgress = []


def progressBar(totalCount, progressCount, increment=10, previousProgress=0):
    'simple progress bar'
    progress = '{:.0f}'.format(progressCount / totalCount * 100)
    if int(progress) % increment == 0 and not progress in loggedProgress:
        if int(progress) > 0:
            print '{}% done'.format(progress)
            loggedProgress.append(progress)


def organizeGroups(f):
    'function to give groups more attributes than they already have.'
    groupList = []
    usedGroups = set(
        [item for item in itertools.chain(*f.kerning.keys()) if item.startswith('@')])
    # for groupName, glyphList in f.groups.items():
    for groupName in usedGroups:
        group = Group()
        group.glyphs = f.groups[groupName]
        group.name = groupName

        if 'MMK_L' in groupName:
            group.side = 'L'
        elif 'MMK_R' in groupName:
            group.side = 'R'
        else:
            group.side = None
        groupList.append(group)

    return groupList


def askGlyphForGroupName(gName, side, groupList):
    for group in groupList:
        if gName in group.glyphs and group.side == side:
            return group.name
            break


def consolidateSingleException(sourceGlyphName, groupName, groupList, side, exceptionsDict):
    '''Merges single exception pairs back into group exceptions, as far as possible.'''
    # kernValueToPairList = {}
    kernValueToPairList = defaultdict(list)

    for glyphName in groupList:
        if side == 'L':
            pair = glyphName, sourceGlyphName
        elif side == 'R':
            pair = sourceGlyphName, glyphName

        # kernValueToPairList.setdefault(kernValue, []).append(pair)
        # kernValueToPairList[kernValue] = []
        kernValue = exceptionsDict[pair]
        kernValueToPairList[kernValue].append(pair)

    if len(kernValueToPairList) > 1:
        bestKernValue = max(
            kernValueToPairList, key=lambda x: len(kernValueToPairList[x]))
        pairs_to_consolidate = kernValueToPairList[bestKernValue]
    else:
        bestKernValue = kernValueToPairList.keys()[0]
        pairs_to_consolidate = kernValueToPairList.values()[0]

    for pair in pairs_to_consolidate:
        del exceptionsDict[pair]

    if side == 'L':
        newPair = groupName, sourceGlyphName
    elif side == 'R':
        newPair = sourceGlyphName, groupName

    exceptionsDict[newPair] = bestKernValue


def make_glyph_to_group_dict(f, side, groupList):
    sideDict = {}
    for glyphName in f.keys():
        groupName = askGlyphForGroupName(glyphName, side, groupList)
        if groupName != None:
            sideDict.setdefault(
                glyphName, askGlyphForGroupName(glyphName, side, groupList))
    return sideDict


def make_glyphList_to_group_dict(side, groupList):
    hashGroupDict = {}
    sideGroups = [group for group in groupList if group.side == side]
    for group in sideGroups:
        # hashGroupDict[hash(frozenset(group.glyphs))] = group.name
        hashGroupDict[frozenset(group.glyphs)] = group.name
    return hashGroupDict


def consolidateExceptions(exceptionDict, organizedGroups):

    leftGlyphListToGroupName = make_glyphList_to_group_dict(
        'L', organizedGroups)
    rightGlyphListToGroupName = make_glyphList_to_group_dict(
        'R', organizedGroups)

    print 'consolidating exceptions ...'
    leftExceptionGlyphs = set([left for left, right in exceptionDict.keys()])
    for leftGlyphName in leftExceptionGlyphs:
        kernedAgainst = [
            right for left, right in exceptionDict.keys() if left == leftGlyphName]
        for glyphList, groupName in rightGlyphListToGroupName.items():
            if glyphList <= set(kernedAgainst):
                consolidateSingleException(
                    leftGlyphName, groupName, glyphList, 'R', exceptionDict)

    rightExceptionGlyphs = set([right for left, right in exceptionDict.keys()])
    for rightGlyphName in rightExceptionGlyphs:
        kernedAgainst = [
            left for left, right in exceptionDict.keys() if right == rightGlyphName]
        for glyphList, groupName in leftGlyphListToGroupName.items():
            if glyphList <= set(kernedAgainst):
                consolidateSingleException(
                    rightGlyphName, groupName, glyphList, 'L', exceptionDict)

    return exceptionDict


def recordKerningPairData(flatPair, kerningPair, kernValue, allVariations, kerningPairData):

    kp = kerningPairData.setdefault(kerningPair, KerningPair())
    kp.kerningPair = kerningPair
    kp.flatPairValueDict.setdefault(kernValue, []).append(flatPair)
    kp.variations = allVariations
    kp.recordedVariations += 1


def makeValueDistribution(kerningPairData, verbatim=True):
    best_value_pairs = {}
    exceptions = {}

    if verbatim == True:
        print 'verbatim mode'
    else:
        print 'non-verbatim mode'

    print 'analyzing value distribution and finding best standard kerning value ...'
    for pair, pairData in kerningPairData.items():

        if verbatim == True:
            if pairData.variations == pairData.recordedVariations:
                # all kerning variations have been found. No unmentioned zero
                # kerns.
                if pairData.variations > 1:
                    # If a pair of groups is found kerned with different
                    # values, the value with maximum occurrence is being
                    # picked.
                    maxOccurring = max(
                        pairData.flatPairValueDict, key=lambda x: len(pairData.flatPairValueDict[x]))
                    bestValue = maxOccurring
                else:
                    bestValue = pairData.flatPairValueDict.keys()[0]

                best_value_pairs[pair] = bestValue

            else:
                # exceptions to non-kerned pairs.
                for kernValue, pairList in pairData.flatPairValueDict.items():
                    for pair in pairList:
                        exceptions[pair] = kernValue
                        print 'exception to unkerned class found: %s %s' % (' '.join(pair), kernValue)
        else:
            # this mode adds kerning pairs, removes exceptions.
            if pairData.variations > 1:
                # If a pair of groups is found kerned with different values,
                # the value with maximum occurrence is being picked.
                maxOccurring = max(
                    pairData.flatPairValueDict, key=lambda x: len(pairData.flatPairValueDict[x]))
                bestValue = maxOccurring
            else:
                bestValue = pairData.flatPairValueDict.keys()[0]

            best_value_pairs[pair] = bestValue

    return best_value_pairs, exceptions


def transferGroups(f_source, f_target):
    f_target.groups.clear()
    newGroups = {}
    targetGlyphs = set(f_target.keys())

    for group, glyphList in f_source.groups.items():
        # newGlyphList = list(set(glyphList) & targetGlyphs)
        # if len(newGlyphList) != len(glyphList):
        #     print group
        #     print set(newGlyphList) - set(glyphList)
        newGroups[group] = sorted(list(set(glyphList) & targetGlyphs))

    f_target.groups.update(newGroups)


def analyzeKerning(f_source, f_target, flattenedPairDict, organizedSourceGroups):
    # this works great if input- and output font is the same. But not for
    # transfer (yet)

    singleGlyphsL = set([left for (left, right) in itertools.chain(
        f_source.kerning.keys()) if not left.startswith('@')])
    singleGlyphsR = set([right for (left, right) in itertools.chain(
        f_source.kerning.keys()) if not right.startswith('@')])
    # list of glyphs kerned on left and right side with additional info

    leftGroupsGlyphLists = [
        group.glyphs for group in organizedSourceGroups if group.side == 'L']
    rightGroupsGlyphLists = [
        group.glyphs for group in organizedSourceGroups if group.side == 'R']
    # nested list of glyph names

    exploded_group_pairs = []
    left_vs_exploded_pairs = []
    exploded_vs_right_pairs = []

    print 'exploding all groups ...'
    for leftGroupList, rightGroupList in itertools.product(leftGroupsGlyphLists, rightGroupsGlyphLists):
        exploded_group_pairs.extend(
            itertools.product(leftGroupList, rightGroupList))

    print 'exploding single glyphs vs right groups ...'
    for rightGroupList in rightGroupsGlyphLists:
        left_vs_exploded_pairs.extend(
            itertools.product(singleGlyphsL, rightGroupList))

    print 'exploding left groups vs single glyphs ...'
    for leftGroupList in leftGroupsGlyphLists:
        exploded_vs_right_pairs.extend(
            itertools.product(leftGroupList, singleGlyphsR))

    print 'analyzing all single pairs ...'
    all_single_pairs = [
        pair for pair in itertools.product(singleGlyphsL, singleGlyphsR)]

    print 'creating reverse group lookup dictionaries ...'
    leftG2GDict = make_glyph_to_group_dict(
        f_source, 'L', organizedSourceGroups)
    rightG2GDict = make_glyph_to_group_dict(
        f_source, 'R', organizedSourceGroups)

    flattenedPairDictSet = set(flattenedPairDict.keys())
    exploded_group_pairs_set = set(exploded_group_pairs)
    left_vs_exploded_pairs_set = set(left_vs_exploded_pairs)
    exploded_vs_right_pairs_set = set(exploded_vs_right_pairs)

    kerningPairData = {}
    # dictionary of kerning pairs and kerningPair objects.

    gr_gr_set = set.intersection(
        exploded_group_pairs_set, flattenedPairDictSet)
    gl_gr_set = set.intersection(
        left_vs_exploded_pairs_set, flattenedPairDictSet)
    gr_gl_set = set.intersection(
        exploded_vs_right_pairs_set, flattenedPairDictSet)
    gl_gl_set = flattenedPairDictSet - exploded_group_pairs_set - \
        left_vs_exploded_pairs_set - exploded_vs_right_pairs_set - gr_gl_set

    progressCount = 0
    totalCount = sum(map(len, [gr_gr_set, gl_gr_set, gr_gl_set, gl_gl_set]))

    print 'iterating through all possible kerning combinations (%s) ...' % len(flattenedPairDict)

    for (left, right) in gr_gr_set:
        progressCount += 1
        progress = progressBar(totalCount, progressCount)
        leftGroupName = leftG2GDict[left]
        rightGroupName = rightG2GDict[right]
        kerningPair = leftGroupName, rightGroupName
        kernValue = flattenedPairDict[(left, right)]
        allVariations = len(list(itertools.product(
            f_source.groups[leftGroupName], f_source.groups[rightGroupName])))
        recordKerningPairData(
            (left, right), kerningPair, kernValue, allVariations, kerningPairData)

    for (left, right) in gl_gr_set:
        progressCount += 1
        progress = progressBar(totalCount, progressCount)
        rightGroupName = rightG2GDict[right]
        kerningPair = left, rightGroupName
        kernValue = flattenedPairDict[(left, right)]
        allVariations = len(
            list(itertools.product([left], f_source.groups[rightGroupName])))
        recordKerningPairData(
            (left, right), kerningPair, kernValue, allVariations, kerningPairData)

    for (left, right) in gr_gl_set:
        progressCount += 1
        progress = progressBar(totalCount, progressCount)
        leftGroupName = leftG2GDict[left]
        kerningPair = leftGroupName, right
        kernValue = flattenedPairDict[(left, right)]
        allVariations = len(
            list(itertools.product(f_source.groups[leftGroupName], [right])))
        recordKerningPairData(
            (left, right), kerningPair, kernValue, allVariations, kerningPairData)

    for (left, right) in gl_gl_set:
        progressCount += 1
        progress = progressBar(totalCount, progressCount)
        kerningPair = left, right
        kernValue = flattenedPairDict[(left, right)]
        allVariations = 1
        recordKerningPairData(
            (left, right), kerningPair, kernValue, allVariations, kerningPairData)

    # best_value_pairs, flatExceptions = makeValueDistribution(kerningPairData, verbatim=False)
    best_value_pairs, flatExceptions = makeValueDistribution(
        kerningPairData, verbatim=True)

    for (left, right), value in flattenedPairDict.items():
        leftItem = leftG2GDict.get(left, left)
        rightItem = rightG2GDict.get(right, right)

        pair = leftItem, rightItem
        # pair_with_value = leftItem, rightItem, value

        if best_value_pairs.get(pair) == value:
            del flattenedPairDict[(left, right)]

        else:
            if not (left, right) in flatExceptions:
                flatExceptions[(left, right)] = value
            else:
                if flatExceptions.get((left, right)) == value:
                    continue
                else:
                    print 'conflicting Exceptions:', left, right, value
            del flattenedPairDict[(left, right)]

    exceptions = consolidateExceptions(flatExceptions, organizedSourceGroups)

    print 'building new kerning object ...'
    newKerning = {}
    newKerning.update(best_value_pairs)
    # print len(best_value_pairs)
    newKerning.update(exceptions)

    return newKerning


ufoLib.UFOWriter = CustomWriter
# subclassing UFO writer to use the writer contained in this script.

f_source = Font(sys.argv[-2])
f_target = Font(sys.argv[-1])
# if f_target.lib['org.unifiedfontobject.normalizer.modTimes']:
#     del(f_target.lib['org.unifiedfontobject.normalizer.modTimes'])

inputDirName, inputFileName = os.path.split(f_target.path.rstrip(os.sep))
outputFileName = inputFileName.replace('.ufo', '_mod.ufo')
outputPath = os.path.join(inputDirName, outputFileName)

flatTargetPairsDict = getKerningPairsFromUFO.UFOkernReader(
    f_target, includeZero=True).allKerningPairs
organizedSourceGroups = organizeGroups(f_source)
newKerning = analyzeKerning(
    f_source, f_target, flatTargetPairsDict, organizedSourceGroups)

transferGroups(f_source, f_target)
f_target.kerning.clear()
f_target.kerning.update(newKerning)

f_target.lib['com.typesupply.MetricsMachine4.groupColors'] = f_source.lib[
    'com.typesupply.MetricsMachine4.groupColors']
f_target.save(outputPath)

print 'done.'
elapsedTime = time.time() - startTime
print '{:.2f} seconds'.format(elapsedTime)
