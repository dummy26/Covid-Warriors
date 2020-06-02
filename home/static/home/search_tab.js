// Speech Recognition API for search tab
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

// search bar
const input = document.querySelector(".finder__input");
const finder = document.querySelector(".finder");
const form = document.querySelector("form");

input.addEventListener("focus", () => {
    finder.classList.add("active");
});

input.addEventListener("blur", () => {
    if (input.value.length === 0) {
        finder.classList.remove("active");
    }
});

// form.addEventListener("submit", (ev) => {
//     ev.preventDefault();
//     finder.classList.add("processing");
//     finder.classList.remove("active");
//     input.disabled = true;
//     setTimeout(() => {
//         finder.classList.remove("processing");
//         input.disabled = false;
//         if (input.value.length > 0) {
//             finder.classList.add("active");
//         }
//     }, 1000);
// });