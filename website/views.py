from flask import Blueprint, Response, render_template, request, url_for, jsonify
from werkzeug.utils import redirect
from .models import User
from text_to_asl import getVideoPath
from camera import Camera

views = Blueprint('views', __name__)

global camera
camera = Camera()

@views.route('/clear_list', methods=['POST'])
def clear_list():
    print(camera.wordList)
    camera.wordList.clear()
    print(camera.wordList)
    return ("nothing")

@views.route ('/update_model', methods=['POST'])
def update_model():
    model = request.form["value"]
    if model == "words":
        camera.updateModel(0)
    else:
        camera.updateModel(1)
    return ("nothing")

@views.route('/get_words', methods=['POST', 'GET'])
def get_words():
    wordList = camera.wordList
    # this should return a jsonified format of the words in the class myWords.words list
    return jsonify({'results':wordList})

@views.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(camera.baseRoutine(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/translate/fromASL', methods=['POST', 'GET'])
def fromASL():
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