from flask import Blueprint, Response, render_template, request, url_for, jsonify
from werkzeug.utils import redirect
from .models import User
from text_to_asl import getVideoPath
from detection import activateModel, myWords

views = Blueprint('views', __name__)

global m
m = myWords()

@views.route('/get_words')
def get_words():
    wordList = m.wordList
    # this should return a jsonified format of the words in the class myWords.words list
    return jsonify({'results':wordList})

@views.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(activateModel(m), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/translate/fromASL', methods=['POST', 'GET'])
def fromASL():
    if request.method == 'POST':
        m.resetList()
        return render_template("from_asl.html", translating=True)
    elif request.method == 'GET':
        return render_template("from_asl.html", translating=False)


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