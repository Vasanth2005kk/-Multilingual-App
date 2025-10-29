# Multilingual Web Application - Setup Guide

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


## License

MIT License - Feel free to use this project for personal or commercial purposes.
