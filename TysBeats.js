Here is the complete code/content for `D:\AIArm\TysBeats.js`:

```javascript
// Tys Beats Generator - A simple JavaScript drum machine

// Initialize the drum sounds as an object
const drumSounds = {
  kick: new Audio('https://s3.amazonaws.com/tyson-beckett/beats/kick.wav'),
  snare: new Audio('https://s3.amazonaws.com/tyson-beckett/beats/snare.wav'),
  hiHat: new Audio('https://s3.amazonaws.com/tyson-beckett/beats/hi-hat.wav')
};

// Create the drum machine interface
const drumMachine = document.createElement('div');
drumMachine.innerHTML = `
  <button id="kick-btn">Kick</button>
  <button id="snare-btn">Snare</button>
  <button id="hi-hat-btn">Hi-Hat</button>
  <button id="stop-btn">Stop</button>
`;

// Add the drum machine interface to the page
document.body.appendChild(drumMachine);

// Initialize the drum sounds and start playback
drumSounds.kick.play();
drumSounds.snare.play();
drumSounds.hiHat.play();

// Set up event listeners for the buttons
const kickBtn = document.getElementById('kick-btn');
const snareBtn = document.getElementById('snare-btn');
const hiHatBtn = document.getElementById('hi-hat-btn');
const stopBtn = document.getElementById('stop-btn');

kickBtn.addEventListener('click', () => {
  drumSounds.kick.play();
});

snareBtn.addEventListener('click', () => {
  drumSounds.snare.play();
});

hiHatBtn.addEventListener('click', () => {
  drumSounds.hiHat.play();
});

stopBtn.addEventListener('click', () => {
  drumSounds.kick.pause();
  drumSounds.snare.pause();
  drumSounds.hiHat.pause();
});