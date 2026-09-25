# PySide6 / QtWidgets - Industry Standard Project Structures by App Level

> No code, just skeleton structures. This is how professional Qt teams organize projects as complexity grows.

---

### LEVEL 1: Basic App (Static, No DB, No API)
**Use for:** Calculators, converters, simple tools, tutorials, prototypes.
**Pattern:** Single window, no persistence except QSettings.

```
basic_app/
├── main.py
├── ui/
│   ├── main_window.ui         # Qt Designer file
│   └── main_window.py         # Logic for main window
├── resources/
│   ├── icons/
│   └── styles.qss             # Stylesheet
├── requirements.txt
└── README.md
```
**Key files:**
- `main.py` - QApplication entry
- `ui/` - All widgets, .ui files
- `resources/` - Icons, images, QSS

**What NOT to add:** No database folder, no api folder.

---

### LEVEL 2: App with Local Database (Offline CRUD)
**Use for:** Inventory, POS, personal expense tracker, library system. Data stays on user's PC.
**Pattern:** Qt SQL Model-View

```
local_db_app/
├── main.py
├── core/
│   ├── database.py            # Connection, init DB, migrations
│   └── config.py              # DB path, app constants
├── models/
│   └── tables.py              # Table definitions / dataclasses
├── ui/
│   ├── main_window.py
│   ├── dialogs/
│   │   ├── add_item_dialog.py
│   │   └── edit_item_dialog.py
│   └── widgets/
│       └── custom_table_view.py
├── data/
│   └── app.db                 # SQLite file (gitignored)
├── resources/
│   ├── icons/
│   └── styles.qss
└── requirements.txt
```
**Key additions from Level 1:**
- `core/database.py` - One place to create connection
- `models/` - What data looks like
- `data/` - Where SQLite file lives
- `ui/dialogs/` + `ui/widgets/` - Split as app grows

---

### LEVEL 3: App with Local DB + Settings + Files
**Use for:** Apps that need to save files, export PDF/Excel, remember window size, user preferences.
**Pattern:** Add persistence layer

```
local_plus_files_app/
├── main.py
├── core/
│   ├── database.py
│   ├── settings.py            # QSettings wrapper
│   ├── file_manager.py        # Import / Export / Save As logic
│   └── config.py
├── models/
│   └── tables.py
├── services/
│   └── export_service.py      # PDF, Excel, CSV export logic
├── ui/
│   ├── main_window.py
│   ├── dialogs/
│   └── widgets/
├── data/
│   ├── app.db
│   ├── exports/               # Generated files
│   └── backups/
├── resources/
│   ├── icons/
│   ├── styles.qss
│   └── templates/             # PDF / Excel templates
└── requirements.txt
```
**Key additions:**
- `core/settings.py` - Handles window geometry, theme, recent files
- `core/file_manager.py` - All file I/O in one place
- `services/` - Business logic separate from UI
- `data/exports/` - Output folder

---

### LEVEL 4: App with Remote API Only (No Local DB)
**Use for:** Weather app, stock tracker, dashboard that pulls from REST API.
**Pattern:** Singleton ApiClient + Service Layer (Industry standard QNetworkAccessManager)

```
api_only_app/
├── main.py
├── core/
│   ├── api_client.py          # SINGLE QNetworkAccessManager for whole app
│   ├── config.py              # BASE_URL, TIMEOUT
│   └── constants.py
├── models/
│   ├── api_models.py          # Dataclasses from API response
│   └── enums.py
├── services/
│   ├── auth_service.py        # If API needs token
│   └── data_service.py        # Fetch / create / update logic
├── ui/
│   ├── main_window.py
│   ├── widgets/
│   │   ├── loading_widget.py  # Spinner
│   │   └── error_widget.py    # Error + Retry button
│   └── dialogs/
├── utils/
│   ├── helpers.py             # Formatters, validators
│   └── logger.py
└── requirements.txt
```
**Key additions:**
- `core/api_client.py` - ONE instance, handles headers, auth token, retry, timeout
- `services/` - UI never calls api_client directly, only services
- `utils/` - Helper functions
- `ui/widgets/loading_widget.py` - For reloading states

