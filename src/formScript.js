window.onload = function() {
  const rangeInput = document.getElementById('range-input');
  const rangeValue = document.getElementById('range-value');
  const form = document.getElementById('my-form');
  const defaultRangeValue = rangeInput.value;


  rangeInput.addEventListener('input', () => {
    rangeValue.textContent = rangeInput.value;
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const textInput = document.getElementById('text-input').value;
    const rangeInput = document.getElementById('range-input').value;
    console.log(`Texte : ${textInput}, Valeur : ${rangeInput}`);
    rangeValue.textContent = defaultRangeValue
    form.reset();
  });
};
