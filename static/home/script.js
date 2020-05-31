// HTML5 Speech Recognition API
function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-in";
        recognition.start();

        recognition.onresult = function(e) {
            document.getElementById('transcript').value = e.results[0][0].transcript;
            recognition.stop();
            document.getElementById('search_form').submit();
        };

        recognition.onerror = function(e) {
            console.log('error in recognize');
            recognition.stop();
        }
        recognition.onend = function(e) {
            var popup = document.getElementById("myPopup");
            popup.classList.toggle("show");
        }
    }
}

//Voice search initial sound
function play_beep() {
    var audioElement = new Audio("../media/audios/voice_search.mp3");
    audioElement.play();
}

// When the user clicks on div, open the popup
function listening_popup() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}