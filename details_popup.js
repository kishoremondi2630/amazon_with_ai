// Gender selection functionality (Disable the other button once one is selected)
function selectGender(gender) {
  const maleButton = document.getElementById('male');
  const femaleButton = document.getElementById('female');
  
  if (gender === 'male') {
    maleButton.disabled = true;
    femaleButton.disabled = false;
    maleButton.classList.add('selected'); // Add the selected class to male
    femaleButton.classList.remove('selected'); // Remove the selected class from female
  } else if (gender === 'female') {
    femaleButton.disabled = true;
    maleButton.disabled = false;
    femaleButton.classList.add('selected'); // Add the selected class to female
    maleButton.classList.remove('selected'); // Remove the selected class from male
  }
}

// Submit button functionality
document.getElementById('submitBtn').addEventListener('click', function() {
  const gender = document.querySelector('.gender-option:disabled');
  const height = document.getElementById('height').value;
  const weight = document.getElementById('weight').value;
  const skinTone = document.getElementById('skin-tone').value;

  // Validate if all fields are filled
  if (!gender || !height || !weight || !skinTone) {
    alert('Please fill all the fields for best Results!');
  } else {
    alert('Please wait for sometime while creating your 3D Model!');
  }
});

// Help button functionality for height
document.getElementById('heightHelpBtn').addEventListener('click', function() {
  document.getElementById('helpPopup').style.display = 'flex';
});

// Close the help popup
document.getElementById('closeHelpBtn').addEventListener('click', function() {
  document.getElementById('helpPopup').style.display = 'none';
});
