import cv2
import importlib
import handTrackingModule as htm
importlib.reload(htm)
from math import *

class letterModel(object):
    def __init__(self):
        self.handModel = htm.handDetector(detectionCon = 1)

    def length(self, start, end):
        x1, y1 = start
        x2, y2 = end
        x = (x2 - x1) ** 2
        y = (y2 - y1) ** 2
        return sqrt(x + y)

    def lineTrack(self, frame, lmList, p1, p2, draw=True):
        if len(lmList) != 0:
            startPoint = (lmList[p1][1], lmList[p1][2])
            endPoint = (lmList[p2][1], lmList[p2][2])

            if draw:
                frame = cv2.line(frame, startPoint, endPoint, (255, 255, 255), 9)
        return (frame, startPoint, endPoint)

    def a(self, lmList):
        if len(lmList) != 0:
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] < lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    def b(self, lmList):
        if len(lmList) != 0:
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            thumb = lmList[4][1] < lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    def c(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][2] < lmList[3][2]
            turned = lmList[12][1] > lmList[10][1]

            if index and middle and ring and pinky and thumb and turned:
                return 1
            else:
                return 0

    def d(self, lmList):
        if len(lmList) != 0:
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            distance = self.length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and distance < 70:
                return 1
            else:
                return 0

    def e(self, lmList):
        if len(lmList) != 0:
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            distance = self.length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and distance < 20:
                return 1
            else:
                return 0

    def f(self, lmList):
        if len(lmList) != 0:
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            distance = self.length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

            if middle and ring and pinky and distance < 20:
                return 1
            else:
                return 0

    def g(self, lmList):
        if (lmList):
            index = lmList[8][1] < lmList[6][1]
            middle = lmList[12][1] > lmList[10][1]
            ring = lmList[16][1] > lmList[14][1]
            pinky = lmList[20][1] > lmList[18][1]
            thumb = lmList[4][1] < lmList[3][1]
            distance = self.length((lmList[6][1], lmList[6][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and thumb and distance < 60:
                return 1
            else:
                return 0

    def h(self, lmList):
        if (lmList):
            index = lmList[8][1] < lmList[6][1]
            middle = lmList[12][1] < lmList[10][1]
            ring = lmList[16][1] > lmList[14][1]
            pinky = lmList[20][1] > lmList[18][1]
            thumb = lmList[4][1] < lmList[3][1]
            distance = self.length((lmList[6][1], lmList[6][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and thumb and distance < 60:
                return 1
            else:
                return 0

    def i(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    # j is a dynamic gesture
    # def j():

    def k(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            distance = self.length((lmList[10][1], lmList[10][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and distance < 40:
                return 1
            else:
                return 0

    def l(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] < lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    def m(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb_in = lmList[3][3] > lmList[11][3]
            distance = self.length((lmList[7][1], lmList[7][2]), (lmList[3][1], lmList[3][2]))

            if index and middle and ring and pinky and thumb_in and distance < 30:
                return 1
            else:
                return 0

    def n(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb_in = lmList[3][3] > lmList[11][3]
            thumb_up = lmList[4][2] < lmList[14][2]

            if index and middle and ring and pinky and thumb_in and thumb_up:
                return 1
            else:
                return 0

    def o(self, lmList):
        if (lmList):
            distance = self.length((lmList[16][1], lmList[16][2]), (lmList[4][1], lmList[4][2]))
            close_fingers = self.length((lmList[8][1], lmList[8][2]), (lmList[3][1], lmList[3][2]))
            turned = lmList[12][1] > lmList[10][1]

            if distance < 20 and close_fingers < 20 and turned:
                return 1
            else:
                return 0

    def p(self, lmList):
        if (lmList):
            index = lmList[8][1] < lmList[6][1]
            middle = lmList[12][1] < lmList[10][1]
            ring = lmList[16][1] > lmList[14][1]
            pinky = lmList[20][1] > lmList[18][1]
            thumb = lmList[4][1] < lmList[3][1]
            distance = self.length((lmList[6][1], lmList[6][2]), (lmList[4][1], lmList[4][2]))

            if index and middle and ring and pinky and thumb and distance < 60:
                return 1
            else:
                return 0

    # def q():

    def r(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]
            distance = self.length((lmList[11][1], lmList[11][2]), (lmList[7][1], lmList[7][2]))

            if index and middle and ring and pinky and thumb and distance < 20:
                return 1
            else:
                return 0

    def s(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    def t(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb_in = lmList[3][3] > lmList[11][3]
            thumb_up = lmList[4][2] < lmList[14][2]
            distance = self.length((lmList[7][1], lmList[7][2]), (lmList[3][1], lmList[3][2]))

            if index and middle and ring and pinky and thumb_in and thumb_up and distance < 20:
                return 1
            else:
                return 0

    def u(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]
            distance = self.length((lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]))

            if index and middle and ring and pinky and thumb and distance < 30:
                return 1
            else:
                return 0

    def v(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]
            distance = self.length((lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]))

            if index and middle and ring and pinky and thumb and distance > 40:
                return 1
            else:
                return 0

    def w(self, lmList):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] > lmList[18][2]
            thumb = lmList[4][1] > lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    # def x():

    def y(self, lmList):
        if (lmList):
            index = lmList[8][2] > lmList[6][2]
            middle = lmList[12][2] > lmList[10][2]
            ring = lmList[16][2] > lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            thumb = lmList[4][1] < lmList[3][1]

            if index and middle and ring and pinky and thumb:
                return 1
            else:
                return 0

    # def z():
    def space(self, lmList, handsType):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            distance = self.length((lmList[5][1], lmList[5][2]), (lmList[4][1], lmList[4][2]))

            if self.frontOrBack(lmList, handsType) and index and middle and ring and pinky and distance < 50:
                return 1
            else:
                return 0

    def delete(self, lmList, handsType):
        if (lmList):
            index = lmList[8][2] < lmList[6][2]
            middle = lmList[12][2] < lmList[10][2]
            ring = lmList[16][2] < lmList[14][2]
            pinky = lmList[20][2] < lmList[18][2]
            distance = self.length((lmList[5][1], lmList[5][2]), (lmList[4][1], lmList[4][2]))

            if not self.frontOrBack(lmList, handsType) and index and middle and ring and pinky and distance < 50:
                return 1
            else:
                return 0
    # def period():
    # def exclamation():
    # def question():

    def leftOrRight(self, handsType):
        for handType in handsType:
            if handType == 'Right':
                return 1
            else:
                return 0

    def frontOrBack(self, lmList, handsType):
        if len(lmList) != 0:
            p1 = lmList[5][1]
            p2 = lmList[17][1]
            if self.leftOrRight(handsType):
                if p2 > p1:
                    return 1
                elif p1 > p2:
                    return 0
            else:
                if p2 < p1:
                    return 1
                elif p1 < p2:
                    return 0

    def isPercentageOf(self, p1, p2):
        percentage = ((p1 - p2) / p2) * 100
        return percentage

    def isSide(self, lmList, handsType):
        if len(lmList) != 0:
            xp1 = lmList[5][1]
            xp2 = lmList[17][1]
            zp1 = lmList[5][3]
            zp2 = lmList[17][3]
            if zp2 > zp1 and (xp2 - xp1) < 30:
                return 1
            else:
                return 0

    def getLetter(self, lmList, handsType):
        letter = ''
        if (self.space(lmList, handsType)):
            letter = ' '
        elif (self.delete(lmList, handsType)):
            letter = '*'
        elif (self.a(lmList)):
            letter = 'a'
        elif (self.b(lmList)):
            letter = 'b'
        elif (self.c(lmList)):
            letter = 'c'
        elif (self.d(lmList)):
            letter = 'd'
        elif (self.e(lmList)):
            letter = 'e'
        elif (self.f(lmList)):
            letter = 'f'
        elif (self.g(lmList)):
            letter = 'g'
        elif (self.h(lmList)):
            letter = 'h'
        elif (self.i(lmList)):
            letter = 'i'
        # elif (j(lmList)):
        #     letter = 'j'
        elif (self.k(lmList)):
            letter = 'k'
        elif (self.l(lmList)):
            letter = 'l'
        elif (self.m(lmList)):
            letter = 'm'
        elif (self.n(lmList)):
            letter = 'n'
        elif (self.o(lmList)):
            letter = 'o'
        elif (self.p(lmList)):
            letter = 'p'
        # elif (q(lmList)):
        #     letter = 'q'
        elif (self.r(lmList)):
            letter = 'r'
        elif (self.s(lmList)):
            letter = 's'
        elif (self.t(lmList)):
            letter = 't'
        elif (self.u(lmList)):
            letter = 'u'
        elif (self.v(lmList)):
            letter = 'v'
        elif (self.w(lmList)):
            letter = 'w'
        # elif (x(lmList)):
        #     letter = 'x'
        elif (self.y(lmList)):
            letter = 'y'
        # elif (z(lmList)):
        #     letter = 'z'

        return letter
