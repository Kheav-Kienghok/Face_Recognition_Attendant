import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# =======================================================================

from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from attendance import check_and_mark_attendance, initialize
import cv2 as cv
import numpy as np
import tensorflow as tf


facenet = FaceNet()
faces_embeddings = np.load("models/Face_Embeddings.npz")
X = faces_embeddings["arr_0"]  # Stored embeddings
Y = faces_embeddings["arr_1"]

encoder = LabelEncoder()
encoder.fit(Y)
encoded_labels = encoder.transform(Y)

# Load Haar Cascade for face detection
haarcascade = cv.CascadeClassifier("models/haarcascade_frontalface_default.xml")

# Optional (For small dataset doesn't recommend it)
try:
    model = tf.keras.models.load_model("models/Predict_Models.h5")  
except FileNotFoundError:
    print("Error: The neural network model file 'Predict_Model.h5' was not found.")
    exit(1)

# Threshold for "unknown" classification
threshold = 0.8

def processing_app():
    
    # Start webcam capture
    cap = cv.VideoCapture(0)
    
    # Set the window name to be non-resizable with a fixed size
    cv.namedWindow("Face Recognition: ", cv.WINDOW_NORMAL)
    cv.resizeWindow("Face Recognition: ", 700, 600)  # You can set your desired dimensions here

    while cap.isOpened():
        _, frame = cap.read()
        
        frame = cv.flip(frame, 1)
        
        rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = haarcascade.detectMultiScale(gray_img, 1.3, 6)  # Neighbors = 5 (increase will lead to less false positive)
        
        for x, y, w, h in faces:
            face_img = rgb_img[y:y+h, x:x+w]
            face_img = cv.resize(face_img, (160, 160))
            
            # Expand dimensions for FaceNet model (1 x 160 x 160 x 3)
            face_img = np.expand_dims(face_img, axis = 0)
            
            y_pred = facenet.embeddings(face_img)
            
            similarities = cosine_similarity(y_pred, X)
            
            probabilities = model.predict(y_pred)
            
            max_similarity = np.max(similarities)
            predicted_index = np.argmax(similarities)

            print(probabilities)
            print(max_similarity)
            
            # Apply threshold to classify as "unknown" or a known person
            if max_similarity < threshold:
                final_name = "Unknown"
                attendance_status = ""
            else:
                final_name = encoder.inverse_transform([encoded_labels[predicted_index]])[0]
                attendance_status = "Present"
                
                # Call the attendance function to mark attendance when a person is recognized
                current_date = datetime.now().strftime("%Y-%m-%d")
                attendance_status = check_and_mark_attendance(final_name, current_date)
            
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)

            name_position = (x + w - 100, y - 10)
            cv.putText(frame, final_name, name_position, cv.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0) if final_name != "Unknown" else (0, 0, 255), 2, cv.LINE_AA)
            
            # Attendance status label (bottom-left corner of the face rectangle)
            status_position = (x, y + h + 30)

            # Set the color based on attendance status
            if attendance_status == "Present":
                color = (0, 255, 255)  # Yellow 
            elif attendance_status == "Late":
                color = (0, 255, 0)    # Green
            else:
                color = (0, 0, 255)    # Red

            # Display the attendance status with the chosen color
            cv.putText(frame, attendance_status, status_position, cv.FONT_HERSHEY_SIMPLEX, 
                    1, color, 2, cv.LINE_AA)

        cv.imshow("Face Recognition: ", frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    initialize()
    processing_app()