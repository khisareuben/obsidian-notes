## My future ultimate gaming setup


- Redragon K631 keyboard - ksh 13,000
- Ultrawide Monitor-Arm Heavy Duty - ksh 30,000
- VIVO Vertebrae Cable Management Kit - ksh 15,000
- Cord Management Organizer Kit - ksh 8,000
- ViprTech Avalanche 2.0 Gaming PC - ksh 120,000
- KOORUI 34E6UC 34 Inch Ultrawide Curved Gaming Monitor 144Hz - ksh 81,000
- Nulaxy Adjustable Laptop Stand - ksh 9,000
- Luxury Smart Toilet with Bidet Built In, Bidet Toilet with Heated Seat, Elongated Japanese Toilet with Automatic Flush, Dryer, Night Light, Digital Display - ksh 225,000
- Gaming chair kilimall - ksh28,000
- Logitech G502 HERO High Performance Wired Gaming Mouse - ksh 11,000
- hp deskjet 2710 printer - ksh 14,000
- Adjustable electric desk - ksh 35,000
- Macbook air - ksh 200,000
- Xiaomi Black Shark 3 12GB – 256GB - ksh 70,000
- Xiaomi G34WQi 34'' - ksh 45,000
- ZTE Nubia Neo 2 - ksh 35,000


```javascript

document.addEventListener('DOMContentLoaded', () => {

const signUpButton = document.getElementById('signUpButton');

const signInButton = document.getElementById('signInButton');

const signUpForm = document.querySelector('.signup');

const signInForm = document.querySelector('.signIn');

const formSummary = document.getElementById('formSummary');

  

// Switch between forms

signUpButton.addEventListener('click', () => {

signUpForm.style.display = 'block';

signInForm.style.display = 'none';

});

  

signInButton.addEventListener('click', () => {

signUpForm.style.display = 'none';

signInForm.style.display = 'block';

});

  

// Form validation and data handling

const registrationForm = document.querySelector('.signup form');

registrationForm.addEventListener('submit', (event) => {

event.preventDefault();

let valid = true;

const formData = {};

  

const name = document.getElementById('name');

const email = document.getElementById('email');

const password = document.getElementById('password');

const confirmPassword = document.getElementById('confirm_password');

const age = document.getElementById('age');

const terms = document.getElementById('conditions');

const contactMethod = document.querySelector('input[name="contact"]:checked');

  

// Clear previous error messages

document.querySelectorAll('.error').forEach(el => el.remove());

  

// Required fields validation

if (!name.value.trim()) {

showError(name, 'Name is required');

valid = false;

} else {

formData.name = name.value.trim();

}

  

if (!email.value.trim()) {

showError(email, 'Email is required');

valid = false;

} else if (!validateEmail(email.value)) {

showError(email, 'Invalid email format');

valid = false;

} else {

formData.email = email.value.trim();

}

  

if (!password.value.trim()) {

showError(password, 'Password is required');

valid = false;

} else if (password.value.length < 8) {

showError(password, 'Password must be at least 8 characters long');

valid = false;

} else {

formData.password = password.value.trim();

}

  

if (!confirmPassword.value.trim()) {

showError(confirmPassword, 'Confirm Password is required');

valid = false;

} else if (password.value !== confirmPassword.value) {

showError(confirmPassword, 'Passwords do not match');

valid = false;

}

  

if (!age.value.trim()) {

showError(age, 'Age is required');

valid = false;

} else if (isNaN(age.value) || age.value < 18 || age.value > 100) {

showError(age, 'Age must be a number between 18 and 100');

valid = false;

} else {

formData.age = age.value.trim();

}

  

if (!contactMethod) {

showError(document.querySelector('input[name="contact"]'), 'Preferred contact method is required');

valid = false;

} else {

formData.contactMethod = contactMethod.value;

}

  

if (!terms.checked) {

showError(terms, 'You must agree to the terms and conditions');

valid = false;

} else {

formData.termsAccepted = true;

}

  

if (valid) {

displayFormData(formData);

alert('Form submitted successfully!');

}

});

  

function showError(element, message) {

clearError(element);

const error = document.createElement('div');

error.className = 'error';

error.style.color = 'red';

error.textContent = message;

element.parentNode.appendChild(error);

}

  

function validateEmail(email) {

const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

return re.test(String(email).toLowerCase());

}

  

function displayFormData(data) {

formSummary.innerHTML = `

<h3>Form Summary</h3>

<p><strong>Name:</strong> ${data.name}</p>

<p><strong>Email:</strong> ${data.email}</p>

<p><strong>Age:</strong> ${data.age}</p>

<p><strong>Contact Method:</strong> ${data.contactMethod}</p>

<p><strong>Terms Accepted:</strong> ${data.termsAccepted ? 'Yes' : 'No'}</p>

`;

}

  

// Real-time feedback

document.getElementById('email').addEventListener('input', (event) => {

const email = event.target;

if (!validateEmail(email.value)) {

showError(email, 'Invalid email format');

} else {

clearError(email);

}

});

  

function clearError(element) {

const error = element.parentNode.querySelector('.error');

if (error) {

error.remove();

}

}

});
```