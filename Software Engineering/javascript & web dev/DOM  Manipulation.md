
### Selecting Elements in the DOM

1. **By ID**:
    
    JavaScript
    
    ```javascript
    const element = document.getElementById('myId');
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **By Class Name**:
    
    JavaScript
    
    ```javascript
    const elements = document.getElementsByClassName('myClass');
    ```
    
    AI-generated code. Review and use carefully. .
    
3. **By Tag Name**:
    
    JavaScript
    
    ```javascript
    const elements = document.getElementsByTagName('div');
    ```
    
    AI-generated code. Review and use carefully. .
    
4. **By CSS Selector**:
    
    JavaScript
    
    ```javascript
    const element = document.querySelector('.myClass');
    const elements = document.querySelectorAll('.myClass');
    ```
    
    AI-generated code. Review and use carefully. .
    

### Traversing the DOM

1. **Parent Node**:
    
    JavaScript
    
    ```javascript
    const parent = element.parentNode;
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **Child Nodes**:
    
    JavaScript
    
    ```javascript
    const children = element.childNodes;
    const firstChild = element.firstChild;
    const lastChild = element.lastChild;
    ```
    
    AI-generated code. Review and use carefully. .
    
3. **Sibling Nodes**:
    
    JavaScript
    
    ```javascript
    const nextSibling = element.nextSibling;
    const previousSibling = element.previousSibling;
    ```
    
    AI-generated code. Review and use carefully. .
    
4. **Descendants**:
    
    JavaScript
    
    ```javascript
    const descendants = element.querySelectorAll('.descendantClass');
    ```
    
    AI-generated code. Review and use carefully. .
    

### Manipulating the DOM

1. **Changing Content**:
    
    JavaScript
    
    ```javascript
    element.textContent = 'New content';
    element.innerHTML = '<p>New HTML content</p>';
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **Changing Attributes**:
    
    JavaScript
    
    ```javascript
    element.setAttribute('src', 'newImage.png');
    element.removeAttribute('alt');
    ```
    
    AI-generated code. Review and use carefully. .
    
3. **Changing Styles**:
    
    JavaScript
    
    ```javascript
    element.style.color = 'blue';
    element.style.fontSize = '20px';
    ```
    
    AI-generated code. Review and use carefully. .
    
4. **Creating and Appending Elements**:
    
    JavaScript
    
    ```javascript
    const newElement = document.createElement('div');
    newElement.textContent = 'Hello, World!';
    document.body.appendChild(newElement);
    ```
    
    AI-generated code. Review and use carefully. .
    

### Event Handling

1. **Adding Event Listeners**:
    
    JavaScript
    
    ```javascript
    element.addEventListener('click', function() {
        alert('Element clicked!');
    });
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **Removing Event Listeners**:
    
    JavaScript
    
    ```javascript
    function handleClick() {
        alert('Element clicked!');
    }
    element.removeEventListener('click', handleClick);
    ```
    
    AI-generated code. Review and use carefully. .
    
3. **Event Object**:
    
    JavaScript
    
    ```javascript
    element.addEventListener('click', function(event) {
        console.log(event.target); // The element that was clicked
    });
    ```
    
    AI-generated code. Review and use carefully. .
    
4. **Common Events**:
    
    - `click`
    - `mouseover`
    - `mouseout`
    - `keydown`
    - `keyup`
    - `submit`