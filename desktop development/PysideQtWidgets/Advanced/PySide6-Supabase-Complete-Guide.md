# PySide6 + Supabase: Complete Desktop App with Auth & Database

> Full project for: Create Account, Login, Login with Google, Auto-Refresh Token, Logout, and Online Database Storage

### Stack
- **UI:** PySide6 (QtWidgets)
- **Backend:** Supabase (Auth + Postgres + Storage)
- **Lang:** Python 3.10+

---

### 1. Supabase Setup (5 mins)

1. Go to https://supabase.com -> New Project
2. **Enable Auth Providers:**
   - Dashboard > Authentication > Providers > Email -> Enable
   - Dashboard > Authentication > Providers > Google -> Enable
     - You need a Google Cloud Console project:
     - Create OAuth 2.0 Client ID > Application type: Web Application
     - Authorized redirect URI: `https://<your-project>.supabase.co/auth/v1/callback`
     - Copy Client ID & Secret into Supabase

3. **Create Tables:** SQL Editor > Run this:

```sql
-- Enable extension
create extension if not exists "uuid-ossp";

-- Notes table
create table public.notes (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade not null,
  title text not null,
  content text,
  created_at timestamp with time zone default now()
);

-- Turn on Row Level Security (CRITICAL)
alter table public.notes enable row level security;

-- Policy: Users can only see their own notes
create policy "Users can manage their own notes"
on public.notes for all
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

-- Storage bucket for user files
insert into storage.buckets (id, name, public) values ('user-files', 'user-files', false);

create policy "Users can manage their own files"
on storage.objects for all
using (bucket_id = 'user-files' and auth.uid()::text = (storage.foldername(name))[1])
with check (bucket_id = 'user-files' and auth.uid()::text = (storage.foldername(name))[1]);
```

4. Get your keys: Project Settings > API > `Project URL` and `anon public` key.

### 2. Project Structure

```
my-pyside-app/
├── .env
├── requirements.txt
├── app.py                 # Entry point
├── supabase_client.py     # Single Supabase instance
├── auth_manager.py        # All auth logic (create, login, google, refresh, logout)
├── login_window.py        # Qt Login UI
├── main_window.py         # Qt Main App UI after login
└── local_server.py        # Tiny localhost server to catch Google OAuth
```

### 3. requirements.txt

```txt
PySide6
supabase
python-dotenv
```

Install: `pip install -r requirements.txt`

### 4. .env

```
SUPABASE_URL=https://xyzxyzxyz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5. supabase_client.py

Single client, used everywhere.

```python
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_ANON_KEY")

if not URL or not KEY:
    raise ValueError("Set SUPABASE_URL and SUPABASE_ANON_KEY in .env")

supabase: Client = create_client(URL, KEY)
```

### 6. local_server.py

Needed to catch Google login redirect on desktop.

```python
import http.server
import urllib.parse
from PySide6.QtCore import QObject, Signal

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        # Parse ?code=... from URL
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            OAuthCallbackHandler.auth_code = params['code'][0]
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Login Successful!</h1><p>You can close this window and go back to the app.</p>")
    
    def log_message(self, format, *args):
        return  # silence logs

def start_server(port=54321):
    server = http.server.HTTPServer(('localhost', port), OAuthCallbackHandler)
    server.handle_request()  # Wait for ONE request
    return OAuthCallbackHandler.auth_code
```

### 7. auth_manager.py (THE CORE)

Handles everything: create, login, google, auto-refresh, logout.

```python
import os
import threading
import time
import webbrowser
from supabase_client import supabase
from local_server import start_server
from PySide6.QtCore import QObject, Signal

