# Projet Bot Discord B2

Ce projet consiste à créer un bot Discord doté de plusieurs fonctionnalités telles qu'un historique des commandes, un système de questionnaire, une protection de l'historique, etc.

Les consignes sont à retrouver [ici](https://github.com/LordPouic/Python/blob/main/Projet%20Bot%20B2)


## Table des matières
- [Fonctionnalité de base](#fonctionnalité-de-base)
- [Installation](#installation)
- [Chemin de l'arbre de réponse](#chemin-de-larbre-de-réponse)
- [Fonctionnalité Bonus](#fonctionnalité-bonus)
- [Auteur](#auteur)
- [Commandes](#commandes)
- [ToDo](#todo)

## Fonctionnalité de base


- Stocker l'historique des commandes via une liste chaînée   [Working]
- Via une file, créer un systeme permettant de protéger l'intégrité de l'historique
- Via un arbre binaire , créer un système de discution  [Working]
- Via une hashtable, stocker soit l'historique
- Sauvegarde des données du bot dans un Historique [Working]

## Installation

Pour utiliser ce bot Discord, veuillez suivre les étapes suivantes :

1. Clonez le dépôt GitHub sur votre ordinateur
2. Créez un fichier `.env` à la racine du projet contenant votre token Discord
3. Dans le fichier `.env` ajouter une variable et y ajouter le token du bot
4. Lancez le script pour lancer le bot


## Commandes

### Commandes le l'arbre :

- `/chatbot` : lance la conversation avec le bot
- `reset` : permet de recommencer la discussion , doit être écris quand le bot est en mode "chatbot"
- `/speakabout` : permet de savoir si un sujet est traité par le bot ou non ( le système fonctionne par mot clé )
- Sujet actuelement écris : Python , Ecla 

#### Chemin de l'arbre de réponse

Le bot utilise un arbre binaire pour poser une série de questions prédéfinies à l'utilisateur afin de définir son besoin. 


![Image Arbre](./image/Arbre.PNG)

### Commandes de l'historique

/historique ( affiche l'historique ) 

/delete_historique ( Efface l'historique en entier )

/delete_last ( efface la derniere commande , ne fonctionne que s'il y a plus d'un élément dans l'historique ) 

/last_command2 ( affiche la derniere commande rentré )

/last_command ( permet de voyagé entre les commandes de l'historique ) [ Not Working ]

### HashTable

/conversation    ( Permet d'afficher l'historique de conversation du user ) 

### Commandes pour la sauvegarde des données

/savedata  Permet de sauvegardé les data des users ( leurs historiques ) dans un fichier JSON

/loaddata Permet de charger les données depuis le fichier JSON


## Fonctionnalité Bonus

/heure  ( affiche l'heure actuelle )

/setup  ( Permet de modifier le prefix du bot )

/commande_liste ( Affiche la liste des commandes actuellement disponible )


/delete ( Permet d'efface X message, limité à 10 pour des raisons de sécurité ) 


### Data

/savedataauto  Permet de sauvegardé les données jusqu'à avoir atteint la data spécifié



### Jeu

/pendu 

/chifoumi 

/plus_ou_moins


### Commande de l'API
Communication avec une API d'une base de données de mangas/manwha

/randommangas   - Pour avoir un mangas/manwha aléatoire

/mangaapi       - Pour avoir des informations sur un mangas spécifié 

### Only Admin

/sync  ( Permet de uploadé les commandes du bot instantanément sans attendre, doit être combiné à un CTRL+R sur discord pour tout mettre à jour )

## ToDo
- Le bot dispose également d'un système de protection de l'historique via une file. Pour éviter que plusieurs personnes travaillent sur l'historique simultanément, l'accès à l'historique est limité à une seule personne à la fois.



## Auteur

Ce projet a été créé et d&veloppé par Alessandro FARAJALLAH.

