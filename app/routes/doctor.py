from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models import Appointment, User, Exercise, DietTip, Treatment
from app import db
from datetime import date

doctor = Blueprint('doctor', __name__)

def doctor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'doctor']:
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# Patient dashboard (also accessible via /patient/)
@doctor.route('/patient-dashboard')
@login_required
def patient_dashboard_redirect():
    return redirect(url_for('patient.dashboard'))

@doctor.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    today = date.today()
    today_appts = Appointment.query.filter_by(preferred_date=today).order_by(
        Appointment.preferred_time
    ).all()
    upcoming = Appointment.query.filter(
        Appointment.preferred_date > today,
        Appointment.status.in_(['pending', 'confirmed'])
    ).order_by(Appointment.preferred_date.asc()).limit(10).all()
    stats = {
        'today': len(today_appts),
        'pending': Appointment.query.filter_by(status='pending').count(),
        'total_patients': User.query.filter_by(role='patient').count(),
        'completed': Appointment.query.filter_by(status='completed').count(),
    }
    return render_template('doctor/dashboard.html',
                           today_appts=today_appts,
                           upcoming=upcoming,
                           stats=stats,
                           config=current_app.config)

@doctor.route('/appointment/<int:appt_id>')
@login_required
@doctor_required
def appointment_detail(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    return render_template('doctor/appointment_detail.html', appt=appt, config=current_app.config)

@doctor.route('/appointment/<int:appt_id>/update', methods=['POST'])
@login_required
@doctor_required
def update_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = request.form.get('status', appt.status)
    appt.doctor_notes = request.form.get('doctor_notes', '')
    appt.video_link = request.form.get('video_link', '')
    db.session.commit()
    flash('Appointment updated.', 'success')
    return redirect(url_for('doctor.dashboard'))

@doctor.route('/add-exercise', methods=['GET', 'POST'])
@login_required
@doctor_required
def add_exercise():
    import json
    if request.method == 'POST':
        instructions_list = request.form.get('instructions', '').split('\n')
        instructions_list = [i.strip() for i in instructions_list if i.strip()]
        exercise = Exercise(
            title=request.form.get('title', ''),
            body_part=request.form.get('body_part', ''),
            difficulty=request.form.get('difficulty', 'beginner'),
            duration=request.form.get('duration', ''),
            description=request.form.get('description', ''),
            instructions=json.dumps(instructions_list),
            benefits=request.form.get('benefits', ''),
            precautions=request.form.get('precautions', ''),
            treatment_id=request.form.get('treatment_id') or None
        )
        db.session.add(exercise)
        db.session.commit()
        flash('Exercise added successfully.', 'success')
        return redirect(url_for('doctor.dashboard'))
    treatments = Treatment.query.filter_by(is_active=True).all()
    return render_template('doctor/add_exercise.html', treatments=treatments, config=current_app.config)
