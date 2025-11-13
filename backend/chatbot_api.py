from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load Q&A data from JSON file
try:
    with open('qa_data.json', 'r') as f:
        qa_data = json.load(f)
except FileNotFoundError:
    qa_data = {
        "symptoms conjunctivitis": "Conjunctivitis symptoms include redness, itching, tearing, and discharge from the eyes. It's often called pink eye.",
        "what is cataract": "A cataract is a clouding of the eye's natural lens, causing blurry vision, faded colors, and glare sensitivity.",
        "cataract symptoms": "Common cataract symptoms include blurry vision, trouble seeing at night, sensitivity to light, and seeing halos around lights.",
        "eye dryness": "For dry eyes, try using artificial tears, taking screen breaks, using a humidifier, and staying hydrated.",
        "digital eye strain": "To reduce digital eye strain, follow the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds.",
        "Glaucoma info": "Glaucoma symptoms can include gradual loss of side (peripheral) vision, blurred vision, and seeing halos or colored rings around lights.",
        "Age-Related Macular Degeneration (AMD) info": "AMD is a disease that damages the macula (central part of the retina) and causes gradual loss of central vision.",
        "Amblyopia (Lazy Eye) info": "Amblyopia is a condition where one eye does not develop clear vision in childhood because the brain favors the other eye.",
        "Astigmatism info": "Astigmatism is a refractive error where the eye's front surface is unevenly curved, causing blurry or distorted vision.",
        "Blepharitis info": "Blepharitis is inflammation of the eyelids causing red, itchy, and swollen eyelid edges.",
        "Color Blindness info": "Color blindness is a condition where people have difficulty distinguishing certain colours, usually red and green.",
        "Convergence Insufficiency info": "Convergence insufficiency is difficulty keeping the eyes aligned when focusing on near objects, causing eyestrain or headaches.",
        "Corneal Conditions info": "Corneal conditions are problems with the clear front layer of the eye causing pain, blurred vision, or light sensitivity.",
        "Diabetic Retinopathy info": "Diabetic retinopathy is damage to the retina's blood vessels due to diabetes, leading to blurred or lost vision if untreated.",
        "Dry Eye info": "Dry eye occurs when eyes do not produce enough tears or good-quality tears, causing burning or irritation.",
        "Farsightedness (Hyperopia) info": "Farsightedness (Hyperopia) means distant objects appear clear but near ones are blurry because images focus behind the retina.",
        "Floaters info": "Floaters are tiny specks or cobweb-like shapes drifting across vision caused by changes in the eye's internal fluid.",
        "Nearsightedness (Myopia) info": "Nearsightedness means near objects appear clear but distant ones look blurry because images focus in front of the retina.",
        "Pink Eye info": "Pink eye (conjunctivitis) causes redness, itchiness, and discharge due to infection or irritation.",
        "Presbyopia info": "Presbyopia is age-related difficulty focusing on near objects, common after age 40.",
        "Uveitis info": "Uveitis is inflammation of the eye's middle layer causing redness, pain, and blurred vision."
    }

# Comprehensive symptom analysis with follow-up questions
symptom_analysis = {
    "redness": {
        "keywords": ["red", "redness", "pink eye", "bloodshot", "pink"],
        "follow_up": "Is the redness accompanied by itching, discharge, or pain?",
        "possible_conditions": ["Conjunctivitis", "Allergic reaction", "Dry eyes", "Eye infection", "Blepharitis"],
        "severity": "moderate",
        "analyzer_type": "eye"
    },
    "itching": {
        "keywords": ["itch", "itching", "itchy", "scratchy"],
        "follow_up": "Do you also have redness, watery eyes, or seasonal allergies?",
        "possible_conditions": ["Allergic conjunctivitis", "Dry eyes", "Blepharitis", "Contact dermatitis"],
        "severity": "mild",
        "analyzer_type": "eye"
    },
    "pain": {
        "keywords": ["pain", "hurts", "sore", "aching", "sharp pain", "throbbing"],
        "follow_up": "Is the pain sharp or dull? Does it feel like something is in your eye?",
        "possible_conditions": ["Corneal abrasion", "Glaucoma", "Uveitis", "Eye infection", "Foreign object"],
        "severity": "serious",
        "analyzer_type": "doctor"
    },
    "blurry": {
        "keywords": ["blurry", "blurred", "fuzzy", "cloudy vision", "difficulty seeing", "hazy"],
        "follow_up": "Is the blurriness constant or does it come and go? Any difficulty seeing at night?",
        "possible_conditions": ["Cataracts", "Refractive error", "Diabetic retinopathy", "Macular degeneration", "Astigmatism"],
        "severity": "moderate",
        "analyzer_type": "retina"
    },
    "dry": {
        "keywords": ["dry", "dryness", "gritty", "sandy", "burning", "scratchy feeling"],
        "follow_up": "Do you spend long hours on screens? Does it improve with eye drops?",
        "possible_conditions": ["Dry eye syndrome", "Computer vision syndrome", "Blepharitis", "Sjogren's syndrome"],
        "severity": "mild",
        "analyzer_type": "eye"
    },
    "discharge": {
        "keywords": ["discharge", "crusty", "sticky", "pus", "watery", "goopy", "mucus"],
        "follow_up": "What color is the discharge? Are your eyelids stuck together in the morning?",
        "possible_conditions": ["Bacterial conjunctivitis", "Viral conjunctivitis", "Eye infection", "Blepharitis"],
        "severity": "moderate",
        "analyzer_type": "eye"
    },
    "floaters": {
        "keywords": ["floaters", "spots", "cobwebs", "dark spots", "flying spots", "specks"],
        "follow_up": "Have you noticed sudden increase in floaters or flashes of light?",
        "possible_conditions": ["Normal aging", "Retinal detachment", "Vitreous detachment", "Uveitis"],
        "severity": "serious",
        "analyzer_type": "retina"
    },
    "sensitivity": {
        "keywords": ["sensitivity", "light sensitivity", "photophobia", "bright light", "glare"],
        "follow_up": "Does light cause pain or discomfort? When did this sensitivity start?",
        "possible_conditions": ["Migraine", "Uveitis", "Corneal abrasion", "Cataracts", "Meningitis"],
        "severity": "moderate",
        "analyzer_type": "eye"
    },
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "tension"],
        "follow_up": "Is the headache around your eyes or forehead? Any nausea or vision changes?",
        "possible_conditions": ["Eye strain", "Migraine", "Sinusitis", "Glaucoma", "Refractive error"],
        "severity": "moderate",
        "analyzer_type": "doctor"
    },
    "flashes": {
        "keywords": ["flashes", "flashing lights", "flickering", "sparkles"],
        "follow_up": "Are the flashes constant or occasional? Any recent eye trauma?",
        "possible_conditions": ["Retinal detachment", "Migraine", "Vitreous detachment"],
        "severity": "serious",
        "analyzer_type": "retina"
    },
    "double vision": {
        "keywords": ["double vision", "diplopia", "seeing double", "overlapping images"],
        "follow_up": "Is the double vision in one eye or both? Does it happen all the time?",
        "possible_conditions": ["Astigmatism", "Cataracts", "Neurological issues", "Corneal problems"],
        "severity": "serious",
        "analyzer_type": "doctor"
    }
}

