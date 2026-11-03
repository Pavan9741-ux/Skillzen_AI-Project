# 🚀 SkillZen AI v2.0 - Complete Installation Guide

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## 🔧 Installation Steps

### 1. Create Project Directory

```bash
# Navigate to your desired location
cd Desktop

# Create project folder
mkdir skillzen-ai
cd skillzen-ai
```

### 2. Create Folder Structure

```bash
# Create all directories
mkdir -p app static/css static/js static/images static/uploads/avatars templates migrations
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
# Install all required packages
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-CORS==4.0.0 Flask-Login==0.6.3 Werkzeug==3.0.1 scikit-learn==1.3.2 numpy==1.26.2 pandas==1.5.3 scipy==1.11.4 nltk==3.8.1 email-validator==2.1.0 python-dotenv==1.0.0 gunicorn==21.2.0 python-dateutil==2.8.2 Pillow==10.1.0

# Optional: Install BERT for advanced AI (requires ~500MB)
pip install sentence-transformers==2.2.2 torch==2.1.0 transformers==4.35.0
```

### 5. Create All Files

Copy all the code from the previous messages into the respective files:

#### Backend Files:
- `app/__init__.py`
- `app/models.py`
- `app/routes.py`
- `app/ai_engine.py`
- `app/ai_engine_advanced.py`
- `app/analytics.py`

#### CSS Files:
- `static/css/main.css`
- `static/css/glassmorphism.css`
- `static/css/animations.css`
- `static/css/themes.css`
- `static/css/profile.css`
- `static/css/dashboard.css`

#### JavaScript Files:
- `static/js/main.js`
- `static/js/api.js`
- `static/js/theme.js`
- `static/js/theme-manager.js`
- `static/js/charts.js`
- `static/js/dashboard.js`
- `static/js/profile.js`

#### Templates:
- `templates/base.html`
- `templates/index.html`
- `templates/student.html`
- `templates/admin.html`
- `templates/dashboard.html`
- `templates/profile.html`
- `templates/skill-trends.html`
- `templates/learning-paths.html`
- `templates/applications.html`

#### Root Files:
- `.env`
- `.gitignore`
- `requirements.txt`
- `run.py`
- `seed_data.py`
- `seed_advanced.py`

### 6. Configure Environment

Create `.env` file:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production-12345
DATABASE_URL=sqlite:///skillzen.db
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

### 7. Initialize Database

```bash
# Seed basic data (companies + admin)
python seed_data.py

# Seed advanced data (skill trends, learning paths, analytics, demo students)
python seed_advanced.py
```

Expected output: