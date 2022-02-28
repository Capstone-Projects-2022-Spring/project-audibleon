from flask import Blueprint, Response, render_template, request
import cv2

views = Blueprint('views', __name__)
camera = cv2.VideoCapture(0)
stateON = False

def gen_frames():  # generate frame by frame from camera
    while stateON:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@views.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/translate/fromASL', methods=['POST', 'GET'])
def fromASL():
    global stateON, camera
    if request.method == 'POST':
        if (stateON == False):
            camera = cv2.VideoCapture(0)
            cv2.destroyAllWindows()
            stateON = True
        else:
            camera.release()
            stateON = False
    return render_template("index.html")

@views.route('/translate/toASL', methods=['POST', 'GET'])
def toASL():
    print("reached text to asl page")
    return render_template("index.html")

@views.route('/translate/audio', methods=['POST', 'GET'])
def audioToText():
    print("reached audio to text page")
    return render_template("index.html")

@views.route('/translate/connect', methods=['POST', 'GET'])
def onlineConnect():
    print("reached online connection page")
    return render_template("index.html")

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        data = request.form
        print(data)

    return render_template("profile.html")

@views.route('/phrases')
def phrases():
    return render_template("phrases.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/help')
def help():
    return render_template("help.html")