# Comprehensive disease information with symptoms and treatment
disease_info = {
    "conjunctivitis": {
        "name": "Conjunctivitis (Pink Eye)",
        "symptoms": ["Redness in one or both eyes", "Itching or irritation", "Gritty feeling", "Discharge that forms crust overnight", "Tearing", "Sensitivity to light"],
        "description": "Inflammation of the conjunctiva, the thin clear tissue that lies over the white part of the eye",
        "types": ["Viral", "Bacterial", "Allergic"],
        "causes": ["Viruses", "Bacteria", "Allergens", "Irritants"],
        "treatment": ["Warm compresses", "Artificial tears", "Antibiotic eye drops (for bacterial)", "Antihistamine drops (for allergic)"],
        "prevention": ["Wash hands frequently", "Avoid touching eyes", "Don't share towels or makeup", "Replace eye cosmetics regularly"],
        "see_doctor": "If symptoms are severe, don't improve after 2-3 days, or if you have eye pain or vision changes",
        "recommended_analyzer": "eye"
    },
    "cataract": {
        "name": "Cataract",
        "symptoms": ["Cloudy or blurry vision", "Fading or yellowing of colors", "Poor night vision", "Sensitivity to light and glare", "Seeing halos around lights", "Frequent changes in eyeglass prescription"],
        "description": "Clouding of the eye's natural lens, usually developing slowly with age",
        "causes": ["Aging", "Diabetes", "Smoking", "Prolonged sun exposure", "Eye injury", "Family history"],
        "treatment": ["Stronger eyeglasses", "Brighter lighting", "Anti-glare sunglasses", "Cataract surgery when vision impairment affects daily activities"],
        "prevention": ["Wear sunglasses with UV protection", "Don't smoke", "Manage health conditions like diabetes", "Eat fruits and vegetables rich in antioxidants"],
        "see_doctor": "When vision impairment affects daily activities like driving, reading, or recognizing faces",
        "recommended_analyzer": "retina"
    },
    "dry eye": {
        "name": "Dry Eye Syndrome",
        "symptoms": ["Stinging or burning sensation", "Stringy mucus in or around eyes", "Eye redness", "Sensitivity to light", "Feeling of something in the eye", "Blurred vision", "Watery eyes (reflex tearing)", "Difficulty wearing contact lenses"],
        "description": "Insufficient tear production or poor tear quality causing eye discomfort",
        "causes": ["Aging", "Screen use", "Dry environments", "Certain medications", "Medical conditions like arthritis", "Laser eye surgery"],
        "treatment": ["Artificial tears", "Prescription eye drops", "Punctal plugs", "Warm compresses", "Lipiflow treatment", "Omega-3 supplements"],
        "prevention": ["Take breaks during screen time", "Use humidifier", "Wear wraparound sunglasses outdoors", "Stay hydrated", "Blink regularly"],
        "see_doctor": "If symptoms persist despite self-care measures or significantly affect your quality of life",
        "recommended_analyzer": "eye"
    },
    "glaucoma": {
        "name": "Glaucoma",
        "symptoms": ["Often no early symptoms", "Gradual loss of peripheral vision", "Tunnel vision in advanced stages", "Eye pain", "Headache", "Nausea and vomiting", "Blurred vision", "Halos around lights", "Eye redness"],
        "description": "Group of eye conditions that damage the optic nerve, often related to high eye pressure",
        "types": ["Open-angle", "Angle-closure", "Normal-tension"],
        "treatment": ["Prescription eye drops", "Oral medications", "Laser therapy", "Surgery"],
        "prevention": ["Regular comprehensive eye exams", "Exercise safely", "Wear eye protection", "Manage blood pressure", "Maintain healthy weight"],
        "see_doctor": "Immediately if experiencing sudden eye pain, headache, nausea, or vision changes - this could be an emergency",
        "recommended_analyzer": "retina"
    },
    "migraine": {
        "name": "Ocular Migraine",
        "symptoms": ["Flashing lights", "Zigzag lines", "Blind spots", "Temporary vision loss", "Headache (may or may not occur)", "Nausea", "Sensitivity to light and sound"],
        "description": "Temporary visual disturbances that may or may not be accompanied by headache",
        "triggers": ["Stress", "Certain foods", "Bright lights", "Lack of sleep", "Hormonal changes", "Weather changes"],
        "treatment": ["Rest in dark, quiet room", "Over-the-counter pain relievers", "Prescription medications", "Identifying and avoiding triggers"],
        "prevention": ["Maintain regular sleep schedule", "Stay hydrated", "Manage stress", "Regular exercise", "Avoid known triggers"],
        "see_doctor": "If visual symptoms are new, changing, or accompanied by other neurological symptoms like weakness or speech difficulties",
        "recommended_analyzer": "doctor"
    },
    "stye": {
        "name": "Stye (Hordeolum)",
        "symptoms": ["Red, painful lump near edge of eyelid", "Swelling of eyelid", "Tearing", "Crusting along eyelid", "Feeling of something is in the eye", "Sensitivity to light"],
        "description": "Infection of an oil gland in the eyelid, causing a painful red bump",
        "causes": ["Bacterial infection (usually staphylococcus)", "Clogged oil glands", "Poor eyelid hygiene"],
        "treatment": ["Warm compresses 4-6 times daily", "Gentle massage", "Antibiotic ointment", "Avoid squeezing or popping", "Over-the-counter pain relievers"],
        "prevention": ["Wash hands before touching eyes", "Remove eye makeup before bed", "Replace eye cosmetics regularly", "Don't share eye makeup"],
        "see_doctor": "If the stye doesn't improve after 48 hours of warm compresses, if vision is affected, or if swelling spreads",
        "recommended_analyzer": "eye"
    },
    "retinal_detachment": {
        "name": "Retinal Detachment",
        "symptoms": ["Sudden appearance of many floaters", "Flashes of light in one or both eyes", "Blurred vision", "Gradual reduction in peripheral vision", "Curtain-like shadow over visual field"],
        "description": "Emergency condition where the retina pulls away from its normal position",
        "causes": ["Aging", "Eye injury", "Extreme nearsightedness", "Previous eye surgery", "Family history"],
        "treatment": ["Immediate medical attention required", "Laser surgery", "Freezing treatment", "Scleral buckle", "Vitrectomy"],
        "prevention": ["Regular eye exams", "Protective eyewear during sports", "Monitor for new floaters or flashes"],
        "see_doctor": "EMERGENCY - seek immediate medical attention if experiencing these symptoms",
        "recommended_analyzer": "retina"
    }
}

