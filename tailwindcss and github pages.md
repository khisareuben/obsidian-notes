

Got it! Let's go step-by-step through the entire process of setting up your TailwindCSS website to deploy on GitHub Pages. I'll cover everything from installing dependencies to configuring GitHub Pages.

### Step 1: Install Dependencies

First, ensure you have Node.js installed on your machine. Then, create a new project directory and navigate into it:



```bash
mkdir my-tailwind-project
cd my-tailwind-project
```

Initialize a new Node.js project:



```bash
npm init -y
```

Install TailwindCSS, PostCSS, and Autoprefixer:



```bash
npm install -D tailwindcss postcss autoprefixer
```

Create the necessary configuration files for TailwindCSS:



```bash
npx tailwindcss init -p
```

This will create a `tailwind.config.js` file and a `postcss.config.js` file in your project root.

### Step 2: Configure TailwindCSS

Update the `tailwind.config.js` file to include the paths to your content files:



```js
module.exports = {
  content: [
    "./src/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Step 3: Set Up Your Project Structure

Create a basic project structure. For example:

```bash
my-tailwind-project/
├── src/
│   ├── index.html
│   └── styles.css
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── package-lock.json
```

### Step 4: Configure TailwindCSS in Your CSS

In your `styles.css` file, include the following:

css

```bash
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 5: Build Your CSS

Add a build script in your `package.json`:



```json
"scripts": {
  "build": "npx tailwindcss -i ./src/styles.css -o ./dist/styles.css --minify"
}
```

Now, run the build script to generate the compiled CSS:



```bash
npm run build
```

### Step 6: Create a GitHub Repository

Create a new repository on GitHub and push your project files to it. In your project directory, run:



```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

### Step 7: Set Up GitHub Actions Workflow

Create a `.github/workflows` directory in your project and add a `github-pages.yml` file:



```yaml
name: Build and Deploy
on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
          publish_branch: gh-pages  # Ensure this line specifies the gh-pages branch

```

### Step 8: Configure GitHub Pages

Go to the repository settings on GitHub and under "Pages" (found in the left sidebar), set the source to the `gh-pages` branch if it isn't set automatically.



if there's an error pushing

It looks like the error you're encountering is due to the Personal Access Token (PAT) not having the `workflow` scope enabled. To fix this, you'll need to update your PAT to include the `workflow` scope. Here's how you can do that:

1. **Generate a New Personal Access Token**:
    
    - Go to your GitHub account settings.
        
    - Navigate to **Developer settings**.
        
    - Select **Personal access tokens**.
        
    - Click on **Generate new token**.
        
    - Make sure to check the **workflow** scope.
        
    - Copy the new token and keep it safe.
        
2. **Update Your GitHub Repository**:
    
    - Use the new token to authenticate your Git operations.
        
    - You can update the token in your repository settings or use it when pushing changes.
        

Here's an example of how to update your token in the repository settings:



```bash
git remote set-url origin https://<your_username>:<new_token>@github.com/khisareuben/sirfranco-website.git
```

Replace `<your_username>` with your GitHub username and `<new_token>` with the new token you generated.

After updating the token, try pushing your changes again:



```bash
git push origin main
```

This should resolve the error and allow you to push your workflow changes to GitHub.


1. **rigger the Workflow**: Push a commit to the `main` branch to trigger the workflow. This will build your project and deploy it to the `gh-pages` branch.
    
    
    
    ```bash
    git add .
    git commit -m "Deploy to GitHub Pages"
    git push origin main
    ```
    
2. **Wait for the Workflow to Complete**: Go to the Actions tab in your GitHub repository to ensure the workflow completes successfully.
    
3. **Configure GitHub Pages**:
    
    - Go to your repository settings on GitHub.
        
    - Navigate to **Pages** in the left sidebar.
        
    - Under "Source," select the `gh-pages` branch from the dropdown menu.
        

This will configure GitHub Pages to serve your site from the `gh-pages` branch.

If you don't see the `gh-pages` branch in the dropdown:

- Make sure the workflow has run successfully and the branch has been created.
    
- Refresh the GitHub Pages settings page.


Great to hear you successfully deployed your site to GitHub Pages! When you clone the repository again in the future, you won't have to set up everything from scratch. Here’s what you need to do:

### Step-by-Step Guide

1. **Clone the Repository**: Use the following command to clone your repository:
    
    
    
    ```bash
    git clone https://github.com/khisareuben/sirfranco-website.git
    cd sirfranco-website
    ```
    
2. **Install Dependencies**: Install the necessary npm packages by running:
    
    
    
    ```bash
    npm install
    ```
    
    This will install all the packages listed in your `package.json`, including TailwindCSS and PostCSS.
    
3. **Build Your Project**: Use the build script defined in your `package.json` to compile your CSS:
    
        
    ```bash

    npm run build
    ```
    

### Summary

By following these steps, you can quickly get back to working on your project without having to redo the setup. Your repository already contains all the configuration files and scripts needed to rebuild the project.