from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route('/')
def start_home_page():
    return render_template('accueil.html')

@app.route('/resultat/<recherche>')
def show_result():
    return render_template('resultat.html')

@app.route('/article/<identifiant>')
def show_article():
    return render_template('article.html')

@app.route('/admin')
def show_admin_page():
    return render_template('admin.html')

@app.route('/admin-nouveau', methods=['POST'])
def show_new_article_page():
    return render_template('newArticle.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

