from app import create_app, socketio

app = create_app(debug=True)

app.app_context().push()

if __name__ == '__main__':
    # app.run(debug=True)

    socketio.run(app)
    #run flask application