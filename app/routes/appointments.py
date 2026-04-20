from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user
from app.models import Appointment, ClinicSettings
from app import db
from datetime import datetime, date, timedelta

appointments = Blueprint('appointments', __name__)

TIME_SLOTS = [
    '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
    '11:00 AM', '11:30 AM', '12:00 PM', '02:00 PM',
    '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM',
    '04:30 PM', '05:00 PM'
]


def _is_date_blocked(d):
    """Check if a specific date is blocked via admin settings."""
    settings = ClinicSettings.get()
    return d.strftime('%Y-%m-%d') in settings.get_blocked_dates()


def _is_date_full(d):
    """Check if all slots for a date are booked."""
    booked_count = Appointment.query.filter(
        Appointment.preferred_date == d,
        Appointment.status.in_(['pending', 'confirmed'])
    ).count()
    return booked_count >= len(TIME_SLOTS)


@appointments.route('/book', methods=['GET', 'POST'])
def book():
    settings = ClinicSettings.get()

    # ── Global kill switch: bookings disabled by admin ──
    if not settings.bookings_enabled:
        return render_template('appointments_closed.html',
                               message=settings.bookings_disabled_message,
                               config=current_app.config)

    if request.method == 'POST':
        # Re-check: admin might have disabled between page load and submit
        if not settings.bookings_enabled:
            flash('Appointments have been temporarily disabled. Please try again later.', 'warning')
            return redirect(url_for('appointments.book'))

        patient_name = request.form.get('patient_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        symptoms = request.form.get('symptoms', '').strip()
        preferred_date_str = request.form.get('preferred_date', '')
        preferred_time = request.form.get('preferred_time', '')
        appointment_type = request.form.get('appointment_type', 'in-person')

        if not all([patient_name, email, phone, preferred_date_str, preferred_time]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('appointments.book'))

        try:
            preferred_date = datetime.strptime(preferred_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('appointments.book'))

        if preferred_date < date.today():
            flash('Please select a future date.', 'danger')
            return redirect(url_for('appointments.book'))

        # ── Check if this specific date is blocked by admin ──
        if _is_date_blocked(preferred_date):
            flash('Sorry, the selected date is not available for appointments. Please choose a different date.', 'warning')
            return redirect(url_for('appointments.book'))

        # ── Check if all slots are full for this date ──
        if _is_date_full(preferred_date):
            flash('All time slots for this date are fully booked. Please select another date.', 'warning')
            return redirect(url_for('appointments.book'))

        # ── Check if this specific slot is admin-blocked ──
        admin_blocked_slots = settings.get_blocked_slots_for_date(preferred_date.strftime('%Y-%m-%d'))
        if preferred_time in admin_blocked_slots:
            flash('Sorry, that time slot is not available. Please choose a different time.', 'warning')
            return redirect(url_for('appointments.book'))

        # ── Check specific slot availability (patient bookings) ──
        existing = Appointment.query.filter(
            Appointment.preferred_date == preferred_date,
            Appointment.preferred_time == preferred_time,
            Appointment.status.in_(['pending', 'confirmed'])
        ).first()
        if existing:
            flash('Sorry, the selected time slot was just taken. Please choose another available slot.', 'warning')
            return redirect(url_for('appointments.book'))

        appointment = Appointment(
            patient_name=patient_name,
            email=email,
            phone=phone,
            symptoms=symptoms,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            appointment_type=appointment_type,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(appointment)
        db.session.commit()

        # ── Auto-disable bookings if the whole day is now full ──
        if settings.auto_disable_full and _is_date_full(preferred_date):
            # Block this date automatically
            blocked = settings.get_blocked_dates()
            d_str = preferred_date.strftime('%Y-%m-%d')
            if d_str not in blocked:
                blocked.append(d_str)
                settings.set_blocked_dates(blocked)
                settings.updated_by = 'system (auto-full)'
                db.session.commit()

        flash(f'Appointment booked successfully! Confirmation ID: #{appointment.id}. We will contact you shortly.', 'success')
        return redirect(url_for('appointments.confirmation', appt_id=appointment.id))

    # ── GET: generate available dates (skip Sundays + blocked + full) ──
    today = date.today()
    blocked_dates = settings.get_blocked_dates()
    available_dates = []
    for i in range(1, 31):
        d = today + timedelta(days=i)
        d_str = d.strftime('%Y-%m-%d')
        if d.weekday() == 6:       # Skip Sundays
            continue
        if d_str in blocked_dates:  # Skip admin-blocked dates
            continue
        if _is_date_full(d):        # Skip fully-booked dates
            continue
        available_dates.append(d_str)

    return render_template('appointments.html',
                           time_slots=TIME_SLOTS,
                           available_dates=available_dates,
                           blocked_dates=blocked_dates,
                           min_date=(today + timedelta(days=1)).strftime('%Y-%m-%d'),
                           config=current_app.config)


@appointments.route('/confirmation/<int:appt_id>')
def confirmation(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    return render_template('appointment_confirmation.html', appt=appt, config=current_app.config)


@appointments.route('/check-slots')
def check_slots():
    date_str = request.args.get('date', '')
    try:
        appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date'}), 400

    settings = ClinicSettings.get()

    # If bookings globally disabled or date is blocked
    if not settings.bookings_enabled:
        return jsonify({'available': [], 'booked': TIME_SLOTS, 'disabled': True,
                        'message': 'Bookings are currently disabled.'})

    if appt_date.strftime('%Y-%m-%d') in settings.get_blocked_dates():
        return jsonify({'available': [], 'booked': TIME_SLOTS, 'blocked': True,
                        'message': 'This date is not available for appointments.'})

    booked = Appointment.query.filter(
        Appointment.preferred_date == appt_date,
        Appointment.status.in_(['pending', 'confirmed'])
    ).with_entities(Appointment.preferred_time).all()

    booked_times = [b[0] for b in booked]

    # Merge in admin-blocked individual slots
    admin_blocked = settings.get_blocked_slots_for_date(date_str)
    unavailable_times = list(set(booked_times + admin_blocked))

    available = [s for s in TIME_SLOTS if s not in unavailable_times]
    is_full = len(available) == 0

    return jsonify({
        'available': available,
        'booked': unavailable_times,
        'is_full': is_full,
        'message': 'All slots are booked for this date. Please choose another.' if is_full else ''
    })
