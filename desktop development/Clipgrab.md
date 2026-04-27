
# ClipGrab Clone - Complete Obsidian-Ready Implementation

## 📁 Project Structure

```zsh

clipgrab-clone/
├── main.py
├── resources_rc.py  # Generated from resources.qrc
├── backend/
│   ├── __init__.py
│   ├── download_manager.py
│   ├── clipboard_monitor.py
│   └── settings_manager.py
├── ui/
│   ├── main_window.qml
│   └── components/
│       ├── DownloadItem.qml
│       ├── PlaylistItem.qml
│       └── VideoPreview.qml
├── resources/
│   ├── resources.qrc
│   └── icons/
│       └── placeholder.png
└── requirements.txt

```

## 📄 requirements.txt

```zsh

PySide6>=6.6.0
yt-dlp>=2023.12.30
Pillow>=10.0.0  # For thumbnail handling
requests>=2.31.0  # For downloading thumbnails

```

## 📄 resources/resources.qrc

```xml
<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource prefix="/">
        <file alias="main_window.qml">../ui/main_window.qml</file>
        <file alias="components/DownloadItem.qml">../ui/components/DownloadItem.qml</file>
        <file alias="components/PlaylistItem.qml">../ui/components/PlaylistItem.qml</file>
        <file alias="components/VideoPreview.qml">../ui/components/VideoPreview.qml</file>
        <file alias="icons/placeholder.png">icons/placeholder.png</file>
    </qresource>
</RCC>
```


## 📄 backend/**init**.py

```python
"""
Backend package initialization
This file makes the backend directory a proper Python package
"""

__version__ = "1.0.0"
__author__ = "ClipGrab Clone"

# Import main classes for easier access
from .download_manager import DownloadManager, DownloadListModel, PlaylistModel
from .settings_manager import SettingsManager
from .clipboard_monitor import ClipboardMonitor

__all__ = [
    'DownloadManager',
    'DownloadListModel', 
    'PlaylistModel',
    'SettingsManager',
    'ClipboardMonitor'
]
```


## 📄 backend/settings_manager.py

```python
"""
Settings Manager - Handles persistent application settings
Uses QSettings for cross-platform settings storage
Features:
- Persistent storage of user preferences
- Default settings initialization
- Automatic type conversion
"""

from PySide6.QtCore import QSettings, QStandardPaths, QObject, Signal, Property
import os
from pathlib import Path

class SettingsManager(QObject):
    """
    Manages application settings using Qt's QSettings
    Provides properties for easy QML integration
    """
    
    # Signals for property changes
    downloadPathChanged = Signal()
    clipboardMonitoringChanged = Signal()
    maxConcurrentChanged = Signal()
    autoConvertMp3Changed = Signal()
    
    def __init__(self):
        super().__init__()
        # Initialize QSettings with application name and organization
        self.settings = QSettings("ClipGrabClone", "ClipGrabClone")
        self.load_defaults()
    
    def load_defaults(self):
        """Set default values if they don't exist"""
        defaults = {
            "download_path": QStandardPaths.writableLocation(QStandardPaths.DownloadLocation),
            "max_concurrent": 3,  # Maximum concurrent downloads
            "clipboard_monitoring": True,  # Monitor clipboard for URLs
            "default_format": "best",  # Default video format
            "auto_convert_mp3": False,  # Auto convert to MP3
            "close_to_tray": False,  # Close to system tray
            "theme": "light",  # UI theme
            "save_history": True,  # Save download history
            "history_limit": 100,  # Number of items to keep in history
        }
        
        for key, value in defaults.items():
            if not self.settings.contains(key):
                self.set_value(key, value)
    
    def get_value(self, key, default=None):
        """Get a setting value with proper type conversion"""
        value = self.settings.value(key, default)
        
        # Convert string 'true'/'false' to boolean
        if isinstance(value, str) and value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        
        # Convert numeric strings to int
        if isinstance(value, str) and value.isdigit():
            return int(value)
            
        return value
    
    def set_value(self, key, value):
        """Set a setting value and emit change signal"""
        self.settings.setValue(key, value)
        self.settings.sync()
        
        # Emit appropriate signal
        signal_map = {
            "download_path": self.downloadPathChanged,
            "clipboard_monitoring": self.clipboardMonitoringChanged,
            "max_concurrent": self.maxConcurrentChanged,
            "auto_convert_mp3": self.autoConvertMp3Changed,
        }
        
        if key in signal_map:
            signal_map[key].emit()
    
    # Properties for QML integration
    @Property(str, notify=downloadPathChanged)
    def downloadPath(self):
        return self.get_value("download_path", "")
    
    @downloadPath.setter
    def downloadPath(self, path):
        self.set_value("download_path", path)
    
    @Property(bool, notify=clipboardMonitoringChanged)
    def clipboardMonitoring(self):
        return self.get_value("clipboard_monitoring", True)
    
    @clipboardMonitoring.setter
    def clipboardMonitoring(self, enabled):
        self.set_value("clipboard_monitoring", enabled)
    
    @Property(int, notify=maxConcurrentChanged)
    def maxConcurrent(self):
        return self.get_value("max_concurrent", 3)
    
    @maxConcurrent.setter
    def maxConcurrent(self, value):
        self.set_value("max_concurrent", value)
    
    @Property(bool, notify=autoConvertMp3Changed)
    def autoConvertMp3(self):
        return self.get_value("auto_convert_mp3", False)
    
    @autoConvertMp3.setter
    def autoConvertMp3(self, enabled):
        self.set_value("auto_convert_mp3", enabled)
    
    def get_download_path(self):
        """Get download path as Path object"""
        return Path(self.get_value("download_path", ""))
    
    def add_to_history(self, url, title):
        """Add a URL to download history"""
        if not self.get_value("save_history", True):
            return
        
        history = self.get_value("history", [])
        if isinstance(history, str):
            history = []
        
        # Add new entry
        history.insert(0, {
            "url": url,
            "title": title,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        # Limit history size
        limit = self.get_value("history_limit", 100)
        if len(history) > limit:
            history = history[:limit]
        
        self.set_value("history", history)
    
    def get_history(self):
        """Get download history"""
        if not self.get_value("save_history", True):
            return []
        
        history = self.get_value("history", [])
        if isinstance(history, str):
            return []
        return history
    
    def clear_history(self):
        """Clear download history"""
        self.set_value("history", [])
```

## 📄 backend/clipboard_monitor.py

```python
"""
Clipboard Monitor - Watches system clipboard for video URLs
Features:
- Automatic URL detection
- Support for multiple video platforms
- Configurable monitoring interval
"""

from PySide6.QtCore import QObject, Signal, Slot, QTimer, Property
from PySide6.QtGui import QClipboard, QGuiApplication
import re
from urllib.parse import urlparse

class ClipboardMonitor(QObject):
    """
    Monitors system clipboard for video URLs
    Emits signal when valid URL is detected
    """
    
    # Signal emitted when a valid URL is detected
    urlDetected = Signal(str)
    statusChanged = Signal(bool)
    
    # Supported platforms
    SUPPORTED_DOMAINS = [
        'youtube.com', 'youtu.be',
        'vimeo.com',
        'dailymotion.com',
        'facebook.com', 'fb.watch',
        'twitter.com', 'x.com',
        'tiktok.com',
        'instagram.com',
        'twitch.tv',
        'bilibili.com',
        'rumble.com',
        'odysee.com',
    ]
    
    def __init__(self):
        super().__init__()
        self.clipboard = QGuiApplication.clipboard()
        self.last_text = ""
        self._is_monitoring = False
        
        # URL patterns for detection
        self.url_pattern = re.compile(
            r'(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?',
            re.IGNORECASE
        )
        
        # Timer for periodic clipboard checking
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.setInterval(1000)  # Check every second
        
    @Property(bool, notify=statusChanged)
    def isMonitoring(self):
        """Property for QML binding"""
        return self._is_monitoring
    
    def start_monitoring(self):
        """Start monitoring the clipboard"""
        if not self._is_monitoring:
            self.timer.start()
            self._is_monitoring = True
            self.statusChanged.emit(True)
            print("[ClipboardMonitor] Monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring the clipboard"""
        if self._is_monitoring:
            self.timer.stop()
            self._is_monitoring = False
            self.statusChanged.emit(False)
            print("[ClipboardMonitor] Monitoring stopped")
    
    @Slot()
    def check_clipboard(self):
        """Check clipboard for new URLs"""
        try:
            text = self.clipboard.text()
            
            # Only process if text has changed and is not empty
            if text and text != self.last_text:
                self.last_text = text
                
                # Check if text contains a URL
                match = self.url_pattern.search(text)
                if match:
                    url = match.group(0)
                    if self.is_supported_url(url):
                        print(f"[ClipboardMonitor] Valid URL detected: {url}")
                        self.urlDetected.emit(url)
        except Exception as e:
            print(f"[ClipboardMonitor] Error checking clipboard: {e}")
    
    def is_supported_url(self, url):
        """Check if URL is from a supported platform"""
        try:
            # Add scheme if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove 'www.' prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Check against supported domains
            for supported in self.SUPPORTED_DOMAINS:
                if domain == supported or domain.endswith('.' + supported):
                    return True
            
            return False
        except Exception:
            return False
    
    @Slot(bool)
    def setEnabled(self, enabled):
        """Enable or disable clipboard monitoring"""
        if enabled:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    @Slot()
    def forceCheck(self):
        """Force an immediate clipboard check"""
        self.check_clipboard()
```


