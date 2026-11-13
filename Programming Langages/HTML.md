### paragraph, heading, break, horizontal line 

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <h1>This is a h1 heading</h1>
    <p>This is a pragraph</p>
    <hr>
    <br>
    <!--pre - (preformatted) tags outs the pragragphs as is or as formated-->
    <pre>This is a paragraph that is pre formatted</pre>
</body>
</html>
```

### hyperlinks

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <a href="https://www.google.com/" target="_blank">Click me</a>
</body>
</html>
```

# Images

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <img src="delta3.jpg" alt="image" height="500">
</body>
</html>
```

### Audio

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
	<audio src="DR PAUL ENENCHE - YOU ARE ALWAYS THERE FOR ME (SONG OF SURRENDER).mp3" controls></audio>
    <audio controls>
        <source src="DR PAUL ENENCHE - YOU ARE ALWAYS THERE FOR ME (SONG OF SURRENDER).mp3">
    </audio>
    <br>
    <audio controls autoplay muted loop>
        <source src="DR PAUL ENENCHE - YOU ARE ALWAYS THERE FOR ME (SONG OF SURRENDER).mp3">
    </audio>
</body>
</html>
```

### Video

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <video src="LET ME WANT WHAT YOU WANT - Dr Paul Enenche.webm" width="500" controls>

    </video>
    <video src="LET ME WANT WHAT YOU WANT - Dr Paul Enenche.webm" width="500" controls autoplay muted loop>
        
    </video>
</body>
</html>
```

### Lists

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <!--Unorderd lists-->
    <h4>Groceries</h4>
    <ul>
        <li>Milk</li>
        <li>Eggs</li>
        <li>Coffee</li>
        <ul>
            <li>coffee beans</li>
            <li>creamer</li>
            <li>sugar</li>
        </ul>
    </ul>

    <!--Ordered lists-->
    <h4>To do list</h4>
    <ol>
        <li>Eat Breakfast</li>
        <li>Got to class</li>
        <li>Go to Work</li>
    </ol>

    <!--Description list-->
    <dl>
        <dt>LAN</dt>
        <dd>Connects computers and devices within a limited area such as home, office or building</dd>
        <dt>CAN</dt>
        <dd>Connects multiple LANs over a campus or group of nearby buildings</dd>
        <dt>MAN</dt>
        <dd>Connects multiple networds over a city or metropolitan region</dd>
    </dl>
</body>
</html>
```

### Tables

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <h3>Store Hours</h3>
    <table border="2">
        <tr> <!--table row, <th> table heading-->
            <th width="100">Sunday</th>
            <th>Monday</th>
            <th>Tuesday</th>
            <th>Wednesday</th>
        </tr>
        <tr align="center"> <!--table row, <td> table data-->
            <td>Closed</td>
            <td>9-5</td>
            <td>9-5</td>
            <td>9-5</td>
        </tr>
    </table>
</body>
</html>
```

### buttons

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <button style="font-size: 25px; background-color: aquamarine; border-radius: 10px;">
        Click Me
    </button>
</body>
</html>
```

### form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <form action="index.php" method="post" enctype="multipart/form-data"> 
        <!--action sends the data to the specified location-->
        <!--enctype is for sending a large data in parts-->

        <!--username-->
        <label for="username">username:</label>
        <input type="text" id="username" minlength="6" maxlength="15" required><br>

        <!--password-->
        <label for="password">password</label>
        <input type="password" id="password" required><br>

        <!--email-->
        <label for="email">email</label>
        <input type="email" id="email" placeholder="johnDoe@gmail.com"><br>

        <!--phone-->
        <label for="phone">phone #:</label>
        <input type="tel" id="phone" placeholder="123-456-7890" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"><br>

        <!--date-->
        <label for="bday">brithdate:</label>
        <input type="date" id="bday"><br>

        <!--number-->
        <label for="quantity">quantity</label>
        <input type="number" id="quantity" min="0" max="99" value="1"><br>

        <!--title Mr,Mrs,Ms-->
        <label for="title">Title: </label>
        <label for="Mr.">Mr.</label>
        <input type="radio" id="Mr." value="Mr." name="title">
        <label for="Ms.">Ms.</label>
        <input type="radio" id="Ms." value="Ms." name="title">
        <label for="PhD.">PhD.</label>
        <input type="radio" id="PhD." value="PhD." name="title"><br>

        <!--dropdown-->
        <label for="payment">payment</label>
        <select id="payment">
            <option value="visa">visa</option>
            <option value="mastercard">mastercard</option>
            <option value="giftcard">giftcard</option>
        </select><br>

        <!--checkbox-->
        <label for="subscribe">subscribe</label>
        <input type="checkbox" id="subscribe"><br>

        <!--comment-->
        <label for="comment">comment</label>
        <textarea id="comment" rows="3" cols="25"></textarea><br>

        <!--adding a file-->
        <label for="file">file:</label>
        <input type="file" id="file" accept="image/png, image/jpeg"><br>

        <input type="reset"><br>
        <input type="submit">


    </form>
</body>
</html>
```

### header and footer, main

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
</head>
<body>
    <header>
        <h1>Welcome to Code</h1>
        <a href="">Home</a>
        <a href="">About Us</a>
        <a href="">Products</a>
        <a href="">Contact Us</a>
    </header><hr>
    <main>
        <h4>We are learning html</h4>
        <p>header, main, footer</p>
    </main>

    <footer>
        <hr>
        author: Code <br>
        &copy; copyright reserverd <br>
        <a href="mailto:johnDoe@gmail.com">johnDoe@gmail.com</a>
    </footer>
</body>
</html>
```

### CSS Styling

`inline styling`
```html
<p style="color: goldenrod;">This is testing</p> <!--inline styling-->
```

`internal styling`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
    <!--internal styling-->
    <style>
        h1 {
            color: blue;
        }
    </style>
</head>
<body>
    <h1>This is a header element</h1>
</body>
</html>
```

`external sytling`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <p id="p1">This is testing</p> <!--inline styling-->
    <h1 id="h1">This is a header element</h1>
    <p id="p2">Externl Styling</p>
</body>
</html>
```
`style.css file`
```css
body{
    background-color: black;
}
h1{
    color: white;
}

#p1{ /*for specific styling you used the id name preceded by # */
    color: yellow;
}
#p2{ /*for specific styling you used the id name preceded by (#) */
    color: yellow;
}
#h1{
    color: yellow;
}

```

#Note: You can also use `class=""` , and in CSS you use `.` instead of `#`

