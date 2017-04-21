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

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import information


def send_mail(destination_adress, token):
    global mail, mdp
    
    source_address = mail
    body = "Rendez-vous à cette adresse pour créer votre compte utilisateur adresse/"
    subject = "Invitation administrateur CMS TP2"
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source_address
    msg['To'] = destination_address

    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(source_address, mdp)
    text = msg.as_string()
    server.sendmail(source_address, destination_address, text)
    server.quit()
