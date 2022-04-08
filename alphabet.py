import cv2
import keyboard
import mediapipe as mp
import time
import importlib
import handTrackingModule as htm
importlib.reload(htm)
from math import *
from detection import myWords

def length(start, end):
    x1, y1 = start
    x2, y2 = end
    x = (x2 - x1)**2
    y = (y2 - y1)**2
    return sqrt(x+y)

def lineTrack(frame, lmList, p1, p2, draw=True):
    if len(lmList) != 0:
        startPoint = (lmList[p1][1], lmList[p1][2])
        endPoint = (lmList[p2][1], lmList[p2][2])

        if draw:
            frame = cv2.line(frame, startPoint, endPoint, (255, 255, 255), 9)
    return (frame, startPoint, endPoint)


def a(lmList):
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

def b(lmList):
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

def c(lmList):
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

def d(lmList):
    if len(lmList) != 0:
        index = lmList[8][2] > lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] < lmList[14][2]
        pinky = lmList[20][2] < lmList[18][2]
        distance = length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

        if index and middle and ring and pinky and distance < 70:
            return 1
        else:
            return 0

def e(lmList):
    if len(lmList) != 0:
        index = lmList[8][2] > lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] < lmList[14][2]
        pinky = lmList[20][2] < lmList[18][2]
        distance = length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

        if index and middle and ring and pinky and distance < 20:
            return 1
        else:
            return 0

def f(lmList):
    if len(lmList) != 0:
        middle = lmList[12][2] > lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        distance = length((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

        if middle and ring and pinky and distance < 20:
            return 1
        else:
            return 0

def g(lmList):
    if (lmList):
        index = lmList[8][1] < lmList[6][1]
        middle = lmList[12][1] > lmList[10][1]
        ring = lmList[16][1] > lmList[14][1]
        pinky = lmList[20][1] > lmList[18][1]
        thumb = lmList[4][1] < lmList[3][1]
        distance = length((lmList[6][1], lmList[6][2]), (lmList[4][1], lmList[4][2]))

        if index and middle and ring and pinky and thumb and distance < 60:
            return 1
        else:
            return 0

def h(lmList):
    if (lmList):
        index = lmList[8][1] < lmList[6][1]
        middle = lmList[12][1] < lmList[10][1]
        ring = lmList[16][1] > lmList[14][1]
        pinky = lmList[20][1] > lmList[18][1]
        thumb = lmList[4][1] < lmList[3][1]
        distance = length((lmList[6][1], lmList[6][2]), (lmList[4][1], lmList[4][2]))

        if index and middle and ring and pinky and thumb and distance < 60:
            return 1
        else:
            return 0

def i(lmList):
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

def k(lmList):
    if (lmList):
        index = lmList[8][2] < lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        distance = length((lmList[10][1], lmList[10][2]), (lmList[4][1], lmList[4][2]))

        if index and middle and ring and pinky and distance < 40:
            return 1
        else:
            return 0

def l(lmList):
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

def m(lmList):
    if (lmList):
        index = lmList[8][2] > lmList[6][2]
        middle = lmList[12][2] > lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        thumb_in = lmList[3][3] > lmList[11][3]
        distance = length((lmList[7][1], lmList[7][2]), (lmList[3][1], lmList[3][2]))

        if index and middle and ring and pinky and thumb_in and distance < 30:
            return 1
        else:
            return 0

def n(lmList):
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

# def o():
# def p():
# def q():

def r(lmList):
    if (lmList):
        index = lmList[8][2] < lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        thumb = lmList[4][1] > lmList[3][1]
        distance = length((lmList[11][1], lmList[11][2]), (lmList[7][1], lmList[7][2]))

        if index and middle and ring and pinky and thumb and distance < 20:
            return 1
        else:
            return 0


def s(lmList):
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


def t(lmList):
    if (lmList):
        index = lmList[8][2] > lmList[6][2]
        middle = lmList[12][2] > lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        thumb_in = lmList[3][3] > lmList[11][3]
        thumb_up = lmList[4][2] < lmList[14][2]
        distance = length((lmList[7][1], lmList[7][2]), (lmList[3][1], lmList[3][2]))

        if index and middle and ring and pinky and thumb_in and thumb_up and distance < 20:
            return 1
        else:
            return 0


def u(lmList):
    if (lmList):
        index = lmList[8][2] < lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        thumb = lmList[4][1] > lmList[3][1]
        distance = length((lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]))

        if index and middle and ring and pinky and thumb and distance < 30:
            return 1
        else:
            return 0


def v(lmList):
    if (lmList):
        index = lmList[8][2] < lmList[6][2]
        middle = lmList[12][2] < lmList[10][2]
        ring = lmList[16][2] > lmList[14][2]
        pinky = lmList[20][2] > lmList[18][2]
        thumb = lmList[4][1] > lmList[3][1]
        distance = length((lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]))

        if index and middle and ring and pinky and thumb and distance > 40:
            return 1
        else:
            return 0


