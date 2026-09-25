# PySide6 / QtWidgets - API Integration (Industry Standard)

> **The Recommended Method: QNetworkAccessManager ONLY**
> No `requests` in production Qt apps. This is how professional Qt developers do it.

---

### Why QNetworkAccessManager (QNAM) and NOT requests?

| requests (Don't use in Qt) | QNetworkAccessManager (Use this) |
| :--- | :--- |
| Blocks UI thread -> App freezes on API call | Async by design -> UI never freezes |
| You need threads / hack to make it work | Integrated with Qt Event Loop |
| No native signal/slot | Emits `finished`, `progress` signals |
| Manual JSON parsing + error handling | Works with Qt's caching, cookies, SSL, proxies automatically |

**Rule:** If your app has `QApplication`, use QNAM.

### Industry Standard Architecture

This is how teams structure API integration in Qt:

```
my_api_app/
├── app.py                 # Entry
├── core/
│   ├── api_client.py      # ONE central QNAM client (Singleton)
│   ├── models.py          # Dataclasses for API responses
│   └── config.py          # Base URL, API keys
├── services/
│   └── api_service.py     # Business logic (e.g., UserService, WeatherService)
├── ui/
│   └── main_window.py     # Only UI, no API calls directly
└── requirements.txt
```

**Flow:** UI Button Click -> Service -> ApiClient (QNAM) -> Signal back -> UI updates

Never call QNAM directly from QWidget. Always go through a Service.

### Step-by-Step Process

#### Step 1: Project Setup

`requirements.txt`
```
PySide6
```

#### Step 2: Create Central ApiClient (core/api_client.py)

This is the most important file. One QNAM for the whole app.

```python
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QObject, Signal, QUrl, QByteArray, QJsonDocument, QUrlQuery
from PySide6.QtCore import Slot
import json

class ApiClient(QObject):
    """
    Singleton API Client using QNetworkAccessManager
    Industry pattern: One instance for entire app
    """
    # Generic signals for any request
    finished = Signal(dict)  # success data
    failed = Signal(str)     # error message
    loading = Signal(bool)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self.manager = QNetworkAccessManager(self)
        self.base_url = "https://jsonplaceholder.typicode.com"  # Replace with your API
        self.headers = {
            b"Content-Type": b"application/json",
            b"Accept": b"application/json"
        }
        self._initialized = True

    def set_auth_token(self, token: str):
        """Call after login"""
        self.headers[b"Authorization"] = f"Bearer {token}".encode()

    def set_base_url(self, url: str):
        self.base_url = url.rstrip("/")

    # ---- CORE METHODS ----
    def _create_request(self, endpoint: str) -> QNetworkRequest:
        url = QUrl(f"{self.base_url}{endpoint}")
        request = QNetworkRequest(url)
        for key, value in self.headers.items():
            request.setRawHeader(key, value)
        return request

    def get(self, endpoint: str, params: dict = None):
        """GET request"""
        self.loading.emit(True)
        if params:
            url = QUrl(f"{self.base_url}{endpoint}")
            query = QUrlQuery()
            for k, v in params.items():
                query.addQueryItem(k, str(v))
            url.setQuery(query)
            request = QNetworkRequest(url)
            for key, value in self.headers.items():
                request.setRawHeader(key, value)
        else:
            request = self._create_request(endpoint)

        reply = self.manager.get(request)
        reply.finished.connect(lambda: self._handle_response(reply))
        return reply

    def post(self, endpoint: str, data: dict):
        """POST request"""
        self.loading.emit(True)
        request = self._create_request(endpoint)
        payload = QByteArray(json.dumps(data).encode())
        reply = self.manager.post(request, payload)
        reply.finished.connect(lambda: self._handle_response(reply))
        return reply

    def put(self, endpoint: str, data: dict):
        self.loading.emit(True)
        request = self._create_request(endpoint)
        payload = QByteArray(json.dumps(data).encode())
        reply = self.manager.put(request, payload)
        reply.finished.connect(lambda: self._handle_response(reply))
        return reply

    def delete(self, endpoint: str):
        self.loading.emit(True)
        request = self._create_request(endpoint)
        reply = self.manager.deleteResource(request)
        reply.finished.connect(lambda: self._handle_response(reply))
        return reply

    @Slot()
    def _handle_response(self, reply: QNetworkReply):
        self.loading.emit(False)
        try:
            if reply.error() == QNetworkReply.NoError:
                raw_data = reply.readAll().data().decode()
                if raw_data:
                    data = json.loads(raw_data)
                    self.finished.emit(data)
                else:
                    self.finished.emit({})
            else:
                # Industry standard error parsing
                status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                error_str = reply.errorString()
                body = reply.readAll().data().decode()
                self.failed.emit(f"[{status}] {error_str} - {body}")
        except Exception as e:
            self.failed.emit(f"Parse error: {str(e)}")
        finally:
            reply.deleteLater()
```

#### Step 3: Define Models (core/models.py)

Never use raw dicts in UI. Use dataclasses.

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Post:
    id: int
    userId: int
    title: str
    body: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", 0),
            userId=data.get("userId", 0),
            title=data.get("title", ""),
            body=data.get("body", "")
        )

@dataclass
class User:
    id: int
    name: str
    email: str
```

#### Step 4: Create Service Layer (services/api_service.py)

UI never talks to ApiClient directly. Service does.

```python
from PySide6.QtCore import QObject, Signal
from core.api_client import ApiClient
from core.models import Post

