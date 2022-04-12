import os
from mimetypes import guess_extension
import speech_recognition as sr
from flask_socketio import emit, join_room, leave_room
from flask import Blueprint, Response, render_template, request, url_for, jsonify, session, make_response
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from website import socketio
from .models import User
from text_to_asl import getVideoPath
from camera import Camera
import random, string

views = Blueprint('views', __name__)

# Variables for Chat Rooms
_users_in_room = {}
_room_of_sid = {}
_name_of_sid = {}

# Camera dictionary
global cameras
cameras = {}

# ------ Routes and Sockets for From ASL -------- #
@socketio.on('connect', namespace='/from_asl')
def connect_camera():
    if session['username'] not in cameras:
        cameras[session['username']] = Camera()
        print("camera created")
    print("client connected")

@socketio.on('input image', namespace='/from_asl')
def queue_image(input):
    # split input string
    input = input.split(",")[1]
    # camera.enqueue_input(input)
    global cameras
    cameras[session['username']].enqueue_input(input)

@views.route('/clear_list', methods=['POST'])
@login_required
def clear_list():
    # camera.wordList.clear()
    global cameras
    cameras[session['username']].wordList.clear()
    return ("nothing")

@views.route('/restart', methods=['POST'])
@login_required
def restart():
    # camera.wordList.clear()
    global cameras
    cameras[session['username']].restartModel()

    #camera.wordList.clear()
    return ("nothing")

@views.route ('/update_model', methods=['POST'])
@login_required
def update_model():
    global cameras
    model = request.form["value"]
    if model == "words":
        # camera.updateModel(0)
        cameras[session['username']].updateModel(0)
    else:
        # camera.updateModel(1)
        cameras[session['username']].updateModel(1)
    return("nothing")

@views.route('/get_words', methods=['POST', 'GET'])
def get_words():
    # wordList = camera.wordList

    global cameras
    wordList = cameras[session['username']].wordList
    # this should return a jsonified format of the words in the class myWords.words list
    return jsonify({'results':wordList})

def generateVideo(username):
    # function to generate video stream from queue of output images
    while True:
        # frame = camera.get_frame()
        global cameras
        frame = cameras[username].get_frame()
        # frame = frame.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@views.route('/video_feed')
@login_required
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generateVideo(session['username']), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/translate/fromASL', methods=['POST', 'GET'])
@login_required
def fromASL():
    session['username'] = current_user.username
    if session['username'] not in cameras:
        cameras[session['username']] = Camera()
        print("camera created")
    return render_template("from_asl.html")

@views.route('/translate/toASL', methods=['POST', 'GET'])
@login_required
def toASL():
    if request.method == 'POST':
        data = request.form.get('text')

        json = getVideoPath(data)

        print("json ", json)
        return render_template("to_asl.html", videos=json)
    else:
        return render_template("to_asl.html")

@views.route('/translate/toASL2', methods=['POST', 'GET'])
@login_required
def toASL2():
    if request.method == 'POST':
        data = request.form.get('text')
        json = getVideoPath(data)

        print("json ", json)
        return json
    else:
        return make_response('')

@views.route('/translate/audio', methods=['POST', 'GET'])
@login_required
def audioToText():
    print("reached audio to text page")
    return render_template("audio.html")

@views.route('/audiorecog', methods=['POST', 'GET'])
@login_required
def audiorecog():
    print('reached upload audio')
    if 'audio_file' in request.files:
        file = request.files['audio_file']
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)

            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            return make_response(transcript, 200)

        return make_response('', 200)

@views.route('/')
@login_required
def home():
    return render_template("index.html")

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html")

@views.route('/phrases')
@login_required
def phrases():
    return render_template("phrases.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/help')
def help():
    return render_template("help.html")

@views.route('/list')
@login_required
def list():

    return render_template('profile_list.html', users=User.query.all(), title='Profiles List')

## -------------------------------------------- CONNECT/CHAT FUNCTIONS -------------------------------------------------

@views.route('/connect', methods=['GET', 'POST'])
def chat_connect():

    if request.method == "POST":
        room_id = request.form['room_id']
        return redirect(url_for("views.waiting_room", room_id=room_id))

    return render_template("connect.html")

@views.route('/room/<string:room_id>')
def enter_room(room_id):

    if room_id not in session:
        return redirect(url_for("views.waiting_room", room_id=room_id))
    
    return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"], mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])

@views.route('/room/<string:room_id>/waitingroom', methods=['GET', 'POST'])
def waiting_room(room_id):

    if request.method == 'POST':
        display_name = request.form['display_name']
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": display_name, "mute_audio": mute_audio, "mute_video": mute_video}
        return redirect(url_for("views.enter_room", room_id=room_id))

    return render_template("chat_waitingroom.html", room_id=room_id)

@socketio.on("connect")
def on_connect():

    sid = request.sid
    print("New Socket Connected", sid)

@socketio.on("join-room")
def on_join_room(data):

    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]

    # Register SID to the Room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name

    # Broadcast to Others in the Room
    print("[{}] New Member Joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)

    # Add to User List Maintained on Server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid})
    else:
        usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid})                          # Send List of Existing Users to the New Member
        _users_in_room[room_id].append(sid)                                         # Add New Member to User List Maintained on Server

    print("\nUsers: ", _users_in_room, "\n")

@socketio.on("disconnect")
def on_disconnect():

    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member Left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nUsers: ", _users_in_room, "\n")

@socketio.on("data")
def on_data(data):

    sender_sid = data['sender_sid']
    target_sid = data['target_sid']

    if sender_sid != request.sid:
        print("[Not Supposed to Happen!] request.sid and sender_id don't match!")

    if data["type"] != "new-ice-candidate":
        print('{} Message from {} to {}'.format(data["type"], sender_sid, target_sid))

    socketio.emit('data', data, room=target_sid)

