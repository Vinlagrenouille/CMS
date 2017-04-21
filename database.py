# coding: utf8

# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where identifiant = :identifiant", {"identifiant": identifiant})
        article = cursor.fetchone()
        return article

    def get_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article")
        articles = cursor.fetchall()
        return articles

    def get_max_id(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select max(id) from article")
        max_id = cursor.fetchone()
        return max_id

    def id_exists(self, idu):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where id = :idu", {"idu": idu})
        if cursor.fetchone() != None:
            return True
        else:
            return False

    def identifiant_exists(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where identifiant = :identifiant", {"identifiant": identifiant})
        if cursor.fetchone() != None:
            return True
        else:
            return False

    def get_5_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where date_publication < date('now')")
        articles = cursor.fetchmany(5)
        return articles

    def update_article(self, titre, paragraphe, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("update article set titre = :titre, paragraphe = :paragraphe where identifiant = :identifiant",
                       {"titre": titre, "paragraphe": paragraphe, "identifiant": identifiant})
        self.get_connection().commit()
        return

    def new_article(self, idu, titre, identifiant, auteur, date_publication, paragraphe):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "insert into article values(:idu, :titre, :identifiant, :auteur, :date_publication, :paragraphe)",
            {"idu": idu, "titre": titre, "identifiant": identifiant, "auteur": auteur,
             "date_publication": date_publication, "paragraphe": paragraphe})
        self.get_connection().commit()
        return

    def recherche(self, text):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "select titre, identifiant, date_publication from article where titre like '%' || :text || '%' or  paragraphe like '%' || :text || '%'",
            {"text": text})
        listArticles = cursor.fetchall()
        return listArticles

    def create_user(self, username, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute(("insert into users(utilisateur, email, salt, hash)"
                            " values(?, ?, ?, ?)"), (username, email, salt,
                                                     hashed_password))
        connection.commit()

    def set_token_for_new_pwd(self, token, email):
        connection = self.get_connection()
        connection.execute('update users set token=:token where email=:email', {"token":token, "email":email})
        connection.commit()
        
    def change_password(self, token, salt, hash):
        connection = self.get_connection()
        connection.execute("update users set hash = :hash, salt = :salt, token = '' where token = :token", {"hash":hash, "salt":salt, "token":token})
        connection.commit()
    
    def get_user_login_info(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash from users where utilisateur=?"),
                    (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]
    
    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("insert into sessions(id_session, utilisateur) "
                            "values(?, ?)"), (id_session, username))
        connection.commit()
        
    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session,))
        connection.commit()
        
    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select utilisateur from sessions where id_session=?"),
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
        
