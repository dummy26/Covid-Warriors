// Speech Recognition API for NAVBAR search
function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-in";
        recognition.start();

        recognition.onstart = function(e) {
            play_beep();
            toggle_listening_popup();
        }

        recognition.onresult = function(e) {
            // sets what was spoken in search bar 
            document.getElementById('transcript').value = e.results[0][0].transcript;
            recognition.stop();
            document.getElementById('search_form').submit();
        }

        recognition.onerror = function(e) {
            console.log('error in recognize', e, e.error);
            recognition.stop();
        }

        recognition.onend = function(e) {
            toggle_listening_popup();
        }
    } else {
        console.log("webkitSpeechRecognition not available");
    }
}

//Voice search initial sound
function play_beep() {
    var audioElement = new Audio("../media/audios/voice_search.mp3");
    audioElement.play();
}

// Listening popup
function toggle_listening_popup() {
    var popup = document.getElementById("listening_popup");
    popup.classList.toggle("show");
}