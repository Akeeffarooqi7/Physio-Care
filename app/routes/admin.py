from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models import (Appointment, ContactMessage, Treatment, Exercise,
                        DietTip, Testimonial, User, ChatHistory, ClinicSettings)
from app import db
from datetime import datetime, date, timedelta

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'doctor']:
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    today = date.today()
    clinic_settings = ClinicSettings.get()
    stats = {
        'total_appointments': Appointment.query.count(),
        'today_appointments': Appointment.query.filter_by(preferred_date=today).count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count(),
        'total_patients': User.query.filter_by(role='patient').count(),
        'total_treatments': Treatment.query.filter_by(is_active=True).count(),
        'bookings_enabled': clinic_settings.bookings_enabled,
    }
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(10).all()
    recent_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(5).all()
    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_appointments=recent_appointments,
                           recent_messages=recent_messages,
                           config=current_app.config)

@admin.route('/appointments')
@login_required
@admin_required
def appointments():
    status_filter = request.args.get('status', 'all')
    query = Appointment.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    appts = query.order_by(Appointment.preferred_date.asc()).all()
    return render_template('admin/appointments.html',
                           appointments=appts,
                           status_filter=status_filter,
                           config=current_app.config)

@admin.route('/appointments/<int:appt_id>/update', methods=['POST'])
@login_required
@admin_required
def update_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = request.form.get('status', appt.status)
    appt.doctor_notes = request.form.get('doctor_notes', appt.doctor_notes)
    appt.video_link = request.form.get('video_link', appt.video_link)
    db.session.commit()
    flash(f'Appointment #{appt_id} updated successfully.', 'success')
    return redirect(url_for('admin.appointments'))

@admin.route('/messages')
@login_required
@admin_required
def messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=msgs, config=current_app.config)

@admin.route('/messages/<int:msg_id>/read', methods=['POST'])
@login_required
@admin_required
def mark_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@admin.route('/treatments')
@login_required
@admin_required
def treatments():
    all_treatments = Treatment.query.order_by(Treatment.sort_order).all()
    return render_template('admin/treatments.html', treatments=all_treatments, config=current_app.config)

@admin.route('/treatments/add', methods=['POST'])
@login_required
@admin_required
def add_treatment():
    name = request.form.get('name', '').strip()
    slug = name.lower().replace(' ', '-').replace('/', '-')
    treatment = Treatment(
        name=name, slug=slug,
        category=request.form.get('category', ''),
        description=request.form.get('description', ''),
        symptoms=request.form.get('symptoms', ''),
        approach=request.form.get('approach', ''),
        recovery_time=request.form.get('recovery_time', ''),
        icon=request.form.get('icon', 'fa-heartbeat'),
        color=request.form.get('color', '#2563eb')
    )
    db.session.add(treatment)
    db.session.commit()
    flash('Treatment added successfully.', 'success')
    return redirect(url_for('admin.treatments'))

@admin.route('/treatments/<int:t_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    t.is_active = not t.is_active
    db.session.commit()
    return jsonify({'success': True, 'is_active': t.is_active})

@admin.route('/testimonials')
@login_required
@admin_required
def testimonials():
    all_t = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=all_t, config=current_app.config)

@admin.route('/testimonials/<int:t_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_testimonial(t_id):
    t = Testimonial.query.get_or_404(t_id)
    t.is_approved = not t.is_approved
    db.session.commit()
    return jsonify({'success': True, 'is_approved': t.is_approved})

@admin.route('/chat-history')
@login_required
@admin_required
def chat_history():
    histories = ChatHistory.query.order_by(ChatHistory.updated_at.desc()).limit(50).all()
    return render_template('admin/chat_history.html', histories=histories, config=current_app.config)

@admin.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users, config=current_app.config)


# ── Appointment Availability Settings ──────────────────────────────

TIME_SLOTS = [
    '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
    '11:00 AM', '11:30 AM', '12:00 PM', '02:00 PM',
    '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM',
    '04:30 PM', '05:00 PM'
]

