![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

My first Django portfolio project - CRM platform designed for music school management.

https://music-studio-crm.onrender.com/

user: admin
password: admin

## Features:

- ### Administrative Management (Superuser):
    - Comprehensive control over subscriptions, students, teachers, and lessons
    - Automated schedule generation
    - Streamlined dashboard for general information overview
    - Access to detailed subscription history
    - Schedule filtering by teacher, student, room, and date

- ### User System:
    - Real-time schedule update notifications via Telegram API
    - Personalized schedule views for individual users
    - Lesson-specific note-taking functionality



## 📋 How to run this project

### 1. Download the project:
```bash
git clone https://github.com/hulchakk/music-studio-crm.git
cd music-studio-crm
```

### 2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements:
```bash
pip install -r requirements.txt
```

### 4. Set up database:
```bash
TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
#The project will work even without a token
#just make sure to set up your .env file.
```

### 5. Create .env file:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user:
```bash
python manage.py createsuperuser
```

### 7. Load test data (Optional):
```bash
python manage.py loaddata test_data.json
```

### 8. Run the server:
```bash
python manage.py runserver
```

### 9. Open in browser:
- Main website: http://127.0.0.1:8000/
- Django admin panel: http://127.0.0.1:8000/admin/