**Critical rule:** No `data/` folder, no SQLite. Data lives online.

---

### LEVEL 5: App with Local DB + Remote API (Offline-First Sync)
**Use for:** The hardest mid-level app. Works offline, syncs when online. e.g., field sales app, clinic app in areas with poor internet.
**Pattern:** Repository Pattern

```
offline_first_app/
├── main.py
├── core/
│   ├── database.py            # Local SQLite
│   ├── api_client.py          # Remote API
│   ├── sync_manager.py        # THE CORE - decides local vs remote, queue
│   ├── network_monitor.py     # Detects online/offline (QNetworkInformation)
│   └── config.py
├── models/
│   ├── local_models.py
│   ├── api_models.py
│   └── sync_models.py         # Sync status: pending, synced, conflict
├── repositories/
│   ├── local_repository.py    # Talks ONLY to SQLite
│   ├── remote_repository.py   # Talks ONLY to API
│   └── repository.py          # Unified repo - UI calls this only
├── services/
│   ├── sync_service.py
│   └── conflict_service.py    # Handles conflicts (local vs remote)
├── ui/
│   ├── main_window.py
│   ├── widgets/
│   │   ├── sync_status_widget.py # Shows "Offline - 5 pending sync"
│   │   └── loading_widget.py
│   └── dialogs/
├── data/
│   ├── app.db
│   └── sync_queue.db          # Queue of unsynced changes
└── requirements.txt
```
**Key additions:**
- `repositories/` - This is the industry pattern for offline-first. UI doesn't know if data is local or remote
- `core/sync_manager.py` - Queues changes when offline
- `core/network_monitor.py` - Listens to internet on/off
- `data/sync_queue.db` - Separate queue

**This is where most junior devs fail - they mix local and remote calls in UI.**

---

### LEVEL 6: App with Auth + Online Database (SaaS App)
**Use for:** Notes app with login, multi-user app, subscription app. Data per user. (Your Supabase / Firebase level)
**Pattern:** Auth + RLS

```
saas_app/
├── main.py
├── app_controller.py          # Decides: show login or main window
├── core/
│   ├── supabase_client.py     # OR firebase_client.py - ONE client
│   ├── database.py            # Optional local cache
│   ├── auth_manager.py        # create_account, login, google, refresh, logout
│   ├── api_client.py          # For other 3rd party APIs
│   ├── config.py
│   └── constants.py
├── models/
│   ├── user_model.py
│   ├── app_models.py
│   └── enums.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── subscription_service.py
├── repositories/
│   ├── user_repository.py
│   └── notes_repository.py
├── ui/
│   ├── login_window.py
│   ├── main_window.py
│   ├── onboarding/
│   │   └── welcome_window.py
│   ├── widgets/
│   │   ├── user_profile_widget.py
│   │   └── subscription_banner.py
│   └── dialogs/
│       └── settings_dialog.py
├── utils/
│   ├── validators.py
│   ├── logger.py
│   └── security.py            # Token storage (QSettings / keyring)
├── data/
│   └── cache/                 # Local cache of online data
├── resources/
│   ├── icons/
│   ├── styles.qss
│   └── images/
├── .env                       # SUPABASE_URL, ANON_KEY (gitignored)
└── requirements.txt
```
**Key additions:**
- `app_controller.py` - Controls auth flow: restore session -> main, else login
- `core/auth_manager.py` - All auth in one place
- `utils/security.py` - Securely store refresh_token (never in plain text)
- `ui/login_window.py` + `onboarding/` - Separate auth UI
- `.env` - Secrets

---

### LEVEL 7: Full Production App (Everything)
**Use for:** Apps you sell, apps with teams, apps that need auto-update, crash reporting, background jobs.
**Pattern:** Clean Architecture + CI/CD

