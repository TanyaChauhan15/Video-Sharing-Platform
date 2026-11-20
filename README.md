# Frameflow — Full-Stack Video Sharing Platform

A YouTube-inspired video sharing application with a **React + Vite + Tailwind** frontend and **Django + Django REST Framework + SQLite** backend. This is real local storage and real HTTP APIs, not mock frontend data.

## Features

- Registration, login, JWT access/refresh tokens, editable profile, logout and protected routes
- Upload local MP4/WebM/OGG videos (up to 200 MB) and optional thumbnails (up to 5 MB)
- HTML5 player with native play/pause, volume, seek, fullscreen and playback speed (browser dependent)
- Video view counts, title/description/creator, search suggestions and search results
- Comments with own-comment deletion, likes/unlikes with uniqueness constraints
- Watch Later with add/remove and dedicated page; category filtering and category pages
- Creator dashboard, profile, dark/light mode, responsive layout and collapsible sidebar
- Django admin, seed command, API tests and database migrations

## Technology

Frontend: React 18, Vite 6, JavaScript/JSX, Tailwind CSS 3, React Router 6, Axios, Lucide React.

Backend: Python 3.10+, Django 5.2, DRF, SimpleJWT, django-cors-headers, Pillow, SQLite, local Django media storage.

## Folder structure

```text
video-sharing-platform/
  backend/
    accounts/          # user serializers, authentication and profile endpoints
    videos/            # models, serializers, views, urls, tests, seed command
      migrations/      # initial schema migration
      management/commands/seed_demo.py
    config/            # settings, urls, WSGI/ASGI
    media/             # locally uploaded video and thumbnail files
    manage.py
    requirements.txt
  frontend/
    src/components/    # layout and video cards
    src/context/       # JWT auth state
    src/pages/         # 10 application pages
    src/api.js         # Axios client and token refresh
    package.json
    vite.config.js
    tailwind.config.js
  .env.example
  .gitignore
  README.md
```

## Windows setup in VS Code

**Prerequisites:** Install Python 3.10+ and Node.js 20+ (includes npm). Optional: install FFmpeg and add it to PATH to generate playable demo clips. Open the extracted `video-sharing-platform` folder in VS Code, then open **Terminal → New Terminal** (PowerShell).

**Terminal 1 — backend:**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:8000
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` and retry, or skip activation and use `.\.venv\Scripts\python.exe` in place of `python` for each command.

**Terminal 2 — frontend:** (from the project root)

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Open **http://localhost:5173**. Django API: **http://127.0.0.1:8000/api/**. Admin: **http://127.0.0.1:8000/admin/** (create admin with `python manage.py createsuperuser`). Both terminals must stay open. For production use, configure secure secrets, HTTPS, file validation, media hosting and hardened deployment settings.

### Demo accounts

After `python manage.py seed_demo`:

- Username: `demo` / Password: `DemoPass123!`
- Username: `creator` / Password: `DemoPass123!`

Seed creates six categories and, **when FFmpeg is installed**, six locally generated playable 4-second MP4 clips, sample comments, likes and a Watch Later item. If FFmpeg is unavailable, it still creates categories/users; upload your own MP4/WebM through **Upload video**. No external video links are required. Run `seed_demo` repeatedly without duplicating existing records. Do not use demo credentials outside local development.

## API reference

All paths are relative to `http://127.0.0.1:8000`. Protected requests require `Authorization: Bearer <access_token>`.

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Register username/password/email | No |
| POST | `/api/auth/login/` | Obtain JWT access and refresh | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| GET, PATCH | `/api/auth/profile/` | Read/update profile | Yes |
| GET | `/api/videos/` | Latest videos; optional `?category=technology` | No |
| GET | `/api/videos/{id}/` | Video details | No |
| POST | `/api/videos/upload/` | Multipart video upload | Yes |
| GET | `/api/videos/search/?q=...` | Search title/description/category | No |
| GET | `/api/videos/my-videos/` | User uploads | Yes |
| POST | `/api/videos/{id}/view/` | Increment views | No |
| GET, POST | `/api/videos/{id}/comments/` | List/post comments | POST yes |
| DELETE | `/api/comments/{id}/` | Delete own comment | Yes |
| POST | `/api/videos/{id}/like/` | Toggle like | Yes |
| GET | `/api/watch-later/` | Saved videos | Yes |
| POST | `/api/watch-later/add/` | Save `{ "video_id": 1 }` | Yes |
| DELETE | `/api/watch-later/{id}/` | Remove by WatchLater record ID | Yes |
| GET | `/api/categories/` | List categories | No |
| GET | `/api/categories/{id}/videos/` | Category videos | No |

List endpoints are paginated except categories and comments. Frontend reads the `results` array and currently displays the first page (18 items) rather than an infinite scroll.

## Test and build

From backend terminal (venv active):

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

From frontend terminal:

```powershell
npm run build
```

Manual smoke test: log in as demo; browse videos; play a clip; search Technology; open category; post/delete comment; like/unlike; add/remove Watch Later; upload a local MP4; check Profile and Dashboard.

## Troubleshooting

- **CORS/network errors:** Django must run on port 8000; Vite on 5173. Ensure `frontend/.env` contains `VITE_API_URL=http://127.0.0.1:8000/api` and restart Vite.
- **Empty home page:** run `python manage.py seed_demo` with FFmpeg available, or upload your own video. Categories always seed.
- **Media not playing:** confirm file is a browser-supported codec (H.264 MP4 or VP8/VP9 WebM recommended); extension alone does not guarantee playable codec. Django serves media only with `DEBUG=1` for local development.
- **401 unauthorized:** sign in again; access tokens expire after 30 minutes, and refresh tokens after seven days.
- **Missing tables:** run `python manage.py migrate`.
- **npm install errors:** install Node.js 20+ and retry `npm install`.
- **PowerShell script execution blocked:** use the execution policy workaround above.
- **Large uploads:** application validation limits videos to 200 MB; production servers need additional upload settings and secure media handling.

## Security/deployment notes

This is a local interview/demo application, **not a production-hardened YouTube clone**. It uses Django's built-in User model, SQLite and filesystem media. JWT refresh tokens are stored in localStorage for simplicity (XSS-sensitive); production should use a safer token strategy, HTTPS, rate limiting, MIME/content scanning, upload transcoding, view deduplication and proper media/CDN infrastructure. Views count every play-page visit, not unique viewers. No recommendation algorithm, subscriptions, streaming transcoding, background jobs or video moderation is implemented.
