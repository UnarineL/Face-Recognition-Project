import webbrowser
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faces.db'
db = SQLAlchemy(app)

class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image_path = db.Column(db.String(200))  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_face', methods=['POST'])
def add_face():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        image = request.files['image']

        if not all([name, address, mobile_number, email, image]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        existing_face = Face.query.filter((Face.name == name) | (Face.email == email)).first()
        if existing_face:
            flash('Profile already exists', 'error')
            return redirect(url_for('index'))

        image_path = save_image(image)
        new_face = Face(name=name, address=address, mobile_number=mobile_number, email=email, image_path=image_path)
        db.session.add(new_face)
        db.session.commit()

        flash('Face data added successfully', 'success')
        return redirect(url_for('faces'))

@app.route('/faces')
def faces():
    stored_faces = Face.query.all()
    return render_template('faces.html', faces=stored_faces)

def save_image(image):
    os.makedirs('static/faces/', exist_ok=True)
    image_path = 'static/faces/' + image.filename
    image.save(image_path)
    return image_path

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.secret_key = 'super_secret_key'
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)
    
