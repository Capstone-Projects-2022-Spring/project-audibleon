var namespace = "/chat";
$(document).ready(function(){

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    var textArea = document.getElementById('audio_words')
    var chatLog = document.getElementById('scrollable');

    socket.on('connect', function() {
        socket.emit('join-room', {});
        console.log('Client connected!');
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
    });

    $('#audio_send').click(function (){
        message = textArea.value;
        console.log(message);
        textArea.value = '';
        socket.emit('input-message', {'msg': message});
    });

    $('#leave').click(function (){
        socket.emit('leave-room', {});
        setTimeout(() => { location.href = '/'; }, 1);

    });

});


