from flask import Blueprint, jsonify, request, session
from app.models import ChatHistory, ContactMessage, Testimonial
from app import db
from datetime import datetime
import uuid
import json

api = Blueprint('api', __name__)

# Comprehensive chatbot knowledge base
CHATBOT_KB = {
    'greetings': {
        'keywords': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'howdy', 'start'],
        'response': "Hello! I'm PhysioBot 🤖, your virtual physiotherapy assistant. I'm here to help you understand your pain and guide you towards recovery.\n\n**I can help you with:**\n• Understanding your symptoms\n• Exercise recommendations\n• Diet and nutrition tips\n• When to see a doctor\n\nWhat's bothering you today? Tell me about your pain or condition.",
    },
    'back_pain': {
        'keywords': ['back pain', 'back ache', 'lower back', 'upper back', 'spine', 'lumbar', 'back hurts', 'backache', 'slipped disc', 'disc'],
        'response': "I understand you're experiencing **back pain**. This is one of the most common conditions we treat.\n\n**Common causes:**\n• Muscle strain or sprain\n• Poor posture\n• Herniated disc\n• Sedentary lifestyle\n• Heavy lifting\n\n**Immediate relief tips:**\n• Apply ice for 20 min (first 48 hours)\n• Then use heat therapy\n• Gentle stretching\n• Avoid prolonged sitting\n\n**Recommended exercises:**\n1. Cat-Cow stretch\n2. Knee-to-chest stretch\n3. Pelvic tilts\n4. Child's pose\n5. Bridge exercise\n\n**Diet tips for back pain:**\n🥦 Anti-inflammatory foods (turmeric, ginger)\n🐟 Omega-3 rich foods (salmon, walnuts)\n🥬 Calcium-rich foods (spinach, dairy)\n\n⚠️ **Disclaimer:** This is general guidance only, not medical diagnosis. Please consult Dr. Johnson for personalized treatment.",
    },
    'neck_pain': {
        'keywords': ['neck pain', 'neck ache', 'stiff neck', 'cervical', 'neck hurts', 'neck tension', 'whiplash'],
        'response': "Neck pain can significantly impact daily life. Let me help you understand it better.\n\n**Common causes:**\n• Poor posture (tech neck)\n• Muscle tension/stress\n• Sleeping in wrong position\n• Whiplash injury\n• Cervical spondylosis\n\n**Immediate relief:**\n• Gentle neck rolls\n• Hot or cold compress\n• Avoid screen time\n• Support with proper pillow\n\n**Recommended exercises:**\n1. Chin tucks\n2. Side neck stretches\n3. Shoulder rolls\n4. Neck rotations\n5. Upper trapezius stretch\n\n**Diet for neck health:**\n🥗 Anti-inflammatory diet\n💊 Magnesium-rich foods (reduce muscle tension)\n🥛 Calcium & Vitamin D\n\n⚠️ **Disclaimer:** Always consult a physiotherapist before starting exercises.",
    },
    'knee_pain': {
        'keywords': ['knee pain', 'knee ache', 'knee hurts', 'knee swelling', 'knee injury', 'runner knee', 'ligament', 'meniscus', 'acl', 'pcl'],
        'response': "Knee pain is very common and treatable with proper physiotherapy.\n\n**Common conditions:**\n• Runner's knee (Patellofemoral pain)\n• Ligament injuries (ACL/PCL/MCL)\n• Meniscus tear\n• Osteoarthritis\n• IT band syndrome\n\n**Immediate care:**\n• RICE method (Rest, Ice, Compression, Elevation)\n• Avoid impact activities\n• Use support brace if needed\n\n**Strengthening exercises:**\n1. Straight leg raises\n2. Wall squats\n3. Calf raises\n4. Hamstring curls\n5. Step-ups\n\n**Diet for joint health:**\n🐟 Omega-3 fatty acids\n🥑 Vitamin E (avocado, nuts)\n🍊 Vitamin C (citrus fruits)\n💧 Stay well hydrated\n\n⚠️ **Disclaimer:** Knee injuries need professional assessment. Book an appointment for proper diagnosis.",
    },
    'shoulder_pain': {
        'keywords': ['shoulder pain', 'shoulder ache', 'frozen shoulder', 'rotator cuff', 'shoulder injury', 'shoulder hurts', 'shoulder stiffness'],
        'response': "Shoulder pain, including frozen shoulder, is a specialty area we excel at treating.\n\n**Common conditions:**\n• Frozen shoulder (adhesive capsulitis)\n• Rotator cuff injury\n• Shoulder impingement\n• Bursitis\n• Tendinitis\n\n**Self-care strategies:**\n• Pendulum exercises\n• Heat before exercise\n• Ice after activity\n• Maintain gentle movement\n\n**Exercises:**\n1. Pendulum swings\n2. Cross-body stretch\n3. Internal/external rotation\n4. Wall climbing\n5. Doorway chest stretch\n\n**Nutrition support:**\n🥩 Protein for muscle repair\n🫐 Antioxidants (berries)\n🥜 Healthy fats (anti-inflammatory)\n\n⚠️ **Disclaimer:** Shoulder conditions need professional evaluation. Early treatment gives better outcomes.",
    },
    'sciatica': {
        'keywords': ['sciatica', 'sciatic', 'leg numbness', 'shooting pain', 'radiating pain', 'buttock pain', 'nerve pain'],
        'response': "Sciatica (sciatic nerve pain) can be quite debilitating, but physiotherapy has excellent results.\n\n**What is sciatica?**\nPain that radiates along the sciatic nerve — from lower back through the buttocks and down each leg.\n\n**Common triggers:**\n• Herniated disc\n• Piriformis syndrome\n• Spinal stenosis\n• Prolonged sitting\n\n**Relief strategies:**\n• Avoid prolonged sitting\n• Gentle stretching\n• Heat/ice therapy\n• Stay active with walking\n\n**Helpful exercises:**\n1. Piriformis stretch\n2. Knee-to-chest\n3. Seated spinal twist\n4. Bird-dog\n5. Glute bridges\n\n**Diet recommendations:**\n🍵 Turmeric (powerful anti-inflammatory)\n🥦 B vitamins for nerve health\n💧 Stay hydrated\n\n⚠️ **Disclaimer:** Sciatica symptoms can worsen. Please consult our specialist for a comprehensive treatment plan.",
    },
    'sports_injury': {
        'keywords': ['sports injury', 'sprain', 'strain', 'muscle pull', 'athletic injury', 'sports', 'workout injury', 'gym injury'],
        'response': "Sports injuries require prompt and proper treatment for optimal recovery.\n\n**Common sports injuries we treat:**\n• Ankle sprains\n• Muscle strains\n• Stress fractures\n• Tennis/golfer's elbow\n• Hamstring injuries\n\n**Immediate RICE protocol:**\n🧊 **R**est - Stop activity immediately\n🧊 **I**ce - Apply for 20 min every 2 hours\n🩹 **C**ompression - Elastic bandage\n⬆️ **E**levation - Raise above heart level\n\n**Recovery phases:**\n1. Acute (0-72 hours) - RICE + rest\n2. Sub-acute - Gentle movement\n3. Rehabilitation - Strengthening\n4. Return to sport - Sport-specific training\n\n**Recovery nutrition:**\n🥩 High protein intake\n🍌 Carbs for energy\n🥗 Antioxidants for healing\n💊 Vitamin C & Zinc\n\n⚠️ **Disclaimer:** Do not play through pain. Get professional assessment.",
    },
    'posture': {
        'keywords': ['posture', 'slouching', 'hunchback', 'rounded shoulders', 'forward head', 'sitting posture', 'desk pain', 'office pain'],
        'response': "Poor posture is a modern epidemic, especially with desk work and smartphone use.\n\n**Common postural issues:**\n• Forward head posture\n• Rounded shoulders\n• Anterior pelvic tilt\n• Kyphosis (hunched back)\n• Tech neck\n\n**Quick posture fixes:**\n• Ear over shoulder over hip (sitting)\n• Screen at eye level\n• Take breaks every 30 minutes\n• Ergonomic workstation setup\n\n**Posture correction exercises:**\n1. Wall angels\n2. Chest openers\n3. Core strengthening\n4. Hip flexor stretches\n5. Thoracic spine mobility\n\n**Workstation checklist:**\n✅ Monitor at eye level\n✅ Feet flat on floor\n✅ Back supported\n✅ Keyboard at elbow height\n\n⚠️ **Disclaimer:** Postural issues can lead to chronic pain. Let us create a personalized correction program for you.",
    },
    'appointment': {
        'keywords': ['book', 'appointment', 'schedule', 'visit', 'consult', 'consultation', 'see doctor', 'meet doctor', 'come in', 'clinic'],
        'response': "I'd be happy to help you book an appointment with Dr. Sarah Johnson! 📅\n\n**Appointment options:**\n🏥 **In-Person Visit** - Full assessment & hands-on treatment\n💻 **Video Consultation** - Online assessment from home\n\n**Our clinic hours:**\n• Monday - Friday: 9:00 AM - 6:00 PM\n• Saturday: 9:00 AM - 2:00 PM\n• Sunday: Closed\n\n**How to book:**\nClick the **'Book Appointment'** button on our website or call us at **(555) 234-5678**.\n\n**What to bring:**\n• Previous medical records\n• List of medications\n• Referral letter (if any)\n• Comfortable clothing\n\nWould you like to proceed to booking now?",
    },
    'cost': {
        'keywords': ['cost', 'price', 'fee', 'charge', 'payment', 'insurance', 'how much', 'afford'],
        'response': "We believe quality physiotherapy should be accessible to everyone.\n\n**Our consultation fees:**\n💰 Initial Consultation (60 min): $120\n💰 Follow-up Session (45 min): $85\n💰 Video Consultation: $75\n💰 Home Visit: From $150\n\n**Insurance:**\nWe accept most major insurance providers. Please contact us to verify your coverage.\n\n**Payment options:**\n• Credit/Debit cards\n• Health savings accounts\n• Payment plans available\n• Insurance direct billing\n\nFor exact pricing or insurance queries, please call us at **(555) 234-5678** or email **care@physiocare.com**.",
    },
    'exercise_general': {
        'keywords': ['exercise', 'workout', 'stretching', 'yoga', 'physiotherapy exercises', 'home exercises', 'rehab exercises'],
        'response': "Exercise is a cornerstone of physiotherapy recovery. Here are general guidelines:\n\n**Types of therapeutic exercises:**\n🏃 **Cardiovascular** - Low-impact walking, swimming, cycling\n💪 **Strengthening** - Resistance training for weak muscles\n🧘 **Flexibility** - Stretching and yoga\n⚖️ **Balance** - Proprioception training\n\n**General principles:**\n• Start slow and progress gradually\n• Pain should not exceed 3/10 during exercise\n• Warm up before and cool down after\n• Consistency is key (3-5x per week)\n• Rest is part of recovery\n\n**Visit our Health Guidance page** for condition-specific exercise programs with detailed instructions!\n\n⚠️ **Disclaimer:** Always consult a physiotherapist before starting a new exercise program if you have an existing injury.",
    },
    'diet_general': {
        'keywords': ['diet', 'food', 'nutrition', 'eat', 'eating', 'what to eat', 'what to avoid', 'anti-inflammatory', 'supplements'],
        'response': "Nutrition plays a vital role in physiotherapy recovery!\n\n**Anti-inflammatory power foods:**\n🐟 Fatty fish (salmon, mackerel, sardines)\n🫐 Berries (blueberries, strawberries)\n🥬 Leafy greens (spinach, kale)\n🫒 Olive oil\n🥜 Nuts and seeds\n🫚 Turmeric & ginger\n\n**Foods to AVOID:**\n❌ Processed/junk food\n❌ Excessive sugar\n❌ Alcohol\n❌ Trans fats\n❌ Excessive caffeine\n\n**Key nutrients for recovery:**\n• Vitamin D - Bone & muscle health\n• Calcium - Bone strength\n• Protein - Muscle repair\n• Omega-3 - Inflammation reduction\n• Magnesium - Muscle relaxation\n\n**Hydration:**\n💧 Drink 8-10 glasses of water daily\n💧 Hydration is critical for joint lubrication\n\nVisit our **Health Guidance** page for condition-specific diet plans!",
    },
    'emergency': {
        'keywords': ['emergency', 'severe pain', 'can\'t move', 'numbness', 'weakness', 'paralysis', 'fall', 'accident', 'fracture', 'broken'],
        'response': "🚨 **This sounds like it may need urgent medical attention!**\n\nIf you are experiencing:\n• Severe, sudden pain\n• Loss of movement or feeling\n• Numbness or tingling\n• Weakness in limbs\n• Pain after a fall or accident\n\n**Please seek emergency care immediately:**\n📞 Call **911** for emergencies\n🏥 Visit your nearest Emergency Room\n📞 Or call us immediately at **(555) 234-5678**\n\n**Do NOT:**\n• Try to self-treat severe injuries\n• Move if you suspect a spinal injury\n• Ignore sudden, severe symptoms\n\nYour safety is our top priority. Please seek immediate medical attention if this is an emergency.",
    },
    'default': {
        'response': "Thank you for reaching out! I want to make sure I give you the most helpful information.\n\n**I can assist with information about:**\n• 🦴 Back pain & spine issues\n• 🦷 Neck pain & stiffness\n• 🦵 Knee pain & injuries\n• 💪 Shoulder pain & frozen shoulder\n• ⚡ Sciatica & nerve pain\n• 🏃 Sports injuries\n• 🧘 Posture correction\n• 🥗 Diet & nutrition advice\n• 🏋️ Exercise recommendations\n• 📅 Appointment booking\n\nCould you describe your symptoms in more detail? For example:\n*\"I have lower back pain after sitting for long hours\"*\n\n⚠️ **Remember:** I provide general guidance only. For proper diagnosis and treatment, please consult Dr. Johnson.",
    }
}