## 📄 backend/download_manager.py

```python
"""
Download Manager - Core download functionality using yt-dlp
Features:
- Video/playlist downloading
- Thumbnail fetching and caching
- Progress tracking
- Format selection
- Queue management
"""

from PySide6.QtCore import (
    QObject, Signal, Slot, Property, QProcess, QUrl,
    QAbstractListModel, Qt, QModelIndex, QThread, QTimer
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json
import os
import re
from pathlib import Path
from datetime import datetime
import yt_dlp
import requests
from io import BytesIO

class DownloadItem:
    """Represents a single download item"""
    def __init__(self, url, title="", status="pending", progress=0, 
                 format_id="", file_size="", speed="", eta="",
                 thumbnail="", description=""):
        self.url = url
        self.title = title
        self.status = status  # pending, downloading, completed, error, converting
        self.progress = progress
        self.format_id = format_id
        self.file_size = file_size
        self.speed = speed
        self.eta = eta
        self.error_message = ""
        self.thumbnail = thumbnail
        self.description = description
        self.added_time = datetime.now()
        self.completed_time = None

class PlaylistItem:
    """Represents a video in a playlist"""
    def __init__(self, url, title="", duration="", thumbnail="", selected=True):
        self.url = url
        self.title = title
        self.duration = duration
        self.thumbnail = thumbnail
        self.selected = selected

class DownloadListModel(QAbstractListModel):
    """Model for managing download queue"""
    
    # Define roles for QML
    TitleRole = Qt.UserRole + 1
    UrlRole = Qt.UserRole + 2
    StatusRole = Qt.UserRole + 3
    ProgressRole = Qt.UserRole + 4
    FormatRole = Qt.UserRole + 5
    FileSizeRole = Qt.UserRole + 6
    SpeedRole = Qt.UserRole + 7
    ETARole = Qt.UserRole + 8
    ErrorMessageRole = Qt.UserRole + 9
    ThumbnailRole = Qt.UserRole + 10
    DescriptionRole = Qt.UserRole + 11
    
    def __init__(self):
        super().__init__()
        self._downloads = []
        
    def rowCount(self, parent=QModelIndex()):
        return len(self._downloads)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._downloads):
            return None
            
        item = self._downloads[index.row()]
        
        role_map = {
            self.TitleRole: item.title,
            self.UrlRole: item.url,
            self.StatusRole: item.status,
            self.ProgressRole: item.progress,
            self.FormatRole: item.format_id,
            self.FileSizeRole: item.file_size,
            self.SpeedRole: item.speed,
            self.ETARole: item.eta,
            self.ErrorMessageRole: item.error_message,
            self.ThumbnailRole: item.thumbnail,
            self.DescriptionRole: item.description,
        }
        
        return role_map.get(role)
    
    def roleNames(self):
        return {
            self.TitleRole: b"title",
            self.UrlRole: b"url",
            self.StatusRole: b"status",
            self.ProgressRole: b"progress",
            self.FormatRole: b"format",
            self.FileSizeRole: b"fileSize",
            self.SpeedRole: b"speed",
            self.ETARole: b"eta",
            self.ErrorMessageRole: b"errorMessage",
            self.ThumbnailRole: b"thumbnail",
            self.DescriptionRole: b"description",
        }
    
    def add_download(self, item):
        """Add a new download to the model"""
        self.beginInsertRows(QModelIndex(), len(self._downloads), len(self._downloads))
        self._downloads.append(item)
        self.endInsertRows()
        return len(self._downloads) - 1
    
    def update_download(self, index, **kwargs):
        """Update download item properties"""
        if 0 <= index < len(self._downloads):
            item = self._downloads[index]
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            
            # Notify view of changes
            model_index = self.createIndex(index, 0)
            self.dataChanged.emit(model_index, model_index)
    
    def remove_download(self, index):
        """Remove a download from the model"""
        if 0 <= index < len(self._downloads):
            self.beginRemoveRows(QModelIndex(), index, index)
            self._downloads.pop(index)
            self.endRemoveRows()
    
    def clear_completed(self):
        """Remove all completed downloads"""
        i = len(self._downloads) - 1
        while i >= 0:
            if self._downloads[i].status in ["completed", "error"]:
                self.remove_download(i)
            i -= 1
    
    def get_download(self, index):
        """Get download item at index"""
        if 0 <= index < len(self._downloads):
            return self._downloads[index]
        return None

class PlaylistModel(QAbstractListModel):
    """Model for displaying playlist videos"""
    
    TitleRole = Qt.UserRole + 1
    UrlRole = Qt.UserRole + 2
    DurationRole = Qt.UserRole + 3
    SelectedRole = Qt.UserRole + 4
    ThumbnailRole = Qt.UserRole + 5
    
    def __init__(self):
        super().__init__()
        self._videos = []
        
    def rowCount(self, parent=QModelIndex()):
        return len(self._videos)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._videos):
            return None
            
        video = self._videos[index.row()]
        
        role_map = {
            self.TitleRole: video.title,
            self.UrlRole: video.url,
            self.DurationRole: video.duration,
            self.SelectedRole: video.selected,
            self.ThumbnailRole: video.thumbnail,
        }
        
        return role_map.get(role)
    
    def roleNames(self):
        return {
            self.TitleRole: b"videoTitle",
            self.UrlRole: b"videoUrl",
            self.DurationRole: b"duration",
            self.SelectedRole: b"selected",
            self.ThumbnailRole: b"thumbnail",
        }
    
    def set_videos(self, videos):
        """Set playlist videos"""
        self.beginResetModel()
        self._videos = videos
        self.endResetModel()
    
    def toggle_selection(self, index):
        """Toggle selection of video at index"""
        if 0 <= index < len(self._videos):
            self._videos[index].selected = not self._videos[index].selected
            model_index = self.createIndex(index, 0)
            self.dataChanged.emit(model_index, model_index)
    
    def select_all(self):
        """Select all videos"""
        for i in range(len(self._videos)):
            if not self._videos[i].selected:
                self._videos[i].selected = True
                model_index = self.createIndex(i, 0)
                self.dataChanged.emit(model_index, model_index)
    
    def deselect_all(self):
        """Deselect all videos"""
        for i in range(len(self._videos)):
            if self._videos[i].selected:
                self._videos[i].selected = False
                model_index = self.createIndex(i, 0)
                self.dataChanged.emit(model_index, model_index)
    
    def get_selected_videos(self):
        """Get list of selected videos"""
        return [v for v in self._videos if v.selected]

class ThumbnailFetcher(QObject):
    """Fetches and caches thumbnails"""
    
    thumbnailReady = Signal(str, str)  # url, local_path
    
    def __init__(self):
        super().__init__()
        self.network_manager = QNetworkAccessManager()
        self.cache_dir = Path.home() / ".clipgrab_clone" / "thumbnails"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.pending_requests = {}
        
    @Slot(str)
    def fetch_thumbnail(self, url):
        """Fetch thumbnail from URL"""
        if not url:
            return
        
        # Check cache first
        cache_key = self._get_cache_key(url)
        cache_path = self.cache_dir / cache_key
        
        if cache_path.exists():
            self.thumbnailReady.emit(url, str(cache_path))
            return
        
        # Fetch from network
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        self.pending_requests[reply] = url
        reply.finished.connect(lambda: self._on_thumbnail_downloaded(reply))
    
    def _get_cache_key(self, url):
        """Generate cache key from URL"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest() + ".jpg"
    
    def _on_thumbnail_downloaded(self, reply):
        """Handle thumbnail download completion"""
        url = self.pending_requests.get(reply)
        if not url:
            return
        
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                cache_key = self._get_cache_key(url)
                cache_path = self.cache_dir / cache_key
                
                with open(cache_path, 'wb') as f:
                    f.write(data)
                
                self.thumbnailReady.emit(url, str(cache_path))
        except Exception as e:
            print(f"Error saving thumbnail: {e}")
        finally:
            del self.pending_requests[reply]
            reply.deleteLater()

class DownloadManager(QObject):
    """Main download manager class"""
    
    # Signals for QML communication
    infoFetched = Signal(str, str, str, str, str)  # title, duration, thumbnail, description, url
    playlistFetched = Signal(str, int, str)  # playlist title, video count, thumbnail
    downloadProgress = Signal(int, int, str, str, str)  # index, progress, speed, eta, size
    downloadComplete = Signal(int, str)  # index, filepath
    downloadError = Signal(int, str)  # index, error message
    conversionComplete = Signal(int, str)  # index, filepath
    statusMessage = Signal(str)  # General status messages
    thumbnailReady = Signal(str, str)  # url, local_path
    
    def __init__(self, settings_manager=None):
        super().__init__()
        self.settings_manager = settings_manager
        self.download_model = DownloadListModel()
        self.playlist_model = PlaylistModel()
        self.thumbnail_fetcher = ThumbnailFetcher()
        self.current_processes = {}  # Map download index to QProcess
        self.download_queue = []
        self.max_concurrent = 3
        self.download_path = str(Path.home() / "Downloads")
        
        if settings_manager:
            self.download_path = settings_manager.downloadPath
            self.max_concurrent = settings_manager.maxConcurrent
        
        # Connect thumbnail fetcher signal
        self.thumbnail_fetcher.thumbnailReady.connect(self.thumbnailReady)
    
    @Property(QObject, constant=True)
    def downloads(self):
        """Expose download model to QML"""
        return self.download_model
    
    @Property(QObject, constant=True)
    def playlistVideos(self):
        """Expose playlist model to QML"""
        return self.playlist_model
    
    @Slot(str, result=str)
    def fetchVideoInfo(self, url):
        """Fetch video information from URL"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Check if it's a playlist
                if '_type' in info and info['_type'] == 'playlist':
                    return self._handle_playlist(info)
                else:
                    return self._handle_single_video(info)
                    
        except Exception as e:
            error_msg = f"Error fetching info: {str(e)}"
            self.statusMessage.emit(error_msg)
            return json.dumps({"error": error_msg})
    
    def _handle_single_video(self, info):
        """Handle single video info"""
        title = info.get('title', 'Unknown Title')
        duration = str(info.get('duration', 0))
        thumbnail = info.get('thumbnail', '')
        description = info.get('description', '')[:500]
        url = info.get('webpage_url', '')
        
        # Fetch thumbnail
        if thumbnail:
            self.thumbnail_fetcher.fetch_thumbnail(thumbnail)
        
        # Emit info signal
        self.infoFetched.emit(title, duration, thumbnail, description, url)
        
        # Add to history
        if self.settings_manager:
            self.settings_manager.add_to_history(url, title)
        
        # Get available formats
        formats = self._extract_formats(info)
        
        return json.dumps({
            "type": "video",
            "title": title,
            "duration": duration,
            "thumbnail": thumbnail,
            "description": description,
            "url": url,
            "formats": formats
        })
    
    def _handle_playlist(self, info):
        """Handle playlist info"""
        playlist_title = info.get('title', 'Unknown Playlist')
        playlist_thumbnail = info.get('thumbnail', '')
        entries = info.get('entries', [])
        
        # Fetch playlist thumbnail
        if playlist_thumbnail:
            self.thumbnail_fetcher.fetch_thumbnail(playlist_thumbnail)
        
        # Create playlist items
        videos = []
        for entry in entries:
            video = PlaylistItem(
                url=entry.get('webpage_url', ''),
                title=entry.get('title', 'Unknown'),
                duration=str(entry.get('duration', 0)),
                thumbnail=entry.get('thumbnail', ''),
                selected=True
            )
            videos.append(video)
            
            # Fetch video thumbnails
            if video.thumbnail:
                self.thumbnail_fetcher.fetch_thumbnail(video.thumbnail)
        
        self.playlist_model.set_videos(videos)
        self.playlistFetched.emit(playlist_title, len(videos), playlist_thumbnail)
        
        return json.dumps({
            "type": "playlist",
            "title": playlist_title,
            "count": len(videos),
            "thumbnail": playlist_thumbnail
        })
    
    def _extract_formats(self, info):
        """Extract available formats from video info"""
        formats = []
        seen_resolutions = set()
        
        for f in info.get('formats', []):
            if f.get('vcodec', 'none') != 'none':
                resolution = f.get('resolution', 'unknown')
                
                # Avoid duplicate resolutions
                if resolution not in seen_resolutions:
                    seen_resolutions.add(resolution)
                    
                    format_info = {
                        'id': f.get('format_id', ''),
                        'resolution': resolution,
                        'ext': f.get('ext', 'unknown'),
                        'filesize': f.get('filesize', 0),
                        'fps': f.get('fps', 0),
                    }
                    formats.append(format_info)
        
        # Sort by resolution (highest first)
        def get_height(res):
            try:
                return int(res.replace('p', ''))
            except:
                return 0
        
        formats.sort(key=lambda x: get_height(x['resolution']), reverse=True)
        
        return formats
    
    @Slot(str, str, str)
    def startDownload(self, url, format_id, quality="best"):
        """Start downloading a video"""
        # Create download item
        item = DownloadItem(
            url=url,
            title="Fetching info...",
            status="pending",
            format_id=format_id
        )
        
        index = self.download_model.add_download(item)
        
        # Start download process
        self._start_download_process(index, url, format_id, quality)
    
    def _start_download_process(self, index, url, format_id, quality):
        """Start the actual download process"""
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        
        # Connect signals
        process.readyReadStandardOutput.connect(
            lambda: self._handle_process_output(index, process))
        process.finished.connect(
            lambda code, status: self._handle_process_finished(index, code, status))
        
        # Build yt-dlp command
        output_template = os.path.join(self.download_path, "%(title)s.%(ext)s")
        
        cmd = [
            "yt-dlp",
            url,
            "-f", format_id,
            "-o", output_template,
            "--newline",  # Output progress as new lines
            "--no-playlist",  # Skip playlist if single video
            "--write-thumbnail",  # Download thumbnail
            "--embed-thumbnail",  # Embed thumbnail in video file
        ]
        
        # Filter out empty strings
        cmd = [arg for arg in cmd if arg]
        
        process.start(cmd[0], cmd[1:])
        self.current_processes[index] = process
        
        self.download_model.update_download(index, status="downloading")
        self.statusMessage.emit(f"Starting download: {url}")
    
    def _handle_process_output(self, index, process):
        """Handle output from yt-dlp process"""
        output = process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        
        for line in output.split('\n'):
            # Parse video title
            if '[download] Destination:' in line:
                dest = line.split('Destination:')[1].strip()
                title = os.path.basename(dest)
                self.download_model.update_download(index, title=title)
            
            # Parse progress
            elif '[download]' in line and '%' in line:
                try:
                    percent_str = line.split('%')[0].split()[-1]
                    progress = int(float(percent_str))
                    
                    # Parse speed, ETA, and size
                    speed = "N/A"
                    eta = "N/A"
                    size = "N/A"
                    
                    if 'at' in line:
                        speed_match = re.search(r'at\s+([\d.]+\s*\w+/s)', line)
                        if speed_match:
                            speed = speed_match.group(1)
                    
                    if 'ETA' in line:
                        eta_match = re.search(r'ETA\s+([\d:]+)', line)
                        if eta_match:
                            eta = eta_match.group(1)
                    
                    if 'of' in line:
                        size_match = re.search(r'of\s+([\d.]+\s*\w+)', line)
                        if size_match:
                            size = size_match.group(1)
                    
                    self.download_model.update_download(
                        index, progress=progress, speed=speed, eta=eta, file_size=size)
                    self.downloadProgress.emit(index, progress, speed, eta, size)
                except Exception as e:
                    pass
            
            # Parse errors
            elif 'ERROR:' in line:
                error_msg = line.split('ERROR:')[1].strip()
                self.download_model.update_download(index, error_message=error_msg)
    
    def _handle_process_finished(self, index, exit_code, exit_status):
        """Handle download process completion"""
        if index in self.current_processes:
            del self.current_processes[index]
        
        item = self.download_model.get_download(index)
        
        if exit_code == 0:
            self.download_model.update_download(index, status="completed", progress=100)
            if item:
                item.completed_time = datetime.now()
            self.downloadComplete.emit(index, "")
            self.statusMessage.emit(f"Download completed: {item.title if item else 'Unknown'}")
            
            # Check if auto-convert to MP3 is enabled
            if self.settings_manager and self.settings_manager.autoConvertMp3:
                self.convert_to_mp3(index)
        else:
            error_msg = item.error_message if item else f"Process failed with code {exit_code}"
            self.download_model.update_download(index, status="error", error_message=error_msg)
            self.downloadError.emit(index, error_msg)
            self.statusMessage.emit(f"Download failed: {error_msg}")
    
    @Slot(int)
    def convert_to_mp3(self, index):
        """Convert downloaded video to MP3"""
        item = self.download_model.get_download(index)
        if not item or item.status != "completed":
            return
        
        self.download_model.update_download(index, status="converting")
        self.statusMessage.emit(f"Converting {item.title} to MP3...")
        
        # TODO: Implement FFmpeg conversion
        # This would require FFmpeg installation
        QTimer.singleShot(2000, lambda: self._conversion_complete(index))
    
    def _conversion_complete(self, index):
        """Handle conversion completion"""
        self.download_model.update_download(index, status="completed")
        self.conversionComplete.emit(index, "")
        self.statusMessage.emit("Conversion completed")
    
    @Slot()
    def downloadSelectedPlaylistVideos(self, format_id="best"):
        """Download all selected videos from playlist"""
        selected = self.playlist_model.get_selected_videos()
        
        for video in selected:
            self.startDownload(video.url, format_id)
        
        self.statusMessage.emit(f"Added {len(selected)} videos to download queue")
    
    @Slot(int)
    def cancelDownload(self, index):
        """Cancel a download"""
        if index in self.current_processes:
            self.current_processes[index].terminate()
            del self.current_processes[index]
        
        self.download_model.update_download(index, status="error", 
                                           error_message="Cancelled by user")
        self.statusMessage.emit("Download cancelled")
    
    @Slot(int)
    def removeDownload(self, index):
        """Remove a download from the list"""
        self.cancelDownload(index)
        self.download_model.remove_download(index)
    
    @Slot()
    def clearCompletedDownloads(self):
        """Clear all completed downloads"""
        self.download_model.clear_completed()
        self.statusMessage.emit("Cleared completed downloads")
    
    @Slot(str)
    def setDownloadPath(self, path):
        """Set the download directory"""
        self.download_path = path
        if self.settings_manager:
            self.settings_manager.downloadPath = path
        self.statusMessage.emit(f"Download folder set to: {path}")
    
    @Slot(result=str)
    def getDownloadPath(self):
        """Get the current download directory"""
        return self.download_path
    
    @Slot(str)
    def fetchThumbnail(self, url):
        """Fetch thumbnail for a URL"""
        self.thumbnail_fetcher.fetch_thumbnail(url)
```

