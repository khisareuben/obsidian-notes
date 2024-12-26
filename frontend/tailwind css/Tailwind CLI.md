
```
my-project/
├── node_modules/
├── src/
│   ├── input.css
│   ├── components/
│   
│   
├── build/
│   ├── index.html
│   └── img/
	└── css/
		└── main.css
	└── favicon.ico
	
├── package.json
├── postcss.config.js
├── tailwind.config
├── .gitignore
└── README.md

```


## 1. initialize the package.json

```bash
npm init -y
```

## 2. install tailwindcss

```bash
npm i -D tailwindcss
or
npm i -D prettier-plugin-tailwindcss
```


**Note!**  the node modules will be in the `.gitignore` file so don't push it to github

## 3. create a config file

```bash
npx tailwindcss init
```


create a folder to hold all your html and js files e.g. `build` 
## 4. update your config file
In the content section put the file path of your html

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./build/**/*.{html,js}"],
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

	"tailwind": "npx tailwindcss -i ./src/input.css -o ./build/css/main.css --watch",

    "prettier": "npx prettier --write '**/*.html'"
  },

    "tailwindcss": "^3.4.15

  }

}
```


## lastly

```bash
npm run prettier
npm run tailwind
```