# Updated comprehensive wellness questionnaire with 10 questions
wellness_questions = [
    {
        "id": "age",
        "question": "Before we begin, please tell me your age.",
        "options": {
            "Under 18": 10,
            "18–25": 9,
            "26–40": 8,
            "41–60": 7,
            "Above 60": 6
        }
    },
    {
        "id": "screen_time",
        "question": "How many hours do you spend on screens (mobile, laptop, TV) daily?",
        "options": {
            "Less than 2 hours": 10,
            "2–4 hours": 8,
            "4–6 hours": 6,
            "6–8 hours": 4,
            "More than 8 hours": 2
        }
    },
    {
        "id": "breaks", 
        "question": "Do you take short breaks like the 20-20-20 rule while using screens?",
        "options": {
            "Always": 10,
            "Often": 8,
            "Sometimes": 6,
            "Rarely": 4,
            "Never": 2
        }
    },
    {
        "id": "sleep",
        "question": "How many hours of sleep do you get each night?",
        "options": {
            "8 or more hours": 10,
            "7–8 hours": 8,
            "6–7 hours": 6,
            "5–6 hours": 4,
            "Less than 5 hours": 2
        }
    },
    {
        "id": "dim_lighting",
        "question": "Do you use your phone or laptop in dim lighting or right before sleeping?",
        "options": {
            "Never": 10,
            "Rarely": 8,
            "Sometimes": 6,
            "Often": 4,
            "Always": 2
        }
    },
    {
        "id": "vitamin_a",
        "question": "How often do you include Vitamin A-rich foods (carrots, spinach, fish, eggs) in your diet?",
        "options": {
            "Daily": 10,
            "3–4 times a week": 8,
            "Once or twice a week": 6,
            "Occasionally": 4,
            "Hardly ever": 2
        }
    },
    {
        "id": "water",
        "question": "How much water do you drink per day?",
        "options": {
            "More than 8 glasses": 10,
            "6–8 glasses": 8,
            "4–6 glasses": 6,
            "2–4 glasses": 4,
            "Less than 2 glasses": 2
        }
    },
    {
        "id": "eye_strain",
        "question": "Do you experience eye strain, burning, or redness?",
        "options": {
            "Never": 10,
            "Rarely": 8,
            "Sometimes": 6,
            "Often": 4,
            "Very frequently": 2
        }
    },
    {
        "id": "blurry_vision",
        "question": "Do you get blurry vision after long screen use?",
        "options": {
            "Never": 10,
            "Rarely": 8,
            "Sometimes": 6,
            "Often": 4,
            "Very frequently": 2
        }
    },
    {
        "id": "eye_checkup",
        "question": "How often do you go for an eye check-up?",
        "options": {
            "Every 6 months": 10,
            "Once a year": 8,
            "Every 2 years": 6,
            "Occasionally": 4,
            "Never": 2
        }
    },
    {
        "id": "blue_light",
        "question": "Do you use blue-light filter or anti-glare glasses while using devices?",
        "options": {
            "Always": 10,
            "Often": 8,
            "Sometimes": 6,
            "Rarely": 4,
            "Never": 2
        }
    }
]

