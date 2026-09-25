# PySide6 & QtWidgets: API Integration — Industry Standard Guide

> **Goal:** How to fetch things from online (REST APIs, JSON) and allow users to access online services, without freezing the UI, in a maintainable desktop app.

---

## 1. Core Mental Model: Why Desktop API Integration is Different

In web development, you just `fetch()`. In desktop Qt, you have 2 golden rules:

1.  **Never block the Main Thread (UI Thread).** If you call `requests.get()` directly in a button click, your whole app freezes until the response comes back. Users will think it crashed.
2.  **Separate Concerns.** UI code (`QWidget`) should NEVER know what `https://api.example.com` is. It should call a service layer.

Industry structure solves both.

### Two Ways to Make HTTP Requests in PySide6

| Method | When to Use | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **A) `QNetworkAccessManager`** | Production Qt apps, large projects | Native Qt, non-blocking by design, integrates with Qt event loop, no extra threads needed | More verbose, async via Signals |
| **B) `requests` + `QThread` / `QRunnable`** | Rapid prototyping, if you already have a Python API client | Simple Pythonic code | You MUST put it in a worker thread, otherwise it blocks |

**Industry Choice:** Use **A) QNetworkAccessManager** for all new code. Use B only if you are wrapping an existing SDK that already uses `requests`.

---

## 2. Industry Standard Project Structure

Don't put everything in `main.py`. This is what professional PySide6 developers do:

```
my_desktop_app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point, QApplication setup
│   ├── config.py               # API keys, base URLs (loaded from .env)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # Dataclasses / Pydantic models for API responses
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api_client.py       # CORE: The reusable QNetworkAccessManager wrapper
│   │   ├── auth_service.py     # Login, token handling
│   │   └── weather_service.py  # Example domain service that uses api_client
│   ├── workers/
│   │   ├── __init__.py
│   │   └── api_worker.py       # Wrapper for requests-based approach (if needed)
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── main_controller.py  # Mediator between UI and services
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py      # QMainWindow
│   │   └── widgets/
│   │       └── weather_widget.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── resources/
│   └── styles.qss
├── .env                        # NEVER commit this
├── .env.example
├── requirements.txt
└── README.md
```

**Key Principle: Layered Architecture**

`View (QWidget) -> Controller -> Service -> ApiClient -> Internet`

View knows nothing about HTTP. Service knows nothing about QWidget.

---

## 3. Step 0: Setup & Security

**requirements.txt**
```
PySide6>=6.6.0
python-dotenv
pydantic>=2.0  # for data validation
```

**app/config.py - Centralize everything**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openweathermap.org/data/2.5")
    API_KEY = os.getenv("API_KEY", "") # Load from .env
    REQUEST_TIMEOUT_MS = 15000

# .env file:
# API_BASE_URL=https://api.example.com/v1
# API_KEY=sk-xxxxxxxxxxxx
```

> **Rule:** Never hardcode API keys in code. Use `.env` + `config.py`. For production, use keyring or OS secure storage.

---

## 4. Step 1: The Heart — Reusable ApiClient (Qt-Native Way)

This is the single most important file. You write it once and reuse it everywhere.

**app/services/api_client.py**
```python
from PySide6.QtCore import QObject, Signal, Slot, QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json
from typing import Dict, Any, Optional
from app.config import Config