```
production_app/
├── main.py
├── app_controller.py
├── core/
│   ├── database.py
│   ├── supabase_client.py
│   ├── api_client.py
│   ├── sync_manager.py
│   ├── auth_manager.py
│   ├── thread_pool.py         # QThreadPool manager
│   ├── worker.py              # QRunnable base class
│   ├── config.py
│   ├── constants.py
│   └── env.py                 # Env loader (dev / prod)
├── models/
│   ├── user_model.py
│   ├── domain_models.py
│   ├── api_models.py
│   └── dto.py                 # Data Transfer Objects
├── repositories/
│   ├── base_repository.py
│   ├── local_repository.py
│   ├── remote_repository.py
│   └── cached_repository.py   # Local + Remote combined
├── services/
│   ├── auth_service.py
│   ├── sync_service.py
│   ├── export_service.py
│   ├── notification_service.py
│   ├── updater_service.py     # Checks for new versions
│   └── analytics_service.py   # PostHog / Mixpanel
├── workers/
│   ├── sync_worker.py         # Background sync
│   ├── export_worker.py       # Heavy export in background
│   └── api_worker.py
├── ui/
│   ├── main_window.py
│   ├── login_window.py
│   ├── viewmodels/            # MVVM pattern - ViewModels
│   │   ├── main_viewmodel.py
│   │   └── login_viewmodel.py
│   ├── views/
│   │   ├── main_view.py
│   │   └── login_view.py
│   ├── widgets/
│   │   ├── custom/
│   │   │   ├── loading_overlay.py
│   │   │   ├── error_banner.py
│   │   │   └── sync_indicator.py
│   │   └── common/
│   ├── dialogs/
│   ├── themes/
│   │   ├── light.qss
│   │   └── dark.qss
│   └── assets/
├── utils/
│   ├── logger.py              # File logger + Sentry
│   ├── validators.py
│   ├── formatters.py
│   ├── security.py
│   ├── crash_reporter.py
│   └── helpers.py
├── data/
│   ├── app.db
│   ├── cache/
│   ├── logs/
│   │   └── app.log
│   └── backups/
├── tests/
│   ├── unit/
│   │   ├── test_auth.py
│   │   └── test_api_client.py
│   ├── integration/
│   └── ui/
├── scripts/
│   ├── build.py               # PyInstaller build script
│   ├── deploy.py
│   └── migrations/
├── resources/
│   ├── icons/
│   ├── images/
│   └── fonts/
├── docs/
│   ├── architecture.md
│   └── api.md
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt       # pytest, black, flake8
├── pyproject.toml            # Tool configs
├── installer/
│   ├── installer.iss          # Inno Setup for Windows
│   └── entitlements.plist     # macOS
└── README.md
```
**Key additions from all previous levels:**
- `workers/` + `core/thread_pool.py` - Heavy work never blocks UI
- `ui/viewmodels/` - MVVM for testable UI
- `tests/` - Unit + integration + UI tests
- `utils/crash_reporter.py` - Sentry / BugSnag
- `services/updater_service.py` - Auto-update via GitHub releases
- `scripts/build.py` + `installer/` - Builds .exe / .dmg
- `docs/` - Architecture docs
- `pyproject.toml` - Black, isort, mypy configs

---

### How to Choose Your Level

| You are building... | Use Level |
| :--- | :--- |
| Calculator, QR generator | 1 |
| Shop inventory that works without internet | 2 |
| Inventory that exports PDF | 3 |
| Weather / Crypto price tracker | 4 |
| Sales app that works in the village without network, syncs in town | 5 |
| Notes app with Google login, each user sees own data | 6 |
| App you will sell / put on website for download | 7 |

### Migration Path (How apps grow)

```
Level 1 -> Level 2: Add core/database.py + models/
Level 2 -> Level 3: Add core/settings.py + services/export_service.py
Level 3 -> Level 4: Replace database.py with api_client.py (or keep both for Level 5)
Level 4 -> Level 5: Add repositories/ layer + sync_manager
Level 5 -> Level 6: Add auth_manager + app_controller
Level 6 -> Level 7: Add workers/, tests/, installer/, viewmodels/
```

**Golden Rule:** Never jump from Level 1 to Level 7. Add one layer at a time.

---
*All structures follow Qt Company's recommended practices and common open-source Qt projects (qBittorrent, VirtualBox UI, etc.)*