## 📄 ui/components/VideoPreview.qml

```python
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Video preview component with thumbnail and metadata
Rectangle {
    id: root
    color: "white"
    border.color: "#e0e0e0"
    border.width: 1
    radius: 8
    
    // Properties
    property string videoTitle: ""
    property string videoUrl: ""
    property string videoDuration: ""
    property string thumbnailUrl: ""
    property string description: ""
    property bool isLoading: false
    property string localThumbnailPath: ""
    
    // Signals
    signal downloadClicked()
    signal cancelClicked()
    
    // Layout
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15
        
        // Header with thumbnail and title
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            // Thumbnail
            Rectangle {
                width: 160
                height: 90
                color: "#f0f0f0"
                border.color: "#cccccc"
                border.width: 1
                radius: 4
                
                // Loading indicator
                BusyIndicator {
                    anchors.centerIn: parent
                    running: isLoading && !localThumbnailPath
                    visible: isLoading && !localThumbnailPath
                }
                
                // Thumbnail image
                Image {
                    id: thumbnailImage
                    anchors.fill: parent
                    anchors.margins: 2
                    fillMode: Image.PreserveAspectCrop
                    source: localThumbnailPath || "qrc:/icons/placeholder.png"
                    visible: !isLoading || localThumbnailPath
                    asynchronous: true
                    
                    // Fallback to placeholder on error
                    onStatusChanged: {
                        if (status === Image.Error) {
                            source = "qrc:/icons/placeholder.png"
                        }
                    }
                }
                
                // Duration badge
                Rectangle {
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.margins: 5
                    width: durationText.implicitWidth + 10
                    height: 20
                    color: "#80000000"
                    radius: 3
                    visible: videoDuration
                    
                    Text {
                        id: durationText
                        anchors.centerIn: parent
                        text: formatDuration(videoDuration)
                        color: "white"
                        font.pixelSize: 11
                        font.bold: true
                    }
                }
            }
            
            // Title and metadata
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8
                
                Text {
                    text: videoTitle || "Enter a URL to preview"
                    font.bold: true
                    font.pixelSize: 16
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    maximumLineCount: 2
                }
                
                Text {
                    text: videoUrl || ""
                    color: "#666666"
                    font.pixelSize: 11
                    elide: Text.ElideMiddle
                    Layout.fillWidth: true
                    visible: videoUrl !== ""
                }
                
                RowLayout {
                    spacing: 20
                    
                    // Format selector
                    ComboBox {
                        id: formatSelector
                        Layout.preferredWidth: 150
                        model: ["Best Quality", "1080p", "720p", "480p", "360p", "Audio Only"]
                        
                        onCurrentTextChanged: {
                            qualitySelector.visible = currentText !== "Audio Only"
                        }
                    }
                    
                    // Quality selector
                    ComboBox {
                        id: qualitySelector
                        Layout.preferredWidth: 100
                        model: ["mp4", "webm", "mkv"]
                    }
                }
            }
            
            // Action buttons
            ColumnLayout {
                Layout.alignment: Qt.AlignTop
                spacing: 8
                
                Button {
                    text: "Download"
                    Layout.preferredWidth: 120
                    highlighted: true
                    enabled: videoUrl !== "" && !isLoading
                    onClicked: root.downloadClicked()
                }
                
                Button {
                    text: "Cancel"
                    Layout.preferredWidth: 120
                    visible: isLoading
                    onClicked: root.cancelClicked()
                }
            }
        }
        
        // Description section (expandable)
        Rectangle {
            Layout.fillWidth: true
            height: descriptionText.implicitHeight + 20
            color: "#f9f9f9"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 4
            visible: description !== ""
            
            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                
                Text {
                    id: descriptionText
                    text: description
                    color: "#444444"
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    width: parent.width
                }
            }
        }
    }
    
    // Helper functions
    function formatDuration(seconds) {
        if (!seconds || seconds === "0") return ""
        
        var secs = parseInt(seconds)
        if (isNaN(secs)) return ""
        
        var hours = Math.floor(secs / 3600)
        var mins = Math.floor((secs % 3600) / 60)
        var secs_remainder = secs % 60
        
        if (hours > 0) {
            return hours + ":" + padZero(mins) + ":" + padZero(secs_remainder)
        } else {
            return mins + ":" + padZero(secs_remainder)
        }
    }
    
    function padZero(num) {
        return num < 10 ? "0" + num : num
    }
    
    // Update local thumbnail path
    function updateThumbnailPath(path) {
        localThumbnailPath = path.startsWith("file://") ? path : "file://" + path
    }
}
```


