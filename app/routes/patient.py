from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Appointment, Exercise, DietTip, ChatHistory
from app import db

patient = Blueprint('patient', __name__)

@patient.route('/dashboard')
@login_required
def dashboard():
    if current_user.role in ['admin', 'doctor']:
        return redirect(url_for('admin.dashboard'))
    my_appointments = Appointment.query.filter_by(
        user_id=current_user.id
    ).order_by(Appointment.preferred_date.desc()).all()
    chat_histories = ChatHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatHistory.updated_at.desc()).limit(5).all()
    return render_template('patient/dashboard.html',
                           appointments=my_appointments,
                           chat_histories=chat_histories,
                           config=current_app.config)
