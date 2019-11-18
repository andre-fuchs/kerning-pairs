# writes FLC-style classes from UFO
# Don't forget to delete Metrics Machine reference groups!
from defcon import Font as defconFont
import re, os, sys


if len(sys.argv) > 1:
	input = sys.argv[1]
else:
	print 'No UFO file provided.'
	sys.exit()
	
if os.path.exists(input):
	font = defconFont(input)
else:
	print 'No UFO file provided.'
	sys.exit()

# filePath = GetFile("Pick UFO...")
kerningGroups = [groupName for groupName in font.groups.keys() if '@MMK_' in groupName]
otherGroups = [groupName for groupName in font.groups.keys() if not groupName in kerningGroups]
	
def getKeyGlyph(groupName):
	if groupName in kerningGroups:
		if alt_mode:
			# this is for groups named 'LAT_LC_a', 'CYR_LC_a.cyr' etc.
	
			if groupName.split('_')[-1] in font.groups[groupName]:
				return '%s' % groupName.split('_')[-1]
			elif '%s_%s' % (groupName.split('_')[-2], groupName.split('_')[-1]) in font.groups[groupName]: # ligatures
				return '%s_%s' % (groupName.split('_')[-2], groupName.split('_')[-1])
			elif '%s_%s_%s' % (groupName.split('_')[-3], groupName.split('_')[-2], groupName.split('_')[-1]) in font.groups[groupName]: # ligatures
				return '%s_%s_%s' % (groupName.split('_')[-3], groupName.split('_')[-2], groupName.split('_')[-1])
			else:
				return font.groups[groupName][0]
	
		else:
			# this is for groups named 'I', 'I_LC', 'S_LC_LEFT_LAT' etc.
			# assuming Metrics Machine-built group names
			glyph = groupName.split('_')[2]

 			if glyph in font.groups[groupName]:
 				return '%s' % glyph
 			elif glyph.lower() in font.groups[groupName]:
 				return '%s' % glyph.lower()
 				
# 			elif '%s_%s' % (groupName.split('_')[-2], groupName.split('_')[-1]) in font.groups[groupName]: # ligatures
# 				return '%s_%s' % (groupName.split('_')[-2], groupName.split('_')[-1])
# 			elif '%s_%s_%s' % (groupName.split('_')[-3], groupName.split('_')[-2], groupName.split('_')[-1]) in font.groups[groupName]: # ligatures
# 				return '%s_%s_%s' % (groupName.split('_')[-3], groupName.split('_')[-2], groupName.split('_')[-1])

			else:
				return font.groups[groupName][0]


def getOtherGlyphs(groupName):
	if groupName in kerningGroups:
		glyphlist = font.groups[groupName]
		glyphlist.remove(getKeyGlyph(groupName))
		return sorted(glyphlist)


def getFlag(groupName):
	if groupName in kerningGroups:
		return groupName.split('_')[1]


def getWSystem(groupName):
	wSystem = None
	for i in groupName.split('_'):
		if re.match(r'(LAT|GRK|CYR)', i):
			wSystem = i
			break
	return wSystem


def getCase(groupName):
	case = None
	for i in groupName.split('_'):
		if len(i) > 1:
			if re.match(r'(UC|LC)', i):
					case = i
	return case

def adobeName(groupName):
	# change class name to match adobe class naming.
	if getFlag(groupName) == 'L':
		flag = 'LEFT'
	else: flag = 'RIGHT'

	name = '_%s' % getKeyGlyph(groupName)

	if getCase(groupName):
		name += '_%s' % getCase(groupName)

	name += '_%s' % flag
	
	if getWSystem(groupName):
		name += '_%s' % getWSystem(groupName)
	
	return name


def writeFLclass(groupName):
	return '''\
%%%%CLASS %s
%%%%GLYPHS  %s' %s
%%%%KERNING %s 0
%%%%END
''' % ('%s' % adobeName(groupName), getKeyGlyph(groupName), ' '.join(getOtherGlyphs(groupName)), getFlag(groupName))


## figure which way the classes are named:
alt_mode = False  # this is the alternate mode, for groups named 'LAT_LC_a', 'CYR_LC_a.cyr' etc.

rex = r'(LAT|CYR|GRK)_(LC|UC)'
counter = 0
for g in kerningGroups:
	if re.search(rex, g): counter += 1
if counter > len(kerningGroups)/2:
	alt_mode = False


# mode1 = False  # this is for groups named 'LAT_LC_a', 'CYR_LC_a.cyr' etc.
# mode2 = False  # this is for groups named 'I_LC', 'S_LC_LEFT_LAT' etc.
# 
# rex1 = r'(LAT|CYR|GRK)_(LC|UC)'
# rex2 = r'(.+?)_(LC|UC)'
# counter1 = 0
# counter2 = 0
# for g in font.groups.keys():
# 	if re.search(rex1, g): counter1 += 1
# 	elif re.search(rex2, g): counter2 += 1
# if counter1 > len(font.groups.keys())/2:
# 	mode1 = True
# if counter2 > len(font.groups.keys())/2:
# 	mode2 = True


print '%%FONTLAB CLASSES\n'

for groupName in sorted(kerningGroups):
#	groupName = '_%s' % groupName[1:]
	print writeFLclass(groupName)

if otherGroups:
	print '#' * 50
	print 'The follwing groups are not kerning groups,\nand were therefore not exported:\n\n%s' % '\n'.join(otherGroups)
