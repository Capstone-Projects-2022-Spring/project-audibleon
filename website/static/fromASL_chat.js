var myVideo, myCanvas;
var namespace = "/chat";
var localMediaStream = null;
var mySID;
$(document).ready(function(){

    var socket = io(location.protocol + '//' + document.domain + ':' + location.port + namespace, {autoConnect: false});

    myVideo = document.getElementById("videoStream");
    myCanvas = document.getElementById("canvasElement");
    var chatLog = document.getElementById('scrollable');

    function sendSnapshot() {
        if (!localMediaStream) {
          return;
        }

        myCanvas.getContext('2d').drawImage(myVideo, 0, 0, myVideo.videoWidth, myVideo.videoHeight, 0, 0, 300, 150);

        let dataURL = myCanvas.toDataURL('image/jpeg');
        socket.emit('input image', dataURL);
    }

    socket.on('connect', function() {
        socket.emit('join-room', {});
        console.log('Client connected!');
    });

    socket.on('get-sid', function(data) {
        mySID = data.sid;
        console.log(mySID);
    });

    socket.on('status', function(data) {
        var newText = document.createTextNode(data.msg);
        chatLog.appendChild(newText);

        $('#scrollable').animate({ scrollTop: 		$('#scrollable').prop('scrollHeight')}, 1000);
    });

    socket.on('output-message', function(data) {
        var newText = document.createTextNode(data.msg);
        chatLog.appendChild(newText);

        $('#scrollable').animate({ scrollTop: 		$('#scrollable').prop('scrollHeight')}, 1000);

        let sid = data.sid;
        if (sid !== mySID){
            getVideoPlaylist(data.msg);
        }
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

    $('#send').click(function (){
        message = document.getElementById("words").innerText;
        clearList();
        socket.emit('input-message', {'msg': message});
    });

    $('#audio').click(function (){
        getAudio();
    });

    $('#clear').click(function (){
        clearList();
    });

    $('#restart').click(function (){
        restart();
    });

    $('#leave').click(function (){
        socket.emit('leave-room', {});
        setTimeout(() => { location.href = '/'; }, 1);

    });

    var myTimer = setInterval(updateText, 2000);



});