class AuthManager(QObject):
    login_success = Signal(object)  # emits user object
    login_failed = Signal(str)
    logged_out = Signal()

    def __init__(self):
        super().__init__()
        self.user = None
        self.session = None
        self._refresh_timer = None

    # --- CREATE ACCOUNT ---
    def create_account(self, email, password):
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                self.user = res.user
                self.session = res.session
                self._start_auto_refresh()
                self.login_success.emit(res.user)
            else:
                self.login_failed.emit("Check your email to confirm account")
        except Exception as e:
            self.login_failed.emit(str(e))

    # --- LOGIN EMAIL/PASSWORD ---
    def login_email(self, email, password):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            self.user = res.user
            self.session = res.session
            self._start_auto_refresh()
            self.login_success.emit(res.user)
        except Exception as e:
            self.login_failed.emit(f"Login failed: {e}")

    # --- LOGIN WITH GOOGLE (Desktop flow) ---
    def login_google(self):
        def run_flow():
            try:
                # This gets the URL Supabase needs to start OAuth
                # We use sign_in_with_oauth which returns a URL
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "google",
                    "options": {"redirect_to": "http://localhost:54321"}
                })
                # res.url is the Google login URL
                webbrowser.open(res.url)
                
                # Start local server and wait for code
                code = start_server(54321)
                
                # Exchange code for session
                # Supabase Python SDK v2: you need to use exchange_code_for_session
                # Note: If using newer supabase-py, do:
                session_res = supabase.auth.exchange_code_for_session({"auth_code": code})
                self.user = session_res.user
                self.session = session_res.session
                self._start_auto_refresh()
                self.login_success.emit(session_res.user)

            except Exception as e:
                self.login_failed.emit(f"Google login failed: {e}")

        threading.Thread(target=run_flow, daemon=True).start()

    # --- AUTO REFRESH TOKEN ---
    # Supabase access_token expires in 1 hour. We refresh every 50 mins.
    def _start_auto_refresh(self):
        if self._refresh_timer:
            self._refresh_timer.cancel()
        
        def refresh_loop():
            while self.session:
                time.sleep(50 * 60)  # 50 minutes
                try:
                    print("Refreshing token...")
                    res = supabase.auth.refresh_session()
                    self.session = res.session
                    print("Token refreshed")
                except Exception as e:
                    print(f"Refresh failed: {e}")
                    break
        
        self._refresh_timer = threading.Thread(target=refresh_loop, daemon=True)
        self._refresh_timer.start()

    def restore_session(self):
        """Call on app startup to stay logged in"""
        try:
            res = supabase.auth.get_session()
            if res:
                self.session = res
                self.user = res.user
                self._start_auto_refresh()
                return res.user
        except:
            pass
        return None

    # --- LOGOUT ---
    def logout(self):
        try:
            supabase.auth.sign_out()
        except:
            pass
        self.user = None
        self.session = None
        self.logged_out.emit()

    # --- DATABASE HELPERS (needs logged in user) ---
    def get_notes(self):
        if not self.user:
            return []
        res = supabase.table("notes").select("*").eq("user_id", self.user.id).order("created_at", desc=True).execute()
        return res.data

    def add_note(self, title, content):
        if not self.user:
            return None
        res = supabase.table("notes").insert({
            "user_id": self.user.id,
            "title": title,
            "content": content
        }).execute()
        return res.data

    def delete_note(self, note_id):
        supabase.table("notes").delete().eq("id", note_id).execute()
```

### 8. login_window.py

Modern login UI.

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from auth_manager import AuthManager

class LoginWindow(QWidget):
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth = auth_manager
        self.setWindowTitle("My App - Login")
        self.setFixedSize(360, 480)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.status = QLabel("")
        self.status.setStyleSheet("color: gray;")

        btn_login = QPushButton("Login")
        btn_create = QPushButton("Create Account")
        btn_google = QPushButton("Continue with Google")
        btn_google.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 8px;")

        btn_login.clicked.connect(self.do_login)
        btn_create.clicked.connect(self.do_create)
        btn_google.clicked.connect(self.do_google)

        self.auth.login_success.connect(self.on_success)
        self.auth.login_failed.connect(self.on_fail)

        layout.addWidget(title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(btn_login)
        layout.addWidget(btn_create)
        layout.addWidget(btn_google)
        layout.addWidget(self.status)
        layout.addStretch()

    def do_login(self):
        self.status.setText("Logging in...")
        self.auth.login_email(self.email_input.text(), self.pass_input.text())

    def do_create(self):
        self.status.setText("Creating account...")
        self.auth.create_account(self.email_input.text(), self.pass_input.text())

    def do_google(self):
        self.status.setText("Opening browser for Google login...")
        self.auth.login_google()

    def on_success(self, user):
        self.status.setText(f"Logged in as {user.email}")

    def on_fail(self, msg):
        QMessageBox.warning(self, "Auth Failed", msg)
        self.status.setText("Failed")
```

