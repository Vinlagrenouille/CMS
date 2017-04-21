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

# Modified by Vincent Navales

import info_mail

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def send_mail_reinit(destination_address, token):
    source_address = info_mail.mail
    body = "Rendez-vous à cette adresse pour réinitialiser votre mot de passe - localhost:5000/changer-mot-de-passe/" + token
    subject = "Récupération du mot de passe CMS TP2"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source_address
    msg['To'] = destination_address

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(source_address, info_mail.mdp)
    text = msg.as_string()
    server.sendmail(source_address, destination_address, text)
    server.quit()


def send_mail_invite(destination_address, token):
    source_address = info_mail.mail
    body = "Rendez-vous à cette adresse pour vous inscrire en tant qu'admin sur CMS TP2 - localhost:5000/inscription/" + token
    subject = "Invitation au rôle d'admin CMS TP2"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source_address
    msg['To'] = destination_address

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(source_address, info_mail.mdp)
    text = msg.as_string()
    server.sendmail(source_address, destination_address, text)
    server.quit()
