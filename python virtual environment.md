

## 🛠️ Step 1: Make Sure Python and venv Are Installed

Check your Python version:

bash

```
python3 --version
```

Install the `venv` module if it’s missing:

bash

```
sudo apt install python3-venv
```

## 🛠️ Step 2: Create a Project Folder

bash

```
mkdir ~/myproject
cd ~/myproject
```

## 🛠️ Step 3: Create the Virtual Environment

bash

```
python3 -m venv venv
```

This creates a folder called `venv` inside your project, containing an isolated Python environment.

## 🛠️ Step 4: Activate the Virtual Environment

Run:

bash

```
source venv/bin/activate
```

You’ll notice your terminal prompt changes to show `(venv)` — meaning you’re inside the virtual environment.

## 🛠️ Step 5: Install Packages

Now you can install packages without affecting your system Python:

bash

```
pip install requests
```

## 🛠️ Step 6: Deactivate When Done

To exit the virtual environment:

bash

```
deactivate
```