# Conversation states to track user interactions
conversation_states = {}

# Track user activity for context-aware responses
user_activity = {}

def get_disease_info(disease_name):
    """Get comprehensive information about a specific disease"""
    disease_name = disease_name.lower()
    
    # Map common terms to disease keys
    disease_mapping = {
        "pink eye": "conjunctivitis",
        "dry eyes": "dry eye",
        "ocular migraine": "migraine",
        "eye sty": "stye",
        "hordeolum": "stye",
        "retinal detachment": "retinal_detachment"
    }
    
    # Check mapping first, then direct match
    disease_key = disease_mapping.get(disease_name, disease_name)
    
    if disease_key in disease_info:
        disease = disease_info[disease_key]
        response = f"{disease['name']}\n\n"
        response += f"Description: {disease['description']}\n\n"
        response += "Common Symptoms:\n- " + "\n- ".join(disease['symptoms']) + "\n\n"
        
        if 'causes' in disease:
            response += "Possible Causes:\n- " + "\n- ".join(disease['causes']) + "\n\n"
        
        if 'treatment' in disease:
            response += "Treatment Options:\n- " + "\n- ".join(disease['treatment']) + "\n\n"
        
        if 'prevention' in disease:
            response += "Prevention Tips:\n- " + "\n- ".join(disease['prevention']) + "\n\n"
        
        response += f"When to See a Doctor: {disease['see_doctor']}\n\n"
        
        # Add analyzer recommendation if available
        if 'recommended_analyzer' in disease:
            analyzer_rec = get_analyzer_recommendation_text(disease['recommended_analyzer'])
            response += f"Recommended Analysis: {analyzer_rec}\n\n"
        
        response += "Remember: This is general information. Always consult an eye care professional for personalized advice. 👁️"
        
        return response
    
    return None

def analyze_symptoms(user_message):
    """Analyze user message for symptoms and determine follow-up questions"""
    user_message = user_message.lower()
    detected_symptoms = []
    possible_conditions = set()
    follow_up_questions = []
    analyzer_types = set()
    
    for symptom, data in symptom_analysis.items():
        for keyword in data["keywords"]:
            if keyword in user_message:
                detected_symptoms.append(symptom)
                possible_conditions.update(data["possible_conditions"])
                follow_up_questions.append(data["follow_up"])
                analyzer_types.add(data["analyzer_type"])
                break
    
    return detected_symptoms, list(possible_conditions), follow_up_questions, list(analyzer_types)

def get_next_follow_up(user_id):
    """Get the next follow-up question for the user"""
    if user_id not in conversation_states:
        return None
    
    state = conversation_states[user_id]
    asked_questions = state.get('asked_questions', [])
    all_questions = state.get('all_questions', [])
    
    # Find the next question that hasn't been asked
    for question in all_questions:
        if question not in asked_questions:
            return question
    
    return None  # No more questions

def get_analyzer_recommendation(analyzer_types, symptoms):
    """Determine which analyzer to recommend based on symptoms"""
    if not analyzer_types:
        return "doctor"  # Default to doctor if unsure
    
    # Priority: doctor > retina > eye
    if "doctor" in analyzer_types:
        return "doctor"
    elif "retina" in analyzer_types:
        return "retina"
    else:
        return "eye"

def get_analyzer_recommendation_text(analyzer_type):
    """Get descriptive text for analyzer recommendation"""
    if analyzer_type == "eye":
        return "Eye Analyzer - for external eye conditions and surface issues"
    elif analyzer_type == "retina":
        return "Retina Analyzer - for vision issues and internal eye health"
    else:
        return "Medical Consultation - for complex or serious symptoms"

