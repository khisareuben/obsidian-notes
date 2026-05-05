
# 🔹 ClipGrab Clone with Playlist Support (PySide6 + QML + yt‑dlp)

### **main.py**



```python
# main.py
# PySide6 + QML frontend with yt-dlp backend
# Supports single video and playlist downloads

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
import yt_dlp

class Downloader(QObject):
    # Signals to communicate with QML
    progressChanged = Signal(int)   # For progress bar updates
    statusChanged = Signal(str)     # For status messages

    @Slot(str, str, bool)
    def download_video(self, url, format_choice, is_playlist):
        """
        Download a video or playlist using yt-dlp.
        :param url: Video or playlist URL
        :param format_choice: 'mp4' or 'mp3'
        :param is_playlist: True if downloading playlist, False for single video
        """
        self.statusChanged.emit("Starting download...")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best' if format_choice == "mp3" else 'bestvideo+bestaudio',
            'outtmpl': '%(title)s.%(ext)s',  # Save file with video title
            'progress_hooks': [self.hook],   # Hook for progress updates
            'noplaylist': not is_playlist,   # Allow playlist if requested
        }

        # Add postprocessor for MP3 conversion
        if format_choice == "mp3":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        # Run yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        self.statusChanged.emit("Download complete!")

    def hook(self, d):
        """Progress hook called by yt-dlp"""
        if d['status'] == 'downloading':
            # Extract percentage and send to QML
            percent = d.get('_percent_str', '0%').replace('%','')
            self.progressChanged.emit(int(float(percent)))
        elif d['status'] == 'finished':
            self.statusChanged.emit("Processing...")

# Qt application setup
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

backend = Downloader()
engine.rootContext().setContextProperty("backend", backend)

engine.load("ui.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```

### **ui.qml**



```q
// ui.qml
// QML frontend for ClipGrab clone
// Allows single video or playlist download

import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 500
    height: 350
    title: "ClipGrab Clone"

    Column {
        anchors.centerIn: parent
        spacing: 10

        // Input field for video/playlist URL
        TextField {
            id: urlInput
            placeholderText: "Enter video or playlist URL"
            width: parent.width * 0.8
        }

        // Format selection (mp4 or mp3)
        ComboBox {
            id: formatChoice
            model: ["mp4", "mp3"]
            width: parent.width * 0.5
        }

        // Checkbox for playlist option
        CheckBox {
            id: playlistCheck
            text: "Download entire playlist"
        }

        // Download button
        Button {
            text: "Download"
            onClicked: backend.download_video(
                urlInput.text,
                formatChoice.currentText,
                playlistCheck.checked
            )
        }

        // Progress bar
        ProgressBar {
            id: progressBar
            width: parent.width * 0.8
            value: 0
        }

        // Status label
        Label {
            id: statusLabel
            text: "Idle"
        }
    }

    // Connect backend signals to QML UI
    Connections {
        target: backend
        onProgressChanged: progressBar.value = progress
        onStatusChanged: statusLabel.text = status
    }
}
```

## 🔹 How It Works

1. **Enter URL** → Paste either a single video or a playlist link.
    
2. **Choose format** → MP4 (video) or MP3 (audio only).
    
3. **Check playlist option** → If checked, yt‑dlp downloads the entire playlist.
    
4. **Download button** → Starts backend process.
    
5. **Progress bar & status label** → Show live updates from yt‑dlp.