class ApiClient(QObject):
    """
    Industry standard wrapper around QNetworkAccessManager.
    Handles GET, POST, PUT, DELETE, headers, auth, errors.
    Emits signals instead of returning directly.
    """
    # Signals: (endpoint, data, status_code) or (endpoint, error_message)
    finished = Signal(str, dict, int)  # endpoint, parsed_json, status_code
    failed = Signal(str, str, int)     # endpoint, error_message, status_code

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.base_url = Config.API_BASE_URL.rstrip("/")
        # Optional: cache, auth header setup
        self._default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if Config.API_KEY:
            self._default_headers["Authorization"] = f"Bearer {Config.API_KEY}"

    def _build_request(self, endpoint: str, headers: Optional[Dict] = None) -> QNetworkRequest:
        url = QUrl(f"{self.base_url}/{endpoint.lstrip('/')}")
        request = QNetworkRequest(url)
        # Merge headers
        all_headers = {**self._default_headers, **(headers or {})}
        for k, v in all_headers.items():
            request.setRawHeader(k.encode(), v.encode())
        return request

    def get(self, endpoint: str, params: Optional[Dict] = None):
        """Non-blocking GET"""
        url_str = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query = "&".join([f"{k}={v}" for k,v in params.items()])
            url_str += f"?{query}"
        
        request = self._build_request(endpoint if not params else f"{endpoint}?{query}")
        
        reply = self.manager.get(request)
        # Use lambda to capture endpoint context
        reply.finished.connect(lambda r=reply, e=endpoint: self._on_finished(r, e))

    def post(self, endpoint: str, data: Dict[str, Any]):
        request = self._build_request(endpoint)
        payload = QByteArray(json.dumps(data).encode('utf-8'))
        reply = self.manager.post(request, payload)
        reply.finished.connect(lambda r=reply, e=endpoint: self._on_finished(r, e))

    @Slot()
    def _on_finished(self, reply: QNetworkReply, endpoint: str):
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        if status_code is None:
            status_code = 0

        if reply.error() != QNetworkReply.NetworkError.NoError:
            error_msg = reply.errorString()
            # Try to read body for API error message
            try:
                body = json.loads(bytes(reply.readAll()).decode())
                error_msg = body.get('message', error_msg)
            except:
                pass
            self.failed.emit(endpoint, error_msg, status_code or 500)
        else:
            try:
                raw = bytes(reply.readAll()).decode('utf-8')
                data = json.loads(raw) if raw else {}
                self.finished.emit(endpoint, data, status_code)
            except json.JSONDecodeError as e:
                self.failed.emit(endpoint, f"Invalid JSON: {e}", status_code)
        
        reply.deleteLater()

# Usage singleton pattern (optional but common)
# api_client = ApiClient() # create once in main.py and inject
```

---

## 5. Step 2: Domain Service Layer

Don't call ApiClient directly from UI. Create a service that represents a feature.

**app/models/weather.py (Pydantic)**
```python
from pydantic import BaseModel
from typing import List

class WeatherData(BaseModel):
    city: str
    temp: float
    description: str
    humidity: int

    @classmethod
    def from_api(cls, api_json: dict):
        # Transform raw API response into clean object
        return cls(
            city=api_json['name'],
            temp=api_json['main']['temp'],
            description=api_json['weather'][0]['description'],
            humidity=api_json['main']['humidity']
        )
```

**app/services/weather_service.py**
```python
from PySide6.QtCore import QObject, Signal
from app.services.api_client import ApiClient
from app.models.weather import WeatherData

class WeatherService(QObject):
    weather_fetched = Signal(WeatherData)
    error_occurred = Signal(str)

    def __init__(self, api_client: ApiClient):
        super().__init__()
        self.api_client = api_client
        # Connect client signals to service handlers
        self.api_client.finished.connect(self._handle_finished)
        self.api_client.failed.connect(self._handle_failed)
        self._current_city = ""

    def fetch_weather(self, city: str):
        self._current_city = city
        self.api_client.get("weather", params={"q": city, "appid": "YOUR_KEY", "units": "metric"})

    def _handle_finished(self, endpoint: str, data: dict, status: int):
        if "weather" in endpoint:
            try:
                weather = WeatherData.from_api(data)
                self.weather_fetched.emit(weather)
            except Exception as e:
                self.error_occurred.emit(f"Parse error: {e}")

    def _handle_failed(self, endpoint: str, error: str, status: int):
        if "weather" in endpoint:
            self.error_occurred.emit(f"[{status}] {error}")
```

---

## 6. Step 3: Controller + View (QtWidgets) — No Freezing

**app/views/widgets/weather_widget.py**
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar
from PySide6.QtCore import Slot

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter city, e.g. Eldoret")
        self.btn = QPushButton("Get Weather")
        self.label = QLabel("Ready.")
        self.loader = QProgressBar()
        self.loader.setRange(0,0) # Indeterminate
        self.loader.hide()

        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        layout.addWidget(self.loader)
        layout.addWidget(self.label)

    @Slot(object)
    def show_weather(self, weather):
        self.loader.hide()
        self.label.setText(f"{weather.city}: {weather.temp}°C, {weather.description} (Humidity {weather.humidity}%)")

    @Slot(str)
    def show_error(self, msg):
        self.loader.hide()
        self.label.setText(f"Error: {msg}")

    def set_loading(self, is_loading: bool):
        self.loader.setVisible(is_loading)
        self.btn.setEnabled(not is_loading)
```

