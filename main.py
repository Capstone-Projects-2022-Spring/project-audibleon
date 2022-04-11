from website import create_app, socketio
from flask_socketio import SocketIO

app = create_app()

app.app_context().push()

if __name__ == '__main__':
    
    # Run the Flask Application using the Flask Dev Web Server
    #app.run(debug=True)
    #app.run(host="0.0.0.0", port=5000)

    # Run the Flask Application using SocketIO
    #socketio.run(app, debug=True)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)