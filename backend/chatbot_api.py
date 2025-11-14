from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

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
        "glaucoma info": "Glaucoma symptoms can include gradual loss of side (peripheral) vision, blurred vision, and seeing halos or colored rings around lights.",
        "age-related macular degeneration info": "AMD is a disease that damages the macula (central part of the retina) and causes gradual loss of central vision.",
        "amblyopia lazy eye info": "Amblyopia is a condition where one eye does not develop clear vision in childhood because the brain favors the other eye.",
        "astigmatism info": "Astigmatism is a refractive error where the eye's front surface is unevenly curved, causing blurry or distorted vision.",
        "blepharitis info": "Blepharitis is inflammation of the eyelids causing red, itchy, and swollen eyelid edges.",
        "color blindness info": "Color blindness is a condition where people have difficulty distinguishing certain colours, usually red and green.",
        "convergence insufficiency info": "Convergence insufficiency is difficulty keeping the eyes aligned when focusing on near objects, causing eyestrain or headaches.",
        "corneal conditions info": "Corneal conditions are problems with the clear front layer of the eye causing pain, blurred vision, or light sensitivity.",
        "diabetic retinopathy info": "Diabetic retinopathy is damage to the retina's blood vessels due to diabetes, leading to blurred or lost vision if untreated.",
        "dry eye info": "Dry eye occurs when eyes do not produce enough tears or good-quality tears, causing burning or irritation.",
        "farsightedness hyperopia info": "Farsightedness (Hyperopia) means distant objects appear clear but near ones are blurry because images focus behind the retina.",
        "floaters info": "Floaters are tiny specks or cobweb-like shapes drifting across vision caused by changes in the eye's internal fluid.",
        "nearsightedness myopia info": "Nearsightedness (Myopia) means near objects appear clear but distant ones look blurry because images focus in front of the retina.",
        "pink eye info": "Pink eye (conjunctivitis) causes redness, itchiness, and discharge due to infection or irritation.",
        "presbyopia info": "Presbyopia is age-related difficulty focusing on near objects, common after age 40.",
        "uveitis info": "Uveitis is inflammation of the eye's middle layer causing redness, pain, and blurred vision."
    }

# ... (rest of your existing code remains the same until the search_qa_data function)

def search_qa_data(user_message):
    """Search for relevant answer in Q&A data with improved matching"""
    user_message = user_message.lower().strip()
    
    # Create a clean version of the message without punctuation for better matching
    clean_message = re.sub(r'[^\w\s]', ' ', user_message)
    clean_message = ' '.join(clean_message.split())  # Remove extra spaces
    
    words = clean_message.split()
    
    # Enhanced keyword mapping with synonyms and variations
    keyword_mapping = {
        # Nearsightedness variations
        "nearsightedness": "nearsightedness myopia info",
        "myopia": "nearsightedness myopia info",
        "nearsighted": "nearsightedness myopia info",
        "short sighted": "nearsightedness myopia info",
        "shortsighted": "nearsightedness myopia info",
        
        # Farsightedness variations  
        "farsightedness": "farsightedness hyperopia info",
        "hyperopia": "farsightedness hyperopia info",
        "farsighted": "farsightedness hyperopia info",
        "long sighted": "farsightedness hyperopia info",
        "longsighted": "farsightedness hyperopia info",
        
        # Common eye conditions
        "conjunctivitis": "symptoms conjunctivitis",
        "pink eye": "symptoms conjunctivitis",
        "cataract": "what is cataract",
        "cataracts": "what is cataract",
        "glaucoma": "glaucoma info",
        "dry eye": "dry eye info",
        "dry eyes": "dry eye info",
        "astigmatism": "astigmatism info",
        "floaters": "floaters info",
        "macular degeneration": "age-related macular degeneration info",
        "amd": "age-related macular degeneration info",
        "lazy eye": "amblyopia lazy eye info",
        "amblyopia": "amblyopia lazy eye info",
        "blepharitis": "blepharitis info",
        "color blindness": "color blindness info",
        "color blind": "color blindness info",
        "diabetic retinopathy": "diabetic retinopathy info",
        "presbyopia": "presbyopia info",
        "uveitis": "uveitis info",
        
        # Symptom queries
        "symptoms of": "symptoms conjunctivitis",  # Default for symptom queries
        "symptom of": "symptoms conjunctivitis",
        "what are the symptoms": "symptoms conjunctivitis",
        
        # General queries
        "what is": "what is cataract",  # Default for "what is" queries
        "tell me about": "what is cataract",
        "information about": "what is cataract"
    }
    
    # Check for exact matches in the mapping first
    for keyword, qa_key in keyword_mapping.items():
        if keyword in clean_message:
            if qa_key in qa_data:
                return qa_data[qa_key]
    
    # Check for partial matches in Q&A keys
    for key, value in qa_data.items():
        key_lower = key.lower()
        
        # Check if any word from the message matches significantly with the key
        for word in words:
            if len(word) > 4:  # Only consider words longer than 4 characters
                if word in key_lower:
                    return value
        
        # Check if the key is contained in the message
        if key_lower in clean_message:
            return value
    
    # Special handling for "what is" + condition pattern
    if "what is" in clean_message or "what are" in clean_message:
        for condition in ["nearsightedness", "myopia", "farsightedness", "hyperopia", 
                         "astigmatism", "cataract", "glaucoma", "conjunctivitis"]:
            if condition in clean_message:
                # Return the appropriate response based on condition
                condition_mapping = {
                    "nearsightedness": "Nearsightedness (Myopia) means near objects appear clear but distant ones look blurry because images focus in front of the retina.",
                    "myopia": "Myopia (Nearsightedness) means near objects appear clear but distant ones look blurry because images focus in front of the retina.",
                    "farsightedness": "Farsightedness (Hyperopia) means distant objects appear clear but near ones are blurry because images focus behind the retina.",
                    "hyperopia": "Hyperopia (Farsightedness) means distant objects appear clear but near ones are blurry because images focus behind the retina.",
                    "astigmatism": "Astigmatism is a refractive error where the eye's front surface is unevenly curved, causing blurry or distorted vision at all distances.",
                    "cataract": "A cataract is a clouding of the eye's natural lens, causing blurry vision, faded colors, and glare sensitivity.",
                    "glaucoma": "Glaucoma is a group of eye conditions that damage the optic nerve, often related to high eye pressure.",
                    "conjunctivitis": "Conjunctivitis (pink eye) is inflammation of the conjunctiva, the thin clear tissue that lies over the white part of the eye."
                }
                return condition_mapping.get(condition, value)
    
    return None

# ... (rest of your existing code remains the same)