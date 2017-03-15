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

	
