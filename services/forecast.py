def _bucket(val, low, mid, high):
    if val is None:
        return "Unknown"
    if val < low:
        return "Low"
    if val < mid:
        return "Medium"
    if val < high:
        return "High"
    return "Very High"

def predict_progression(disease: str, temp, humidity, rainfall):
    """
    Simple, explainable rules:
    - Fungal diseases (Powdery Mildew, Rust, Leaf Spot) worsen with high humidity and rainfall
    - Heat stress helps some diseases but often interacts with humidity
    """
    # Base today severity
    if disease == "Healthy":
        today = "Low"
    else:
        # humidity primary driver
        if humidity is None:
            today = "Medium"
        elif humidity >= 80 or (rainfall and rainfall >= 5):
            today = "High"
        elif humidity >= 60:
            today = "Medium"
        else:
            today = "Low"

    # Project next 7 & 14 days (proxy = current conditions; upgrade later with forecast API)
    # If it’s already humid/wet, assume escalation.
    if disease == "Healthy":
        risk7 = "Low"
        risk14 = "Low"
    else:
        if humidity is None:
            risk7, risk14 = "Medium", "High"
        elif humidity >= 80 or (rainfall and rainfall >= 5):
            risk7, risk14 = "High", "Very High"
        elif humidity >= 60:
            risk7, risk14 = "Medium", "High"
        else:
            risk7, risk14 = "Low", "Medium"

    return today, risk7, risk14

def advice_for(disease: str, risk7: str, weather: dict):
    """
    Short actionable tips. Keep it lightweight.
    """
    base = []
    if disease == "Healthy":
        base.append("Plant looks healthy—continue routine monitoring.")
    else:
        base.append(f"Detected: {disease}. Start monitoring daily.")

    # Humidity/rain suggestions
    hum = weather.get("humidity", 0) or 0
    rain = weather.get("rainfall", 0.0) or 0.0

    if hum >= 70 or rain >= 3:
        base.append("Increase airflow: prune dense leaves; avoid overhead watering.")
        base.append("Water early morning; keep leaves dry.")
    else:
        base.append("Maintain regular watering at soil level, not the foliage.")

    if disease in {"Powdery Mildew", "Leaf Spot", "Rust"}:
        base.append("Remove and bin infected leaves—do not compost.")
        base.append("Consider a mild fungicide or organic option (e.g., potassium bicarbonate).")

    # Risk escalation
    if risk7 in {"High", "Very High"}:
        base.append("Plan preventive treatment within 48 hours due to rising risk.")

    return base