def generate_conclusion(user_id):
    """Generate final conclusion based on collected symptoms"""
    if user_id not in conversation_states:
        return "I understand you have some eye concerns. For proper diagnosis, I recommend consulting an eye care professional. Thank you for using VisionAI! 👁️💙"
    
    state = conversation_states[user_id]
    detected_symptoms = state.get('symptoms', [])
    possible_conditions = state.get('conditions', [])
    analyzer_types = state.get('analyzer_types', [])
    
    if not detected_symptoms:
        return "Based on our conversation, I recommend monitoring your symptoms and consulting an eye doctor if they persist or worsen. Thank you for using VisionAI! 👁️💙"
    
    # Determine overall severity and recommended analyzer
    severities = [symptom_analysis[s]["severity"] for s in detected_symptoms if s in symptom_analysis]
    recommended_analyzer = get_analyzer_recommendation(analyzer_types, detected_symptoms)
    analyzer_text = get_analyzer_recommendation_text(recommended_analyzer)
    
    conclusion = "Based on our discussion about your symptoms, here's my assessment:\n\n"
    conclusion += "Symptoms you described: " + ", ".join(detected_symptoms) + "\n\n"
    
    if possible_conditions:
        conclusion += "These symptoms could potentially relate to: " + ", ".join(possible_conditions[:3]) + "\n\n"
    
    # Analyzer recommendation
    conclusion += "RECOMMENDED ACTION:\n"
    conclusion += f"Based on your symptoms, I recommend using our {analyzer_text}.\n\n"
    
    # Medical advice based on severity
    if "serious" in severities or recommended_analyzer == "doctor":
        conclusion += "URGENT RECOMMENDATION:\n"
        conclusion += "Your symptoms may indicate a condition that requires prompt medical attention. I strongly recommend visiting an eye doctor or emergency room as soon as possible.\n\n"
    else:
        conclusion += "NEXT STEPS:\n"
        conclusion += f"• Use our {analyzer_text.split(' - ')[0]} for initial assessment\n"
        conclusion += "• Schedule an appointment with an ophthalmologist or optometrist for comprehensive evaluation\n"
        conclusion += "• Monitor your symptoms and seek immediate care if they worsen\n\n"
    
    conclusion += "ADDITIONAL SUGGESTIONS:\n"
    # Add specific suggestions
    if "dry" in detected_symptoms:
        conclusion += "- Use preservative-free artificial tears for temporary relief\n"
    if "redness" in detected_symptoms or "itching" in detected_symptoms:
        conclusion += "- Apply cool compresses to closed eyelids\n"
        conclusion += "- Avoid eye makeup until symptoms resolve\n"
    if "blurry" in detected_symptoms:
        conclusion += "- Ensure proper lighting when reading or using screens\n"
        conclusion += "- Take regular breaks from near work\n"
    if "floaters" in detected_symptoms or "flashes" in detected_symptoms:
        conclusion += "- Avoid strenuous activities until evaluated by a doctor\n"
        conclusion += "- Note any changes in the number or pattern of floaters\n"
    
    conclusion += "\nIMPORTANT: I am an AI assistant and this is not medical advice. Please consult a qualified healthcare provider for proper diagnosis and treatment recommendations.\n\n"
    conclusion += "Thank you for using VisionAI! Wishing you the best for your eye health journey! 👁️💙"
    
    # Clear conversation state
    if user_id in conversation_states:
        del conversation_states[user_id]
    
    return conclusion

def is_conclusion_request(user_message, user_id="default_user"):
    """Check if user wants to conclude the conversation with context awareness"""
    user_message = user_message.lower()
    
    # Check for "that's all" specifically
    if "that's all" in user_message or "that is all" in user_message:
        # Check if user has done symptom analysis and wellness check
        has_symptoms = user_id in conversation_states and conversation_states[user_id].get('symptoms')
        has_wellness = user_activity.get(user_id, {}).get('wellness_completed', False)
        
        if has_symptoms and has_wellness:
            return "professional_advice"
        else:
            return "thank_you"
    
    # Check for thank you specifically
    thank_you_phrases = ["thank you", "thanks", "thankyou"]
    if any(phrase in user_message for phrase in thank_you_phrases):
        # Check if user has done symptom analysis and wellness check
        has_symptoms = user_id in conversation_states and conversation_states[user_id].get('symptoms')
        has_wellness = user_activity.get(user_id, {}).get('wellness_completed', False)
        
        if has_symptoms and has_wellness:
            return "thank_you_full"
        else:
            return "thank_you_simple"
    
    # Other conclusion phrases
    conclusion_phrases = [
        "no more symptoms", "nothing else", "that's everything", 
        "that's it", "conclude", "what do you think", "what could it be", 
        "what should i do", "conclusion", "advice", "no more", "done", 
        "finished"
    ]
    
    if any(phrase in user_message for phrase in conclusion_phrases):
        return "general_conclusion"
    
    return None

def is_disease_query(user_message):
    """Check if user is asking about a specific disease"""
    disease_keywords = [
        "symptoms of", "what is", "tell me about", "information about",
        "conjunctivitis", "cataract", "glaucoma", "dry eye", "migraine", "stye",
        "pink eye", "ocular migraine", "eye sty", "retinal detachment", "floaters",
        "macular degeneration", "amblyopia", "lazy eye", "astigmatism", "blepharitis",
        "color blindness", "convergence insufficiency", "corneal", "diabetic retinopathy",
        "farsightedness", "hyperopia", "nearsightedness", "myopia", "presbyopia", "uveitis"
    ]
    
    user_message = user_message.lower()
    return any(keyword in user_message for keyword in disease_keywords)

