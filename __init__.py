from flask import Flask #import von Flask
from flask_sqlalchemy import SQLAlchemy #Import von SQLAlchemy -> Datenbank
from os import path
from flask_login import LoginManager

db = SQLAlchemy() #Datenbank von SQLAlchemy
DB_NAME = "database.db" #Parameter der datenbank

UPLOAD_FOLDER = '/path/to/the/uploads' #Upload Folder der Files

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "FITNESSBLOG"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from .views import views #import von view
    from .auth import auth #import von auth

    app.register_blueprint(views, url_prefix="/") #Blueprint von view
    app.register_blueprint(auth, url_prefix="/") #Blueprint von auth

    from .models import User, Post, Comment, File #import der klassen von models

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app) #Login Manager initalisieren

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #User id zuordnen

    return app

#Datenbank erstellen
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!") 
#Datenbank erstellt