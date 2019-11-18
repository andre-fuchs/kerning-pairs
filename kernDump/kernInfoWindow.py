# coding: utf-8
from vanilla import Window, RadioGroup, TextBox, Slider, Button
import getKerningPairsFromUFO
import os


class KernInfoWindow(object):

    def __init__(self):
        self.f = CurrentFont()
        self.u = getKerningPairsFromUFO.UFOkernReader(self.f)
        self.absKerning = int(self.u.absoluteKerning)
        self.amountOfPairs = len(self.u.allKerningPairs)

        self.textString = (
            'The font has %s flat kerning pairs.\n'
            'Set at %s points, the absolute amount\n'
            'of kerning would cover the distance of\n%s.')

        wWidth = 300
        wHeight = 250

        if self.amountOfPairs:
            message = u'CONGRATULATIONS! \U0001F600'
        else:
            message = u'Bummer. \U0001F622'

        self.w = Window((wWidth, wHeight), message)

        self.w.measurementSystem = RadioGroup(
            (20, 15, -10, 20),
            ["Metric", "Imperial"],
            callback=self.parametersChanged,
            isVertical=False)

        self.w._pointSize = TextBox(
            (20, 145, -30, 17),
            'Point size:')

        self.w.pointSize = Slider(
            (100, 145, -30, 17),
            minValue=0,
            maxValue=1000,
            callback=self.parametersChanged,
            value=12)

        pointSize = int(self.w.pointSize.get())
        absKerning = int(
            self.absKerning * (pointSize / self.f.info.unitsPerEm))

        self.w.text = TextBox(
            (20, 45, -20, 85),
            self.textString % (
                self.amountOfPairs,
                int(self.w.pointSize.get()),
                self.convertToMetric(absKerning)))

        self.w.button = Button(
            (20, -40, -30, 20),
            "Copy kerning pairs to clipboard",
            callback=self.button)

        self.w.open()

    def convertToImperial(self, number):
        remainderList = []

        if number >= 72:
            # points to inches:
            number, remainder = divmod(number, 72)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        if number >= 12:
            # inches to feet:
            number, remainder = divmod(number, 12)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        # if number >= 3:
        #     # feet to yards:
        #     number, remainder = divmod(number, 3)
        #     remainderList.insert(0, remainder)
        #     if number == 0:
        #         remainderList.insert(0, number)

        if number >= 5280:
            # feet to miles:
            number, remainder = divmod(number, 5280)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        remainderList.insert(0, number)
        while len(remainderList) < 4:
            remainderList.insert(0, 0)

        remainderList = [int(round(number)) for number in remainderList]

        unitsList = ['miles', 'feet', 'inches', 'points']
        singularUnits = {
            'miles': 'mile',
            'feet': 'foot',
            'inches': 'inch',
            'points': 'point'}

        combinedList = zip(remainderList, unitsList)
        sentenceList = []

        for (number, unit) in combinedList:
            if int(number) != 0:
                if int(number) == 1:
                    sentenceList.append(
                        u'%s\u00A0%s' % (number, singularUnits[unit]))
                else:
                    sentenceList.append(
                        u'%s\u00A0%s' % (number, unit))

        if len(sentenceList) == 0:
            sentenceList = ['absolutely zero']

        if len(sentenceList) > 1:
            sentenceList.insert(-1, 'and')

        sentence = ', '.join(sentenceList)
        sentence = sentence.replace(', and,', ' and')

        return sentence

    def convertToMetric(self, number):
        # ps point assumed
        number = number * 0.352777778
        # ps point to millimeters

        remainderList = []

        if number >= 10:
            # mm to cm
            number, remainder = divmod(number, 10)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        if number >= 100:
            # cm to m
            number, remainder = divmod(number, 100)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        if number >= 1000:
            # m to km
            number, remainder = divmod(number, 1000)
            remainderList.insert(0, remainder)

            if number == 0:
                remainderList.insert(0, number)

        remainderList.insert(0, number)
        remainderList = [int(round(number)) for number in remainderList]

        while len(remainderList) < 4:
            remainderList.insert(0, 0)

        unitsList = ['km', 'm', 'cm', 'mm']
        combinedList = zip(remainderList, unitsList)
        sentenceList = []

        for (number, unit) in combinedList:
            if number != 0:
                sentenceList.append(u'%s\u00A0%s' % (number, unit))

        if len(sentenceList) == 0:
            sentenceList = ['absolutely zero']

        if len(sentenceList) > 1:
            sentenceList.insert(-1, 'and')

        sentence = ', '.join(sentenceList)
        sentence = sentence.replace(', and,', ' and')

        return sentence

    def parametersChanged(self, sender=None):

        measurementSystem = self.w.measurementSystem.get()
        pointSize = int(self.w.pointSize.get() / 4.0) * 4
        absKerning = int(self.absKerning * pointSize / self.f.info.unitsPerEm)

        if measurementSystem == 0:
            absKerning = self.convertToMetric(absKerning)
        else:
            absKerning = self.convertToImperial(absKerning)

        self.w.text.set(
            self.textString % (self.amountOfPairs, pointSize, absKerning))

    def button(self, sender=None):

        output = '\n'.join(self.u.output)
        scrap = os.popen('pbcopy', 'w')
        scrap.write(output)
        scrap.close()


if CurrentFont():
    KernInfoWindow()
else:
    print('No font is open.')
