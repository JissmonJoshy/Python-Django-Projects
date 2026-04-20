import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# -------------------------
# 1. Load Pre-trained Model
# -------------------------
model_path = "C:/PRASOBH/COLLEGE/2024MID/Skincare_Beauty_Products/Skincare_Beauty_Products/skincare_beauty_products/data_skintone/working/skin_tone_model.h5"
try:
    model = load_model(model_path)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

# -------------------------
# 2. Define Categories
# -------------------------
categories = ['dark', 'light', 'mid-dark', 'mid-light']

# -------------------------
# 3. Image Preprocessing & Prediction
# -------------------------
def predict_skin_tone(img_path):
    """
    Preprocess the image, predict skin tone, and visualize results.
    """
    try:
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize pixel values

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        confidence = np.max(prediction)

        # Display image with prediction
        plt.imshow(img)
        plt.title(f'Predicted Skin Tone: {categories[predicted_class]} ({confidence:.2f})')
        plt.axis('off')
        plt.show()

        print(f'📝 Predicted Skin Tone Class: {categories[predicted_class]}')
        print(f'🎯 Confidence Score: {confidence:.2f}')

    except Exception as e:
        print(f"❌ Error processing image: {e}")

# -------------------------
# 4. Test Predictions with Example Images
# -------------------------
img_paths = [
    'C:/PRASOBH/COLLEGE/2024MID/Skincare_Beauty_Products/Skincare_Beauty_Products/skincare_beauty_products/data_skintone/light/10015832.jpg',
    'C:/PRASOBH/COLLEGE/2024MID/Skincare_Beauty_Products/Skincare_Beauty_Products/skincare_beauty_products/data_skintone/mid-dark/24284023.jpg'
]

for img_path in img_paths:
    if os.path.exists(img_path):
        print(f"\n🔍 Predicting for image: {img_path}")
        predict_skin_tone(img_path)
    else:
        print(f"❌ Image not found: {img_path}")
