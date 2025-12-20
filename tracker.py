from datetime import datetime

class DataTracker:
    def calculate_severity_scores(self, pain, itch, redness, spread, confidence):
        user_score = (pain + itch + redness + spread) / 4
        ai_score = confidence * 10
        final_score = (0.6 * user_score) + (0.4 * ai_score)
        
        if final_score <= 3:
            severity = "Mild"
        elif final_score <= 6:
            severity = "Moderate"
        else:
            severity = "Severe"
        
        return {
            "user_score": round(user_score, 2),
            "ai_score": round(ai_score, 2),
            "final_score": round(final_score, 2),
            "severity_label": severity,
            "symptoms": {"pain": pain, "itch": itch, "redness": redness, "spread": spread}
        }