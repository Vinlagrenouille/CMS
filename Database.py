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
        cursor.execute("select * from article where identifiant = :identifiant", {"identifiant":identifiant})
        article = cursor.fetchone()
        return article

    # def get_article(self):
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("select * from article")
    #     articles = cursor.fetchall()
    #     return [article[0] for article in articles]

    def get_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article")
        articles = cursor.fetchall()
        return articles

    def get_5_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where date_publication < date('now')")
        articles = cursor.fetchmany(5)
        return articles

    def update_article(self, titre, paragraphe, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("update article set titre = :titre and paragraphe = :paragraphe where identifiant = :identifiant", {"titre":titre, "paragraphe":paragraphe, "identifiant":idenfiant})
        return
