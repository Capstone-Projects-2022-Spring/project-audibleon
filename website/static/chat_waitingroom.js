var audioMuted = false;
var videoMuted = false;

document.addEventListener("DOMContentLoaded", (event)=>{

    var muteAudioField = document.getElementById("mute_audio_inp");
    var muteVideoField = document.getElementById("mute_video_inp");
    var muteBttn = document.getElementById("bttn_mute");
    var muteVidBttn = document.getElementById("bttn_vid_mute");
    var myVideo = document.getElementById("local_vid");

    muteBttn.addEventListener("click", (event)=>{
        audioMuted = !audioMuted;
        let local_stream = myVideo.srcObject;
        local_stream.getAudioTracks().forEach((track)=>{track.enabled = !audioMuted;});

        muteAudioField.value = (audioMuted)? "1":"0";

        document.getElementById("mute_icon").innerText = (audioMuted)? "mic_off": "mic";
    });

    muteVidBttn.addEventListener("click", (event)=>{
        videoMuted = !videoMuted;
        let local_stream = myVideo.srcObject;
        local_stream.getVideoTracks().forEach((track)=>{track.enabled = !videoMuted;});

        muteVideoField.value = (videoMuted)? "1":"0";

        document.getElementById("vid_mute_icon").innerText = (videoMuted)? "videocam_off": "videocam";
    });

    startCamera();

});

var camera_allowed = false;
var mediaConstraints = {
    audio: true,
    video: {
        height: 360
    }
};

function validate() {

    if (!camera_allowed) {
        alert("Please Allow Camera and Mic Permissions!");
    }

    return camera_allowed;

}

function startCamera() {

    navigator.mediaDevices.getUserMedia(mediaConstraints).then((stream)=>{
        document.getElementById("local_vid").srcObject = stream;
        camera_allowed = true;
    }).catch((e)=>{
        console.log("Error! Unabled to Start Video! ", e);
        document.getElementById("permission_alert").style.display = "block";
    });

}