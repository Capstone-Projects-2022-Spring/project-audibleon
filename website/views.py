from flask import Blueprint, Response, render_template, request, make_response
import cv2
from .models import User
from text_to_asl import getVideoPath

views = Blueprint('views', __name__)
global camera

camera = cv2.VideoCapture(0)
global switch

switch=1

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@views.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/translate/fromASL', methods=['POST', 'GET'])
def fromASL():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('stop') == 'Stop Translation':
            print('pressed!')
            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch=1
    elif request.method=='GET':
        return render_template("from_asl.html")
    return render_template("from_asl.html")

@views.route('/translate/toASL', methods=['POST', 'GET'])
def toASL():
    if request.method == 'POST':
        data = request.form.get('text')

        data = getVideoPath(data)

        print("path: ", data)
        render_template("to_asl.html", path=data)

    return render_template("to_asl.html", path='')

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

@views.route('/list')
def list():

    return render_template('profile_list.html', users=User.query.all(), title='Profiles List')