class PostService(QObject):
    posts_loaded = Signal(list)  # List[Post]
    post_created = Signal(Post)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.api = ApiClient()
        # Connect only once
        self.api.finished.connect(self._on_finished)
        self.api.failed.connect(self._on_failed)
        self._current_action = ""

    def fetch_posts(self):
        self._current_action = "fetch"
        self.api.get("/posts")

    def create_post(self, title: str, body: str):
        self._current_action = "create"
        self.api.post("/posts", {"title": title, "body": body, "userId": 1})

    def _on_finished(self, data: dict):
        if self._current_action == "fetch":
            if isinstance(data, list):
                posts = [Post.from_dict(item) for item in data[:20]]  # first 20
                self.posts_loaded.emit(posts)
        elif self._current_action == "create":
            post = Post.from_dict(data)
            self.post_created.emit(post)

    def _on_failed(self, error_msg: str):
        self.error.emit(error_msg)
```

#### Step 5: UI Layer (ui/main_window.py)

UI only handles signals, loading states, and display.

```python
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from services.api_service import PostService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 API Integration - QNAM Standard")
        self.setGeometry(200, 200, 700, 500)

        self.service = PostService()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Header
        header = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.btn_load = QPushButton("Load Posts")
        self.btn_load.clicked.connect(self.service.fetch_posts)
        header.addWidget(self.status_label)
        header.addStretch()
        header.addWidget(self.btn_load)
        layout.addLayout(header)

        # List
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Create form
        form = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Post title")
        self.body_input = QLineEdit()
        self.body_input.setPlaceholderText("Post body")
        self.btn_create = QPushButton("Create Post")
        self.btn_create.clicked.connect(self.create_post)
        form.addWidget(self.title_input)
        form.addWidget(self.body_input)
        form.addWidget(self.btn_create)
        layout.addLayout(form)

        # Connect service signals to UI slots
        self.service.posts_loaded.connect(self.on_posts_loaded)
        self.service.post_created.connect(self.on_post_created)
        self.service.error.connect(self.on_error)
        
        # Connect loading state from ApiClient
        self.service.api.loading.connect(self.on_loading)

    def create_post(self):
        title = self.title_input.text().strip()
        body = self.body_input.text().strip()
        if not title:
            return
        self.service.create_post(title, body)

    # --- SLOTS ---
    def on_posts_loaded(self, posts):
        self.list_widget.clear()
        for post in posts:
            self.list_widget.addItem(f"[{post.id}] {post.title}")

    def on_post_created(self, post):
        self.status_label.setText(f"Created: {post.title}")
        self.list_widget.insertItem(0, f"[{post.id}] {post.title} (NEW)")

    def on_error(self, msg):
        self.status_label.setText(f"Error: {msg}")
        self.status_label.setStyleSheet("color: red;")

    def on_loading(self, is_loading: bool):
        if is_loading:
            self.status_label.setText("Loading...")
            self.btn_load.setEnabled(False)
            self.btn_create.setEnabled(False)
        else:
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("")
            self.btn_load.setEnabled(True)
            self.btn_create.setEnabled(True)
```

#### Step 6: App Entry (app.py)

```python
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MyQtApiApp")
    app.setOrganizationName("MyCompany")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### How to Handle Authenticated APIs (like Supabase, your own backend)

In `core/config.py`:

```python
API_BASE_URL = "https://your-api.supabase.co"
```

In your Login flow, after you get token:

```python
from core.api_client import ApiClient

api = ApiClient()
api.set_auth_token("eyJhbGciOi... your jwt")
api.set_base_url("https://xyz.supabase.co/rest/v1")

# Now all requests automatically have Authorization header
api.get("/notes?select=*")
```

### Advanced: Handling Query Params, File Upload, Timeouts

```python
# GET with params
api.get("/users", params={"page": 1, "limit": 10})

# Set timeout (industry standard 15s)
request = self._create_request(endpoint)
request.setTransferTimeout(15000)  # 15 seconds in ms, Qt 6.5+

# File upload (multipart)
from PySide6.QtNetwork import QHttpMultiPart, QHttpPart
multipart = QHttpMultiPart(QHttpMultiPart.FormDataType)
# ... add parts
reply = self.manager.post(request, multipart)
multipart.setParent(reply)  # important: prevent GC
```

### Common Mistakes to Avoid

1.  **Creating new QNetworkAccessManager per request** -> WRONG. Use ONE singleton like above. Qt caches connections.
2.  **Not calling reply.deleteLater()** -> Memory leak. Always call it.
3.  **Using requests inside QWidget** -> Freezes app for 2-5 seconds, users think app crashed.
4.  **Parsing JSON in UI thread without try/except** -> App crashes on bad API response.

### Testing the Project

```bash
python app.py
# Click Load Posts -> Will fetch from jsonplaceholder.typicode.com/posts
# Type title + body -> Create Post
```

This template works for any REST API: Supabase, Firebase REST, Django, FastAPI, etc. Just change `base_url`.

---

### Want this as ZIP?

This file is ready to copy. Structure above is exactly how Qt Company recommends in their docs and how companies like Autodesk, VirtualBox Qt frontend do API integration.

If you want file upload + pagination + auth refresh integrated into this same template, tell me the API you are using and I'll extend it.
