try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch(e) {
  console.error(e);
  $('.no-browser-support').show();
  $('.app').hide();
}

var noteTextarea = $('#note-textarea');
var instructions = $('#recording-instructions');
//var notesList = $('ul#notes');

var noteContent = '';




// Get all notes from previous sessions and display them.
//var notes = getAllNotes();
//renderNotes(notes);



/*-----------------------------
      Voice Recognition
------------------------------*/

// If false, the recording will stop after a few seconds of silence.
// When true, the silence period is longer (about 15 seconds),
// allowing us to keep recording even when the user pauses.
recognition.continuous = true;

// This block is called every time the Speech APi captures a line.
recognition.onresult = function(event) {

  // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far.
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  // There is a weird bug on mobile, where everything is repeated twice.
  // There is no official solution so far so we have to handle an edge case.
  var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript);

  if(!mobileRepeatBug) {
    noteContent += transcript;
    noteTextarea.val(noteContent);
  }
};

recognition.onstart = function() {
  instructions.text('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  instructions.text('You were quiet for a while so voice recognition turned itself off.');
  $("#start-record-btn").attr("disabled", false);
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    instructions.text('No speech was detected. Try again.');
  };
}



/*-----------------------------
      App buttons and input
------------------------------*/

$('#start-record-btn').on('click', function(e) {
  if (noteContent.length) {
    noteContent += ' ';
  }
  recognition.start();
  $("#start-record-btn").attr("disabled", true);
});


// Sync the text inside the text area with the noteContent variable.
noteTextarea.on('input', function() {
  noteContent = $(this).val();
})


$('#read-note-btn').on('click', function(e) {
  recognition.stop();
  instructions.text('Reading voice note.');
  readOutLoud(noteContent);
  console.log('Hello');
  $("#start-record-btn").attr("disabled", false);
});


$('#pause-record-btn').on('click', function(e) {
  recognition.stop();
  console.log('pause');
  instructions.text('Voice recognition paused.');
  $("#start-record-btn").attr("disabled", false);
});




/*-----------------------------
      Speech Synthesis
------------------------------*/

function readOutLoud(message) {
  var speech = new SpeechSynthesisUtterance();
  var voices = window.speechSynthesis.getVoices();
  speech.voice = voices[0];
  // Set the text and voice attributes.
  //speech.voice = voices[9]
  console.log(speech.voice);
	speech.text = message;
	speech.volume = 1;
	speech.rate = 0.8;
	speech.pitch = 1;

	window.speechSynthesis.speak(speech);
}