**app/controllers/main_controller.py**
```python
from PySide6.QtCore import QObject

class MainController(QObject):
    def __init__(self, view, weather_service):
        super().__init__()
        self.view = view
        self.weather_service = weather_service

        # View -> Controller
        self.view.btn.clicked.connect(self.on_fetch_clicked)
        # Service -> View
        self.weather_service.weather_fetched.connect(self.view.show_weather)
        self.weather_service.error_occurred.connect(self.view.show_error)

    def on_fetch_clicked(self):
        city = self.view.input.text().strip()
        if not city:
            return
        self.view.set_loading(True)
        self.view.label.setText(f"Fetching weather for {city}...")
        self.weather_service.fetch_weather(city)
```

**app/main.py - Wiring Everything**
```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app.services.api_client import ApiClient
from app.services.weather_service import WeatherService
from app.views.widgets.weather_widget import WeatherWidget
from app.controllers.main_controller import MainController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Demo - Industry Structure")
        self.widget = WeatherWidget()
        self.setCentralWidget(self.widget)

def main():
    app = QApplication(sys.argv)
    
    api_client = ApiClient()
    weather_service = WeatherService(api_client)
    
    window = MainWindow()
    controller = MainController(window.widget, weather_service)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## 7. Alternative: Using `requests` Safely (With QThread)

If you MUST use `requests` (e.g., legacy SDK):

**app/workers/api_worker.py**
```python
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Slot
import requests

class WorkerSignals(QObject):
    finished = Signal(dict)
    error = Signal(str)

class ApiRunnable(QRunnable):
    def __init__(self, url: str, params: dict = None):
        super().__init__()
        self.url = url
        self.params = params or {}
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        try:
            resp = requests.get(self.url, params=self.params, timeout=10)
            resp.raise_for_status()
            self.signals.finished.emit(resp.json())
        except Exception as e:
            self.signals.error.emit(str(e))

# In your Controller:
# self.thread_pool = QThreadPool()
# runnable = ApiRunnable("https://api.example.com/data")
# runnable.signals.finished.connect(self.on_data)
# self.thread_pool.start(runnable)
```

> **NEVER do this:** `data = requests.get(...)` inside a button slot. It will freeze.

---

## 8. Advanced Patterns Used in Production

### A) Authentication & Token Refresh
```python
# In ApiClient, add:
def set_auth_token(self, token: str):
    self._default_headers["Authorization"] = f"Bearer {token}"

# Handle 401 in _on_finished -> emit `unauthorized` signal -> AuthService refreshes token -> retries request
```

### B) Allowing Users to Access Online Services (OAuth)
For "Login with Google":
1. Use `QDesktopServices.openUrl(QUrl(auth_url))` to open browser.
2. Start a tiny local HTTP server (`http.server`) on `http://localhost:8080/callback` to catch the code.
3. Exchange code for token via ApiClient.
4. Store token securely using `keyring` library.

Library: `pip install keyring` -> `keyring.set_password("myapp", "access_token", token)`

### C) Caching
Use `QNetworkAccessManager` cache or simple dict with TTL to avoid re-fetching same data.

### D) Pagination & Rate Limits
Your service should handle:
```python
def fetch_all_pages(self):
    self.page = 1
    self.api_client.get(f"items?page={self.page}")

# on finished, if has_more -> fetch next page automatically
```

---

## 9. Error Handling Checklist (Industry)

1.  **Network errors:** No internet, timeout -> show friendly message, retry button
2.  **API errors:** 400, 401, 404, 500 -> parse JSON error message
3.  **Parsing errors:** API changed format -> log + show error
4.  **Loading state:** Always show spinner + disable button while fetching
5.  **Logging:** Use `logging` module, not `print()`

---

## 10. TL;DR — What to Do For Your Next Project

1.  Create the folder structure above.
2.  Copy `ApiClient` — it's your core.
3.  For each API endpoint/feature, create a Service (e.g., `UserService`, `PaymentService`).
4.  Models = Pydantic dataclasses to validate API responses.
5.  Controller connects UI signals to service calls.
6.  View only updates labels, never calls internet.
7.  Always show loading state.

This pattern is used by apps like Autodesk, Dropbox desktop clients, and most professional Qt apps.

---

**Next Steps for You:** Tell me what API you want to integrate (Weather, Firebase, Supabase, M-Pesa, your own backend?), and I can generate the specific `Service` + `Widget` for it using this structure.
