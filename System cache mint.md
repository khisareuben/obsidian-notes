
### Clear Memory Cache (RAM)

Open a terminal and run:



```bash
sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

🔍 What this does:

- `sync`: flushes filesystem buffers to disk.
    
- `echo 3`: clears PageCache (1), dentries (2), and inodes (4).
    
- `tee`: ensures the command runs with elevated permissions.
    

You can also target specific caches:

- `echo 1`: clears PageCache only.
    
- `echo 2`: clears dentries and inodes.