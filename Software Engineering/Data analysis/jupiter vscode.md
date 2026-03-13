
### 🔧 Step 1: Install the Jupyter Extension

- Open VSCodium.
    
- Go to **Extensions** (left sidebar, the square icon).
    
- Search for **Jupyter**.
    
- Install the extension published by Microsoft (it works in VSCodium too). _(If you don’t see it, you may need to enable VSCode marketplace in VSCodium — there’s a setting called_ `extensionsGallery` _in_ `settings.json` _that points to the VSCode marketplace.)_
    

### 🔧 Step 2: Make Sure You Have Python Extension

- Install the **Python extension** as well.
    
- This gives you syntax highlighting, IntelliSense, and integrates with Jupyter.
    

### 🔧 Step 3: Open or Create a Notebook

- Create a new file with the extension `.ipynb`.
    
- Or open an existing notebook.
    
- VSCodium will recognize it and open the Jupyter interface (cells, run buttons, etc.).
    

### 🔧 Step 4: Select Your Kernel

- At the top right of the notebook, you’ll see **“Select Kernel”**.
    
- Choose your Python environment (the one where you installed pandas, numpy, matplotlib, seaborn, jupyterlab).
    
- If it doesn’t show up, you may need to install `ipykernel`:
    
    bash
    
    ```
    pip install ipykernel
    ```
    

### 🔧 Step 5: Run Cells

- Write code in a cell (e.g., `import pandas as pd`).
    
- Press **Shift+Enter** to run the cell.
    
- Output will appear directly below the cell, just like in JupyterLab.
    

### ✅ Practical Tip

Since you already installed `jupyterlab`, you have everything you need. The only extra package you might need is `ipykernel` so VSCodium can connect to your Python environment.