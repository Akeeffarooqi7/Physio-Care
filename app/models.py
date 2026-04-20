from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='patient')  # admin, doctor, patient
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(256))
    medical_history = db.Column(db.Text)
    profile_image = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic',
                                   foreign_keys='Appointment.user_id')
    chat_histories = db.relationship('ChatHistory', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<User {self.username}>'


class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(64))
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    approach = db.Column(db.Text)
    recovery_time = db.Column(db.String(64))
    icon = db.Column(db.String(64))
    color = db.Column(db.String(32), default='#2563eb')
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exercises = db.relationship('Exercise', backref='treatment', lazy='dynamic')
    diet_tips = db.relationship('DietTip', backref='treatment', lazy='dynamic')

    def __repr__(self):
        return f'<Treatment {self.name}>'


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body_part = db.Column(db.String(64))
    difficulty = db.Column(db.String(32), default='beginner')
    duration = db.Column(db.String(32))
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)  # JSON array
    benefits = db.Column(db.Text)
    precautions = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    video_url = db.Column(db.String(256))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_instructions(self):
        try:
            return json.loads(self.instructions) if self.instructions else []
        except:
            return []

    def __repr__(self):
        return f'<Exercise {self.title}>'


class DietTip(db.Model):
    __tablename__ = 'diet_tips'
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(64))
    food_item = db.Column(db.String(128))
    category = db.Column(db.String(64))  # vitamins, protein, anti-inflammatory, etc.
    benefit = db.Column(db.Text)
    tips = db.Column(db.Text)
    icon = db.Column(db.String(64))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<DietTip {self.food_item}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    symptoms = db.Column(db.Text)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    appointment_type = db.Column(db.String(32), default='in-person')  # in-person, video
    doctor_notes = db.Column(db.Text)
    video_link = db.Column(db.String(256))
    reminder_sent = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.patient_name} on {self.preferred_date}>'


class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(128), nullable=False)
    condition = db.Column(db.String(128))
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    recovery_story = db.Column(db.Text)
    occupation = db.Column(db.String(64))
    avatar_color = db.Column(db.String(32), default='#2563eb')
    is_approved = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.patient_name}>'


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(256))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    reply_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'


class ChatHistory(db.Model):
    __tablename__ = 'chat_histories'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    messages = db.Column(db.Text)  # JSON array of {role, content, timestamp}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_messages(self):
        try:
            return json.loads(self.messages) if self.messages else []
        except:
            return []

    def add_message(self, role, content):
        msgs = self.get_messages()
        msgs.append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        })
        self.messages = json.dumps(msgs)
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f'<ChatHistory session={self.session_id}>'


class ClinicSettings(db.Model):
    """Single-row table for clinic-wide settings (appointment availability, etc.)."""
    __tablename__ = 'clinic_settings'
    id = db.Column(db.Integer, primary_key=True)
    bookings_enabled = db.Column(db.Boolean, default=True)
    bookings_disabled_message = db.Column(db.Text,
        default='Appointments are temporarily unavailable. Please call us or check back later.')
    blocked_dates = db.Column(db.Text, default='[]')   # JSON array of "YYYY-MM-DD"
    blocked_slots = db.Column(db.Text, default='{}')   # JSON dict {"YYYY-MM-DD": ["09:00 AM", ...]}
    auto_disable_full = db.Column(db.Boolean, default=True)  # auto-disable when all slots booked
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(120))

    def get_blocked_dates(self):
        try:
            return json.loads(self.blocked_dates) if self.blocked_dates else []
        except Exception:
            return []

    def set_blocked_dates(self, dates_list):
        self.blocked_dates = json.dumps(sorted(set(dates_list)))

    def get_blocked_slots(self):
        try:
            return json.loads(self.blocked_slots) if self.blocked_slots else {}
        except Exception:
            return {}

    def get_blocked_slots_for_date(self, date_str):
        return self.get_blocked_slots().get(date_str, [])

    def block_slot(self, date_str, time_str):
        slots = self.get_blocked_slots()
        if date_str not in slots:
            slots[date_str] = []
        if time_str not in slots[date_str]:
            slots[date_str].append(time_str)
        self.blocked_slots = json.dumps(slots)

    def unblock_slot(self, date_str, time_str):
        slots = self.get_blocked_slots()
        if date_str in slots and time_str in slots[date_str]:
            slots[date_str].remove(time_str)
            if not slots[date_str]:
                del slots[date_str]
        self.blocked_slots = json.dumps(slots)

    @staticmethod
    def get():
        """Return the singleton settings row, creating it if absent."""
        row = ClinicSettings.query.first()
        if not row:
            row = ClinicSettings()
            db.session.add(row)
            db.session.commit()
        return row

    def __repr__(self):
        return f'<ClinicSettings bookings_enabled={self.bookings_enabled}>'


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text)
    category = db.Column(db.String(64))
    tags = db.Column(db.String(256))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
