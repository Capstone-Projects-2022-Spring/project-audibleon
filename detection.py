import os
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.utils import label_map_util
from object_detection.builders import model_builder
import cv2

WORKSPACE_PATH = 'RealTimeObjectDetection/Tensorflow/workspace'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
MODEL_PATH = WORKSPACE_PATH+'/models'
CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/'
CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'

class wordsModel(object):
    def __init__(self):
        self.configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
        self.detection_model = model_builder.build(model_config=self.configs['model'], is_training=False)
        print("model built")

        self.cap = cv2.VideoCapture(0)
        print("camera created")

        self.ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        self.ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-6')).expect_partial()
        self.category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH + '/label_map.pbtxt')
        self.label_map = read_label_map(ANNOTATION_PATH + '/label_map.pbtxt')
        print("checkpoints restored, label map created")

    @tf.function
    def detect_fn(self, image):
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

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