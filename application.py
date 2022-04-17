from website import create_app, socketio
from flask_socketio import SocketIO

application = create_app()

application.app_context().push()

if __name__ == '__main__':
    
    # Run the Flask Application using the Flask Dev Web Server
    #application.run(debug=True)
    #application.run(host="0.0.0.0", port=5000)

    # Run the Flask Application using SocketIO
    #socketio.run(application, debug=True)
    socketio.run(application, host="0.0.0.0", port=5000, debug=False)