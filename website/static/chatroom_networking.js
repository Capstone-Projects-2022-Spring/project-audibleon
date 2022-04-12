var myID;
var _peer_list = {};

// SocketIO
var protocol = window.location.protocol;
var socket = io(protocol + '//' + document.domain + ':' + location.port, {autoConnect: false});

document.addEventListener("DOMContentLoaded", (event)=>{
    startCamera();
});

var camera_allowed = false;
var mediaConstraints = {
    audio: true,
    video: {
        height: 360
    }
};

function startCamera() {

    navigator.mediaDevices.getUserMedia(mediaConstraints).then((stream)=>{
        myVideo.srcObject = stream;
        camera_allowed = true;
        setAudioMuteState(audioMuted);
        setVideoMuteState(videoMuted);
        // Start the SocketIO Connection
        socket.connect();
    }).catch((e)=>{
        console.log("getUserMedia Error! ", e);
        alert("Error! Unable to Access Camera or Mic! ");
    });

}

socket.on("connect", ()=>{
    console.log("Socket Connected...");
    socket.emit("join-room", {"room_id": myRoomID});
});

socket.on("user-connect", (data)=>{
    console.log("User Connected", data);
    let peer_id = data['sid'];
    let display_name = data['name'];
    _peer_list[peer_id] = undefined;
    addVideoElement(peer_id, display_name);
});

socket.on("user-disconnect", (data)=>{
    console.log("User Disconnected", data);
    let peer_id = data['sid'];
    closeConnection(peer_id);
    removeVideoElement(peer_id);
});

socket.on("user-list", (data)=>{
    console.log("User List Received", data);
    myID = data['my_id'];
    
    // If Not the First to Connect to the Room, Existing User List Received
    if ("list" in data) {
        let recvd_list = data['list'];
        // Add Existing Users to User List
        for (peer_id in recvd_list) {
            display_name = recvd_list[peer_id];
            _peer_list[peer_id] = undefined;
            addVideoElement(peer_id, display_name);
        }
        start_webrtc;
    }

});

function closeConnection(peer_id) {

    if (peer_id in _peer_list) {
        _peer_list[peer_id].onicecandidate = null;
        _peer_list[peer_id].ontrack = null;
        _peer_list[peer_id].onnegotiationneeded = null;

        // Remove User from User List
        delete _peer_list[peer_id];
    }

}

function log_user_list() {

    for (let key in _peer_list) {
        console.log(`${key}: ${_peer_list[key]}`);
    }

}

// -------------------------------------------------------- WebRTC -------------------------------------------------------------

var PC_CONFIG = {
    iceServers: [
        {
            urls: ['stun:stun.1.google.com:19302',
                    'stun.stun1.1.google.com:19302',
                    'stun.stun2.1.google.com:19302',
                    'stun.stun3.1.google.com:19302',
                    'stun.stun4.1.google.com:19302'
                ]
        },
    ]
};

function log_error(e) {
    console.log("[ERROR] ", e);
}

function sendViaServer(data) {
    socket.emit("data", data);
}

socket.on("data", (msg)=>{
    switch(msg["type"]) {
        case "offer":
            handleOfferMsg(msg);
            break;
        case "answer":
            handleAnswerMsg(msg);
            break;
        case "new-ice-candidate":
            handleNewICECandidateMsg(msg);
            break;
    }
});

function start_webrtc() {

    for (let peer_id in _peer_list) {
        invite(peer_id);
    }

}

function invite(peer_id) {

    if (_peer_list[peer_id]) {
        console.log("[Not Supposed to Happen!] Attempting to Start a Connection that Already Exists!");
    }
    else if (peer_id === myID) {
        console.log("[Not Supposed to Happen!] Attempting to Connect to Self!");
    }
    else {
        console.log(`Creating Peer Connection for <${peer_id}> ...`);
        createPeerConnection(peer_id);

        let local_stream = myVideo.srcObject;
        local_stream.getTracks().forEach((track)=>{_peer_list[peer_id].addTrack(track, local_stream);});
    }

}

function createPeerConnection(peer_id) {

    _peer_list[peer_id] = new RTCPeerConnection(PC_CONFIG);

    _peer_list[peer_id].onicecandidate = (event) => {handleICECandidateEvent(event, peer_id)};
    _peer_list[peer_id].ontrack = (event) => {handleTrackEvent(event, peer_id)};
    _peer_list[peer_id].onnegotiationneeded = () => {handleNegotiationNeededEvent(peer_id)};

}

function handleNegotiationNeededEvent(peer_id) {

    _peer_list[peer_id].createOffer().then((offer)=>{
        return _peer_list[peer_id].setLocalDescription(offer);
    }).then(()=>{
        console.log(`Sending Offer to <${peer_id}> ...`);
        sendViaServer({
            "sender_id": myID,
            "target_id": peer_id,
            "type": "offer",
            "sdp": _peer_list[peer_id].localDescription
        });
    }).catch(log_error);

}

function handleOfferMsg(msg) {

    peer_id = msg['sender_id'];

    console.log(`Offer Received from <${peer_id}>`);

    createPeerConnection(peer_id);
    let desc = new RTCSessionDescription(msg['sdp']);
    _peer_list[peer_id].setRemoteDescription(desc).then(()=>{
        let local_stream = myVideo.srcObject;
        local_stream.getTracks().forEach((track)=>{_peer_list[peer_id].addTrack(track, local_stream);});
    }).then(()=>{
        return _peer_list[peer_id].createAnswer();
    }).then((answer)=>{
        return _peer_list[peer_id].setLocalDescription(answer);
    }).then(()=>{
        console.log(`Sending Answer to <${peer_id}>`);
        sendViaServer({
            "sender_id": myID,
            "target_id": peer_id,
            "type": "answer",
            "sdp": _peer_list[peer_id].localDescription
        });
    }).catch(log_error);

}

function handleAnswerMsg(msg) {

    peer_id = msg['sender_id'];
    console.log(`Answer Received from <${peer_id}>`);
    let desc = new RTCSessionDescription(msg['sdp']);
    _peer_list[peer_id].setRemoteDescription(desc);

}

function handleICECandidateEvent(event, peer_id) {

    if (event.candidate) {
        sendViaServer({
            "sender_id": myID,
            "target_id": peer_id,
            "type": "new-ice_candidate",
            "candidate": event.candidate
        });
    }

}

function handleNewICECandidateMsg(msg) {

    console.log(`ICE Candidate Received from <${peer_id}>`);
    var candidate = new RTCIceCandidate(msg.candidate);
    _peer_list[msg["sender_id"]].addIceCandidate(candidate).catch(log_error);

}

function handleTrackEvent(event, peer_id) {

    console.log(`Track Event Received from <${peer_id}>`);

    if (event.streams) {
        getVideoObj(peer_id).srcObject = event.streams[0];
    }

}