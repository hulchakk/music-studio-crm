# Music Studio CRM

A Django-based CRM platform for managing music school operations: students, teachers, lessons, and schedules.

Solves the problem of coordinating complex lesson schedules, tracking student progress, and managing subscription billing for music schools.

## Tech Stack

| Tech | Why |
|------|-----|
| Django | Rapid development, built-in admin panel, proven ORM |
| Python | Readable code, rich ecosystem for data handling |
| SQLite | Zero-config database suitable for initial deployment |
| Bootstrap | Quick, responsive UI without custom CSS overhead |
| Telegram API | Real-time notifications for schedule updates |

## Getting Started

```bash
git clone https://github.com/hulchakk/music-studio-crm.git
cd music-studio-crm
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo 'TELEGRAM_BOT_TOKEN=your_token_here' > .env
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver
```

Visit http://localhost:8000 (app) or http://localhost:8000/admin (admin panel).

**Demo:** https://music-studio-crm.onrender.com/ (admin / admin)

## Features

**Admin Dashboard:**
- Full control over subscriptions, students, teachers, and lessons
- Automated schedule generation and filtering (by teacher, student, room, date)
- Subscription history tracking

**Student & Teacher Views:**
- Real-time schedule notifications via Telegram
- Personalized schedule views
- Lesson notes

## Key Decisions

- **SQLite for MVP:** Fast iteration without database setup; upgrade to PostgreSQL when scaling beyond single-instance deployment
- **Telegram notifications:** Chosen for instant reach; user base already on Telegram; not tied to email infrastructure
- **Automatic schedule generation:** Reduces manual entry errors; stored once, modified as needed

## Status

Live at https://music-studio-crm.onrender.com/. Next: role-based permissions UI, student payment history dashboard.
