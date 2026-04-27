
## Option 1: Override pip restriction directly

Add the `--break-system-packages` flag when installing:


```zsh
pip install PySide6 --break-system-packages
pip install shiboken6 --break-system-packages
```

This tells pip to ignore the “externally managed” warning and force the install into the system Python.