def search_qa_data(user_message):
    """Search for relevant answer in Q&A data"""
    user_message = user_message.lower()
    
    # Direct keyword matching - improved to handle hyperopia/farsightedness
    for key, value in qa_data.items():
        key_lower = key.lower()
        # Check if user message contains key words or synonyms
        if (key_lower in user_message or 
            ("hyperopia" in user_message and "farsightedness" in key_lower) or
            ("farsightedness" in user_message and "farsightedness" in key_lower)):
            return value
    
    # Check for partial matches and synonyms
    words = user_message.split()
    for word in words:
        for key, value in qa_data.items():
            # Handle hyperopia specifically
            if word == "hyperopia" and "farsightedness" in key.lower():
                return value
            if word in key.lower() and len(word) > 3:  # Only consider words longer than 3 characters
                return value
    
    return None

def calculate_wellness_score(answers):
    """Calculate wellness score based on user answers"""
    total_score = 0
    max_possible = len(wellness_questions) * 10
    
    for answer in answers.values():
        total_score += answer
    
    percentage = (total_score / max_possible) * 100
    return round(percentage)

def get_wellness_category(score):
    """Categorize the wellness score"""
    if score >= 80:
        return "Excellent", "Your eye care habits are outstanding! Keep maintaining these healthy practices."
    elif score >= 60:
        return "Good", "You have good eye care habits with some room for improvement in certain areas."
    elif score >= 40:
        return "Fair", "Your eye health habits need some attention. Consider implementing the suggestions below."
    else:
        return "Needs Improvement", "Your eyes may be experiencing significant strain. It's important to make lifestyle changes."

