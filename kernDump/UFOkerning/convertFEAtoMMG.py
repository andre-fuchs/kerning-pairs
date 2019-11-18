import re
import os, sys
from random import randint

if len(sys.argv) > 1:
	input = sys.argv[1]
else:
	print 'No feature file provided.'
	sys.exit()

if os.path.isfile(input):
 	f = open(input, 'r')
	output = open(os.path.splitext(f.name)[0]+'.mmg', 'w')
else:
	print 'No proper UFO file provided.'
	sys.exit()


leftglyphs = []
rightglyphs = []
#start writing the mmg file
output.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n<xml>\n')

#finding out which glyphs are present in a class
# def glyphlist(line):
# 	result = ''
# 	result += '    <glyphs>\n'
# 	
# 	glyphs = line.split('[')[1]
# 	glyphs = glyphs.strip('];\n').split()
# 	for x in glyphs:
# 		result += '      '+x+'\n'
# 	result += '    </glyphs>\n  </group>\n'
# 	return result
		

#writing groups, and finally putting the glyphs inside
def kernclass():
	glyphXMLstring = ''
	for line in f:
		left = False
		right = False
		red = str(0.1*randint(0,10))+' '
		green = str(0.1*randint(0,10))+' '
		blue = str(0.1*randint(0,10))+' '
		start = ('  <group color="'+ red + green + blue +'0.25" name="')
		end_l = ('" side="left" type="kerning">\n')
		end_r = ('" side="right" type="kerning">\n')


		# @ALPHA_UC_LEFT_GRK
		if line.startswith('@'):
#			glyphXMLstring = glyphlist(line)
			classname = line.split('=')[0].strip('@ ')
			glyphs = line.split('[')[1]
			glyphs = glyphs.strip('];\n').split()
			
			glyphXMLstring = '    <glyphs>\n      %s\n    </glyphs>\n  </group>' % '\n      '.join(glyphs)

			
			if 'LEFT' in classname.split('_'):
				left = True
			elif 'RIGHT' in classname.split('_'):
				right = True
			else:
				(left, right) = (True, True)
				

				
			if (left, right) == (True, True):
				ok = False
				for g in glyphs:
					if not g in leftglyphs:
		 				leftglyphs.append(g)
						ok = True
		 			else:
		 				print 'Glyph %s has already been used. Check class %s' % (g, classname)
						ok = False
						break
				if ok:
					print classname, 'fine'
					output.write(start+classname+end_l)		
					output.write(glyphXMLstring)

				ok = False			
				for g in glyphs:
					if not g in rightglyphs:
						rightglyphs.append(g)
						ok = True
		 			else:
		 				print 'Glyph %s has already been used. Check class %s' % (g, classname)
						ok = False
						break
				
				if ok:
					output.write(start+classname+end_r)
					output.write(glyphXMLstring)

			if (left, right) == (True, False):
				ok = False
				for g in glyphs:
					if not g in leftglyphs:
		 				leftglyphs.append(g)
						ok = True
		 			else:
		 				print 'Glyph %s has already been used. Check class %s' % (g, classname)
						ok = False
						break
				if ok:
					output.write(start+classname+end_l)		
					output.write(glyphXMLstring)

			if (left, right) == (False, True):
				ok = False			
				for g in glyphs:
					if not g in rightglyphs:
						rightglyphs.append(g)
						ok = True
		 			else:
		 				print 'Glyph %s has already been used. Check class %s' % (g, classname)
						ok = False
						break
				
				if ok:
					output.write(start+classname+end_r)
					output.write(glyphXMLstring)


#run
kernclass()

output.write('\n</xml>')

#cleanup
f.close()
output.close()


	