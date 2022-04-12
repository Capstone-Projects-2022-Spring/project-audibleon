import threading
import binascii
from time import sleep
import base64
import numpy as np
import cv2
from detection import wordsModel
import tensorflow as tf
from object_detection.utils import visualization_utils as viz_utils
from alphabet import letterModel

def base64ToOpenCV(base64_img):
    im_bytes = base64.b64decode(base64_img)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def openCVTobase64(opencv_img):
    # img = cv2.imread(opencv_img)
    _, im_arr = cv2.imencode('.jpg', opencv_img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

class Camera(object):
    def __init__(self):
        self.to_process = []
        self.to_output = []
        self.wordList = []
        self.modelType = 0

        # self.cam = cv2.VideoCapture(0)

        self.words = wordsModel()
        self.letters = letterModel()

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def restartModel(self):
        self.to_output.clear()
        self.to_process.clear()

    def updateModel(self, num):
        if num < 1:
            self.modelType = 0
        else:
            self.modelType = 1

    # def baseRoutine(self):
    #     while True:
    #         success, frame = self.cam.read()
    #         if success:
    #
    #             frame = cv2.flip(frame, 1)
    #
    #             if self.modelType == 0:
    #                 output_img = self.processWordModel(frame)
    #             else:
    #                 output_img = self.processLettersModel(frame)
    #
    #             _, im_arr = cv2.imencode('.jpg', output_img)
    #             frame = im_arr.tobytes()
    #             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #         else:
    #             pass

    def process_one(self):
        if not self.to_process:
            return
        # input is an ascii string.
        input_str = self.to_process.pop(0)
        # convert to openCV format
        input_img = base64ToOpenCV(input_str)
        # flip horizontally before using for input
        # IF TURNING OFF MODEL HIDE THIS LINE
        input_img = cv2.flip(input_img, 1)

        ## IF TURNING OFF MODEL ENABLE THIS LINE
        # output_img = cv2.flip(input_img, 1)

        ## IF TURNING OFF MODEL HIDE THESE FOUR LINES
        if self.modelType == 0:
            output_img = self.processWordModel(input_img)
        else:
            output_img = self.processLettersModel(input_img)

        # output_str is a base64 string in ascii
        output_str = openCVTobase64(output_img)

        # convert eh base64 string in ascii to base64 string in _bytes_
        self.to_output.append(binascii.a2b_base64(output_str))


        # _, im_arr = cv2.imencode('.jpg', output_img)

        # self.to_output.append(im_arr)
        # im_bytes = im_arr.tobytes()
        #
        # im_b64 = base64.b64encode(im_bytes)
        #
        # # self.to_output.append(im_bytes)
        #
        # # # output_str is a base64 string in ascii
        # # output_bytes = openCVTobase64(input_img)
        #
        # # convert eh base64 string in ascii to base64 string in _bytes_
        # self.to_output.append(binascii.a2b_base64(im_b64))

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

        # while True:
        #     success, frame = self.cam.read()
        #     if success:
        #         frame = cv2.flip(frame, 1)
        #
        #         if self.modelType == 0:
        #             output_img = self.processWordModel(frame)
        #         else:
        #             output_img = self.processLettersModel(frame)
        #
        #         _, im_arr = cv2.imencode('.jpg', output_img)
        #         self.to_output.append(im_arr)
        #         # frame = im_arr.tobytes()
        #         # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #     else:
        #         pass

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)

    # process each frame with the full words model
    def processWordModel(self, input_img):
        if len(self.wordList) == 0:
            oldWord = ''
        else:
            oldWord = next(reversed(self.wordList))

        ## process image passed
        image_np = np.array(input_img)
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = self.words.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}

        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        label_id_offset = 1
        image_np_with_detections = image_np.copy()
        res = [(i, j) for i, j in zip(detections['detection_classes'], detections['detection_scores'])]

        for i in res:
            if i[1] >= .50:
                gesture_id = int(i[0])

                newWord = self.words.label_map.get(gesture_id)
                if oldWord != newWord:
                    self.wordList.append(newWord)
                    oldWord = newWord

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            self.words.category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.5,
            agnostic_mode=False)

        return image_np_with_detections

    # process a single frame with the letters model
    def processLettersModel(self, input_img):
        frame = self.letters.handModel.findHands(input_img)
        lmList = self.letters.handModel.findPosition(frame, draw=False)
        handsType = self.letters.handModel.findHandType()

        newLetter = self.letters.getLetter(lmList, handsType)

        if newLetter == '':
            pass
        elif len(self.wordList) == 0:
            # there is nothing in the word list currently - this is the first entry
            if (newLetter != ' ') and (newLetter != '*'):
                self.wordList.append(newLetter)
        else:
            oldWord = next(reversed(self.wordList))
            if len(oldWord) > 0:
                oldLetter = oldWord[-1]
            else:
                oldLetter = ''

            if oldLetter != newLetter:
                string = oldWord+newLetter
                if newLetter == '*':
                    string = string[:-2]
                self.wordList[len(self.wordList)-1] = string

        if newLetter == ' ':
            newLetter = 'SPACE'
        elif newLetter == '*':
            newLetter = 'DELETE'

        cv2.putText(frame, newLetter, (0, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        return frame
