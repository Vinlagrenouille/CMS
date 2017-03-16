from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from Database import Database

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
def show_result(text):
    listArticles = get_db().recherche(text)
    return render_template('resultat.html', listArticles=listArticles)


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


@app.route('/admin-nouveau', methods=['GET', 'POST'])
def show_new_article_page():
    return render_template('nouvelArticle.html')


@app.route('/admin-modifier/<identifiant>', methods=['GET', 'POST'])
def show_modifie_article_page(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('404.html'), 404
    return render_template('modifieArticle.html', article=article)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