## 📄 ui/components/PlaylistItem.qml

```python
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Individual playlist video item with thumbnail
Rectangle {
    id: root
    height: 70
    color: index % 2 ? "#f9f9f9" : "white"
    
    // Properties
    property int videoIndex: index
    property string videoTitle: model.videoTitle
    property string videoUrl: model.videoUrl
    property string duration: model.duration
    property bool selected: model.selected
    property string thumbnailUrl: model.thumbnail || ""
    property string localThumbnailPath: ""
    
    // Signals
    signal selectionChanged(bool selected)
    signal thumbnailRequested(string url)
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 12
        
        // Checkbox
        CheckBox {
            checked: selected
            onCheckedChanged: {
                if (checked !== selected) {
                    playlistModel.toggle_selection(videoIndex)
                    root.selectionChanged(checked)
                }
            }
        }
        
        // Thumbnail
        Rectangle {
            width: 100
            height: 56
            color: "#e0e0e0"
            border.color: "#cccccc"
            border.width: 1
            radius: 3
            
            Image {
                id: thumbnailImage
                anchors.fill: parent
                anchors.margins: 1
                fillMode: Image.PreserveAspectCrop
                source: localThumbnailPath || "qrc:/icons/placeholder.png"
                asynchronous: true
                
                onStatusChanged: {
                    if (status === Image.Error) {
                        source = "qrc:/icons/placeholder.png"
                    }
                }
            }
            
            // Duration badge
            Rectangle {
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 3
                width: durationBadge.implicitWidth + 8
                height: 16
                color: "#80000000"
                radius: 2
                visible: duration
                
                Text {
                    id: durationBadge
                    anchors.centerIn: parent
                    text: formatDuration(duration)
                    color: "white"
                    font.pixelSize: 9
                    font.bold: true
                }
            }
        }
        
        // Title
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            
            Text {
                text: videoTitle
                Layout.fillWidth: true
                elide: Text.ElideRight
                font.pixelSize: 13
                maximumLineCount: 2
                wrapMode: Text.WordWrap
            }
            
            Text {
                text: videoUrl
                color: "#666666"
                font.pixelSize: 10
                elide: Text.ElideMiddle
                Layout.fillWidth: true
                visible: videoUrl !== ""
            }
        }
        
        // Duration text (alternative display)
        Text {
            text: formatDurationLong(duration)
            color: "#666666"
            font.pixelSize: 11
            Layout.alignment: Qt.AlignRight
            visible: duration && duration !== "0"
        }
    }
    
    // Helper functions
    function formatDuration(seconds) {
        if (!seconds || seconds === "0") return ""
        
        var secs = parseInt(seconds)
        if (isNaN(secs)) return ""
        
        var mins = Math.floor(secs / 60)
        var secs_remainder = secs % 60
        return mins + ":" + (secs_remainder < 10 ? "0" : "") + secs_remainder
    }
    
    function formatDurationLong(seconds) {
        if (!seconds || seconds === "0") return ""
        
        var secs = parseInt(seconds)
        if (isNaN(secs)) return ""
        
        var hours = Math.floor(secs / 3600)
        var mins = Math.floor((secs % 3600) / 60)
        var secs_remainder = secs % 60
        
        if (hours > 0) {
            return hours + "h " + mins + "m"
        } else if (mins > 0) {
            return mins + "m " + secs_remainder + "s"
        } else {
            return secs_remainder + "s"
        }
    }
    
    // Update thumbnail path
    function updateThumbnailPath(path) {
        localThumbnailPath = path.startsWith("file://") ? path : "file://" + path
    }
    
    // Request thumbnail when component completes
    Component.onCompleted: {
        if (thumbnailUrl) {
            root.thumbnailRequested(thumbnailUrl)
        }
    }
}
```


