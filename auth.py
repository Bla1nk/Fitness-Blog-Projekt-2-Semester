from flask import Blueprint, render_template, redirect, url_for, request, flash #Import der Flaskopperatoren
from . import db #Import der Datenbank
from .models import User #Import der User Klasse
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST']) #Login/ GET da Userdaten vom Server abgerufen werden sollen POST um die HTML Daten an den Server zu senden 
def login():
    if request.method == 'POST': 
        email = request.form.get("email")
        password = request.form.get("password") #User besitzen Email sowie Passwort 

        user = User.query.filter_by(email=email).first() #nach vorhanden Email adressen filtern
        if user:
            if check_password_hash(user.password, password): #Wenn das Passwort zu der Email passt
                flash("Sie sind jetzt Angemeldet!", category='success') #User eigeloged ->Success
                login_user(user, remember=True)
                return redirect(url_for('views.home'))#kehrt zur Homepage zurück
            else:
                flash('Password is incorrect.', category='error')#Flasches Passwort -> error
        else:
            flash('Email does not exist.', category='error') #Email nicht in der Datenbank gefunden -> error

    return render_template("login.html", user=current_user) #Kehrt zum Login Seite zurück


@auth.route("/sign-up", methods=['GET', 'POST'])#Signup, User erstellen/ GET da Userdaten vom Server abgerufen werden sollen POST um die HTML Daten an den Server zu senden 
def sign_up():
    if request.method == 'POST': 
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")  #Abfrage nach Email Usrname Passwort sowie Passwort wiederholen

        email_exists = User.query.filter_by(email=email).first() #wenn die email bereits einem anderen User hinzugefügt wurde
        username_exists = User.query.filter_by(username=username).first()
         #Wenn der Username bereits einem anderen User zugeordnet ist

        if email_exists:#wenn die email bereits exsistiert 
            flash('Email wird bereits benutzt', category='error') #->error
        elif username_exists: #wenn der Username bereits exsistiert 
            flash('Username ist leider schon vergeben', category='error') #-> error
        elif password1 != password2:#Wenn Passwort 1 nicht identisch dem 2ten Passwort ist 
            flash('Passwörter sind leider nicht identisch!', category='error') #-> error
        elif len(username) < 5:
            flash('Username ist zu kurz', category='error') #Wenn der username kürzer als 5 ist ->error
        elif len(password1) < 6: #Wenn das passwort kürzer als 6 ist
            flash('Passwort ist zu kurz', category='error') # ->error
        elif len(email) < 4:#wenn die email kürzer als 4 ist
            flash("Email exsistiert nicht", category='error')#->error
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)#User wird der datenbank hinzugefügt
            db.session.commit()#Auf Datenbank hochgeladen
            login_user(new_user, remember=True) #User wurde erstellt
            flash('Benutzer wurde erstellt!')
            
            return redirect(url_for('views.home')) #kehrt auf Homepage zurück

    return render_template("signup.html", user=current_user) #Bei error kehrt wieder zur Sign-up Page /User erstellen Seite zurück

#Auslogen von User
@auth.route("/logout")
@login_required#User muss eingeloged sein
def logout():
    logout_user()#User wird ausgeloged
    return redirect(url_for("views.home")) #kehrt zur Homepage zurück

