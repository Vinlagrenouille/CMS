#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import make_response
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from database import Database
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)

def prochain_id():
    prochain = get_db().get_max_id()
    return prochain

def valider_form(idu, titre, identifiant, auteur, date, paragraphe):
    erreur = ""
    prochain = get_db().get_max_id()
    if len(idu) == 0 or len(idu) > 2000000000:
        erreur= "Vous devez mettre un identifiant unique, le prochain numéro qui est : " + str(prochain[0]+1) + " par exemple! "
    if get_db().id_exists(idu):
        erreur = erreur + "Votre identifiant existe dans la base de donnée, vous pouvez utiliser le prochain numéro qui est : " + str(prochain[0]+1) + ". "
    if len(titre) == 0:
        erreur= erreur + "Vous devez mettre un titre. "
    if len(titre) > 99:
        erreur= erreur + "Le titre est trop long. "
    if len(identifiant) == 0:
        erreur= erreur + "Vous devez mettre un identifiant. "
    if len(identifiant) > 49:
        erreur= erreur + "L'identifiant est trop long. "        
    if  len(auteur) == 0:
        erreur= erreur + "Vous devez mettre un auteur. "
    if len(auteur) > 99:
        erreur= erreur + "Le nom de l'auteur est trop long. "
    if len(date) == 0: 
        erreur= erreur + "Vous devez mettre une date au format AAAA-MM-JJ. "
    # if date[4:-5] != "-" or date[8:-2] != "-":
    #     erreur= erreur + "Vous devez mettre une date au format AAAA-MM-JJ. "
    if len(paragraphe) == 0:
        erreur= erreur + "Vous devez mettre un paragraphe."
    if len(paragraphe) > 499:
        erreur= erreur + "Le paragraphe est trop long. "
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
def show_admin_page():
    articles = get_db().get_articles()
    return render_template('admin.html', articles=articles)


@app.route('/admin-nouveau')
def show_new_article_page():
    return render_template('nouvelArticle.html')


@app.route('/envoyer', methods=['GET','POST'])
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
def show_modifie_article_page(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    return render_template('modifieArticle.html', article=article, identifiant=identifiant)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404