def w(lmList):
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

def y(lmList):
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
# def space():
# def delete():
# def period():
# def exclamation():
# def question():

def leftOrRight(handsType):
    for handType in handsType:
        if handType == 'Right':
            return 1
        else:
            return 0

def frontOrBack(lmList, handsType):
    if len(lmList) != 0:
        p1 = lmList[5][1]
        p2 = lmList[17][1]
        if leftOrRight(handsType):
            if p2 > p1:
                return 1
            elif p1 > p2:
                return 0
        else:
            if p2 < p1:
                return 1
            elif p1 < p2:
                return 0

def isPercentageOf(p1, p2):
    percentage = ((p1 - p2)/p2) * 100
    return percentage


def isSide(lmList, handsType):
    if len(lmList) != 0:
        xp1 = lmList[5][1]
        xp2 = lmList[17][1]
        zp1 = lmList[5][3]
        zp2 = lmList[17][3]
        if zp2 > zp1 and (xp2 - xp1) < 30:
            return 1
        else:
            return 0

cam = cv2.VideoCapture(0)

def activateLetters(m: myWords, h: htm.handDetector):
    pTime = 0
    oldLetter = ''
    string = ''
    while True:
        success, frame = cam.read()
        frame = cv2.flip(frame, 1)

        frame = h.findHands(frame)

        lmList = h.findPosition(frame, draw=False)
        handsType = h.findHandType()


        newLetter = getLetter(lmList)

        if newLetter != '':
            if oldLetter != newLetter:
                string = string + newLetter
                oldLetter = newLetter
                m.resetList()
                m.addWord(string)
        #
        # if newLetter is not None:
        #     if (oldWord is not None) and newLetter != ' ':
        #
        #
        #     if oldLetter != newLetter:
        #         oldLetter = newLetter
        #
        #         if newLetter != ' ':
        #             newWord = newWord + newLetter
        #             print(newWord)
        #
        # if oldWord != newWord:
        #     print(oldWord+'!'+newWord)
        #
        #     m.addWord(newWord)
        #     oldWord = newWord
        #     newWord = ''

        cv2.putText(frame, newLetter, (0, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # if len(lmList) != 0:
        # if(lmList[5][3] > 130):
        # if(lmList[9][3] < lmList[5][3]):
        # z = lmList[9][3]
        # z2 = lmList[5][3]
        # cv2.putText(frame, f'pinky{z} < index{z2}', (0, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

        # Calculating the Frames per Seconds (FPS)
        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime

        # Displaying the FPS (ERROR PRINTING HIGH NUMBERS)
        # cv2.putText(frame, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        try:
            if keyboard.is_pressed('q'):
                print("exiting model")
                cam.release()
                return m
        except:
            pass

def getLetter(lmList):
    letter = ''
    if (a(lmList)):
        letter='a'
    elif (b(lmList)):
        letter='b'
    elif (c(lmList)):
        letter='c'
    elif (d(lmList)):
        letter = 'd'
    elif (e(lmList)):
        letter = 'e'
    elif (f(lmList)):
        letter = 'f'
    elif (g(lmList)):
        letter = 'g'
    elif (h(lmList)):
        letter = 'h'
    elif (i(lmList)):
        letter = 'i'
    # elif (j(lmList)):
    #     letter = 'j'
    elif (k(lmList)):
        letter = 'k'
    elif (l(lmList)):
        letter = 'l'
    elif (m(lmList)):
        letter = 'm'
    elif (n(lmList)):
        letter = 'n'
    # elif (o(lmList)):
    #     letter = 'o'
    # elif (p(lmList)):
    #     letter = 'p'
    # elif (q(lmList)):
    #     letter = 'q'
    elif (r(lmList)):
        letter = 'r'
    elif (s(lmList)):
        letter = 's'
    elif (t(lmList)):
        letter = 't'
    elif (u(lmList)):
        letter = 'u'
    elif (v(lmList)):
        letter = 'v'
    elif (w(lmList)):
        letter = 'w'
    # elif (x(lmList)):
    #     letter = 'x'
    elif(y(lmList)):
        letter = 'y'
    # elif (z(lmList)):
    #     letter = 'z'

    return letter