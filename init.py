from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from flask import url_for, render_template
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import List
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projects')

db = SQLAlchemy(app)

class Projects(db.Model):  # Correctly inherit from db.Model
    __tablename__ = 'projects'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    proj_type = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    link = db.Column(db.String(200), nullable=True)

#upload folder

UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upload', methods=['POST']) #Photo upload
def upload_photo():
    if request.method =='POST':
        mrx = request.files['photo_url']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(mrx.filename))
        mrx.save(file_path)
        file_url = f'/static/uploads/{mrx.filename}'
        return jsonify({'file_url': file_url})
       

@app.route('/')
#loads template for frontpage as well as display projects
def frontpage():
    class Projects:
        def __init__(self, id, name, proj_type, photo_url, description, link):
            self.id = id
            self.name = name
            self.proj_type = proj_type
            self.photo_url = photo_url
            self.description = description
            self.link = link   
    
    sql = f"SELECT * FROM projects"
    sql = text(sql)
    
    
            
    result = db.engine.connect().execute(sql)
    projects = []
    
    for row in result:
        projects.append(Projects(row[0],row[1], row[2], row[3], row[4], row[5]))
        
    return render_template('front-page.html', projects=projects)


@app.route('/projects', methods=['GET', 'POST'])

    
def projects():
    class Projects:
        def __init__(self, id, name, proj_type, photo_url, description, link):
            self.id = id
            self.name = name
            self.proj_type = proj_type
            self.photo_url = photo_url
            self.description = description
            self.link = link   
    
    sql = f"SELECT * FROM projects"
    sql = text(sql)
    
    
            
    result = db.engine.connect().execute(sql)
    projects = []
    
    for row in result:
        projects.append(Projects(row[0],row[1], row[2], row[3], row[4], row[5]))
        
    return render_template('projects.html' , projects=projects)

@app.route('/add_project', methods=['POST'])

    
def add_project():
    obj = request.json
    print(obj)
    new_project = Projects(
    name=obj['name'],
    proj_type=obj['proj_type'],
    description=obj['description'],
    photo_url=obj['photo_url'],
    link=obj['proj_link'])
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': 'Project added successfully'}), 201
    

@app.route('/login')
def login():
    return render_template('login.html')


        
if __name__ == '__main__':
    app.run(debug=True)