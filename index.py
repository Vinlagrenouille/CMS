#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import abort
from flask import render_template
from flask import make_response
from flask import g
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import Response
from random import randint
from database import Database
import datetime
import json
import sys
import hashlib
import unicodedata
import uuid
from functools import wraps
import gmail

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


def prochain_id():
    prochain = get_db().get_max_id()
    return prochain


def valider_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return render_template("401.html"), 401
        return f(*args, **kwargs)
    return decorated


def valider_form(idu, titre, identifiant, auteur, date, paragraphe):
    erreur = ""
    prochain = get_db().get_max_id()
    if len(idu) == 0 or len(idu) > 2000000000:
        erreur = "Vous devez mettre un identifiant unique, le prochain numéro qui est : " + str(
            prochain[0] + 1) + " par exemple!; "
    if get_db().id_exists(idu):
        erreur = erreur + "Votre identifiant existe dans la base de donnée, vous pouvez utiliser le prochain numéro qui est : " + str(
            prochain[0] + 1) + ".; "
    if len(titre) == 0:
        erreur = erreur + "Vous devez mettre un titre.; "
    if len(titre) > 99:
        erreur = erreur + "Le titre est trop long.; "
    if len(identifiant) == 0:
        erreur = erreur + "Vous devez mettre un identifiant.; "
    if len(identifiant) > 49:
        erreur = erreur + "L'identifiant est trop long.; "
    if get_db().identifiant_exists(identifiant):
        erreur = erreur + "L'identifiant existe, veuillez en choisir un autre.; "
    if len(auteur) == 0:
        erreur = erreur + "Vous devez mettre un auteur.; "
    if len(auteur) > 99:
        erreur = erreur + "Le nom de l'auteur est trop long.; "
    if len(date) == 0 or valider_date(date) == False:
        erreur = erreur + "Vous devez mettre une date au format AAAA-MM-JJ.; "
    if len(paragraphe) == 0:
        erreur = erreur + "Vous devez mettre un paragraphe.; "
    if len(paragraphe) > 499:
        erreur = erreur + "Le paragraphe est trop long.; "
    return erreur


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/', methods=['GET', 'POST'])
def start_home_page():
    articles = get_db().get_5_articles()
    return render_template('accueil.html', articles=articles)


@app.route('/resultat-recherche')
def show_result():
    recherche = request.cookies.get('recherche')
    listArticles = get_db().recherche(recherche)
    return render_template('resultat.html', listArticles=listArticles)


@app.route('/recherche', methods=['POST'])
def donnees_recherche():
    recherche = request.form['recherche']
    response = make_response(redirect('resultat-recherche'))
    response.set_cookie('recherche', recherche)
    return response


