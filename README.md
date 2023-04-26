Le projet ainsi que le readme ne sont pas du tout terminés.

# Projet de bot Discord pour l'école

![Bot Discord](/image/ppdiscord%20-%20Copie.PNG)

Ce projet est un bot Discord développé en Python pour un projet d'école. Le bot dispose de plusieurs fonctionnalités, dont :

- Système d'historique avec une liste doublement chainée
- Système de sauvegarde des commandes dans un fichier JSON
- Mini-jeux tels que Chifoumi, Pendu et Plus ou Moins
- Possibilité de changer manuellement la langue et le préfixe du bot

## Installation

Pour installer le bot Discord, vous devez :

1. Cloner le projet : `git clone https://github.com/aless124/Discord_Bot.git`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Créer un fichier `.env` avec les informations suivantes :

DISCORD_TOKEN ="VotreTokenDeBot"
DISCORD_ID = "VotreIdDiscord"

## Utilisation

Pour utiliser le bot Discord, vous pouvez utiliser les commandes suivantes :

    !help : affiche la liste des commandes disponibles
    !language [lang] : change la langue du bot (par défaut : fr)
    !prefix [prefix] : change le préfixe du bot (par défaut : !)
    !history : affiche l'historique des commandes
    !play [game] : joue à un mini-jeu (Chifoumi, Pendu ou Plus ou Moins)

## Auteur

Ce projet a été réalisé par Alessandro FARAJALLAH en B2A informatique


## ToDo

Fonctionnalité du bot 

1 - Via une liste chainée, une pile ou une file, créer un système de d'historique des commandes de votre bot. Ce système devra avoir comme fonctionnalités :

    - de quoi voir la dernière commande rentrée
    
    - de quoi voir toutes les commandes rentrée par un utilisateur depuis sa première connexion
    
    - de quoi se déplacer dans cet historique (en avant et en arrière)
    
    - de quoi vider l'historique

2.

[x] Option pour changer le prefix

[x] Arbre binaire de réponse ( pour faire un chatbot )

[ ] Emoji pour voyager dans son historique

[x] Les jeux pour jouer avec le bot

[x] Stockage des infos par utilisateur  

[ ] Via une file, créer un systeme permettant de protéger l'intégrité de l'historique, pour cela il faudra trouver un moyen de limiter l'accès à l'historique pour qu'une seule personne à la fois ne puisse travailler dessus.

[ ] Utiliser date pour faire calendrier - rappel 

[x]  Trouver une solution afin que lorsque que le bot s'arrête ses données stockées dans les différentes structures et collections crées précédement se soient pas perdues.

[ ] Trouver moyen de faire tourner constamment le bot

[ ] Connecter bot à une api
NOTE :
Problème :
Fix delete_at_end

/!\ Fix delete_history = delete_at_end

Note for later :

interaction.followup.send() should be used instead of send_message()



