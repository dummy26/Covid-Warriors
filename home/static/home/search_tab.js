// Speech Recognition API for NAVBAR search
function search_tab_startDictation() {

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
            document.getElementById('search_tab_transcript').value = e.results[0][0].transcript;
            recognition.stop();
            document.getElementById('search_tab_form').submit();
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