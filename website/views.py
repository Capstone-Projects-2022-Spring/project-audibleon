from flask import Blueprint, Response, render_template, request, make_response, url_for
import cv2
from werkzeug.utils import redirect
from .models import User
from text_to_asl import getVideoPath
from detection import activateModel, getCamera

views = Blueprint('views', __name__)


global camera
camera = getCamera()
global switch
switch=1

@views.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(activateModel(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

        json = getVideoPath(data)

        print("json ", json)
        return render_template("to_asl.html", videos=json)
    else:
        return render_template("to_asl.html")

@views.route('/display/<filename>')
def display_video(filename):
    print('display_video filename:'+filename)
    return redirect(url_for('static', filename='videos/'+filename), code=301)

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

