#API/Interface programmable du CMS 

#ADRESSE DE BASE DU SITE
Dans les exemples ci-dessous se trouvent l'adresse du site telle que prévue par défaut par Flask.
Bien sûr, si vous deviez avoir une autre adresse locale, vous devez remplacer http://127.0.0.1:5000 par votre adresse locale.

#OBTENIR TOUS LES ARTICLES
- L'adresse permettant d'obtenir tous les articles en JSON est la suivante : http://127.0.0.1:5000/api/articles/
La méthode "GET" est à utiliser ici. Une méthode POST vous affichera une erreur "405 METHOD NOT ALLOWED".
Cette adresse permet d'obtenir l'auteur, l'identifiant unique de l'article ainsi que son titre.

#OBTENIR UN ARTICLE PAR SON IDENTIFIANT
- Utilisez l'adresse suivante : http://127.0.0.1:5000/api/article/<identifiant>
Vous veillerez à remplacer <identifiant> dans l'adresse ci-dessus par l'identifiant unique de votre article. Par exemple "bon-programmeur", sans les guillemets.
Si jamais vous deviez entrer un mauvais identifiant, vous obtiendrez une erreur 404.
La méthode "GET" est à utiliser ici. Une autre méthode vous affichera une erreur "405 METHOD NOT ALLOWED".

#POSTER UN NOUVEL ARTICLE
- Utilisez l'adresse suivante : http://127.0.0.1:5000/api/article/nouveau/
La méthode "PUT" est à utiliser ici. Une autre méthode vous affichera une erreur "405 METHOD NOT ALLOWED".

Vous obtiendrez une réponse 400 si :
- L'identifiant, après "identifiant", n'est pas unique
- Ou l'id, après "id" n'est pas unique 
- Ou si la requête JSON n'est pas valide.

Vous veillerez à utiliser le header suivant : "Content-Type: application/json". 

Votre corps doit contenir les éléments suivants, dans l'ordre et au format JSON :
'{"id": "1", "titre": "Le titre de votre choix", "identifiant": "identifiant-de-votre-choix", "auteur": "L'auteur souhaité", "date_publication": "AAAA-MM-JJ", "pararaphe": "Un paragraphe agréable à lire"}'

Sous Windows, si vous n'utilisez pas CygWin, il est probable que vous ayez à utiliser les caractère d'"escape" en formattant votre requète de la manière suivante :
'{\"id\": \"101\", \"titre\": \"Ayez foi en Clean Code\",\"identifiant\": \"clean-code\",\"auteur\": \"Bucket Head\",\"date_publication\": \"2017-04-01\",\"paragraphe\": \"Il est temps de devenir un meilleur programmeur en faisant marcher ses neurones\"}'

On peut voit ici que les guillemets à l'intérieur des accolades doivent tous avoir un backslash avant.

Enfin, nous avons fait des tests avec curl sous CygWin, Advanced Rest Client sous Chrome.

Une requête curl sous Cygwin ressemble à ceci :
curl -i -H "Content-Type: application/json" -X POST -d '{"id": "101", "titre": "Ayez foi en Clean Code","identifiant": "clean-code","auteur": "Bucket Head","date_publication": "2017-04-01","pararaphe": "Il est temps de devenir un meilleur programmeur en faisant marcher ses neurones"}' http://127.0.0.1:5000/api/articles/nouveau/

Bonnes requêtes !