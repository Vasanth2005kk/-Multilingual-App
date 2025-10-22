# Multilingual Web Application - Setup Guide

## Project Structure

```
multilingual-app/
├── backend/
│   ├── app.py                 # Flask app with API and database
│   ├── translations.db        # SQLite database (auto-generated)
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── main.js           # Vue app entry point
│   │   ├── App.vue           # Root component
│   │   ├── pages/
│   │   │   ├── Home.vue      # Home page
│   │   │   ├── About.vue     # About page
│   │   │   ├── Contact.vue   # Contact page
│   │   │   ├── Settings.vue  # Settings page
│   │   │   └── Profile.vue   # Profile page
│   │   └── index.html        # HTML template
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── .env                  # Environment variables
```

---

## Backend Setup (Flask)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Create `requirements.txt`:
```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
```

Then install:
```bash
pip install -r requirements.txt
```

### 4. Run Flask Server
```bash
python app.py
```

The backend will start on `http://localhost:5000`

**API Endpoints:**
- `GET /api/health` - Health check
- `GET /api/languages` - List available languages
- `GET /api/translations/<lang>` - Get translations for a specific language (e.g., `/api/translations/en`, `/api/translations/ta`)

---

## Frontend Setup (Vue.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### 4. Build for Production
```bash
npm run build
```

Output will be in the `dist/` folder.

---

## Running the Complete Application

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` in your browser.

---

## Key Features Explained

### 1. Multilingual Translation System

**Database Schema:**
```sql
CREATE TABLE translation (
  id INTEGER PRIMARY KEY,
  key VARCHAR(255) NOT NULL,
  lang VARCHAR(10) NOT NULL,
  value TEXT NOT NULL,
  UNIQUE(key, lang)
)
```

Example entries:
```
id | key           | lang | value
1  | navbar.home   | en   | Home
2  | navbar.home   | ta   | முகப்பு
3  | navbar.about  | en   | About
4  | navbar.about  | ta   | பற்றி
```

### 2. Flask API Response Format

**Request:** `GET /api/translations/en`

**Response:**
```json
{
  "navbar": {
    "home": "Home",
    "about": "About",
    "contact": "Contact",
    "settings": "Settings",
    "profile": "Profile"
  },
  "home": {
    "title": "Welcome to Multilingual App",
    "subtitle": "Switch between English and Tamil effortlessly",
    "description": "This application demonstrates..."
  },
  ...
}
```

### 3. Vue.js i18n Integration

**In Components:**
```vue
<h1>{{ $t('home.title') }}</h1>
```

**Language Switching:**
```javascript
// In Settings.vue
this.$loadTranslations('ta')  // Switches to Tamil
```

The `$loadTranslations` function:
- Fetches translations from Flask API
- Updates `vue-i18n` locale messages
- Persists language preference in localStorage
- Updates all translated text immediately (no page reload)

### 4. Responsive Design

All pages use modern CSS with:
- Gradient backgrounds
- Smooth animations and transitions
- Mobile-friendly layouts
- Flexbox and media queries for responsiveness

---

## Adding More Languages

### 1. Add Translations to Database

In `app.py`, add new translations to the `init_db()` function:

```python
Translation(key='navbar.home', lang='es', value='Inicio'),
Translation(key='home.title', lang='es', value='Bienvenido a la Aplicación Multilingüe'),
# ... more Spanish translations
```

### 2. Update Settings Page

Modify `pages/Settings.vue` to include the new language option:

```vue
<option value="es">{{ $t('settings.spanish') }}</option>
```

Add the translation:
```python
Translation(key='settings.spanish', lang='en', value='Spanish'),
Translation(key='settings.spanish', lang='ta', value='ஸ்பானிய'),
```

---

## Troubleshooting

### CORS Errors
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that both backend and frontend are running
- Verify the proxy configuration in `vite.config.js`

### Translations Not Loading
- Check browser console for fetch errors
- Verify Flask server is running on `http://localhost:5000`
- Ensure the language code matches database entries (en, ta, etc.)

### Database Issues
- Delete `translations.db` to reset the database
- Run `python app.py` again to reinitialize

### Vite Build Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Ensure Node.js version 16+ is installed

---

## Environment Variables

Create `.env` file in the frontend directory:
```
VITE_API_BASE_URL=http://localhost:5000
```

Update `main.js` to use it:
```javascript
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
const response = await fetch(`${apiBase}/api/translations/${locale}`)
```

---

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

### Serve with Flask

Modify `app.py`:
```python
from flask import send_from_directory

@app.route('/')
def serve():
    return send_from_directory('path/to/frontend/dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('path/to/frontend/dist', path)
```

### Deploy

Use platforms like Heroku, Vercel, or AWS:
- Backend: Deploy Flask app
- Frontend: Deploy `dist/` folder or serve via Flask

---

## Testing the Application

1. Navigate to Home page - displays welcome message in selected language
2. Click Settings - change language from English to Tamil
3. Check all pages update instantly (navbar, titles, labels)
4. Verify localStorage saves language preference
5. Refresh page - language preference persists
6. Navigate between pages - all content is translated

---

## API Reference

### GET /api/health
Returns server status.

**Response:** `{ "status": "OK" }`

---

### GET /api/languages
Returns list of available languages.

**Response:** `{ "languages": ["en", "ta"] }`

---

### GET /api/translations/<lang>
Returns all translations for a language.

**Parameters:**
- `lang` (string): Language code (en, ta, etc.)

**Response:** Nested object with translations

**Example:** `GET /api/translations/ta`
```json
{
  "navbar": { "home": "முகப்பு", ... },
  "home": { "title": "...", ... }
}
```

---

## License

MIT License - Feel free to use this project for personal or commercial purposes.