from flask import Blueprint, render_template, request, flash, redirect, url_for #Flask implementation hinzugefügt
from flask_login import login_required, current_user #Import von flask_login mit den Eigenschaften Login_required und current_user ->Um die Funktionen nutzen zu können
from importlib_metadata import files
from .models import Post, User, Comment, File #Import der Klassen
from . import db #Import von Datenbank
import os
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)


#Homepage Anzeigen lassen website/home
@views.route("/")
@views.route("/home")#website/home
@login_required #Login wird für def home benötigt / Um auf die Seite FitnessBlogeintrag erstellen zu kommen
def home():
    posts = Post.query.all() #posts werden hinzugefügt
    return render_template("home.html", user=current_user, posts=posts) #nach Erstellung des Posts gehe zu homepage/home


@views.route("/create-post", methods=['GET', 'POST']) #Blogeintrag erstellen/ GET da Blogeinträge vom Server abgerufen werden sollen, von anderen Nutzer POST um die HTML Daten an den Server zu senden 
@login_required #Posts können nur von eingelogden Usern verfasst werden
def create_post():
    if request.method == "POST": 
        text = request.form.get('text') #Post besteht nur aus Text

        if not text:
            flash('Fitness Blogeintrag kann nicht leer sein!', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)#Post auf die Datenbank hochladen
            db.session.commit() #Post Hochgeladen
            flash('Fitnessblogeintrag erstellt!', category='success') #Nachricht das der Vorgang funktioniert hat -> success
            return redirect(url_for('views.home'))#Nach upload kehre auf Homepage zurück

    return render_template('create_post.html', user=current_user)


#Blogeintrag Löschen, aber nur seine Eigenen
@views.route("/delete-post/<id>")
@login_required #Posts können nur von angemeldeten Usern gelöscht werden
def delete_post(id):
    post = Post.query.filter_by(id=id).first() #Post.id, filtern welcher Post zu welchem User gehört

    if not post:
        flash("Blogeintrag exsistiert leider nicht!", category='error') #Man kann nur Blogeinträge löschen welche exsitieren
    elif current_user.id != post.id:
        flash('Leider kannst du diesen Blogeintrag nicht löschen', category='error') #Wenn man versucht einen Posteintrag von einem anderen User zu Löschen
    else:
        db.session.delete(post)
        db.session.commit()#Blogeintrag aus der Datenbank Löschen
        flash('Blogeintrag gelöscht!', category='success') #Ausgabe das das Löschen erfolgreich war

    return redirect(url_for('views.home'))

#Username anzeigen welcher den Post verfasst haben/ Anzeigen welche Posts dieser User gepostet hat
@views.route("/posts/<username>")
@login_required #User muss angemeldet sein
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Leider exsistiert kein User mit diesem Namen', category='error') #Suche nach post von Usern die nicht exsistieren
        return redirect(url_for('views.home')) #auf Homepage zurückkehren

    posts = user.posts #Nach Posts von Username filtern
    return render_template("posts.html", user=current_user, posts=posts, username=username) #Geht auf eine Seite welche alle Posts des Users anzeigt

#Kommentar auf einen FitnessBlogeintrag erstellen
@views.route("/create-comment/<post_id>", methods=['POST']) #Kommentar erstellen zugeordet an den User POST Kommentar html wird an den Server gesendet
@login_required #User muss angemeldet sein
def create_comment(post_id): #Kommentar mit dem Post verlinken
    text = request.form.get('text') #Form des Kommentars ist Text 

    if not text:
        flash('Kommentar darf nicht leer sein!', category='error') #Wenn der Kommentar leer ist
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id) #Wenn der Kommentar nicht leer ist
            db.session.add(comment)#Kommentar dem Server hinzufügen
            db.session.commit()#Kommentar wird hochgeladen
        else:
            flash('Blogeintrag exsistiert nicht', category='error')#Wenn der Blogeintrag nicht exsistiert, Error Meldung

    return redirect(url_for('views.home')) #nach erstellen des Kommentars/oder bei Fehlermeldung kehre auf Homepage zurück

#Eigenen Kommentar Löschen
@views.route("/delete-comment/<comment_id>") #Kommentar_id
@login_required#User muss angemeldet sein
def delete_comment(comment_id): #Kommentar identifizieren -> id
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Kommentar exsistiert leider nicht!', category='error') #Error meldung falls der Kommentar nicht exsistiert
    elif current_user.id != comment.author and current_user.id != comment.post.author: #Wenn man den Kommentar eines anderen Users Löschen möchtest
        flash('Leider kannst du diesen Kommentar nicht löschen.', category='error') #Meldung das du diesen Kommentar nicht löschen kannst Error
    else:
        db.session.delete(comment) #Kommentar aus dem server Löschen
        db.session.commit()#Kommentar gelöscht

    return redirect(url_for('views.home')) #Kehrt nach Homepage zurück

#File hinzufügen zum Kommentar
@views.route("/create-file/<post_id>", methods=['POST', 'GET'])
@login_required
def create_file(post_id):
    if 'file' not in request.files:
            flash('Kein Bild!')
            return redirect(url_for('views.home'))
        
    if files.filename == '':
            flash('Es wurde kein Bild hochgeladen')
            return redirect(url_for('views.home'))
    if files(files.filename):
            filename = secure_filename(files.filename)
            files.save(os.path.join(views.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('views.home', name=filename))