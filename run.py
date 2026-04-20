import json
from app import create_app, db
from app.models import User, Treatment, Exercise, DietTip, Testimonial

app = create_app()

def seed_database():
    """Populate the database with initial data."""
    # Admin user
    if not User.query.filter_by(email='admin@physiocare.com').first():
        admin = User(username='admin', email='admin@physiocare.com',
                     first_name='Dr. Sarah', last_name='Johnson',
                     role='admin', phone='+1-555-234-5678')
        admin.set_password('admin123')
        db.session.add(admin)

    # Doctor user
    if not User.query.filter_by(email='doctor@physiocare.com').first():
        doc = User(username='drjohnson', email='doctor@physiocare.com',
                   first_name='Dr. Sarah', last_name='Johnson',
                   role='doctor', phone='+1-555-234-5679')
        doc.set_password('doctor123')
        db.session.add(doc)

    # Demo patient
    if not User.query.filter_by(email='patient@demo.com').first():
        pat = User(username='patient_demo', email='patient@demo.com',
                   first_name='Alex', last_name='Smith',
                   role='patient', phone='+1-555-111-2222')
        pat.set_password('patient123')
        db.session.add(pat)

    # Treatments
    treatments_data = [
        {
            'name': 'Back Pain Relief', 'slug': 'back-pain-relief',
            'category': 'Spine & Core', 'icon': 'fa-spine',
            'color': '#ef4444', 'sort_order': 1,
            'description': 'Comprehensive treatment for acute and chronic back pain using evidence-based physiotherapy techniques including manual therapy, exercise prescription, and postural correction.',
            'symptoms': 'Dull aching pain in lower or upper back, muscle spasms, stiffness after rest, pain radiating to legs, difficulty standing straight.',
            'approach': 'Manual therapy, spinal mobilization, core strengthening exercises, postural re-education, heat/cold therapy, ergonomic advice.',
            'recovery_time': '4-8 weeks'
        },
        {
            'name': 'Neck Pain Treatment', 'slug': 'neck-pain-treatment',
            'category': 'Cervical Spine', 'icon': 'fa-head-side',
            'color': '#3b82f6', 'sort_order': 2,
            'description': 'Targeted treatment for cervical pain, stiffness, and tech neck syndrome. Our approach addresses both the symptoms and root causes.',
            'symptoms': 'Neck stiffness, headaches, pain radiating to shoulders or arms, numbness or tingling in hands, muscle tension.',
            'approach': 'Cervical mobilization, soft tissue massage, deep neck flexor strengthening, postural correction, ergonomic assessment.',
            'recovery_time': '3-6 weeks'
        },
        {
            'name': 'Knee Pain & Rehabilitation', 'slug': 'knee-pain-rehabilitation',
            'category': 'Lower Limb', 'icon': 'fa-running',
            'color': '#f59e0b', 'sort_order': 3,
            'description': 'Comprehensive knee rehabilitation for sports injuries, arthritis, post-surgical recovery, and chronic knee conditions.',
            'symptoms': 'Pain during activity, swelling, stiffness, clicking sounds, difficulty climbing stairs, instability.',
            'approach': 'Quadriceps and hamstring strengthening, proprioception training, gait analysis, taping, manual therapy.',
            'recovery_time': '6-12 weeks'
        },
        {
            'name': 'Frozen Shoulder', 'slug': 'frozen-shoulder',
            'category': 'Upper Limb', 'icon': 'fa-hand-paper',
            'color': '#8b5cf6', 'sort_order': 4,
            'description': 'Specialized treatment for adhesive capsulitis (frozen shoulder) with progressive mobilization and pain management strategies.',
            'symptoms': 'Severe shoulder stiffness, pain at night, inability to lift arm above head, restricted movement in all directions.',
            'approach': 'Gradual joint mobilization, stretching program, pain management, shoulder strengthening, activity modification.',
            'recovery_time': '12-18 months'
        },
        {
            'name': 'Sports Injury Rehabilitation', 'slug': 'sports-injury-rehabilitation',
            'category': 'Sports Medicine', 'icon': 'fa-futbol',
            'color': '#10b981', 'sort_order': 5,
            'description': 'Return-to-sport programs for athletes of all levels. Evidence-based rehabilitation for ligament injuries, muscle strains, and sports-specific conditions.',
            'symptoms': 'Pain after sports activity, swelling, limited performance, instability, reduced strength.',
            'approach': 'Sport-specific rehabilitation, neuromuscular training, strength and conditioning, injury prevention strategies.',
            'recovery_time': '6-16 weeks'
        },
        {
            'name': 'Sciatica Treatment', 'slug': 'sciatica-treatment',
            'category': 'Neurological', 'icon': 'fa-bolt',
            'color': '#06b6d4', 'sort_order': 6,
            'description': 'Targeted treatment for sciatic nerve pain with neural mobilization, spinal decompression, and targeted exercises.',
            'symptoms': 'Shooting pain from back to leg, numbness or tingling in leg/foot, weakness, pain worsened by sitting.',
            'approach': 'Neural mobilization, McKenzie method, piriformis release, core stability, ergonomic advice.',
            'recovery_time': '4-12 weeks'
        },
        {
            'name': 'Post-Surgery Rehabilitation', 'slug': 'post-surgery-rehabilitation',
            'category': 'Surgical Recovery', 'icon': 'fa-hospital',
            'color': '#f97316', 'sort_order': 7,
            'description': 'Comprehensive post-operative rehabilitation after knee replacement, hip replacement, spinal surgery, and shoulder surgery.',
            'symptoms': 'Post-surgical weakness, scar tissue, limited range of motion, reduced function, pain management.',
            'approach': 'Phased rehabilitation program, scar tissue management, progressive strengthening, gait training.',
            'recovery_time': '3-6 months'
        },
        {
            'name': 'Posture Correction', 'slug': 'posture-correction',
            'category': 'Preventive Care', 'icon': 'fa-person-standing',
            'color': '#84cc16', 'sort_order': 8,
            'description': 'Scientific assessment and correction of postural imbalances causing pain and affecting quality of life.',
            'symptoms': 'Slouching, rounded shoulders, forward head posture, upper/lower cross syndrome, chronic tension.',
            'approach': 'Postural assessment, muscle imbalance correction, ergonomic education, movement retraining.',
            'recovery_time': '8-12 weeks'
        },
    ]

    for t_data in treatments_data:
        if not Treatment.query.filter_by(slug=t_data['slug']).first():
            treatment = Treatment(**t_data)
            db.session.add(treatment)

    db.session.flush()

    # Exercises
    exercises_data = [
        {
            'title': 'Cat-Cow Stretch', 'body_part': 'back',
            'difficulty': 'beginner', 'duration': '5 minutes',
            'description': 'A gentle spinal mobilization exercise that alternates between arching and rounding the back.',
            'instructions': json.dumps([
                'Start on hands and knees with neutral spine',
                'Inhale: drop belly down, lift head and tailbone (Cow)',
                'Exhale: round spine up, tuck chin and pelvis (Cat)',
                'Move slowly and breathe with each movement',
                'Repeat 10-15 times, 2-3 sets'
            ]),
            'benefits': 'Improves spinal flexibility, reduces back tension, warms up spine',
            'precautions': 'Avoid if you have acute disc herniation. Move gently.',
        },
        {
            'title': 'Knee-to-Chest Stretch', 'body_part': 'back',
            'difficulty': 'beginner', 'duration': '3 minutes',
            'description': 'Relieves lower back tension by stretching the lower back and hip muscles.',
            'instructions': json.dumps([
                'Lie on your back on a firm surface',
                'Bring one knee to chest, hold with both hands',
                'Hold for 20-30 seconds, breathing deeply',
                'Switch legs and repeat',
                'Then bring both knees to chest simultaneously',
                'Perform 3-5 repetitions per leg'
            ]),
            'benefits': 'Stretches lower back, hip flexors, and glutes. Relieves compression.',
            'precautions': 'Avoid pulling forcefully. Stop if pain worsens.',
        },
        {
            'title': 'Chin Tuck Exercise', 'body_part': 'neck',
            'difficulty': 'beginner', 'duration': '5 minutes',
            'description': 'Strengthens deep neck flexors and corrects forward head posture.',
            'instructions': json.dumps([
                'Sit or stand with spine tall',
                'Look straight ahead',
                'Gently draw chin straight back (like making a double chin)',
                'Hold for 5 seconds',
                'Release slowly',
                'Repeat 10-15 times, 3 sets per day'
            ]),
            'benefits': 'Corrects forward head posture, strengthens neck muscles, reduces headaches.',
            'precautions': 'Movement should be pain-free. Do not force.',
        },
        {
            'title': 'Straight Leg Raises', 'body_part': 'knee',
            'difficulty': 'beginner', 'duration': '10 minutes',
            'description': 'Strengthens quadriceps without stressing the knee joint.',
            'instructions': json.dumps([
                'Lie on your back',
                'Bend one knee with foot flat on floor',
                'Keep other leg straight',
                'Tighten thigh muscle of straight leg',
                'Lift leg to 45° (height of bent knee)',
                'Hold 3 seconds, lower slowly',
                '3 sets of 15 repetitions each leg'
            ]),
            'benefits': 'Strengthens quad without knee stress. Essential for knee rehabilitation.',
            'precautions': 'Keep core engaged. Do not arch lower back excessively.',
        },
        {
            'title': 'Pendulum Shoulder Exercise', 'body_part': 'shoulder',
            'difficulty': 'beginner', 'duration': '5 minutes',
            'description': 'Gentle shoulder mobilization using gravity to decompress the joint.',
            'instructions': json.dumps([
                'Stand beside a table or chair for support',
                'Lean forward, let affected arm hang down freely',
                'Gently swing arm in small circles (clockwise)',
                'Reverse direction after 30 seconds',
                'Swing forward-backward and side-to-side',
                'Perform 2-3 minutes, 2-3 times daily'
            ]),
            'benefits': 'Decompresses shoulder joint, maintains range of motion, reduces stiffness.',
            'precautions': 'Use gravity only — no active muscle effort. Very gentle.',
        },
        {
            'title': 'Piriformis Stretch', 'body_part': 'back',
            'difficulty': 'beginner', 'duration': '5 minutes',
            'description': 'Releases the piriformis muscle to relieve sciatic nerve compression.',
            'instructions': json.dumps([
                'Lie on your back with knees bent',
                'Cross right ankle over left knee (figure-4 position)',
                'Grasp behind left thigh',
                'Gently pull both legs toward chest',
                'Hold 30-45 seconds, breathe deeply',
                'Switch sides. Repeat 3 times each side.'
            ]),
            'benefits': 'Relieves sciatica, hip tightness, lower back pain.',
            'precautions': 'Avoid if hip replacement. Keep movement gentle.',
        },
        {
            'title': 'Shoulder Cross-Body Stretch', 'body_part': 'shoulder',
            'difficulty': 'beginner', 'duration': '3 minutes',
            'description': 'Stretches the posterior shoulder capsule and rotator cuff muscles.',
            'instructions': json.dumps([
                'Stand or sit upright',
                'Bring one arm across chest',
                'Use other hand to gently press arm closer to chest',
                'Hold for 30 seconds',
                'Switch arms',
                'Repeat 3 times per arm'
            ]),
            'benefits': 'Improves shoulder internal rotation, reduces impingement.',
            'precautions': 'Do not force if painful. Gentle pressure only.',
        },
        {
            'title': 'Neck Side Stretch', 'body_part': 'neck',
            'difficulty': 'beginner', 'duration': '5 minutes',
            'description': 'Releases tension in the upper trapezius and neck muscles.',
            'instructions': json.dumps([
                'Sit upright with shoulders relaxed',
                'Slowly tilt head to right side',
                'Optionally place right hand on head for gentle pressure',
                'Hold 30 seconds, feeling stretch on left side',
                'Return to center slowly',
                'Repeat on other side. 3 rounds each.'
            ]),
            'benefits': 'Reduces neck tension, improves cervical range of motion.',
            'precautions': 'Never force or bounce. Stop if pain radiates to arm.',
        },
    ]

    for e_data in exercises_data:
        if not Exercise.query.filter_by(title=e_data['title']).first():
            exercise = Exercise(**e_data)
            db.session.add(exercise)

    # Diet tips
    diet_data = [
        {
            'condition': 'joint_pain', 'food_item': 'Fatty Fish (Salmon, Sardines)',
            'category': 'Omega-3', 'icon': '🐟',
            'benefit': 'Rich in omega-3 fatty acids that reduce joint inflammation and cartilage damage.',
            'tips': 'Aim for 2-3 servings per week. Grill or bake; avoid frying.'
        },
        {
            'condition': 'joint_pain', 'food_item': 'Turmeric & Ginger',
            'category': 'Anti-inflammatory', 'icon': '🫚',
            'benefit': 'Curcumin in turmeric is a powerful anti-inflammatory comparable to some medications.',
            'tips': 'Add to warm milk, curries, or smoothies. Combine with black pepper to enhance absorption.'
        },
        {
            'condition': 'joint_pain', 'food_item': 'Leafy Greens',
            'category': 'Vitamins', 'icon': '🥬',
            'benefit': 'Spinach, kale, and broccoli provide Vitamin K, calcium, and antioxidants for bone and joint health.',
            'tips': 'Eat a variety of dark leafy greens daily. Raw or lightly steamed for maximum nutrients.'
        },
        {
            'condition': 'joint_pain', 'food_item': 'Berries',
            'category': 'Antioxidants', 'icon': '🫐',
            'benefit': 'Blueberries, strawberries contain anthocyanins that fight inflammation and oxidative stress.',
            'tips': 'Add to breakfast, smoothies, or eat as snacks. Fresh or frozen are both excellent.'
        },
        {
            'condition': 'muscle_recovery', 'food_item': 'Lean Protein Sources',
            'category': 'Protein', 'icon': '🥩',
            'benefit': 'Essential amino acids in chicken, eggs, and legumes rebuild damaged muscle tissue.',
            'tips': 'Consume 25-30g protein within 30 min of exercise. Spread intake throughout the day.'
        },
        {
            'condition': 'muscle_recovery', 'food_item': 'Tart Cherry Juice',
            'category': 'Recovery', 'icon': '🍒',
            'benefit': 'Reduces muscle soreness and accelerates recovery after exercise due to anti-inflammatory compounds.',
            'tips': 'Drink 250-350ml twice daily for 4-5 days post-injury or intense exercise.'
        },
        {
            'condition': 'muscle_recovery', 'food_item': 'Sweet Potatoes',
            'category': 'Carbohydrates', 'icon': '🍠',
            'benefit': 'Complex carbs and potassium support glycogen replenishment and prevent muscle cramps.',
            'tips': 'Eat post-workout for recovery fuel. Also great source of Vitamin A for immune health.'
        },
        {
            'condition': 'general', 'food_item': 'Water & Hydration',
            'category': 'Hydration', 'icon': '💧',
            'benefit': 'Joint cartilage is 70-80% water. Dehydration directly worsens joint pain and stiffness.',
            'tips': 'Drink 8-10 glasses daily. More if active or in hot weather. Add lemon for vitamin C.'
        },
        {
            'condition': 'general', 'food_item': 'Nuts & Seeds',
            'category': 'Healthy Fats', 'icon': '🥜',
            'benefit': 'Walnuts, flaxseeds, and chia seeds provide omega-3s, vitamin E, and anti-inflammatory benefits.',
            'tips': 'A handful daily is ideal. Add to salads, smoothies, or eat as snacks.'
        },
        {
            'condition': 'general', 'food_item': 'Calcium-Rich Foods',
            'category': 'Minerals', 'icon': '🥛',
            'benefit': 'Calcium is the primary mineral in bones. Adequate intake prevents osteoporosis and fractures.',
            'tips': 'Include dairy, fortified plant milks, sardines, and leafy greens. Best absorbed with Vitamin D.'
        },
        {
            'condition': 'general', 'food_item': 'Vitamin D Sources',
            'category': 'Vitamins', 'icon': '☀️',
            'benefit': 'Vitamin D is critical for calcium absorption, bone strength, and muscle function.',
            'tips': '15-20 min of sunlight daily. Also from fatty fish, egg yolks, and fortified foods.'
        },
    ]

    for d_data in diet_data:
        if not DietTip.query.filter_by(food_item=d_data['food_item']).first():
            tip = DietTip(**d_data)
            db.session.add(tip)

    # Testimonials
    testimonials_data = [
        {
            'patient_name': 'Michael R.', 'condition': 'Lower Back Pain',
            'occupation': 'Software Engineer',
            'review': 'After 3 years of chronic lower back pain from desk work, Dr. Johnson\'s treatment program completely transformed my life. Within 8 weeks, I was pain-free and have remained so for over a year!',
            'rating': 5, 'is_featured': True, 'avatar_color': '#2563eb',
            'recovery_story': 'I had tried everything — chiro, massage, medications. Nothing lasted. Dr. Johnson did a thorough assessment, identified muscle imbalances, and gave me a targeted exercise program. Game-changer!'
        },
        {
            'patient_name': 'Jennifer L.', 'condition': 'Frozen Shoulder',
            'occupation': 'Professional Tennis Player',
            'review': 'I thought my tennis career was over with a frozen shoulder diagnosis. Dr. Johnson\'s specialized treatment got my full range of motion back in 4 months. I\'m back competing at the highest level.',
            'rating': 5, 'is_featured': True, 'avatar_color': '#10b981',
            'recovery_story': 'The progressive mobilization program was very gradual but incredibly effective. My shoulder went from 30% to 100% range of motion. Extraordinary care and expertise.'
        },
        {
            'patient_name': 'Robert K.', 'condition': 'Post-ACL Surgery',
            'occupation': 'Football Coach',
            'review': 'My post-ACL rehab with Dr. Johnson was exceptional. She designed a sport-specific program that got me back coaching and even playing recreational football — better than before surgery.',
            'rating': 5, 'is_featured': True, 'avatar_color': '#f59e0b',
            'recovery_story': 'The return-to-sport protocols were evidence-based and carefully progressive. I never felt rushed, and the outcome exceeded all expectations.'
        },
        {
            'patient_name': 'Priya S.', 'condition': 'Sciatica',
            'occupation': 'Yoga Instructor',
            'review': 'Even as a yoga teacher, sciatica had me unable to work for months. The neural mobilization techniques and targeted exercises Dr. Johnson prescribed brought lasting relief.',
            'rating': 5, 'is_featured': True, 'avatar_color': '#8b5cf6',
            'recovery_story': 'I appreciated the holistic approach — not just treating the nerve pain but addressing the underlying causes and teaching me how to maintain my spine health long-term.'
        },
        {
            'patient_name': 'David M.', 'condition': 'Chronic Neck Pain',
            'occupation': 'Architect',
            'review': 'Years of hunching over blueprints created severe neck problems. The combination of manual therapy and corrective exercises gave me my life back. I can now work comfortably for full days.',
            'rating': 5, 'is_featured': False, 'avatar_color': '#ef4444',
            'recovery_story': 'The ergonomic assessment was particularly valuable — small changes to my workstation combined with the exercises made a huge difference.'
        },
        {
            'patient_name': 'Sarah T.', 'condition': 'Knee Arthritis',
            'occupation': 'Marathon Runner',
            'review': 'I was told I\'d never run again due to knee arthritis. Dr. Johnson proved them wrong. With proper strengthening and technique correction, I completed my 5th marathon last month!',
            'rating': 5, 'is_featured': False, 'avatar_color': '#06b6d4',
            'recovery_story': 'The key was understanding that strengthening the right muscles could offload the arthritic joint. The program was challenging but incredibly rewarding.'
        },
    ]

    for t_data in testimonials_data:
        if not Testimonial.query.filter_by(patient_name=t_data['patient_name']).first():
            t = Testimonial(**t_data)
            db.session.add(t)

    db.session.commit()
    print("Database seeded successfully!")

with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
