const fs = require('fs')

window.onload = function() {

  const rangeInput = document.getElementById('range-input');
  const rangeValue = document.getElementById('range-value');
  const form = document.getElementById('my-form');
  const defaultRangeValue = rangeInput.value;
  const input = document.querySelector('input[type="file"]');
  const formConfig = document.getElementById('config-form')


  rangeInput.addEventListener('input', () => {
    rangeValue.textContent = rangeInput.value;
  });
  formConfig.addEventListener('submit', (event) =>{
    event.preventDefault();
    const textInput = document.getElementById('text-input').value;
    const rangeInput = document.getElementById('range-input').value;
    console.log(`Texte : ${textInput}, Valeur : ${rangeInput}`);
    rangeValue.textContent = defaultRangeValue;
    fetch('http://localhost:8000/config',{
      method:'POST',
      body: JSON.stringify({textToSpeech:textInput, NumberOfPerson:rangeInput}),
      headers: {'Content-Type': 'application/json'}
    }).then(response => response.json()).catch(error => console.error(error));
    formConfig.reset();
  })
  

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData();
    const personNumber = document.getElementById('PersonNumber');

    formData.append('image', input.files[0]);
    fetch('http://localhost:8000/image', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      personNumber.textContent = "Nombre de personnes dans la salle : " + data.personCount + " Nombre de personnes autorisées : " + data.personAllowed;
      if (data.personCount > data.personAllowed) {
        const context = new AudioContext();
        // On fetch d'abord avec l'image, S'il ya plus de plus personnes que de perosnnes autorisées,
        // On fetch une deuxieme fois pour l'audio en FR, et une troisieme fois pour l'audio Anglais
        fetch('http://localhost:8000/fr.wav')
          .then(response => response.arrayBuffer())
          .then(arrayBuffer => context.decodeAudioData(arrayBuffer))
          .then(audioBuffer => {
            const source = context.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(context.destination);
            source.start();
            source.onended = function () {
              fetch('http://localhost:8000/En.wav')
                .then(response => response.arrayBuffer())
                .then(arrayBuffer => context.decodeAudioData(arrayBuffer))
                .then(audioBuffer => {
                  const source = context.createBufferSource();
                  source.buffer = audioBuffer;
                  source.connect(context.destination);
                  source.start();
                })
                .catch(error => console.log(error));
            }
          })
          .catch(error => console.log(error));
      }
    })
    .catch(error => console.error(error));
    
    
    form.reset();
    
  });
};
