from . import db  #Datenbank importieren
from flask_login import UserMixin #Managen von Usern  -> Anmelden Abmelden Angemeldet bleiben bei refresh etc.
from sqlalchemy.sql import func


class User(db.Model, UserMixin): #Klasse User/Benutzer db.Models->Hochladen in die Datenbank
    id = db.Column(db.Integer, primary_key=True)#id Kennung der User
    email = db.Column(db.String(150), unique=True) #Eingabe der Email 
    username = db.Column(db.String(150), unique=True)#Eingabe des Benutzer/Usernamens
    password = db.Column(db.String(150))#Passwort des Users
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())#Zeit der Erstellung des Users
    post = db.relationship('Post', backref='user', passive_deletes=True)#Verlinkung der Posts zum User
    comments = db.relationship('Comment', backref='user', passive_deletes=True)#Verlinkung der Kommentare
    file = db.relationship('File', backref='user', passive_deletes=True)#Verlinkung der Files


class Post(db.Model): #Klasse Post hochladen in die Datenbank
    id = db.Column(db.Integer, primary_key=True)#Posts werden dem User zuordnen
    text = db.Column(db.Text, nullable=False)#Text hochladen
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())#Zeitangabe für die erstellung des Posts
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)#Verlinkung zu dem Users/Authors des Posts
    comments = db.relationship('Comment', backref='post', passive_deletes=True)#Kommentare zum Post hinzufügen
    file = db.relationship('File', backref='post', passive_deletes=True)#Files zum Post hinzufügen

class Comment(db.Model): #Klasse Kommentar hochladen in die Datenbank
    id = db.Column(db.Integer, primary_key=True)#Kommentar dem User zuordnen
    text = db.Column(db.String(200), nullable=False)#Text hochladen
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())#Zeitangabe für die erstellung des Kommentars
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)#Verlinkung zum Users/Authors des Kommentars -> ondelete="Casacade" Kommentare werden bei der Löschung des Users ebenfalls gelöscht
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)#Verlinkung auf den Post auf welchen Kommentiert wurde

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)#File wird dem User zugeordnet
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())#Zeitangabe wann der File Hochgeladen wurde
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)#Verlinkung des Users/Authors zu dem Hochgeladenen File
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)#Verlinkung auf den Post auf welchen Kommentiert wurde/ File hochgeladen