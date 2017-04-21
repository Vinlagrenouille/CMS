create table article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication text,
  paragraphe varchar(500)
);

insert into article values (1, 'Être un bon programmeur prend du temps', 'bon-programmeur', 'pro-programmeur', '2017-03-13', 'Sauf exceptions, on ne naît pas programmeur compétent. Au mieux...');
insert into article values (2, 'Être un programmeur rapide', 'rapide-programmeur', 'pro-programmeur', '2017-03-10', 'Sauf exceptions, on ne naît pas programmeur rapide. Au mieux...');
insert into article values (3, 'Être un programmeur gentil prend du temps', 'gentil-programmeur', 'pro-programmeur', '2017-03-09', 'Tous les programmeurs sont par essence, mauvais et méchants, sauf..');
insert into article values (4, 'Comment être un très mauvais programmeur', 'mauvais-programmeur', 'pro-programmeur', '2017-03-11', 'Internet étant présent partout dans nos vies, il est de plus en plus difficile de rester un mauvais programmeur. Ne vous laissez cependant pas abattre...');
insert into article values (5, 'Être un mauvais programmeur mais gagner sa vie quand meme', 'gagner-sa-vie', 'pro-programmeur', '2017-01-01', 'Faites comme tout le monde, faites du front-end en attendant de pouvoir faire du back-end correctement.');
insert into article values (6, 'Coder avec les pieds', 'coder-pieds', 'JJ Jacques', '2017-04-05', 'Prenez vos pieds, posez les sur votre bureau, accrochez-vous à votre chaise, appuyez sur les touches avec votre petit doigt de pied !');
insert into article values (7, 'Mal coder', 'mal-coder', 'pro-programmeur', '2017-02-01', 'Comme dans Call of Duty : ne respectez rien. Aucune convention ou aucune documentation.');
insert into article values (8, 'Être un beau programmeur', 'etre-beau-programmeur', 'Heavy Gunner', '2016-01-01', 'Connaissez-vous pile ou face ? C est la même chose. A votre naissance.');

create table users (
  id integer primary key autoincrement,
  utilisateur varchar(25),
  salt varchar(32),
  hash varchar(128)
  );

create table sessions (
  id integer primary key,
  id_session varchar(32),
  utilisateur varchar(25)
  );

insert into users(utilisateur, salt, hash) values ('correcteur', 'e56373736e7646bd85213083ce9f10bf', 'f265b8a63f4a37faf85088030fb34ddb245e194ca1793965225789a4165d0c48fb6dde55ebba6ee85fd3acbfd5295b322d425c28fee79fa64d7be8ef6fe19a99');