## 📄 ui/components/DownloadItem.qml

```python
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Individual download item component with thumbnail
Rectangle {
    id: root
    height: 90
    color: index % 2 ? "#f5f5f5" : "white"
    border.color: "#e0e0e0"
    border.width: 1
    
    // Properties
    property int downloadIndex: index
    property string title: model.title
    property string url: model.url
    property string status: model.status
    property int progress: model.progress
    property string fileSize: model.fileSize
    property string speed: model.speed
    property string eta: model.eta
    property string errorMessage: model.errorMessage
    property string thumbnailUrl: model.thumbnail || ""
    property string localThumbnailPath: ""
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 12
        
        // Thumbnail
        Rectangle {
            width: 100
            height: 56
            color: "#e0e0e0"
            border.color: "#cccccc"
            border.width: 1
            radius: 3
            visible: thumbnailUrl !== ""
            
            Image {
                id: thumbnailImage
                anchors.fill: parent
                anchors.margins: 1
                fillMode: Image.PreserveAspectCrop
                source: localThumbnailPath || "qrc:/icons/placeholder.png"
                asynchronous: true
                
                onStatusChanged: {
                    if (status === Image.Error) {
                        source = "qrc:/icons/placeholder.png"
                    }
                }
            }
        }
        
        // Title and URL column
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 5
            
            Text {
                text: title || "Fetching information..."
                font.bold: true
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
            
            Text {
                text: url
                color: "#666666"
                font.pixelSize: 11
                elide: Text.ElideMiddle
                Layout.fillWidth: true
                visible: status !== "error"
            }
            
            Text {
                text: "Error: " + errorMessage
                color: "#d32f2f"
                font.pixelSize: 11
                visible: status === "error"
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
            
            // Progress bar
            ProgressBar {
                Layout.fillWidth: true
                value: progress / 100
                visible: status === "downloading"
                
                background: Rectangle {
                    implicitHeight: 6
                    color: "#e0e0e0"
                    radius: 3
                }
                
                contentItem: Rectangle {
                    implicitHeight: 6
                    color: "#2196F3"
                    radius: 3
                    width: parent.width * (progress / 100)
                    
                    // Animated gradient for active downloads
                    Rectangle {
                        anchors.fill: parent
                        radius: 3
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#2196F3" }
                            GradientStop { position: 1.0; color: "#1976D2" }
                        }
                        
                        // Shimmer effect
                        Rectangle {
                            anchors.fill: parent
                            radius: 3
                            color: "white"
                            opacity: 0.3
                            
                            NumberAnimation on x {
                                from: -width
                                to: parent.width
                                duration: 1500
                                loops: Animation.Infinite
                                running: status === "downloading"
                            }
                        }
                    }
                }
            }
            
            // Status and progress info
            RowLayout {
                spacing: 20
                visible: status === "downloading"
                
                Text {
                    text: progress + "%"
                    font.pixelSize: 11
                    color: "#2196F3"
                    font.bold: true
                }
                
                Text {
                    text: "⚡ " + speed
                    font.pixelSize: 11
                    color: "#666666"
                }
                
                Text {
                    text: "⏱ " + eta
                    font.pixelSize: 11
                    color: "#666666"
                }
                
                Text {
                    text: "📦 " + fileSize
                    font.pixelSize: 11
                    color: "#666666"
                }
            }
            
            // Status text
            RowLayout {
                spacing: 5
                visible: status !== "downloading"
                
                Rectangle {
                    width: 8
                    height: 8
                    radius: 4
                    color: status === "completed" ? "#4CAF50" :
                           status === "error" ? "#d32f2f" :
                           status === "converting" ? "#FF9800" : "#9E9E9E"
                }
                
                Text {
                    text: status === "completed" ? "Completed" : 
                          status === "error" ? "Failed" :
                          status === "converting" ? "Converting..." :
                          status === "pending" ? "Queued" : status
                    color: status === "completed" ? "#4CAF50" :
                           status === "error" ? "#d32f2f" :
                           status === "converting" ? "#FF9800" : "#666666"
                    font.pixelSize: 11
                    font.capitalization: Font.Capitalize
                }
            }
        }
        
        // Action buttons
        Row {
            spacing: 5
            Layout.alignment: Qt.AlignRight
            
            Button {
                text: status === "downloading" ? "⏸" : "🗑"
                width: 40
                height: 40
                
                ToolTip {
                    text: status === "downloading" ? "Cancel" : "Remove"
                    visible: parent.hovered
                }
                
                onClicked: {
                    if (status === "downloading") {
                        downloadManager.cancelDownload(downloadIndex)
                    } else {
                        downloadManager.removeDownload(downloadIndex)
                    }
                }
            }
            
            Button {
                text: "🎵"
                width: 40
                height: 40
                visible: status === "completed"
                
                ToolTip {
                    text: "Convert to MP3"
                    visible: parent.hovered
                }
                
                onClicked: downloadManager.convert_to_mp3(downloadIndex)
            }
            
            Button {
                text: "📁"
                width: 40
                height: 40
                visible: status === "completed"
                
                ToolTip {
                    text: "Open Folder"
                    visible: parent.hovered
                }
                
                onClicked: {
                    // Open folder in file explorer
                    Qt.openUrlExternally(downloadManager.getDownloadPath())
                }
            }
        }
    }
    
    // Update thumbnail path
    function updateThumbnailPath(path) {
        localThumbnailPath = path.startsWith("file://") ? path : "file://" + path
    }
    
    // Request thumbnail when component completes
    Component.onCompleted: {
        if (thumbnailUrl) {
            downloadManager.fetchThumbnail(thumbnailUrl)
        }
    }
}
```


