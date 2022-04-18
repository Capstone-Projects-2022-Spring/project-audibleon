import cv2
import mediapipe as mp
import handTrackingModule as htm
import alphabet as alp
import math
from array import *
import unittest

class TestLetterModelMethods(unittest.TestCase):

    def setUp(self):
        self.alp = alp.letterModel()
        self.handsType = ['Right']
        self.lmList = [[0, 200, 300],
                      [1, 195, 280],
                      [2, 193, 278 ],
                      [3, 191, 276],
                      [4, 189, 274],
                      [5, 198, 272],
                      [6, 198, 270],
                      [7, 198, 268],
                      [8, 198, 266],
                      [9, 200, 272],
                      [10, 200, 270],
                      [11, 200, 268],
                      [12, 200, 266],
                      [13, 202, 272],
                      [14, 202, 270],
                      [15, 202, 268],
                      [16, 202, 266],
                      [17, 205, 272],
                      [18, 205, 270],
                      [19, 205, 268],
                      [20, 205, 266]]
        self.camera = cv2.VideoCapture(0)
        
    def test_length(self):
        p1 = (4, 7)
        p2 = (15, 30)
        x1, y1 = p1
        x2, y2 = p2
        self.assertEqual(self.alp.length(p1, p2), math.dist([x1, y1], [x2, y2]) )
        
    def test_leftOrRight(self):
        self.assertEqual(self.alp.leftOrRight(self.handsType), 1)
    
    def test_frontOrBack(self):
        self.assertEqual(self.alp.frontOrBack(self.lmList, self.handsType), 1)  
        
    def test_space(self):
        self.assertEqual(self.alp.space(self.lmList, self.handsType), 1)
        
    def test_capture(self):
        ret, frame = self.camera.read()
        self.assertTrue(ret)
        
    def tearDown(self):
        self.camera.release()
        
unittest.main(argv=[''], verbosity=2, exit=False)
if __name__ == '__main__':
    unittest.main()