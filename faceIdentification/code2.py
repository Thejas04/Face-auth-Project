import cv2
import os

def face_detection(image_path):
    # Load the face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return faces, image

def process_images():
    # Create a directory to store the captured face images
    os.makedirs('processed_images', exist_ok=True)

    # Create a dictionary to store the ID numbers for each face
    face_ids = {}

    # Get the list of image file paths in the face_images folder
    image_folder = 'face_images'
    image_paths = [os.path.join(image_folder, image_file) for image_file in os.listdir(image_folder) if image_file.endswith('.jpg')]

    # Process each image
    for i, image_path in enumerate(image_paths):
        faces, image = face_detection(image_path)

        # Draw rectangles around the detected faces and assign an ID number
        for (x, y, w, h) in faces:
            face_id = i + 1  # Assign a unique ID number for each face
            face_ids[face_id] = image_path  # Store the image path with the ID number
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, str(face_id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Save the processed image
        cv2.imwrite(os.path.join('processed_images', f'processed_{i}.jpg'), image)

    # Print the ID numbers and corresponding image paths
    for face_id, image_path in face_ids.items():
        print(f'Face ID: {face_id}, Image Path: {image_path}')

# Call the function to process the images
process_images()