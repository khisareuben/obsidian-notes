
Absolutely! Let’s break down the process of capturing form inputs, storing them in an object, and displaying them on a webpage.

### 1. Capturing Form Inputs

When a user submits a form, you can capture the input values using JavaScript. This is typically done by adding an event listener to the form’s submit event.

### 2. Storing Inputs in an Object

Once you have the input values, you can store them in a JavaScript object. This makes it easy to manage and access the data.

### 3. Displaying the Data

Finally, you can dynamically update the webpage to display the captured data. This involves manipulating the DOM (Document Object Model) to insert the data into the appropriate elements on the page.

### Step-by-Step Example

#### HTML Form

Here’s a simple HTML form:

HTML

```html
<form id="myForm">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required>
  
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required>
  
  <input type="submit" value="Submit">
</form>

<div id="formData"></div>
```

AI-generated code. Review and use carefully. .

#### JavaScript

Here’s the JavaScript to capture the form inputs, store them in an object, and display them:

JavaScript

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('myForm');
  const formDataDiv = document.getElementById('formData');

  form.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Capture form inputs
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    // Store inputs in an object
    const formData = {
      name: name,
      email: email
    };

    // Display the data
    displayFormData(formData);
  });

  function displayFormData(data) {
    formDataDiv.innerHTML = `
      <p>Name: ${data.name}</p>
      <p>Email: ${data.email}</p>
    `;
  }
});
```

AI-generated code. Review and use carefully. .

### Explanation

1. **Event Listener**: The `DOMContentLoaded` event ensures the script runs after the DOM is fully loaded. The `submit` event listener on the form captures the form submission.
2. **Prevent Default**: `event.preventDefault()` prevents the form from submitting in the traditional way, allowing you to handle the data with JavaScript.
3. **Capture Inputs**: The values of the form inputs are captured using `document.getElementById('inputId').value`.
4. **Store in Object**: The captured values are stored in a JavaScript object for easy access and manipulation.
5. **Display Data**: The `displayFormData` function updates the inner HTML of a designated `div` to display the captured data.

### Benefits

- **Real-time Feedback**: You can provide immediate feedback to users as they fill out the form.
- **Dynamic Updates**: The webpage can be updated dynamically without needing to reload.
- **Data Management**: Storing data in an object makes it easy to manage and manipulate.