from flask import Flask
from flask import render_template
from flask import make_response
from flask import g
from flask import request
from flask import redirect
<<<<<<< HEAD
from flask import url_for
=======
>>>>>>> 649670e172753f49a0f1fd93f87121255a0b3343
from database import Database

app = Flask(__name__)


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
    if recherche is None:
        return render_template('404.html'), 404
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


@app.route('/admin-nouveau', methods=['GET','POST'])
def show_new_article_page():
    idu = request.form['idu']
    titre = request.form['titre']   
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date = request.form['date']
    paragraphe = request.form['paragraphe']
    if len(idu) == 0 or len(titre) == 0 or len(identifiant) == 0 or len(auteur) == 0 or len(date) == 0 or len(paragraphe) == 0:
        return render_template('admin-nouveau.html', erreur="Il y a une erreur sur la page")
    else:
        get_db().new_article(idu, titre, identifiant, auteur, date, paragraphe)
        return redirect('/form-merci')


@app.route('/admin-modifier/<identifiant>', methods=['GET', 'POST'])
def show_modifie_article_page(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    return render_template('modifieArticle.html', article=article)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
