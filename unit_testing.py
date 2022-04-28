import unittest, numpy, cv2, base64, detection, alphabet, camera
from camera import Camera
from website.models import User
import text_to_asl
import speech_recognition as sr

class TestDetection(unittest.TestCase):

    def test_model_built(self):
        model = detection.wordsModel()
        self.assertTrue(model.built, True)

    def test_camera_created(self):
        model = detection.wordsModel()
        self.assertTrue(model.camera, True)

    def test_model_checkpoints(self):
        model = detection.wordsModel()
        self.assertTrue(model.checkpoints, True)

class TestCamera(unittest.TestCase):

    def test_cameraClass_created(self):
        # tests to see if the camera is properly created with both model types
        camera = Camera()
        self.assertEqual(camera.modelType, 0)
        self.assertIsInstance(camera.words, detection.wordsModel)
        self.assertIsInstance(camera.letters, alphabet.letterModel)

    def test_camera_enqueue(self):
        # test to see if items can be added to the to_process list of the camera
        camera = Camera()
        self.assertEqual(len(camera.to_process), 0)
        camera.enqueue_input(100)
        self.assertEqual(len(camera.to_process), 1)
        camera.enqueue_input(200)
        self.assertEqual(len(camera.to_process), 2)

    def test_camera_restart(self):
        # test to see if the to_output and to_process lists are cleared
        camera = Camera()
        camera.enqueue_input(100)
        camera.enqueue_input(200)
        camera.enqueue_input(300)
        self.assertEqual(len(camera.to_process), 3)

        camera.restartModel()
        self.assertEqual(len(camera.to_process), 0)
        self.assertEqual(len(camera.to_output), 0)

    def test_camera_update_model(self):
        # test to see if the model can be updated to using updateModel
        camera = Camera()
        self.assertEqual(camera.modelType, 0)

        camera.updateModel(2349)
        self.assertEqual(camera.modelType, 1)

        camera.updateModel(-203)
        self.assertEqual(camera.modelType, 0)

        camera.updateModel(1)
        self.assertEqual(camera.modelType, 1)

        camera.updateModel(0)
        self.assertEqual(camera.modelType, 0)

    def test_camera_get_frame(self):
        # tests to see if item removed from the to_output list
        camera = Camera()
        camera.to_output.append(100)
        output = camera.get_frame()
        self.assertEqual(output, 100)

    def test_camera_base64_to_openCV(self):
        # tests to see if image opened as base64 string converted to open cv image
        with open('website/static/audibleON_logo.png', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            self.assertIsInstance(encoded_string, bytes)
            output_img = camera.base64ToOpenCV(encoded_string)
            self.assertIsInstance(output_img, numpy.ndarray)

    def test_camera_openCV_to_base64(self):
        # tests to see if an image is converted from opencv file to base64 type
        img = cv2.imread('website/static/audibleON_logo.png', cv2.IMREAD_COLOR)
        self.assertIsInstance(img, numpy.ndarray)
        output_img = camera.openCVTobase64(img)
        self.assertIsInstance(output_img, bytes)

    def test_camera_process_image(self):
        # tests to see if image is create on to_output list
        camera = Camera()
        img = open('website/static/audibleON_logo.png', "rb")
        encoded_string = base64.b64encode(img.read())
        img.close()

        self.assertEqual(len(camera.to_output), 0)
        self.assertEqual(len(camera.to_process), 0)
        camera.enqueue_input(encoded_string)
        self.assertEqual(len(camera.to_process), 1)

        camera.process_one()

        self.assertEqual(len(camera.to_process), 0)
        self.assertEqual(len(camera.to_output), 1)

        frame = camera.get_frame()
        self.assertIsInstance(frame, bytes)
        self.assertEqual(len(camera.to_output), 0)

class TestTextToASL(unittest.TestCase):
    def test_tokens_from_string(self):
        string = "this is my string"
        expOutput = ['this', 'is', 'my', 'string']
        actOutput = text_to_asl.getTokensFromString(string)
        self.assertEqual(actOutput, expOutput)

        string = "THIS IS MY STRING"
        actOutput = text_to_asl.getTokensFromString(string)
        self.assertEqual(actOutput, expOutput)

        string = "123456 this is mystringtesting"
        expOutput = ['123456', 'this', 'is', 'mystringtesting']
        actOutput = text_to_asl.getTokensFromString(string)
        self.assertEqual(actOutput, expOutput)

    def test_videos_from_tokens(self):
        tokens = ["this", "is", "my", "string"]
        videos = text_to_asl.getVideosFromTokens(tokens)
        self.assertNotEqual(len(videos),2)

        tokens = ['alskfjals', 'alkjra;lkaslkj', 'qqwqruiotp']
        videos = text_to_asl.getVideosFromTokens(tokens)
        self.assertEqual(len(videos),2)

    def test_video_path(self):
        string = "this is my string"
        videos = text_to_asl.getVideoPath(string)
        self.assertNotEqual(len(videos), 2)

        string = "asjlaksjflakjs lakjs lkajs flkajs flkaj slfajk"
        videos = text_to_asl.getVideoPath(string)
        self.assertEqual(len(videos), 2)

    def test_audio_to_text(self):
        expOutput = 'four score and seven years ago our fathers brought forth on this continent a new nation conceived in liberty and dedicated to the proposition that all men are created equal'
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile('website/static/gettysburg10.wav')

        with audioFile as source:
            data = recognizer.record(source)
        actOutput = recognizer.recognize_google(data, key=None)
        self.assertEqual(actOutput, expOutput)

    def test_audio_to_asl(self):
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile('website/static/gettysburg10.wav')

        with audioFile as source:
            data = recognizer.record(source)
        string = recognizer.recognize_google(data, key=None)

        videos = text_to_asl.getVideoPath(string)
        self.assertNotEqual(len(videos), 2)

if __name__ == '__main__':
    unittest.main()