window.onload = function() {
  const rangeInput = document.getElementById('range-input');
  const rangeValue = document.getElementById('range-value');
  const form = document.getElementById('my-form');
  const defaultRangeValue = rangeInput.value;
  const input = document.querySelector('input[type="file"]');


  rangeInput.addEventListener('input', () => {
    rangeValue.textContent = rangeInput.value;
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', input.files[0]);
   fetch('http://localhost:8000/image', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => console.error(error));


    const textInput = document.getElementById('text-input').value;
    const rangeInput = document.getElementById('range-input').value;
    console.log(`Texte : ${textInput}, Valeur : ${rangeInput}`);
    rangeValue.textContent = defaultRangeValue
    form.reset();
  });
};