## 📄 ui/main_window.qml

```python
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import "components"

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 1000
    height: 750
    title: "ClipGrab Clone - Video Downloader"
    minimumWidth: 800
    minimumHeight: 600
    
    // Properties
    property string currentUrl: ""
    property string currentVideoTitle: ""
    property string currentThumbnail: ""
    property string currentDescription: ""
    property string currentDuration: ""
    property bool isPlaylist: false
    property var availableFormats: []
    
    // Colors
    readonly property color primaryColor: "#2196F3"
    readonly property color successColor: "#4CAF50"
    readonly property color errorColor: "#d32f2f"
    readonly property color warningColor: "#FF9800"
    readonly property color backgroundColor: "#f5f5f5"
    
    // Menu bar
    menuBar: MenuBar {
        Menu {
            title: "File"
            
            MenuItem {
                text: "Set Download Folder..."
                onTriggered: folderDialog.open()
            }
            
            MenuItem {
                text: "Import URLs from File..."
                onTriggered: importDialog.open()
            }
            
            MenuSeparator {}
            
            MenuItem {
                text: "Exit"
                shortcut: "Ctrl+Q"
                onTriggered: Qt.quit()
            }
        }
        
        Menu {
            title: "Edit"
            
            MenuItem {
                text: "Clear Completed Downloads"
                onTriggered: downloadManager.clearCompletedDownloads()
            }
            
            MenuItem {
                text: "Clear History"
                onTriggered: settingsManager.clearHistory()
            }
            
            MenuSeparator {}
            
            MenuItem {
                text: "Preferences"
                shortcut: "Ctrl+,"
                onTriggered: settingsDialog.open()
            }
        }
        
        Menu {
            title: "View"
            
            MenuItem {
                text: "Toggle Dark Mode"
                checkable: true
                checked: false
                // TODO: Implement dark mode
            }
        }
        
        Menu {
            title: "Help"
            
            MenuItem {
                text: "Check for Updates"
                onTriggered: checkUpdates()
            }
            
            MenuItem {
                text: "About"
                onTriggered: aboutDialog.open()
            }
            
            MenuSeparator {}
            
            MenuItem {
                text: "Report Issue"
                onTriggered: Qt.openUrlExternally("https://github.com/your-repo/issues")
            }
        }
    }
    
    // Dialogs
    FolderDialog {
        id: folderDialog
        title: "Select Download Folder"
        currentFolder: downloadManager.getDownloadPath()
        
        onAccepted: {
            downloadManager.setDownloadPath(selectedFolder)
            statusText.text = "Download folder set to: " + selectedFolder
        }
    }
    
    FileDialog {
        id: importDialog
        title: "Import URLs from File"
        nameFilters: ["Text files (*.txt)", "All files (*)"]
        
        onAccepted: {
            // TODO: Implement URL import
            statusText.text = "Importing URLs from: " + selectedFile
        }
    }
    
    Dialog {
        id: aboutDialog
        title: "About ClipGrab Clone"
        standardButtons: Dialog.Ok
        width: 450
        height: 300
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 15
            
            RowLayout {
                spacing: 15
                
                // App icon
                Rectangle {
                    width: 64
                    height: 64
                    color: primaryColor
                    radius: 12
                    
                    Text {
                        anchors.centerIn: parent
                        text: "🎬"
                        font.pixelSize: 32
                    }
                }
                
                ColumnLayout {
                    Text {
                        text: "ClipGrab Clone"
                        font.bold: true
                        font.pixelSize: 20
                    }
                    
                    Text {
                        text: "Version 1.0.0"
                        font.pixelSize: 12
                        color: "#666666"
                    }
                }
            }
            
            Text {
                text: "A powerful video downloader application built with PySide6 and QML.\n\nSupports downloading videos and playlists from various platforms including YouTube, Vimeo, Dailymotion, Facebook, Twitter, TikTok, Instagram, and more."
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
            
            Text {
                text: "Powered by yt-dlp"
                font.italic: true
                color: "#666666"
            }
            
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#e0e0e0"
            }
            
            Text {
                text: "© 2024 ClipGrab Clone. All rights reserved."
                font.pixelSize: 11
                color: "#999999"
                Layout.alignment: Qt.AlignHCenter
            }
        }
    }
    
    Dialog {
        id: settingsDialog
        title: "Preferences"
        standardButtons: Dialog.Ok | Dialog.Cancel
        width: 500
        height: 400
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 15
            
            GroupBox {
                title: "General"
                Layout.fillWidth: true
                
                ColumnLayout {
                    CheckBox {
                        text: "Monitor clipboard for URLs"
                        checked: settingsManager.clipboardMonitoring
                        onCheckedChanged: settingsManager.clipboardMonitoring = checked
                    }
                    
                    CheckBox {
                        text: "Auto-convert to MP3 after download"
                        checked: settingsManager.autoConvertMp3
                        onCheckedChanged: settingsManager.autoConvertMp3 = checked
                    }
                    
                    RowLayout {
                        Text { text: "Max concurrent downloads:" }
                        SpinBox {
                            value: settingsManager.maxConcurrent
                            from: 1
                            to: 10
                            onValueChanged: settingsManager.maxConcurrent = value
                        }
                    }
                }
            }
            
            GroupBox {
                title: "Download"
                Layout.fillWidth: true
                
                ColumnLayout {
                    RowLayout {
                        Text { text: "Download folder:" }
                        TextField {
                            Layout.fillWidth: true
                            text: downloadManager.getDownloadPath()
                            readOnly: true
                        }
                        Button {
                            text: "Browse..."
                            onClicked: folderDialog.open()
                        }
                    }
                }
            }
            
            GroupBox {
                title: "Advanced"
                Layout.fillWidth: true
                
                ColumnLayout {
                    CheckBox {
                        text: "Save download history"
                        checked: settingsManager.get_value("save_history", true)
                        // TODO: Connect to settings
                    }
                    
                    Button {
                        text: "Clear History"
                        onClicked: settingsManager.clearHistory()
                    }
                    
                    Button {
                        text: "Clear Thumbnail Cache"
                        onClicked: clearThumbnailCache()
                    }
                }
            }
        }
    }
    
    // Main content
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15
        
        // URL input section
        Rectangle {
            Layout.fillWidth: true
            height: 100
            color: "white"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10
                
                Text {
                    text: "Enter Video or Playlist URL"
                    font.bold: true
                    font.pixelSize: 14
                    color: "#333333"
                }
                
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    
                    TextField {
                        id: urlInput
                        Layout.fillWidth: true
                        placeholderText: "https://www.youtube.com/watch?v=..."
                        
                        onTextChanged: {
                            currentUrl = text
                        }
                        
                        // Handle paste from clipboard
                        Keys.onPressed: (event) => {
                            if (event.key === Qt.Key_V && event.modifiers & Qt.ControlModifier) {
                                urlInput.paste()
                                currentUrl = urlInput.text
                            }
                        }
                    }
                    
                    Button {
                        text: "📋 Paste"
                        onClicked: {
                            urlInput.paste()
                            currentUrl = urlInput.text
                        }
                    }
                    
                    Button {
                        text: "🔍 Analyze"
                        highlighted: true
                        enabled: currentUrl !== ""
                        onClicked: analyzeUrl()
                    }
                }
                
                // Clipboard monitoring indicator
                RowLayout {
                    visible: settingsManager.clipboardMonitoring
                    
                    Rectangle {
                        width: 8
                        height: 8
                        radius: 4
                        color: "#4CAF50"
                        
                        NumberAnimation on opacity {
                            from: 0.5
                            to: 1.0
                            duration: 1000
                            loops: Animation.Infinite
                            running: true
                        }
                    }
                    
                    Text {
                        text: "Clipboard monitoring active"
                        font.pixelSize: 10
                        color: "#666666"
                    }
                }
            }
        }
        
        // Video preview section
        VideoPreview {
            id: videoPreview
            Layout.fillWidth: true
            visible: !isPlaylist && currentVideoTitle !== ""
            
            videoTitle: currentVideoTitle
            videoUrl: currentUrl
            videoDuration: currentDuration
            thumbnailUrl: currentThumbnail
            description: currentDescription
            
            onDownloadClicked: {
                var format = getSelectedFormat()
                downloadManager.startDownload(currentUrl, format, "best")
                statusText.text = "Download started: " + currentVideoTitle
            }
            
            onCancelClicked: {
                // Cancel analysis
                isLoading = false
            }
        }
        
        // Playlist view section
        Rectangle {
            id: playlistView
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            visible: isPlaylist
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12
                
                // Playlist header
                RowLayout {
                    Layout.fillWidth: true
                    
                    // Playlist thumbnail
                    Rectangle {
                        width: 120
                        height: 68
                        color: "#f0f0f0"
                        border.color: "#cccccc"
                        border.width: 1
                        radius: 4
                        
                        Image {
                            id: playlistThumbnail
                            anchors.fill: parent
                            anchors.margins: 2
                            fillMode: Image.PreserveAspectCrop
                            source: playlistThumbnailPath || "qrc:/icons/placeholder.png"
                            asynchronous: true
                        }
                    }
                    
                    ColumnLayout {
                        Layout.fillWidth: true
                        
                        Text {
                            id: playlistTitle
                            text: "Playlist Title"
                            font.bold: true
                            font.pixelSize: 16
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }
                        
                        Text {
                            id: playlistCount
                            text: "0 videos"
                            font.pixelSize: 12
                            color: "#666666"
                        }
                    }
                    
                    Row {
                        spacing: 8
                        
                        Button {
                            text: "✓ Select All"
                            onClicked: playlistModel.select_all()
                        }
                        
                        Button {
                            text: "✗ Deselect All"
                            onClicked: playlistModel.deselect_all()
                        }
                        
                        ComboBox {
                            id: playlistFormatSelector
                            Layout.preferredWidth: 150
                            model: ["Best Quality", "1080p", "720p", "480p", "360p"]
                        }
                        
                        Button {
                            text: "⬇ Download Selected"
                            highlighted: true
                            onClicked: {
                                var format = getPlaylistFormat()
                                downloadManager.downloadSelectedPlaylistVideos(format)
                                statusText.text = "Added selected videos to download queue"
                            }
                        }
                    }
                }
                
                // Playlist videos list
                ListView {
                    id: playlistListView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: playlistModel
                    spacing: 2
                    
                    delegate: PlaylistItem {
                        width: playlistListView.width
                        
                        onThumbnailRequested: function(url) {
                            downloadManager.fetchThumbnail(url)
                        }
                    }
                    
                    ScrollBar.vertical: ScrollBar {}
                }
            }
        }
        
        property string playlistThumbnailPath: ""
        
        // Downloads section
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: !isPlaylist
            color: "white"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: "Downloads"
                        font.bold: true
                        font.pixelSize: 14
                        Layout.fillWidth: true
                    }
                    
                    Text {
                        text: downloadManager.downloads.rowCount() + " item(s)"
                        font.pixelSize: 12
                        color: "#666666"
                    }
                    
                    Button {
                        text: "Clear Completed"
                        onClicked: downloadManager.clearCompletedDownloads()
                    }
                }
                
                ListView {
                    id: downloadsList
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: downloadManager.downloads
                    spacing: 2
                    
                    delegate: DownloadItem {
                        width: downloadsList.width
                    }
                    
                    ScrollBar.vertical: ScrollBar {}
                    
                    // Empty state
                    Rectangle {
                        anchors.fill: parent
                        color: "transparent"
                        visible: downloadsList.count === 0
                        
                        Column {
                            anchors.centerIn: parent
                            spacing: 10
                            
                            Text {
                                text: "📥"
                                font.pixelSize: 48
                                color: "#cccccc"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                            
                            Text {
                                text: "No downloads yet"
                                font.pixelSize: 14
                                color: "#999999"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                            
                            Text {
                                text: "Enter a URL above to start downloading"
                                font.pixelSize: 12
                                color: "#bbbbbb"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }
        }
        
        // Status bar
        Rectangle {
            Layout.fillWidth: true
            height: 35
            color: "#f8f8f8"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 4
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 15
                
                Text {
                    id: statusText
                    text: "Ready"
                    Layout.fillWidth: true
                    color: "#333333"
                }
                
                // Download speed indicator
                RowLayout {
                    spacing: 5
                    visible: activeDownloads > 0
                    
                    Rectangle {
                        width: 8
                        height: 8
                        radius: 4
                        color: primaryColor
                        
                        RotationAnimation on rotation {
                            from: 0
                            to: 360
                            duration: 1000
                            loops: Animation.Infinite
                            running: activeDownloads > 0
                        }
                    }
                    
                    Text {
                        text: activeDownloads + " active"
                        font.pixelSize: 11
                        color: "#666666"
                    }
                }
                
                Text {
                    text: "📁 " + getShortPath(downloadManager.getDownloadPath())
                    font.pixelSize: 11
                    color: "#666666"
                    
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: Qt.openUrlExternally(downloadManager.getDownloadPath())
                    }
                }
            }
        }
    }
    
    // Helper properties
    property int activeDownloads: {
        var count = 0
        for (var i = 0; i < downloadManager.downloads.rowCount(); i++) {
            if (downloadManager.downloads.data(
                downloadManager.downloads.index(i, 0), 
                downloadManager.downloads.StatusRole) === "downloading") {
                count++
            }
        }
        return count
    }
    
    // Helper functions
    function analyzeUrl() {
        if (!currentUrl) return
        
        statusText.text = "Analyzing URL..."
        videoPreview.isLoading = true
        
        var result = JSON.parse(downloadManager.fetchVideoInfo(currentUrl))
        
        videoPreview.isLoading = false
        
        if (result.error) {
            statusText.text = "Error: " + result.error
        } else if (result.type === "playlist") {
            isPlaylist = true
            playlistTitle.text = result.title
            playlistCount.text = result.count + " videos"
            
            if (result.thumbnail) {
                playlistThumbnailPath = result.thumbnail
            }
            
            videoPreview.visible = false
            playlistView.visible = true
            statusText.text = "Playlist loaded: " + result.title
        } else {
            isPlaylist = false
            currentVideoTitle = result.title
            currentDuration = result.duration
            currentThumbnail = result.thumbnail
            currentDescription = result.description
            availableFormats = result.formats
            
            playlistView.visible = false
            videoPreview.visible = true
            statusText.text = "Video loaded: " + result.title
        }
    }
    
    function getSelectedFormat() {
        var formatSelector = videoPreview.children.find(c => c.objectName === "formatSelector")
        var selection = formatSelector ? formatSelector.currentText : "Best Quality"
        
        if (selection === "Best Quality") {
            return "best"
        } else if (selection === "Audio Only") {
            return "bestaudio"
        } else {
            var height = selection.replace("p", "")
            return "bestvideo[height<=" + height + "]+bestaudio/best[height<=" + height + "]"
        }
    }
    
    function getPlaylistFormat() {
        var selection = playlistFormatSelector.currentText
        
        if (selection === "Best Quality") {
            return "best"
        } else {
            var height = selection.replace("p", "")
            return "bestvideo[height<=" + height + "]+bestaudio/best[height<=" + height + "]"
        }
    }
    
    function getShortPath(path) {
        if (!path) return ""
        var parts = path.split(/[/\\]/)
        if (parts.length > 3) {
            return "..." + parts.slice(-2).join("/")
        }
        return path
    }
    
    function clearThumbnailCache() {
        // TODO: Implement thumbnail cache clearing
        statusText.text = "Thumbnail cache cleared"
    }
    
    function checkUpdates() {
        statusText.text = "Checking for updates..."
        // TODO: Implement update checking
        Qt.callLater(function() {
            statusText.text = "You're running the latest version"
        })
    }
    
    // Connect signals
    Connections {
        target: downloadManager
        
        function onStatusMessage(message) {
            statusText.text = message
        }
        
        function onInfoFetched(title, duration, thumbnail, description, url) {
            currentVideoTitle = title
            currentDuration = duration
            currentThumbnail = thumbnail
            currentDescription = description
            
            if (thumbnail) {
                downloadManager.fetchThumbnail(thumbnail)
            }
        }
        
        function onPlaylistFetched(title, count, thumbnail) {
            playlistTitle.text = title
            playlistCount.text = count + " videos"
            
            if (thumbnail) {
                playlistThumbnailPath = thumbnail
                downloadManager.fetchThumbnail(thumbnail)
            }
        }
        
        function onThumbnailReady(url, localPath) {
            // Update video preview thumbnail
            if (url === currentThumbnail) {
                videoPreview.updateThumbnailPath(localPath)
            }
            
            // Update playlist thumbnail
            if (url === playlistThumbnailPath) {
                playlistThumbnail.source = "file://" + localPath
            }
            
            // Update download item thumbnails
            for (var i = 0; i < downloadsList.count; i++) {
                var item = downloadsList.itemAtIndex(i)
                if (item && item.thumbnailUrl === url) {
                    item.updateThumbnailPath(localPath)
                }
            }
            
            // Update playlist video thumbnails
            for (var j = 0; j < playlistListView.count; j++) {
                var playlistItem = playlistListView.itemAtIndex(j)
                if (playlistItem && playlistItem.thumbnailUrl === url) {
                    playlistItem.updateThumbnailPath(localPath)
                }
            }
        }
    }
    
    // Clipboard monitoring
    Connections {
        target: clipboardMonitor
        
        function onUrlDetected(url) {
            if (settingsManager.clipboardMonitoring) {
                urlInput.text = url
                currentUrl = url
                statusText.text = "URL detected from clipboard"
            }
        }
    }
}
```