def get_personalized_suggestions(answers, score):
    """Generate personalized suggestions based on low-scoring areas"""
    suggestions = []
    
    # Age-based suggestions
    age = answers.get('age', 0)
    if age <= 6:  # Above 60
        suggestions.append("Consider more frequent eye check-ups due to age-related vision changes")
    
    # Screen time and breaks
    if answers.get('screen_time', 0) <= 4:
        suggestions.append("Reduce screen time and practice the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds")
    
    if answers.get('breaks', 0) <= 6:
        suggestions.append("Make conscious effort to take regular breaks during screen use to reduce eye strain")
    
    # Sleep and lighting
    if answers.get('sleep', 0) <= 6:
        suggestions.append("Aim for 7-8 hours of quality sleep nightly in a dark, quiet environment")
    
    if answers.get('dim_lighting', 0) <= 6:
        suggestions.append("Avoid using devices in dim lighting and stop screen use at least 1 hour before bedtime")
    
    # Nutrition and hydration
    if answers.get('vitamin_a', 0) <= 6:
        suggestions.append("Include more Vitamin A-rich foods like carrots, spinach, sweet potatoes, and eggs in your diet")
    
    if answers.get('water', 0) <= 6:
        suggestions.append("Increase water intake to at least 8 glasses daily to support overall eye health")
    
    # Eye comfort and vision
    if answers.get('eye_strain', 0) <= 4 or answers.get('blurry_vision', 0) <= 4:
        suggestions.append("Use artificial tears as needed and consider a humidifier in dry environments")
        suggestions.append("Ensure proper lighting and adjust screen brightness to comfortable levels")
    
    # Regular check-ups and protection
    if answers.get('eye_checkup', 0) <= 6:
        suggestions.append("Schedule regular comprehensive eye examinations to monitor your eye health")
    
    if answers.get('blue_light', 0) <= 6:
        suggestions.append("Consider using blue-light filters or anti-glare glasses for prolonged screen use")
    
    # General tips for all users
    general_tips = [
        "Wear UV-protection sunglasses when outdoors",
        "Maintain a balanced diet rich in leafy greens, fish, and colorful fruits",
        "Avoid smoking and limit alcohol consumption",
        "Practice good contact lens hygiene if applicable",
        "Maintain proper distance from screens (arm's length)"
    ]
    
    suggestions.extend(general_tips)
    
    return suggestions

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        user_id = "default_user"
        
        # Initialize user activity tracking
        if user_id not in user_activity:
            user_activity[user_id] = {
                'wellness_completed': False,
                'symptoms_discussed': False,
                'last_interaction': 'greeting'
            }
        
        if not user_message:
            return jsonify({'response': "Please describe your symptoms or ask about eye health. I'm here to help!"})
        
        # Handle conversation end detection with context
        conclusion_type = is_conclusion_request(user_message, user_id)
        if conclusion_type:
            if conclusion_type == "thank_you_full":
                response = "Thank you for using VisionAI. If you have any questions please feel free to ask!"
                # Reset activity tracking
                user_activity[user_id] = {
                    'wellness_completed': False,
                    'symptoms_discussed': False,
                    'last_interaction': 'conclusion'
                }
                return jsonify({'response': response})
            elif conclusion_type == "professional_advice":
                response = "I understand you have some eye concerns. For proper diagnosis, I recommend consulting an eye care professional. Thank you for using VisionAI! 👁️💙"
                # Reset activity tracking
                user_activity[user_id] = {
                    'wellness_completed': False,
                    'symptoms_discussed': False,
                    'last_interaction': 'conclusion'
                }
                return jsonify({'response': response})
            elif conclusion_type == "thank_you_simple":
                response = "You're welcome! I'm glad I could help. Remember to prioritize your eye health! 👁️💙"
                return jsonify({'response': response})
            elif conclusion_type == "general_conclusion":
                response = generate_conclusion(user_id)
                return jsonify({'response': response})
        
        # Handle wellness check start
        if user_message.lower() in ['wellness', 'start wellness', 'wellness check']:
            return jsonify({
                'response': "I'll help you assess your eye wellness! I'll ask you a few questions about your lifestyle habits to give you a personalized score and suggestions.",
                'start_wellness': True
            })
        
        # Handle greetings with improved responses
        greetings = {
            "hello": "Hello! How are you doing today? I hope you're having a wonderful day! 👋\n\nI'm your VisionAI Eye Care Assistant, here to help you with:\n\n- Symptom analysis and guidance\n- Disease information\n- Eye wellness assessment\n- General eye health tips\n\nWhat would you like to explore today?",
            "hi": "Hi there! 👋 Great to see you! How can I assist with your eye health today?\n\nYou can describe any symptoms, ask about eye conditions, or take our wellness assessment.",
            "hey": "Hey! Welcome to VisionAI! 😊\n\nI'm here to help you with all things related to eye health. Whether you have questions about symptoms, conditions, or just want some eye care tips, I've got you covered!\n\nWhat's on your mind today?",
            "good morning": "Good morning! 🌞 What a great time to check on your eye health!\n\nHow can I help you start your day with clearer vision and healthier eyes?",
            "good afternoon": "Good afternoon! 😊 Hope you're having a productive day!\n\nHow can I assist with your eye health concerns today?",
            "good evening": "Good evening! 🌙 Perfect time for an eye health check-in before the day ends.\n\nWhat would you like to know about your eye health today?"
        }
        
        for keyword, response_text in greetings.items():
            if keyword in user_message.lower():
                user_activity[user_id]['last_interaction'] = 'greeting'
                return jsonify({'response': response_text})
        
        # Check Q&A data first for general questions - FIXED HYPEROPIA ISSUE
        qa_response = search_qa_data(user_message)
        if qa_response:
            # Special handling for hyperopia to ensure consistent response
            if "hyperopia" in user_message.lower() or "farsightedness" in user_message.lower():
                return jsonify({'response': "Farsightedness (Hyperopia) means distant objects appear clear but near ones are blurry because images focus behind the retina."})
            return jsonify({'response': qa_response})
        
        # Check if user is asking about a specific disease
        if is_disease_query(user_message):
            # Try to extract disease name and get information
            for disease_key in disease_info.keys():
                if disease_key in user_message.lower():
                    disease_response = get_disease_info(disease_key)
                    if disease_response:
                        return jsonify({'response': disease_response})
            
            # Check for disease name variations with improved mapping
            disease_mappings = {
                "pink eye": "conjunctivitis",
                "dry eye": "dry eye",
                "dry eyes": "dry eye", 
                "ocular migraine": "migraine",
                "stye": "stye",
                "retinal": "retinal_detachment",
                "floaters": "retinal_detachment",
                "macular": "amd",
                "amd": "amd",
                "lazy eye": "amblyopia",
                "amblyopia": "amblyopia",
                "astigmatism": "astigmatism",
                "blepharitis": "blepharitis",
                "color blind": "color blindness",
                "convergence": "convergence insufficiency",
                "corneal": "corneal conditions",
                "diabetic retinopathy": "diabetic retinopathy",
                "farsighted": "farsightedness",
                "farsightedness": "farsightedness",
                "hyperopia": "farsightedness",  # Map hyperopia to farsightedness
                "nearsighted": "nearsightedness",
                "myopia": "nearsightedness",
                "presbyopia": "presbyopia",
                "uveitis": "uveitis"
            }
            
            for keyword, disease_key in disease_mappings.items():
                if keyword in user_message.lower():
                    # For diseases not in disease_info, use Q&A data
                    qa_response = search_qa_data(disease_key)
                    if qa_response:
                        return jsonify({'response': qa_response})
        
        # Check if we're in the middle of a symptom analysis conversation
        if user_id in conversation_states:
            state = conversation_states[user_id]
            
            # Analyze the new message for additional symptoms
            new_symptoms, new_conditions, new_questions, new_analyzers = analyze_symptoms(user_message)
            
            # Update state with new information
            if new_symptoms:
                state['symptoms'].extend([s for s in new_symptoms if s not in state['symptoms']])
                state['conditions'].extend([c for c in new_conditions if c not in state['conditions']])
                state['all_questions'].extend([q for q in new_questions if q not in state['all_questions']])
                state['analyzer_types'].extend([a for a in new_analyzers if a not in state['analyzer_types']])
                user_activity[user_id]['symptoms_discussed'] = True
            
            # Get next follow-up question
            next_question = get_next_follow_up(user_id)
            
            if next_question:
                # Mark this question as asked
                if 'asked_questions' not in state:
                    state['asked_questions'] = []
                state['asked_questions'].append(next_question)
                
                response = "I understand. " + next_question + "\n\nYou can say 'that's all' when you're ready for my assessment."
                return jsonify({'response': response})
            else:
                # No more questions, provide conclusion
                conclusion = generate_conclusion(user_id)
                return jsonify({'response': conclusion})
        
        # New symptom analysis conversation
        detected_symptoms, possible_conditions, follow_up_questions, analyzer_types = analyze_symptoms(user_message)
        
        if detected_symptoms:
            # Initialize conversation state
            conversation_states[user_id] = {
                'symptoms': detected_symptoms,
                'conditions': possible_conditions,
                'all_questions': follow_up_questions,
                'analyzer_types': analyzer_types,
                'asked_questions': []
            }
            user_activity[user_id]['symptoms_discussed'] = True
            
            if follow_up_questions:
                # Ask the first follow-up question
                conversation_states[user_id]['asked_questions'].append(follow_up_questions[0])
                response = "I understand you're experiencing " + ", ".join(detected_symptoms) + ". " + follow_up_questions[0] + "\n\nYou can say 'that's all' when you're ready for my assessment."
            else:
                # No follow-up questions needed, provide conclusion
                response = generate_conclusion(user_id)
            
            return jsonify({'response': response})
        else:
            # General response for non-symptom queries
            general_responses = {
                "retinal analysis": "Our Retinal Analysis feature uses advanced AI to examine retinal images for early detection of conditions like diabetic retinopathy, glaucoma, and macular degeneration. It provides comprehensive screening for internal eye health.",
                "eye analyzer": "The Eye Analyzer focuses on external eye conditions using image analysis technology. It's perfect for assessing visible issues like conjunctivitis, cataracts, dry eyes, and eyelid problems.",
                "retina analyzer": "The Retina Analyzer uses cutting-edge AI technology to examine retinal images and detect early signs of serious eye conditions. It's particularly useful for monitoring diabetic retinopathy, glaucoma, and age-related macular degeneration.",
                "eye analyser": "Our Eye Analyzer specializes in external eye assessment, helping identify conditions like conjunctivitis, styes, dry eye syndrome, and other visible eye issues through advanced image analysis.",
                "thank you": "You're welcome! I'm glad I could help. Remember to prioritize your eye health! 👁️💙",
            }
            
            for keyword, response_text in general_responses.items():
                if keyword in user_message.lower():
                    return jsonify({'response': response_text})
            
            # Default response
            return jsonify({
                'response': "I understand you're asking about eye health. Could you describe any specific symptoms you're experiencing, or ask about a specific eye condition?\n\nYou can also type 'wellness' for an eye health assessment."
            })
    
    except Exception as e:
        return jsonify({'response': "I'm having some technical difficulties. Please try again in a moment."})

