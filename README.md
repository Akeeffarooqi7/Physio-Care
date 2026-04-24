# PhysioCare Clinic Website

A full-featured physiotherapy clinic website built with Flask, featuring appointment booking, patient/doctor dashboards, an AI chatbot, exercise & diet recommendations, and an admin panel.


## 🌐 Live Preview
https://physio-care-production.up.railway.app/


![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

### Public
- Responsive homepage with hero section, featured treatments, testimonials, and clinic stats
- 8 treatment categories with detailed pages (symptoms, approach, recovery time)
- Health guidance page with exercises and diet tips
- Contact form with email, phone, and WhatsApp support
- AI-powered **PhysioBot** chatbot covering 10+ conditions
- Dark / light theme toggle

### Appointment Booking
- 30-day availability calendar (Sundays excluded)
- 14 time slots per day (9 AM - 5 PM) with real-time availability checking
- Admin controls to block dates/slots and toggle bookings on or off

### Patient Portal
- Registration, login, and profile management
- View appointment history and past chat sessions

### Doctor Dashboard
- Today's and upcoming appointments (10-day view)
- Appointment detail view with notes and status updates
- Add exercises for patients

### Admin Panel
- CRUD management for treatments, testimonials, exercises, and diet tips
- Appointment management with status filters
- Contact message inbox with reply system
- User management and clinic settings
- Chat history viewer

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask, SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate |
| Frontend | Jinja2, Bootstrap 5, Font Awesome, AOS animations |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | Bcrypt password hashing, role-based access (admin/doctor/patient) |
| Server | Gunicorn |

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/physio_website.git
cd physio_website

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app (seeds the database on first run)
python run.py
```

The app will be available at **http://localhost:5000**.

### Default Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@physiocare.com | admin123 |
| Doctor | doctor@physiocare.com | doctor123 |
| Patient | patient@demo.com | patient123 |

## Configuration

Configuration lives in `config.py`. Key settings can be overridden with environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | dev key (override in production) |
| `DATABASE_URL` | PostgreSQL connection string | SQLite (`physio.db`) |
| `MAIL_SERVER` | SMTP server | smtp.gmail.com |
| `MAIL_PORT` | SMTP port | 587 |
| `MAIL_USERNAME` | Email account | - |
| `MAIL_PASSWORD` | Email password | - |

## Project Structure

```
physio_website/
├── run.py                  # Entry point & database seeding
├── config.py               # App configuration
├── Procfile                # Heroku deployment
├── requirements.txt
└── app/
    ├── __init__.py         # App factory
    ├── models.py           # 10 database models
    ├── routes/
    │   ├── main.py         # Public pages
    │   ├── auth.py         # Authentication
    │   ├── appointments.py # Booking system
    │   ├── api.py          # Chatbot & contact API
    │   ├── admin.py        # Admin dashboard
    │   ├── doctor.py       # Doctor panel
    │   └── patient.py      # Patient dashboard
    ├── templates/          # Jinja2 templates
    └── static/
        ├── css/style.css   # Custom styling
        ├── js/             # Main, chatbot & theme scripts
        └── images/
```

## Deployment

The app is configured for **Heroku** deployment out of the box:

```bash
heroku create
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set DATABASE_URL=<your-postgres-url>
git push heroku main
```

## License

This project is licensed under the MIT License.
