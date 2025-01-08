
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, request, jsonify, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user, current_user, login_required, logout_user , LoginManager


#Configs
app = Flask(__name__, static_url_path='/static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database')

app.config["SECRET_KEY"] = "thisisase"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
#End of models definition
#Code snippets from:https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
#accessed on 22nd decemeber
#Used base login and register feature to add authentication to the app to allow other features
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


#Models definition
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)

class Projects(db.Model):  # Correctly inherit from db.Model
    __tablename__ = 'projects'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    proj_type = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    user = db.relationship('Users', backref='comments')
    project = db.relationship('Projects', backref='comments')
    
with app.app_context():
    db.create_all()


UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.route('/')
#loads template for frontpage as well as display projects
def frontpage():
    projects = Projects.query.all()
    
    return render_template('front-page.html', projects=projects)

#loads template for about
@app.route('/about')
def about():
    return render_template('about.html')

#loads template for projects
@app.route('/projects', methods=['GET', 'POST']) 
def projects():
    projects = Projects.query.all()
    
    # Create a dictionary to store comments organized by project_id
    comments_dict = {}
    
     # Get all comments with their associated users
    comments_query = db.session.query(Comments, Users)\
        .join(Users, Comments.user_id == Users.id)\
        .order_by(Comments.project_id)\
        .all()
    print(comments_query)
    
    # Organize comments by project_id
    for comment, user in comments_query:
        if comment.project_id not in comments_dict:
            comments_dict[comment.project_id] = []
            
        comment_data = {
            'id': comment.id,
            'text': comment.text,
            'username': user.username,
            'user_id': comment.user_id,
            'project_id': comment.project_id
        }
        comments_dict[comment.project_id].append(comment_data)
        
    return render_template('projects.html' , projects=projects,comments=comments_dict)

#Section for uploading photo
#Code adapted from: https://openjavascript.info/2022/06/08/how-to-upload-a-file-using-the-fetch-api/ 
# Accessed on 12/12/2024
# This code allowed me to upload a photo file to the server which has been adapted to link to other projects
@app.route('/upload', methods=['POST']) #Photo upload
def upload_photo():
    if request.method =='POST':
        mrx = request.files['photo_url']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(mrx.filename))
        mrx.save(file_path)
        file_url = f'/static/uploads/{mrx.filename}'
        return jsonify({'file_url': file_url})

#Section for adding projects
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
    
    return jsonify({
        'id': new_project.id,
        'name': new_project.name,
        'proj_type': new_project.proj_type,
        'description': new_project.description,
        'photo_url': new_project.photo_url,
        'link': new_project.link
    })

#section to delete projects
@app.route('/delete_project', methods=['POST'])
def delete_project():
    if request.method =='POST':
        project_id = request.form['project_id']
        project = Projects.query.get(project_id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    else:
        flash('Project not deleted!', 'error')
        return redirect(url_for('projects'))
    
    return redirect(url_for('projects'))  

#a section to add comments
@app.route('/comment', methods=['POST'])
def comment():
    if request.method =='POST':
        if not current_user.is_authenticated:
            flash('You need to be logged in to comment','error')
            return redirect(url_for('projects'))
        
        comment = Comments( 
                            text = request.form['comment'],
                            user_id = current_user.id,
                            project_id = request.form['project_id'])
        
        db.session.add(comment)   
        
        db.session.commit()
        flash('Comment added successfully!', 'success')
    return redirect(url_for('projects'))

#authentication

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        user = Users(username=request.form.get('username'),
                     password=request.form.get('password'))
        
        db.session.add(user)
        
        db.session.commit()
        
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
#End of models definition
#Code snippets from:https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
#accessed on 22nd decemeber
#Used base login and register feature to add authentication to the app to allow other features 
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get('username')).first()
        
        if user.password == request.form.get('password'):
            login_user(user)
            flash('You were successfully logged in!', 'success')
            print('Flashed: success')
            return redirect(url_for('projects'))
        else:
            flash('Login failed! Please check your credentials and try again.', 'error')
            print('Flashed: error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You were successfully logged out!', 'success')
    return redirect(url_for('login'))
#end of authentication


        
if __name__ == '__main__':
    app.run(debug=True)