@app.route('/api/wellness/start', methods=['GET'])
def start_wellness():
    """Start the wellness questionnaire"""
    return jsonify({
        'question': wellness_questions[0]["question"],
        'question_id': wellness_questions[0]["id"],
        'options': list(wellness_questions[0]["options"].keys()),
        'question_number': 1,
        'total_questions': len(wellness_questions)
    })

@app.route('/api/wellness/answer', methods=['POST'])
def process_wellness_answer():
    """Process wellness questionnaire answers"""
    try:
        data = request.json
        current_question_id = data.get('question_id')
        answer_text = data.get('answer')
        previous_answers = data.get('previous_answers', {})
        user_id = "default_user"
        
        # Find current question and its index
        current_index = 0
        for i, q in enumerate(wellness_questions):
            if q["id"] == current_question_id:
                current_index = i
                break
        
        current_question = wellness_questions[current_index]
        
        # Get score for this answer
        answer_score = current_question["options"].get(answer_text, 0)
        previous_answers[current_question_id] = answer_score
        
        # Check if this is the last question
        if current_index == len(wellness_questions) - 1:
            # Calculate final score
            final_score = calculate_wellness_score(previous_answers)
            category, category_description = get_wellness_category(final_score)
            suggestions = get_personalized_suggestions(previous_answers, final_score)
            
            result_message = f"🌟 Wellness Assessment Complete! 🌟\n\nYour Score: {final_score}/100\nCategory: {category}\n\n{category_description}\n\n📋 Personalized Suggestions:\n" + "\n".join([f"• {suggestion}" for suggestion in suggestions])

            if final_score < 60:
                result_message += "\n\n💡 Consider scheduling an eye examination to discuss your eye health concerns with a professional."

            result_message += "\n\nThank you for completing the wellness assessment! Wishing you healthy eyes! 👁️💙"
            
            # Mark wellness as completed in user activity
            if user_id not in user_activity:
                user_activity[user_id] = {}
            user_activity[user_id]['wellness_completed'] = True
            
            return jsonify({
                'completed': True,
                'final_score': final_score,
                'category': category,
                'category_description': category_description,
                'suggestions': suggestions,
                'message': result_message
            })
        else:
            # Send next question
            next_question = wellness_questions[current_index + 1]
            next_question_data = {
                'completed': False,
                'question': next_question["question"],
                'question_id': next_question["id"],
                'options': list(next_question["options"].keys()),
                'question_number': current_index + 2,
                'total_questions': len(wellness_questions),
                'previous_answers': previous_answers
            }
            
            return jsonify(next_question_data)
    
    except Exception as e:
        print(f"Error in wellness answer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'VisionAI Comprehensive Chatbot API'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)