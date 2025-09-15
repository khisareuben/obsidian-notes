

### Basic Video Download

To download a video in the best available quality:



```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

Replace `VIDEO_ID` with the actual YouTube link.

### 🎧 Download Audio Only (e.g. MP3)

To extract just the audio from a video:



```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will download and convert the audio to MP3 format.

### 📺 Choose Specific Quality or Format

To list all available formats:



```bash
yt-dlp -F "https://www.youtube.com/watch?v=VIDEO_ID"
```

Then download a specific format using its code:



```bash
yt-dlp -f FORMAT_CODE "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 📁 Download Playlist

To download all videos in a playlist:

```shell
yt-dlp --yes-playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID"

//with best quality
yt-dlp --yes-playlist -f "bv*+ba/best" https://www.youtube.com/watch?v=eq-yfNZ8pXw&list=PL_2gaMQW5HNZgfxtp2p-tlUp3zfqx19kk


```


```bash
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

You can also organize them into folders:



```bash
yt-dlp -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" "URL"
```

### 🧠 Pro Tips

- ✅ To update yt-dlp: `yt-dlp -U`
    
- ✅ To resume a failed download: `yt-dlp -c "URL"`
    
- ✅ To embed subtitles: `yt-dlp --write-auto-sub --embed-subs "URL"`





### Command-Line Alternatives

| Tool                | Description                                                               | Notes                                |
| ------------------- | ------------------------------------------------------------------------- | ------------------------------------ |
| **youtube-dl**      | The original CLI tool yt-dlp was forked from. Still works for many sites. | Less actively maintained than yt-dlp |
| **ytdl-sub**        | Automates yt-dlp with YAML configs for Plex/Kodi setups.                  | Great for batch downloads & metadata |
| **SCrawler**        | Downloads from YouTube, Reddit, Twitter, TikTok, etc.                     | Supports images and videos           |
| **youtube-dl-exec** | A lightweight wrapper around youtube-dl or yt-dlp.                        | Simplifies scripting and automation  |
|                     |                                                                           |                                      |

You can explore more on AlternativeTo’s yt-dlp page — it lists over 100 tools across platforms.

### 🖥️ GUI Wrappers (if CLI is too buggy)

| Tool                      | Description                                              | Platform       |
| ------------------------- | -------------------------------------------------------- | -------------- |
| **Youtube-DLG**           | GUI for youtube-dl and yt-dlp using wxPython.            | Windows, Linux |
| **Open Video Downloader** | Electron-based GUI for yt-dlp. Supports batch downloads. | Windows, macOS |
| **MacYTDL**               | AppleScript-based GUI for macOS users.                   | macOS          |
| **yt-dlp Web UI**         | Lightweight web interface for yt-dlp.                    | Docker-based   |


### Step 1: List Available Formats

Run this to see all video/audio options:



```bash
yt-dlp -F "https://www.youtube.com/watch?v=VIDEO_ID"
```

This shows format codes like `137`, `22`, `140`, etc., along with resolution, codec, and whether it's video-only or audio-only.

### 🎯 Step 2: Choose a Specific Format

Use the format code from the list:



```bash
yt-dlp -f 22 "https://www.youtube.com/watch?v=VIDEO_ID"
```

This downloads format `22`, which might be 720p MP4 with audio.

### 🧠 Advanced Selection (Best Video + Best Audio)

If you want to **combine best video and audio**, use:



```bash
yt-dlp -f "bv+ba" "https://www.youtube.com/watch?v=VIDEO_ID"
```

- `bv` = best video-only stream
    
- `ba` = best audio-only stream
    
- yt-dlp will **merge** them into one file
    

### 📏 Filter by Resolution or Codec

Want to cap resolution at 720p and use MP4?



```bash
yt-dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]" "https://www.youtube.com/watch?v=VIDEO_ID"
```

This grabs the best MP4 video ≤720p and M4A audio.

### 🧰 Bonus Flags

- `--merge-output-format mp4` → force final file to be MP4
    
- `-S "res:720"` → sort formats by resolution
    
- `--format-sort "res,ext"` → prioritize resolution and file type