@admin.route('/appointment-settings', methods=['GET', 'POST'])
@login_required
@admin_required
def appointment_settings():
    settings = ClinicSettings.get()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'toggle_bookings':
            settings.bookings_enabled = not settings.bookings_enabled
            settings.updated_by = current_user.email
            db.session.commit()
            state = 'enabled' if settings.bookings_enabled else 'disabled'
            flash(f'Appointment bookings {state} successfully.', 'success')

        elif action == 'update_message':
            msg = request.form.get('disabled_message', '').strip()
            if msg:
                settings.bookings_disabled_message = msg
                settings.updated_by = current_user.email
                db.session.commit()
                flash('Disabled booking message updated.', 'success')

        elif action == 'toggle_auto_disable':
            settings.auto_disable_full = not settings.auto_disable_full
            settings.updated_by = current_user.email
            db.session.commit()
            state = 'enabled' if settings.auto_disable_full else 'disabled'
            flash(f'Auto-disable on full day {state}.', 'success')

        elif action == 'block_date':
            date_str = request.form.get('block_date', '').strip()
            if date_str:
                blocked = settings.get_blocked_dates()
                if date_str not in blocked:
                    blocked.append(date_str)
                    settings.set_blocked_dates(blocked)
                    settings.updated_by = current_user.email
                    db.session.commit()
                    flash(f'Date {date_str} blocked for appointments.', 'success')
                else:
                    flash('Date already blocked.', 'warning')

        elif action == 'unblock_date':
            date_str = request.form.get('unblock_date', '').strip()
            blocked = settings.get_blocked_dates()
            if date_str in blocked:
                blocked.remove(date_str)
                settings.set_blocked_dates(blocked)
                settings.updated_by = current_user.email
                db.session.commit()
                flash(f'Date {date_str} unblocked.', 'success')

        elif action == 'block_slot':
            date_str = request.form.get('slot_date', '').strip()
            time_str = request.form.get('slot_time', '').strip()
            if date_str and time_str:
                settings.block_slot(date_str, time_str)
                settings.updated_by = current_user.email
                db.session.commit()
                flash(f'Slot {time_str} on {date_str} blocked.', 'success')

        elif action == 'unblock_slot':
            date_str = request.form.get('slot_date', '').strip()
            time_str = request.form.get('slot_time', '').strip()
            if date_str and time_str:
                settings.unblock_slot(date_str, time_str)
                settings.updated_by = current_user.email
                db.session.commit()
                flash(f'Slot {time_str} on {date_str} unblocked.', 'success')

        return redirect(url_for('admin.appointment_settings'))

    # Compute stats for upcoming dates
    today = date.today()
    all_blocked_slots = settings.get_blocked_slots()
    upcoming_dates_info = []
    for i in range(1, 15):
        d = today + timedelta(days=i)
        if d.weekday() == 6:  # skip Sunday
            continue
        d_str = d.strftime('%Y-%m-%d')
        booked_count = Appointment.query.filter(
            Appointment.preferred_date == d,
            Appointment.status.in_(['pending', 'confirmed'])
        ).count()
        admin_blocked_count = len(all_blocked_slots.get(d_str, []))
        total_slots = len(TIME_SLOTS)
        unavailable = booked_count + admin_blocked_count
        is_blocked = d_str in settings.get_blocked_dates()
        upcoming_dates_info.append({
            'date': d,
            'date_str': d_str,
            'booked': booked_count,
            'admin_blocked': admin_blocked_count,
            'total': total_slots,
            'available': max(0, total_slots - unavailable),
            'is_full': unavailable >= total_slots,
            'is_blocked': is_blocked,
        })

    return render_template('admin/appointment_settings.html',
                           settings=settings,
                           upcoming_dates=upcoming_dates_info,
                           time_slots=TIME_SLOTS,
                           total_slots=len(TIME_SLOTS),
                           config=current_app.config)


@admin.route('/appointment-settings/toggle-bookings', methods=['POST'])
@login_required
@admin_required
def quick_toggle_bookings():
    """AJAX endpoint for quick-toggle from dashboard."""
    settings = ClinicSettings.get()
    settings.bookings_enabled = not settings.bookings_enabled
    settings.updated_by = current_user.email
    db.session.commit()
    return jsonify({
        'success': True,
        'bookings_enabled': settings.bookings_enabled,
    })


@admin.route('/appointment-settings/block-date', methods=['POST'])
@login_required
@admin_required
def ajax_block_date():
    """AJAX endpoint for blocking/unblocking a single date."""
    data = request.get_json() or {}
    date_str = data.get('date', '')
    block = data.get('block', True)  # True = block, False = unblock
    settings = ClinicSettings.get()
    blocked = settings.get_blocked_dates()

    if block and date_str not in blocked:
        blocked.append(date_str)
    elif not block and date_str in blocked:
        blocked.remove(date_str)

    settings.set_blocked_dates(blocked)
    settings.updated_by = current_user.email
    db.session.commit()
    return jsonify({'success': True, 'blocked_dates': settings.get_blocked_dates()})


@admin.route('/appointment-settings/block-slot', methods=['POST'])
@login_required
@admin_required
def ajax_block_slot():
    """AJAX endpoint for blocking/unblocking a single time slot on a date."""
    data = request.get_json() or {}
    date_str = data.get('date', '')
    time_str = data.get('time', '')
    block = data.get('block', True)

    if not date_str or not time_str:
        return jsonify({'success': False, 'error': 'Date and time required'}), 400

    settings = ClinicSettings.get()
    if block:
        settings.block_slot(date_str, time_str)
    else:
        settings.unblock_slot(date_str, time_str)

    settings.updated_by = current_user.email
    db.session.commit()
    return jsonify({
        'success': True,
        'blocked_slots': settings.get_blocked_slots_for_date(date_str),
    })


@admin.route('/appointment-settings/date-slots/<date_str>')
@login_required
@admin_required
def date_slot_detail(date_str):
    """Returns JSON with per-slot status for a given date (used by the admin UI)."""
    from datetime import datetime as dt
    try:
        d = dt.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date'}), 400

    settings = ClinicSettings.get()
    admin_blocked = settings.get_blocked_slots_for_date(date_str)

    booked_appts = Appointment.query.filter(
        Appointment.preferred_date == d,
        Appointment.status.in_(['pending', 'confirmed'])
    ).all()
    booked_map = {}
    for a in booked_appts:
        booked_map[a.preferred_time] = {
            'patient': a.patient_name,
            'status': a.status,
            'id': a.id,
        }

    slots_info = []
    for slot in TIME_SLOTS:
        status = 'available'
        detail = None
        if slot in booked_map:
            status = 'booked'
            detail = booked_map[slot]
        elif slot in admin_blocked:
            status = 'admin_blocked'
        slots_info.append({
            'time': slot,
            'status': status,
            'detail': detail,
        })

    return jsonify({
        'date': date_str,
        'slots': slots_info,
        'admin_blocked': admin_blocked,
    })