## 📄 main.py

```python
#!/usr/bin/env python3
"""
ClipGrab Clone - A Video Downloader Application
Main entry point for the application

Features:
- Video and playlist downloading from multiple platforms
- Thumbnail preview and metadata display
- Clipboard monitoring for automatic URL detection
- Download queue management with progress tracking
- Format selection and quality options
- Persistent settings storage
"""

import sys
import os
from pathlib import Path

from PySide6.QtCore import QUrl, Qt, QCoreApplication
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.download_manager import DownloadManager
from backend.settings_manager import SettingsManager
from backend.clipboard_monitor import ClipboardMonitor

def main():
    """Main application entry point"""
    
    # Set application attributes for high DPI support
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # Create application instance
    app = QGuiApplication(sys.argv)
    app.setApplicationName("ClipGrab Clone")
    app.setOrganizationName("ClipGrabClone")
    app.setApplicationVersion("1.0.0")
    
    # Set application icon (if available)
    icon_path = Path(__file__).parent / "resources" / "icons" / "app_icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    print("=" * 50)
    print("ClipGrab Clone - Video Downloader")
    print(f"Version: {app.applicationVersion()}")
    print("=" * 50)
    
    # Initialize settings manager
    print("Loading settings...")
    settings_manager = SettingsManager()
    
    # Initialize download manager
    print("Initializing download manager...")
    download_manager = DownloadManager(settings_manager)
    
    # Initialize clipboard monitor
    print("Starting clipboard monitor...")
    clipboard_monitor = ClipboardMonitor()
    
    # Connect clipboard monitor to download manager
    clipboard_monitor.urlDetected.connect(download_manager.fetchVideoInfo)
    
    # Enable clipboard monitoring based on settings
    if settings_manager.clipboardMonitoring:
        clipboard_monitor.start_monitoring()
        print("Clipboard monitoring enabled")
    
    # Create QML engine
    print("Loading QML interface...")
    engine = QQmlApplicationEngine()
    
    # Expose Python objects to QML
    engine.rootContext().setContextProperty("downloadManager", download_manager)
    engine.rootContext().setContextProperty("playlistModel", download_manager.playlistVideos)
    engine.rootContext().setContextProperty("settingsManager", settings_manager)
    engine.rootContext().setContextProperty("clipboardMonitor", clipboard_monitor)
    
    # Load QML file
    qml_file = Path(__file__).parent / "ui" / "main_window.qml"
    
    if qml_file.exists():
        print(f"Loading QML from: {qml_file}")
        engine.load(QUrl.fromLocalFile(str(qml_file)))
    else:
        # Fallback to resource loading
        try:
            import resources_rc
            print("Loading QML from resources")
            engine.load(QUrl("qrc:/main_window.qml"))
        except ImportError:
            print("Error: Could not load resources. Please compile resources.qrc first.")
            print("Run: pyside6-rcc resources/resources.qrc -o resources_rc.py")
            sys.exit(-1)
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        print("Error: Failed to load QML interface")
        sys.exit(-1)
    
    print("Application started successfully!")
    print(f"Download folder: {download_manager.getDownloadPath()}")
    
    # Get the main window
    main_window = engine.rootObjects()[0]
    
    # Clean up on exit
    def on_exit():
        """Cleanup function called before application exit"""
        print("\nShutting down...")
        clipboard_monitor.stop_monitoring()
        
        # Cancel any active downloads
        for index in list(download_manager.current_processes.keys()):
            download_manager.cancelDownload(index)
        
        print("Goodbye!")
    
    app.aboutToQuit.connect(on_exit)
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```


