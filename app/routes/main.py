from flask import Blueprint, render_template, current_app
from app.models import Treatment, Testimonial, Exercise, DietTip
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    treatments = Treatment.query.filter_by(is_active=True).order_by(Treatment.sort_order).limit(6).all()
    testimonials = Testimonial.query.filter_by(is_approved=True, is_featured=True).limit(6).all()
    if not testimonials:
        testimonials = Testimonial.query.filter_by(is_approved=True).limit(6).all()
    return render_template('index.html',
                           treatments=treatments,
                           testimonials=testimonials,
                           config=current_app.config)

@main.route('/about')
def about():
    return render_template('about.html', config=current_app.config)

@main.route('/treatments')
def treatments():
    all_treatments = Treatment.query.filter_by(is_active=True).order_by(Treatment.sort_order).all()
    return render_template('treatments.html', treatments=all_treatments, config=current_app.config)

@main.route('/treatments/<slug>')
def treatment_detail(slug):
    treatment = Treatment.query.filter_by(slug=slug, is_active=True).first_or_404()
    exercises = Exercise.query.filter_by(treatment_id=treatment.id, is_active=True).all()
    diet_tips = DietTip.query.filter_by(treatment_id=treatment.id, is_active=True).all()
    related = Treatment.query.filter(
        Treatment.is_active == True,
        Treatment.id != treatment.id
    ).limit(3).all()
    return render_template('treatment_detail.html',
                           treatment=treatment,
                           exercises=exercises,
                           diet_tips=diet_tips,
                           related=related,
                           config=current_app.config)

@main.route('/health-guidance')
def health_guidance():
    exercises_back = Exercise.query.filter_by(body_part='back', is_active=True).all()
    exercises_neck = Exercise.query.filter_by(body_part='neck', is_active=True).all()
    exercises_knee = Exercise.query.filter_by(body_part='knee', is_active=True).all()
    exercises_shoulder = Exercise.query.filter_by(body_part='shoulder', is_active=True).all()
    diet_joint = DietTip.query.filter_by(condition='joint_pain', is_active=True).all()
    diet_muscle = DietTip.query.filter_by(condition='muscle_recovery', is_active=True).all()
    diet_general = DietTip.query.filter_by(condition='general', is_active=True).all()
    return render_template('health_guidance.html',
                           exercises_back=exercises_back,
                           exercises_neck=exercises_neck,
                           exercises_knee=exercises_knee,
                           exercises_shoulder=exercises_shoulder,
                           diet_joint=diet_joint,
                           diet_muscle=diet_muscle,
                           diet_general=diet_general,
                           config=current_app.config)

@main.route('/testimonials')
def testimonials():
    all_testimonials = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=all_testimonials, config=current_app.config)

@main.route('/contact')
def contact():
    return render_template('contact.html', config=current_app.config)
