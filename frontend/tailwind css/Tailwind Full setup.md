# This is full setup
- you first need to have nodejs installed

### configure tailwind
inside a folder of your project

```bash
npx tailwindcss init
```

add two folder: `build` and `src` 
in the build folder add `index.html` 

### we need to update the tailwind config file
```js
/** @type {import('tailwindcss').Config} */

module.exports = {

  content: ['./build/*.html'],

  theme: {

    extend: {},

  },

  plugins: [],

}
```


#### then create an input.css file in the src folder and add
```css
@tailwind base;

@tailwind components;

@tailwind utilities;
```

#### then go to the terminal and run

```bash
npx tailwindcss -i ./src/input.css -o ./build/css/style.css
```

a css folder will be created inside the folder with a `style.css` file which contains all of the tailwind styles