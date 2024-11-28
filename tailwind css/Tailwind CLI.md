
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
```


## 6. write a script on the package.json

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