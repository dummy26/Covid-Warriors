const states = [
    'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadar Nagar Haveli', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal'
]

const searchInput = document.getElementById("search_tab_transcript");

const suggestionPanel = document.querySelector('.suggestions');

searchInput.addEventListener('keyup', () => {
    const input = searchInput.value.toLowerCase();
    suggestionPanel.innerHTML = '';
    const suggestions = states.filter((state) => {
        return state.toLowerCase().startsWith(input);
    });
    suggestions.forEach((suggested) => {
        const div = document.createElement('div');
        div.innerHTML = suggested;
        suggestionPanel.appendChild(div);
        div.addEventListener('click', () => {
            searchInput.value = div.innerHTML;
            searchInput.focus();
        });
    });

    if (input === '') {
        suggestionPanel.innerHTML = '';
    }
})



// Speech Recognition API for search tab
function search_tab_startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        let recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-in";
        recognition.start();

        recognition.onstart = (e) => {
            play_beep();
            toggle_listening_popup();
        }

        recognition.onresult = (e) => {
            document.getElementById('search_tab_transcript').value = e.results[0][0].transcript;
            recognition.stop();
            document.getElementById('search_tab_form').submit();
        }

        recognition.onerror = (e) => {
            console.log('error in recognize', e, e.error);
            recognition.stop();
        }

        recognition.onend = (e) => {
            toggle_listening_popup();
        }
    } else {
        console.log("webkitSpeechRecognition not available");
    }
}

//Voice search initial sound
function play_beep() {
    let audioElement = new Audio("../media/audios/voice_search.mp3");
    audioElement.play();
}

// Listening popup
function toggle_listening_popup() {
    let popup = document.getElementById("listening_popup");
    popup.classList.toggle("show");
}

// search bar
const input = document.querySelector(".finder__input");
const finder = document.querySelector(".finder");

input.addEventListener("focus", () => {
    finder.classList.add("active");
});

input.addEventListener("blur", () => {
    if (input.value.length === 0) {
        finder.classList.remove("active");
    }
});