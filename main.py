from website import create_app, socketio
from flask_socketio import SocketIO

app = create_app()

app.app_context().push()

if __name__ == '__main__':
    
    # Run the Flask Application using the Flask Dev Web Server
    #app.run(debug=True)

    # Run the Flask Application using SocketIO
    socketio.run(app, debug=True, port=5000)

