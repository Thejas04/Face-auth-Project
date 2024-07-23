from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid

app = Flask(__name__)

def face_detection(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces, image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register-face')
def face():
    return render_template('face.html')

@app.route('/available-users')
def users():
    image_paths = [filename for filename in os.listdir('static/uploads') if filename.endswith('.jpg')]
    return render_template('users.html', image_paths=image_paths)

@app.route('/upload', methods=['POST'])
def upload():
    image_file = request.files['image']
    image_id = str(uuid.uuid4())
    image_path = os.path.join('static/uploads', f'{image_id}.jpg')
    image_file.save(image_path)
    faces, image = face_detection(image_path)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, image_id, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imwrite(image_path, image)
    return redirect(url_for('result', image_id=image_id))

@app.route('/result/<image_id>')
def result(image_id):
    processed_image_path = f'uploads/{image_id}.jpg'
    return render_template('result.html', image_path=processed_image_path, image_id=image_id)

@app.route('/confirmation/<image_id>')
def confirmation(image_id):
    
    face_id = "ABC123"  
    return render_template('confirmation.html', face_id=face_id)

if __name__ == '__main__':
    app.run(debug=True)