@app.route('/article/<identifiant>')
def show_article(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    return render_template('article.html', article=article)


@app.route('/admin')
@authentication_required
def show_admin_page():
    articles = get_db().get_articles()
    return render_template('admin.html', articles=articles)


@app.route('/admin-nouveau')
@authentication_required
def show_new_article_page():
    return render_template('nouvelArticle.html')


@app.route('/envoyer', methods=['GET', 'POST'])
@authentication_required
def envoyer():
    idu = request.form['idu']
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date = request.form['date']
    paragraphe = request.form['paragraphe']
    values = idu, titre, identifiant, auteur, date, paragraphe
    erreur = valider_form(idu, titre, identifiant, auteur, date, paragraphe)
    if erreur != "":
        return render_template('nouvelArticle.html', erreur=erreur, values=values)
    else:
        get_db().new_article(idu, titre, identifiant, auteur, date, paragraphe)
        return redirect('/form-merci')


@app.route('/editer', methods=['GET', 'POST'])
@authentication_required
def editer():
    titre = request.form['titre']
    paragraphe = request.form['paragraphe']
    identifiant = request.form['identifiant']
    get_db().update_article(titre, paragraphe, identifiant)
    return redirect('/form-merci')


@app.route('/form-merci')
def show_merci():
    return render_template('form-merci.html')


@app.route('/admin-modifier/<identifiant>', methods=['GET', 'POST'])
@authentication_required
def show_modifie_article_page(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    return render_template('modifieArticle.html', article=article, identifiant=identifiant)

@app.route('/recuperation')
def show_recuperation_page():
    return render_template('reinitialiserMDP.html')

@app.route('/reinitialisation', methods=['POST'])
def send_recuperation_mail():
    email = request.form['email']
    if email == "":
        return redirect('/recuperation')
    token = uuid.uuid4().hex
    get_db().set_token_for_new_pwd(token, email)

    gmail.send_mail_reinit(email, token)
    
    return redirect('/reinit-merci')

@app.route('/reinit-merci')
def show_reinit_thanks_page():
    return render_template("reinit-merci.html")

@app.route('/inviter-un-admin')
@authentication_required
def show_invite_page():
    return render_template("inviterAdmin.html")

@app.route('/invitation', methods=['POST'])
@authentication_required
def invite_someone():
    email = request.form['email']
    if email == "":
        return redirect('/inviter-un-admin')
    token = uuid.uuid4().hex
    get_db().set_token_to_invite(token, email)
    
    gmail.send_mail_invite(email, token)
    
    return redirect('/admin')
                            
@app.route('/inscription/<token>', methods=["GET", "POST"])
def change_password(token):
    if request.method == "GET":
        return render_template("inscription.html")
    else:
        utilisateur = request.form["utilisateur"]
        mdp = request.form["mdp"]
        if mdp == "" or utilisateur == "":
            return render_template("inscription.html", error="Tous les champs sont obligatoires.")
        salt = uuid.uuid4().hex
        hashed = hashlib.sha512(mdp+salt).hexdigest()
        get_db().confirm_inscription(token, utilisateur, salt, hashed)
        
        return redirect("/connexion");
                                                                    
@app.route('/changer-mot-de-passe/<token>', methods=["GET", "POST"])
def new_password(token):
    if request.method == "GET":
        return render_template("nouveauMDP.html")
    else:
        mdp = request.form["mdp"]
        if mdp == "":
            return render_template("nouveauMDP.html", error="Veuillez rentrer un mot de passe")
        salt = uuid.uuid4().hex
        hashed = hashlib.sha512(mdp+salt).hexdigest()
        get_db().change_password(token, salt, hashed)

        return redirect("/nouveau-mot-de-passe-valide");

@app.route('/nouveau-mot-de-passe-valide')
def show_pwd_valid():
    return render_template("confirm-merci.html")

@app.route('/connexion')
def show_connexion_page():
    if "id" in session:
        return redirect("/admin")
    return render_template('connexion.html')
    
@app.route('/validation', methods=['POST'])
def connect():
    utilisateur = request.form['utilisateur']
    mdp = request.form['mdp']

    if utilisateur == "" or mdp == "":
        return redirect("/connexion")
    
    user = get_db().get_user_login_info(utilisateur)
    if user is None:
        return redirect("/connexion")

    salt = user[0]
    hashed_password = hashlib.sha512(mdp + salt).hexdigest()
    if hashed_password == user[1]:
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, utilisateur)
        session['id'] = id_session
    return redirect("/admin")

@app.route('/admin-inscription/<token>', methods=['GET', 'POST'])
@authentication_required
def sign_up(token):
    user = get_db().get_user_by_token(token)
    if user is None:
        return render_template('404.html'), 404
    #return render_template('inscription.html', user = user))

@app.route('/deconnexion')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")

@app.route('/api/articles/', methods=["GET"])
def liste_articles():
    if request.method == "GET":
        articles = get_db().get_articles()
        data = [{"titre": each[1], "identifiant": 'http://127.0.0.1:5000/article/'+each[2], "auteur": each[3]} for each in articles]
        return jsonify(data)

@app.route('/api/article/<identifiant>', methods=["GET"])
def get_all_data_article(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    else:
        data = [{"id": article[0], "titre": article[1], "identifiant": article[2], "auteur": article[3], "date_publication": article[4], "paragraphe": article[5]}]
        return jsonify(data)   

@app.route('/api/article/nouveau/', methods=["POST"])
def nouvel_article():
    data = request.get_json()
    data_en_json = json.loads(data)
    if not request.json or get_db().identifiant_exists(data_en_json['identifiant']) or get_db().id_exists(data_en_json['id']):
        abort(400)
    else:
        article = get_db().new_article(data_en_json['id'], data_en_json['titre'], data_en_json['identifiant'], data_en_json['auteur'], data_en_json['date_publication'], data_en_json['paragraphe'])
    return "", 201

@app.route('/batir-ident/<identifiant>', methods=["GET"])
def verifier_identifiant(identifiant):
    identifiant_existe = get_db().identifiant_exists(identifiant)
    if identifiant_existe == True:
        return identifiant + str(randint(0,9999))
    else:
        return enlever_accents(identifiant)

def enlever_accents(identifiant):
    string_replaced = unicodedata.normalize('NFKD', identifiant).encode('ASCII', 'ignore')
    return string_replaced

def is_authenticated(session):
    return "id" in session

def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 40
4

app.secret_key = "H\x9e\xbf3?\x9fR\xea\x9a\xa4dte{\xbfLB]\xb2\xa1\xa4\x1f3&"

