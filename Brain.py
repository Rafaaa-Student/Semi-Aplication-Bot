import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN warnings
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
# Tambahan kalau masih muncul warning deprecated
tf.get_logger().setLevel('ERROR')
import tf_keras
from PIL import Image, ImageOps
import numpy as np

# Load modelnya sekali saja di sini dengan tf_keras untuk kompatibilitas Teachable Machine
model = tf_keras.models.load_model("keras_model.h5", compile=False)
labels = open("labels.txt", "r").readlines()

def check_image(image_path):
    # Logika pengolahan gambar (Resize ke 224x224 sesuai standar TM)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    # turn the image into a numpy array
    image_array = np.asarray(image)
    
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Load the image into the array
    data[0] = normalized_image_array
    
    # Predicts the model
    prediction = model.predict(data)
    
    # Ambil hasil prediksi tertinggi
    index = np.argmax(prediction)
    class_name = labels[index]
    confidence_score = prediction[0][index]
    
    return class_name.strip(), confidence_score