def find_response(message):
    message_lower = message.lower().strip()

    # Check each category
    for category, data in CHATBOT_KB.items():
        if category == 'default':
            continue
        keywords = data.get('keywords', [])
        for keyword in keywords:
            if keyword in message_lower:
                return data['response']

    return CHATBOT_KB['default']['response']

@api.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data.get('message', '').strip()
    session_id = data.get('session_id') or session.get('chat_session_id')

    if not session_id:
        session_id = str(uuid.uuid4())
        session['chat_session_id'] = session_id

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    bot_response = find_response(user_message)

    # Save chat history
    try:
        from flask_login import current_user
        chat_hist = ChatHistory.query.filter_by(session_id=session_id).first()
        if not chat_hist:
            chat_hist = ChatHistory(
                session_id=session_id,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            db.session.add(chat_hist)

        chat_hist.add_message('user', user_message)
        chat_hist.add_message('bot', bot_response)
        db.session.commit()
    except Exception:
        pass

    return jsonify({
        'response': bot_response,
        'session_id': session_id,
        'timestamp': datetime.utcnow().isoformat()
    })

@api.route('/contact', methods=['POST'])
def contact():
    data = request.get_json() or request.form
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'error': 'Required fields missing'}), 400

    msg = ContactMessage(
        name=name, email=email, phone=phone,
        subject=subject, message=message
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message sent successfully!'})

@api.route('/body-info/<part>')
def body_info(part):
    BODY_PARTS = {
        'neck': {
            'title': 'Neck Pain',
            'icon': '🫀',
            'description': 'Neck pain affects millions. Common causes include poor posture, muscle strain, and cervical issues.',
            'symptoms': ['Stiffness and limited motion', 'Headaches from neck tension', 'Radiating pain to shoulders', 'Numbness or tingling in arms'],
            'exercises': ['Chin tucks (3×10 reps)', 'Side neck stretches (hold 30 sec)', 'Shoulder rolls (10 circles each)', 'Levator scapulae stretch'],
            'diet': ['Magnesium-rich foods (spinach, almonds)', 'Anti-inflammatory turmeric milk', 'Omega-3 (salmon, chia seeds)', 'Stay hydrated (8+ glasses/day)'],
            'color': '#3b82f6'
        },
        'shoulder': {
            'title': 'Shoulder Pain',
            'icon': '💪',
            'description': 'Shoulder disorders range from frozen shoulder to rotator cuff injuries, all highly treatable.',
            'symptoms': ['Deep aching or sharp pain', 'Limited range of motion', 'Weakness in arm movements', 'Pain at night/during sleep'],
            'exercises': ['Pendulum swings (30 sec)', 'Cross-body stretch (30 sec each)', 'Internal rotation stretch', 'Doorway chest stretch'],
            'diet': ['Vitamin C (collagen production)', 'Protein (muscle repair)', 'Anti-inflammatory berries', 'Curcumin supplements'],
            'color': '#8b5cf6'
        },
        'back': {
            'title': 'Back Pain',
            'icon': '🦴',
            'description': 'Back pain is the leading cause of disability. 80% of people experience it at some point.',
            'symptoms': ['Dull or shooting pain', 'Muscle spasms', 'Stiffness after rest', 'Pain radiating to legs'],
            'exercises': ['Cat-cow stretch (10 reps)', 'Knee-to-chest stretch', 'Pelvic tilts (15 reps)', 'Bird-dog exercise (10 reps each)'],
            'diet': ['Calcium-rich foods (bone health)', 'Vitamin D (supplements/sunlight)', 'Anti-inflammatory diet', 'Collagen-boosting foods'],
            'color': '#ef4444'
        },
        'knee': {
            'title': 'Knee Pain',
            'icon': '🦵',
            'description': 'Knee pain affects people of all ages, from athletes to elderly. Physiotherapy is highly effective.',
            'symptoms': ['Pain during activity', 'Swelling or stiffness', 'Clicking or grinding sound', 'Difficulty bearing weight'],
            'exercises': ['Straight leg raises (3×15)', 'Quad sets (3×15)', 'Mini squats (3×10)', 'Hamstring stretches'],
            'diet': ['Omega-3 fatty acids', 'Glucosamine-rich foods', 'Vitamin E (anti-oxidant)', 'Collagen (bone broth)'],
            'color': '#f59e0b'
        },
        'hip': {
            'title': 'Hip Pain',
            'icon': '🏃',
            'description': 'Hip pain can stem from arthritis, bursitis, or muscle imbalances. Early treatment prevents worsening.',
            'symptoms': ['Groin or outer hip pain', 'Stiffness in hip joint', 'Limping or altered gait', 'Pain radiating to thigh'],
            'exercises': ['Hip flexor stretch', 'Clamshells (3×15)', 'Hip circles (10 each)', 'Glute bridges (3×15)'],
            'diet': ['Calcium and Vitamin D', 'Protein for muscle support', 'Anti-inflammatory foods', 'Bone broth'],
            'color': '#10b981'
        },
        'ankle': {
            'title': 'Ankle & Foot Pain',
            'icon': '🦶',
            'description': 'Ankle sprains and foot conditions are among the most common sports injuries.',
            'symptoms': ['Swelling and bruising', 'Pain on weight-bearing', 'Instability while walking', 'Limited range of motion'],
            'exercises': ['Alphabet tracing (foot circles)', 'Calf raises (3×15)', 'Towel scrunches', 'Resistance band exercises'],
            'diet': ['Anti-inflammatory foods', 'Vitamin C (ligament healing)', 'Calcium (bone repair)', 'Magnesium (muscle cramps)'],
            'color': '#06b6d4'
        },
    }
    part_data = BODY_PARTS.get(part)
    if not part_data:
        return jsonify({'error': 'Body part not found'}), 404
    return jsonify(part_data)

@api.route('/testimonial', methods=['POST'])
def submit_testimonial():
    data = request.get_json() or request.form
    from app.models import Testimonial
    testimonial = Testimonial(
        patient_name=data.get('patient_name', ''),
        condition=data.get('condition', ''),
        review=data.get('review', ''),
        rating=int(data.get('rating', 5)),
        occupation=data.get('occupation', ''),
        is_approved=False
    )
    db.session.add(testimonial)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Thank you! Your testimonial will be reviewed.'})
