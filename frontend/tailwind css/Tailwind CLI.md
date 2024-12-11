
## 1. initialize the package.json

```bash
npm init -y
```

## 2. install tailwindcss

```bash
npm i -D tailwindcss
```

## 3. create a config file

```bash
npx tailwindcss init
```


create a folder to hold all your html and js files e.g. `public` 
## 4. update your config file
In the content section put the file path of your html

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```


## 5. create a src file and in it an input.css

Add the code below in the `input.css` 

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

# writin your own classes
@layer components {
.menu-components {
	@apply text-white bg-indigo-500 p-2;
 }
}
# whenever you write menu-components it will app the classes defined inside

# changing classes properties
@layer utilities{
.text-green-500{
	color: white;
	background: teal;
 }
}
# whenever you write text-green-500 it will apply the white color and teal bg
```


## 6. write a script on the package.json

in django the output will be inside the static files e.g.                   `./static/css/main.css`

```json
{

  "scripts": {

    "build": "tailwindcss -i ./src/input.css -o ./css/main.css",

    "watch": "tailwindcss -i ./src/input.css -o ./css/main.css --watch"

  },

    "tailwindcss": "^3.4.15

  }

}
```


## lastly

```bash
npm run build
npm run watch
```