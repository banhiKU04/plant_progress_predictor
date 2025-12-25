import os
import random

# Path to your downloaded PlantVillage dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "PlantVillage")

# List all class folders automatically
class_names = [d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]

def detect_disease(img_path: str):
    """
    Lightweight detector for low-config PC.
    Returns a random disease from the downloaded dataset to simulate predictions.
    """
    disease = random.choice(class_names)
    confidence = round(random.uniform(0.7, 0.95), 2)  # Random confidence
    return disease, confidence
