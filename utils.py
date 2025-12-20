"""
Utility functions for Skin Condition Tracker
"""

def validate_inputs(pain, itch, redness, spread):
    """Validate symptom input values"""
    errors = []
    for name, value in [("Pain", pain), ("Itch", itch), ("Redness", redness), ("Spread", spread)]:
        if value < 0 or value > 10:
            errors.append(f"{name} must be between 0 and 10")
    return errors

def format_confidence(confidence):
    """Format confidence as percentage"""
    return f"{confidence*100:.1f}%"

def get_condition_info(condition):
    """Get detailed information about a skin condition"""
    info = {
        "Acne": {
            "description": "Common skin condition with clogged pores and inflammation.",
            "advice": "Keep skin clean, avoid picking, consider over-the-counter treatments with benzoyl peroxide or salicylic acid.",
            "severity": "Usually mild to moderate"
        },
        "Carcinoma": {
            "description": "Type of skin cancer that can appear as a pearly or waxy bump, or a flat, flesh-colored or brown scar-like lesion.",
            "advice": "IMPORTANT: Requires immediate medical attention. See a dermatologist as soon as possible.",
            "severity": "Potentially serious"
        },
        "Eczema": {
            "description": "Condition causing itchy, inflamed, and sometimes blistered skin.",
            "advice": "Moisturize regularly, avoid triggers, use gentle skin care products.",
            "severity": "Varies from mild to severe"
        },
        "Keratosis": {
            "description": "Rough, scaly patches on skin, often in sun-exposed areas.",
            "advice": "Use sunscreen, monitor for changes, consult dermatologist if concerned.",
            "severity": "Usually benign but should be monitored"
        },
        "Milia": {
            "description": "Small white bumps, often on face, caused by keratin trapped under the skin.",
            "advice": "Usually resolves on its own. Gentle exfoliation may help.",
            "severity": "Mild, cosmetic concern"
        },
        "Rosacea": {
            "description": "Chronic condition causing facial redness and sometimes small, pus-filled bumps.",
            "advice": "Avoid triggers (spicy foods, alcohol, extreme temperatures), use gentle skincare.",
            "severity": "Chronic but manageable"
        }
    }
    return info.get(condition, {
        "description": "Skin condition",
        "advice": "Consult a healthcare professional for proper diagnosis and treatment.",
        "severity": "Unknown"
    })