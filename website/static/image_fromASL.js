var myVideo, myCanvas;
var namespace = "/from_asl";
var localMediaStream = null;
$(document).ready(function(){

    var socket = io(location.protocol + '//' + document.domain + ':' + location.port + namespace, {autoConnect: false});

    myVideo = document.getElementById("videoStream");
    myCanvas = document.getElementById("canvasElement");

    function sendSnapshot() {
        if (!localMediaStream) {
          return;
        }

        myCanvas.getContext('2d').drawImage(myVideo, 0, 0, myVideo.videoWidth, myVideo.videoHeight, 0, 0, 300, 150);

        let dataURL = myCanvas.toDataURL('image/jpeg');
        socket.emit('input image', dataURL);
    }

    socket.on('connect', function() {
        console.log('Client video connected!');
    });

    var constraints = {
        video: {
          width: { min: 640 },
          height: { min: 480 }
        }
      };

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        myVideo.srcObject = stream;
        localMediaStream = stream;
        socket.connect()

        setInterval(function () {
          sendSnapshot();
        }, 100);
      }).catch(function(error) {
        console.log(error);
      });
});


