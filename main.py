import cv2 as cv
import numpy as np
import os
import tensorflow as tf
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize FaceNet for embeddings and load pre-trained data
facenet = FaceNet()
faces_embeddings = np.load("models/Face_Embedding.npz")
Y = faces_embeddings['Y']

# Encode labels
encoder = LabelEncoder()
encoder.fit(Y)

# Load Haar Cascade for face detection
haarcascade = cv.CascadeClassifier("models/haarcascade_frontalface_default.xml")

# Load pre-trained neural network model for face classification
try:
    model = tf.keras.models.load_model("models/Predict_Model.h5")  # Adjust the model path as needed
except FileNotFoundError:
    print("Error: The neural network model file 'Predict_Model.h5' was not found.")
    exit(1)

# Start webcam capture
cap = cv.VideoCapture(0)

# Threshold for "unknown" classification
threshold = 0.55

# Face Recognition Loop
while cap.isOpened():
    _, frame = cap.read()
    
    # Convert the frame to RGB and grayscale
    rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = haarcascade.detectMultiScale(gray_img, 1.3, 6)  # Neighbors = 5 (increase will least to less false positive)
    
    # Process each detected face
    for x, y, w, h in faces:
        # Extract and resize face region
        face_img = rgb_img[y:y+h, x:x+w]
        face_img = cv.resize(face_img, (160, 160))
        
        # Expand dimensions for FaceNet model (1 x 160 x 160 x 3)
        face_img = np.expand_dims(face_img, axis=0)
        
        # Get the face embedding
        y_pred = facenet.embeddings(face_img)
        
        # Predict the class probabilities using the neural network
        probabilities = model.predict(y_pred)
        
        # Get the predicted class index with the highest probability
        max_prob = np.max(probabilities)
        predicted_class = np.argmax(probabilities)
        
        # print(max_prob)
        
        # Apply threshold to classify as "unknown" or a known person
        if max_prob < threshold:
            final_name = "unknown"
        else:
            final_name = encoder.inverse_transform([predicted_class])[0]
        
        # Draw rectangle and label around detected face
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
        cv.putText(frame, str(final_name), (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 3, cv.LINE_AA)
    
    # Display the resulting frame   
    cv.imshow("Face Recognition: ", frame)
    
    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release the capture and close windows
cap.release()
cv.destroyAllWindows()