### 9. main_window.py

Your app after login.

```python
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QHBoxLayout, QLabel
from auth_manager import AuthManager

class MainWindow(QMainWindow):
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth = auth_manager
        self.setWindowTitle(f"My App - {self.auth.user.email}")
        self.setGeometry(100, 100, 600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QHBoxLayout()
        header.addWidget(QLabel(f"User: {self.auth.user.email}"))
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.do_logout)
        header.addWidget(btn_logout)
        layout.addLayout(header)

        self.note_list = QListWidget()
        layout.addWidget(self.note_list)

        input_row = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Note title")
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Content")
        btn_add = QPushButton("Add Note")
        btn_add.clicked.connect(self.add_note)
        
        input_row.addWidget(self.title_input)
        input_row.addWidget(self.content_input)
        input_row.addWidget(btn_add)
        layout.addLayout(input_row)

        self.load_notes()

    def load_notes(self):
        self.note_list.clear()
        notes = self.auth.get_notes()
        for n in notes:
            self.note_list.addItem(f"{n['title']} - {n['content']}")

    def add_note(self):
        title = self.title_input.text()
        content = self.content_input.text()
        if not title:
            return
        self.auth.add_note(title, content)
        self.title_input.clear()
        self.content_input.clear()
        self.load_notes()

    def do_logout(self):
        self.auth.logout()
```

### 10. app.py - Entry Point

```python
import sys
from PySide6.QtWidgets import QApplication
from auth_manager import AuthManager
from login_window import LoginWindow
from main_window import MainWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.auth = AuthManager()
        
        self.login_win = LoginWindow(self.auth)
        self.main_win = None

        self.auth.login_success.connect(self.show_main)
        self.auth.logged_out.connect(self.show_login)

        # Try to restore session on startup
        user = self.auth.restore_session()
        if user:
            self.show_main(user)
        else:
            self.login_win.show()

    def show_main(self, user):
        self.login_win.hide()
        self.main_win = MainWindow(self.auth)
        self.main_win.show()

    def show_login(self):
        if self.main_win:
            self.main_win.close()
        self.login_win.show()
        self.login_win.status.setText("Logged out")

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
```

### How Auto-Refresh Works

1. Supabase gives you an `access_token` (valid 1 hour) + `refresh_token` (valid forever until logout)
2. `_start_auto_refresh()` starts a background thread that calls `refresh_session()` every 50 mins
3. `restore_session()` on startup checks if a session is saved in local storage (Supabase Python SDK stores it in a file `.supabase` or memory) - so user stays logged in after closing app.

For production, save session to QSettings:

```python
from PySide6.QtCore import QSettings
settings = QSettings("MyCompany", "MyApp")
settings.setValue("refresh_token", session.refresh_token)
```

### Security Checklist for Your App

- [ ] NEVER commit `.env` to git
- [ ] Only use `anon` key in app, never `service_role`
- [ ] Enable RLS on ALL tables (see SQL above)
- [ ] In Supabase Dashboard > Auth > URL Configuration: set Site URL to `http://localhost:54321`

### Next Steps

1. Run: `python app.py`
2. Create account -> Check Supabase > Authentication > Users
3. Add notes -> Check Table Editor > notes

You now have a full offline+online desktop app.

---

Want a ZIP of this project? Tell me and I'll bundle it.
