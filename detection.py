import os
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import cv2
import numpy as np
import keyboard
from playsound import playsound

WORKSPACE_PATH = 'RealTimeObjectDetection/Tensorflow/workspace'
# SCRIPTS_PATH = 'RealTimeObjectDetection/Tensorflow/scripts'
# APIMODEL_PATH = 'RealTimeObjectDetection/Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
# IMAGE_PATH = WORKSPACE_PATH+'/images'
MODEL_PATH = WORKSPACE_PATH+'/models'
# PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'/pre-trained-models'
# CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/'
CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'

config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)
print("model built")

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("camera created")

def read_label_map(label_map_path):
    item_id = None
    item_name = None
    items = {}

    with open(label_map_path, "r") as file:
        for line in file:
            line.replace(" ", "")
            if line == "item{":
                pass
            elif line == "}":
                pass
            elif "id" in line:
                item_id = int(line.split(":", 1)[1].strip())-1
            elif "name" in line:
                item_name = line.split(":", 1)[1].replace("'", "").strip()

            if item_id is not None and item_name is not None:
                items[item_id] = item_name
                item_id = None
                item_name = None

    return items

ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-6')).expect_partial()
category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')
label_map = read_label_map(ANNOTATION_PATH+'/label_map.pbtxt')

class myWords:
    wordList = []
    modelRunning = 0

    def addWord(self, word):
        self.wordList.append(word)
    def resetList(self):
        self.wordList = []

def getCamera():
    return cap

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

def activateModel(m: myWords):
    oldWord = ''

    while True:
        ret, frame = cap.read()
        frame2 = cv2.flip(frame, 1)

        image_np = np.array(frame2)
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
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

                    newWord = label_map.get(gesture_id)
                    if oldWord != newWord:
                        m.addWord(newWord)
                        oldWord = newWord


                    # if gesture_id == 0:
                    #     playsound("hello_en.mp3")
                    # if gesture_id == 1:
                    #     playsound("help_en.mp3")
                    # if gesture_id == 2:
                    #     playsound("yes_en.mp3")
                    # if gesture_id == 3:
                    #     playsound("no_en.mp3")
                    # if gesture_id == 4:
                    #     playsound("i_en.mp3")
                    # if gesture_id == 5:
                    #     playsound("i_love_you_en.mp3")
                    # if gesture_id == 6:
                    #     playsound("stand_en.mp3")
                    # if gesture_id == 7:
                    #     playsound("telephone_en.mp3")
                    # if gesture_id == 8:
                    #     playsound("mom_en.mp3")
                    # if gesture_id == 9:
                    #     playsound("thank_you_en.mp3")

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.5,
            agnostic_mode=False)

        # cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
        ret, buffer = cv2.imencode('.jpg', image_np_with_detections)
        frame3 = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame3 + b'\r\n')

        try:
            if keyboard.is_pressed('q'):
                print("exiting model")
                cap.release()
                return m
        except:
            pass