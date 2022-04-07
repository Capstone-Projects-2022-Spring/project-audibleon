from flask import Response, render_template, request, url_for, jsonify
from werkzeug.utils import redirect
from app.main.models import User
from .text_to_asl import getVideoPath
from .detection import activateModel, myWords
from . import main
from .. camera import Camera, Makeup_artist
from app import socketio
from flask_socketio import emit

# views = Blueprint('views', __name__)

global m
m = myWords()
camera = Camera(Makeup_artist())

@socketio.on('input image', namespace='/video')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)
    # image_data = input  # Do your magical Image processing here!!
    # # image_data = image_data.decode("utf-8")
    # image_data = "data:image/jpeg;base64," + image_data
    # # print("OUTPUT " + image_data)
    # emit('out-image-event', {'image_data': image_data}, namespace='/video')


@socketio.on('connect', namespace='/video')
def test_connect():
    # app.logger.info("client connected")
    print('client connected')

def gen():
    """Video streaming generator function."""

    # app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/get_words')
def get_words():
    wordList = m.wordList
    # this should return a jsonified format of the words in the class myWords.words list
    return jsonify({'results':wordList})

@main.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(activateModel(m), mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/translate/fromASL', methods=['POST', 'GET'])
def fromASL():
    if request.method == 'POST':
        m.resetList()
        if request.form['translateButton'] == 'Words':
            return render_template("from_asl.html", translating=True, wordsModel=True)
        elif request.form['translateButton'] == 'Alphabet':
            return render_template("from_asl.html", translating=True, wordsModel=False)
        else:
            return render_template("from_asl.html", translating=False)
    elif request.method == 'GET':
        return render_template("from_asl.html", translating=False)


@main.route('/translate/toASL', methods=['POST', 'GET'])
def toASL():
    if request.method == 'POST':
        data = request.form.get('text')

        json = getVideoPath(data)

        print("json ", json)
        return render_template("to_asl.html", videos=json)
    else:
        return render_template("to_asl.html")

@main.route('/display/<filename>')
def display_video(filename):
    print('display_video filename:'+filename)
    return redirect(url_for('static', filename='videos/'+filename), code=301)

@main.route('/translate/audio', methods=['POST', 'GET'])
def audioToText():
    print("reached audio to text page")
    return render_template("index.html")

@main.route('/translate/connect', methods=['POST', 'GET'])
def onlineConnect():
    print("reached online connection page")
    return render_template("index.html")

@main.route('/')
def home():
    return render_template("index.html")

@main.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        data = request.form
        print(data)

    return render_template("profile.html")

@main.route('/phrases')
def phrases():
    return render_template("phrases.html")

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/help')
def help():
    return render_template("help.html")

@main.route('/list')
def list():

    return render_template('profile_list.html', users=User.query.all(), title='Profiles List')