#!/bin/env python
import os
import sys
import xml.etree.ElementTree as ET

__doc__ = '''\
mmg to flc:
Converts Metrics Machine group files (.mmg) to
FontLab-compatible class files (.flc).

usage:
python mmg2flc.py file.mmg

'''


class Group(object):
    def __init__(self, name, keyglyph, side, glyphs):

        self.name = name
        self.side = side
        self.keyglyph = keyglyph
        self.glyphs = glyphs


class Parser(object):
    def __init__(self):
        self.glyphdict = {}
        self.grouplist = []
        self.output = []

    def parse(self, tree):
        for parent in tree.getiterator():
            if parent.tag == 'group':
                for child in parent:
                    self.glyphdict[parent.get('name')] = child.text.split()
        return self.glyphdict

    def makeClasses(self, group):
        self.group = group
        if len(group.glyphs) > 0:
            if group.keyglyph in group.glyphs:
                group.glyphs.remove(group.keyglyph)
                kg = group.keyglyph
            else:
                kg = group.glyphs[0]
                group.glyphs.remove(kg)

            # syntax example:
            '''\
            %%CLASS _PARENLEFT_SC_RIGHT
            %%GLYPHS  parenleft.sc' braceleft.sc bracketleft.sc
            %%KERNING R 0
            %%END
            '''

            self.output.append('%%%%CLASS _%s\r%%%%GLYPHS  %s\' %s\r%%%%KERNING %s 0\r%%%%END\r' % (group.name, kg, ' '.join(group.glyphs), group.side))
            return self.output

    def convert(self):
        li = []
        for i in self.glyphdict:
            li.append(i)

        for i in li:
            spli = [i.split('_') for i in li]

        for i in spli:
            while len(i) != 5:
                i.append('')

        deco = [((a[3], a[1]), a) for a in spli]
        deco.sort()
        sorted = [v for k, v in deco]

        for i in sorted:
            i = filter(None, i)
            i = '_'.join(i)

            # finding side
            if 'LEFT' in i.split('_'):
                side = 'L'
            elif 'RIGHT' in i.split('_'):
                side = 'R'
            else:
                side = 'LR'

            # finding keyglyph
            if len(i.split('_')) > 3:
                if i.split('_')[1] == 'UC':
                    kg = i.split('_')[0].title()
                elif i.split('_')[1] == 'LC':
                    kg = i.split('_')[0].lower()
                elif i.split('_')[1] == 'SC':
                    kg = '%s.sc' % i.split('_')[0].lower()
                else:
                    kg = i.split('_')[0].lower()
            else:
                kg = i.split('_')[0].lower()

            # the glyphs`
            glyphs = self.glyphdict[i]

            myGroup = Group(i, kg, side, glyphs)
            self.makeClasses(myGroup)


def readFile(path):
    # Reading content of a file, closing the file.

    file = open(path, 'r')
    data = file.read()
    file.close()
    return data


def run():

    inputfile = sys.argv[1]
    path = inputfile.split(os.sep)[:-1]
    outputfilename = '%s.flc' % inputfile.split(os.sep)[-1].split('.')[0]
    input = readFile(inputfile)

    mmgconverter = Parser()
    tree = ET.XML(input)
    mmgconverter.parse(tree)
    mmgconverter.convert()

    path.append(outputfilename)
    outputfile = open(os.sep.join((path)), 'w')
    outputfile.write('%%FONTLAB CLASSES\r\r')
    for i in mmgconverter.output:
        outputfile.write(i)
        outputfile.write('\r')
    outputfile.close()


if __name__ == "__main__":
    run()
