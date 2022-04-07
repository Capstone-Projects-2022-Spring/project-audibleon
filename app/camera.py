# imports for camera.py
import threading
import binascii
from time import sleep
# from utils import base64_to_pil_image, pil_image_to_base64

# imports for makeup_artist.py
from PIL import Image

# imports for util.py
from io import BytesIO
import base64
import numpy as np
import cv2

################
# From util.py #
################

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
#
# def pil_image_to_base64(pil_image):
#     buf = BytesIO()
#     pil_image.save(buf, format="JPEG")
#     return base64.b64encode(buf.getvalue())
#
#
# def base64_to_pil_image(base64_img):
#     return Image.open(BytesIO(base64.b64decode(base64_img)))

#########################
# From makeup_artist.py #
#########################

class Makeup_artist(object):
    def __init__(self):
        pass
    def apply_makeup(self, img):
        return cv2.flip(img, 1)
        #return img.transpose(Image.FLIP_LEFT_RIGHT)

##################
# From camera.py #
##################

class Camera(object):
    def __init__(self, makeup_artist):
        self.to_process = []
        self.to_output = []
        self.makeup_artist = makeup_artist

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return

        # input is an ascii string.
        input_str = self.to_process.pop(0)

        # convert it to a pil image
        input_img = base64ToOpenCV(input_str)

        ################## where the hard work is done ############

        # output_img is an PIL image
        output_img = self.makeup_artist.apply_makeup(input_img)

        # output_str is a base64 string in ascii
        output_str = openCVTobase64(output_img)

        # convert eh base64 string in ascii to base64 string in _bytes_
        self.to_output.append(binascii.a2b_base64(output_str))

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)