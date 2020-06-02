if ('speechSynthesis' in window) {
    var txtInput = document.getElementById('text_to_speak').textContent;

    var tts = window.speechSynthesis;
    var toSpeak = new SpeechSynthesisUtterance(txtInput);

    toSpeak.pitch = 1;
    toSpeak.rate = 1.6;

    var play_btn = document.querySelector('#play_btn');

    play_btn.addEventListener('click', () => {
        if (!tts.speaking || tts.paused) {
            // without cancel it doesnt speak anymore, try removing later
            tts.cancel();
            tts.speak(toSpeak);
            console.log("started speaking");
            play_btn.setAttribute("src", "../media/icons/pause.png")
        } else if (tts.speaking) {
            // tts.pause(); //this lags a bit
            tts.cancel();
            console.log("speaking cancelled");
            play_btn.setAttribute("src", "../media/icons/play.png")

        }

    });
    // show play icon when finished speaking 
    toSpeak.onend = function(e) {
        play_btn.setAttribute("src", "../media/icons/play.png");
        console.log("speaking finished");

    }
} else {
    console.log('speechSynthesis not available');
    play_btn.style.display = 'none';
}