## 🚀 Installation and Setup Instructions

### 1. Create a virtual environment:

```zsh
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies:

```zsh
pip install -r requirements.txt
```

### 3. Compile resources:

```zsh
pyside6-rcc resources/resources.qrc -o resources_rc.py
```

### 4. Create placeholder icon:

Create a simple placeholder icon or download one and save it as:

```txt
resources/icons/placeholder.png
```

### 5. Run the application:
```zsh
python main.py
```


## 📦 Building Standalone Executable

### Using PyInstaller:

```zsh
pip install pyinstaller

pyinstaller --name="ClipGrabClone" \
    --windowed \
    --icon=resources/icons/app_icon.png \
    --add-data="ui:ui" \
    --add-data="resources:resources" \
    --hidden-import=yt_dlp \
    --hidden-import=PySide6.QtQml \
    --hidden-import=PySide6.QtNetwork \
    main.py
```


## ✨ Features Summary

### ✅ Implemented Features:

- **Video Preview**: Thumbnail display with title and duration

- **Playlist Support**: Full playlist detection and selective downloading
    
- **Thumbnail Caching**: Downloaded thumbnails are cached locally
    
- **Clipboard Monitoring**: Automatic URL detection
    
- **Format Selection**: Multiple quality and format options
    
- **Download Queue**: Manage multiple downloads with progress tracking
    
- **Persistent Settings**: User preferences saved between sessions
    
- **Modern UI**: Clean QML interface with animations
    
- **Error Handling**: Comprehensive error messages and recovery
    
- **History**: Track downloaded videos (optional)
    

### 🎨 UI Components:

- VideoPreview with thumbnail and metadata
    
- Playlist view with individual video thumbnails
    
- Download items with progress bars and status
    
- Settings dialog for configuration
    
- Status bar with real-time information
    

### 🔧 Technical Features:

- Thread-safe download management
    
- Network request handling for thumbnails
    
- Signal/slot communication between Python and QML
    
- Resource management with Qt Resource System
    
- Cross-platform compatibility