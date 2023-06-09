# region import

from datetime import datetime, timedelta
from pymongo import MongoClient
import pymongo
import uuid
import time
import classe.Liste as Liste
import classe.Queue as Queue
import classe.Arbre as Arbre
import classe.hash as Hash
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time
import asyncio
from random import randint
import requests
import json
# endregion


# region variable
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID = os.getenv('DISCORD_ID')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
API_KEY = os.getenv('API_KEY')
intents = discord.Intents.default()
intents = intents.all()
client = discord.Client(intents=intents)


# Global Variable
bot = app_commands.CommandTree(client)
MyConversation = Hash.Hashtable([("User", ["Content"])])

Dictionnaire_User = {}
FILENAME = "Projet_DiscordBotPy\json\data.json"
prefix = ";"
LockSystem = False

SaveArbre = Arbre.T

# endregion

# region Json

# Ouvrir le fichier JSON et charger son contenu

# Fonction pour sauvegarder les données dans le fichier JSON


def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f)

# Fonction pour charger les données depuis le fichier JSON


def load_data():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, renvoyer un dictionnaire vide
        print("Le fichier n'existe pas encore.")
        return {}


# test
# Enregistrer des données
'''
my_data = {"users": ["Alice", "Bob", "Charlie","test"]}
save_data(my_data)
# Charger des données
loaded_data = load_data()
print(loaded_data)  # {'users': ['Alice', 'Bob', 'Charlie']}
'''
# endregion

# region app command
# Bot Commands


@bot.command(name="savedata", description="Save the data in the json file")
async def savedata(ctx):
    await ctx.response.send_message("Saving data...")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Data = {ctx.user.id: Dictionnaire_User[ctx.user.id].Display()}
    save_data(Data)
    await ctx.channel.send("Data saved !")


@bot.command(name="savedataauto", description="save data during a certain time")
async def save_data_auto(ctx, hour_of_ending: int, day_of_ending: int):
    Hour = datetime.now().strftime('%H')
    Jour = datetime.now().strftime('%d')
    Jour = int(Jour)

    await ctx.response.send_message("Saving data")

    while day_of_ending != Jour:
        if ctx.user.id not in Dictionnaire_User.keys():
            Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
            print("User added to the dictionary")

        Data = {ctx.user.id: Dictionnaire_User[ctx.user.id].Display()}
        save_data(Data)
        await asyncio.sleep(10)

    if day_of_ending == Jour:
        while int(Hour) != int(hour_of_ending):
            if ctx.user.id not in Dictionnaire_User.keys():
                Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
                print("User added to the dictionary")

            Data = {ctx.user.id: Dictionnaire_User[ctx.user.id].Display()}
            save_data(Data)
            await asyncio.sleep(10)

    await ctx.channel.send("Data saved !")


@bot.command(name="loaddata", description="Load the data from the json file")
async def loaddata(ctx):
    await ctx.response.send_message("Loading data...")
    Data = load_data()
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()

    if Data[str(ctx.user.id)] == None:
        await ctx.channel.send("No data to load")
        return
    else:
        for i in Data[str(ctx.user.id)]:
            Dictionnaire_User[ctx.user.id].InsertToEnd(i)

    await ctx.channel.send("Data loaded !")


@bot.command(name="delete")
async def delete(ctx, nbr_msg: int):
    nbr_msg += 1  # On ajoute 1 pour compter le message de la commande
    if nbr_msg > 11:
        await ctx.followup.send("You can only purge 10 messages at a time.")
        return
    elif nbr_msg < 1:
        await ctx.followup.send("You need to purge at least one message.")
        return
    else:
        await ctx.response.defer()
        # Attente de 1 seconde pour permettre à Discord de s'adapter
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=nbr_msg)
        # await ctx.chan.send_message("Deleted {nbr_msg} messages.")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[ctx.user.id].InsertToEnd("delete")


@bot.command(name="heure")
async def Heure(ctx):
    await ctx.response.send_message(f"il est {datetime.now().strftime('%H:%M:%S')}")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[ctx.user.id].InsertToEnd("Heure")


@bot.command(name="setup", description="Setup the hello command")
async def hello_setup(ctx):
    global prefix
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("setup")
    await ctx.response.send_message("Bonjour ! Hi ! \n Please choose a language \n ( French 1 , English 2 )")
    msg = await client.wait_for('message')
    if msg.content == '1':
        Language = "Français"
        await ctx.channel.send(f'Merci {msg.author}! {Language} choisi !')
    elif msg.content == '2':
        Language = "English"
        await ctx.channel.send(f'thanks {msg.author}! {Language} choosen !')
    else:
        Language = "language set to English ( default) due to wrong input"
        await ctx.channel.send(f'{msg.author}! {Language} choosen !')
        Language = "English"

    await ctx.channel.send("Please choose a prefix \n ( default : ; ) \n Actual prefix : " + prefix)

    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check)

    while len(msg.content) == 1 and msg.content.isalnum() and Language == "Français":
        await ctx.channel.send("Le caractère entré est une lettre ou un chiffre. Vous ne pouvez choisir qu'un charactère special \n exemple : !, #, $, %, &, /, (, ), =, +, -, *, @, etc.")
        msg = await client.wait_for('message', check=check)
        time.sleep(1)
    while len(msg.content) == 1 and msg.content.isalnum() and Language == "English":
        await ctx.channel.send("The character entered is a letter or a number. You can only choose a special character \n example : !, #, $, %, &, /, (, ), =, +, -, *, @, etc.")
        msg = await client.wait_for('message', check=check)
        time.sleep(1)

    prefix = msg.content
    await ctx.channel.send(f'Prefix set to {prefix}')
    await ctx.channel.send(f'Language set to {Language}')


@bot.command(name="historique", description="Display the history of the bot")
async def historique(ctx):
    global LockSystem
    counter = 0
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    list_command = Dictionnaire_User[ctx.user.id].Display()

    if list_command == None:
        await ctx.response.send_message("No history")
    else:
        if(LockSystem == False):
            LockSystem = True
            for i in list_command:
                counter = counter + 1
                i = str(counter)+". "+i
                await ctx.channel.send(i)
            await ctx.response.send_message("Historique affiché")
            LockSystem = False


@bot.command(name="delete_historique", description="Delete the history of the bot")
async def delete_historique(ctx):
    global LockSystem
    await ctx.response.send_message("History deleted")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    if LockSystem == False:
        LockSystem = True
        Dictionnaire_User[ctx.user.id].DeleteAll()
        LockSystem = False

    return


@bot.command(name="last_command2", description="Display the last command")
async def last_command2(ctx):
    global LockSystem
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    if Dictionnaire_User[ctx.user.id].DisplayLast() == None:
        await ctx.response.send_message("No history")
    else:
        if LockSystem == False:
            LockSystem = True
            await ctx.response.send_message("Last command : " + Dictionnaire_User[ctx.user.id].DisplayLast())
            LockSystem = False
    Dictionnaire_User[ctx.user.id].InsertToEnd("last_command")
    return


@bot.command(name="last_command", description="Display the last command")
async def last_command(ctx):
    Emoji1 = "⏪"
    Emoji2 = "⏩"
    Emoji3 = "❌"
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    if Dictionnaire_User[ctx.user.id].DisplayLast() == None:
        await ctx.response.send_message("No history")
    else:
        msg = await ctx.channel.send("Last command : " + Dictionnaire_User[ctx.user.id].DisplayLast())
     # React to the message with the emoji
        await msg.add_reaction(Emoji1)
        await msg.add_reaction(Emoji2)
        await msg.add_reaction(Emoji3)
    # Wait for the reaction
    index = 0

    while True:
        reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.user and str(reaction.emoji) == Emoji1)
        # If the reaction is the same as the emoji, display last command -1

        if str(reaction.emoji) == Emoji1:
            await ctx.channel.send("Last command : " + Dictionnaire_User[ctx.user.id].DisplayOne(index))
            index = index - 1

        reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.user and str(reaction.emoji) == Emoji2)
    # If the reaction is the same as the emoji, display last command +1
        if str(reaction.emoji) == Emoji2:
            await ctx.channel.send("Last command : " + Dictionnaire_User[ctx.user.id].DisplayOne(index))
            index = index + 1
        if str(reaction.emoji) == Emoji3:
            await ctx.channel.send("End of History")
            break

    Dictionnaire_User[ctx.user.id].InsertToEnd("last_command")
    return


@bot.command(name="delete_last", description="Delete the last command")
async def delete_last(ctx):

    await ctx.response.send_message("Last command deleted from the History")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].delete_at_end()
    return


@bot.command(name="commande_liste", description="Liste des commandes")
async def commande(ctx):
    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete  ( delete X previous msg )\n delete_historique \n commande_liste \n chatbot \n **```API```** \n mangaapi \n randommangas \n **```Extra```** \n conversation \n speakabout \n last_command \n last_command2 \n delete_last \n savedata \n savedataauto \n loaddata \n heure \n sync \n"
    await ctx.response.send_message("Liste des commandes : \n " + Commands + "\n \n \n prefix : **;**")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("commande_liste")
    return
'''
@bot.command(name="chatbot",description="activate the ChatBot mod")
async def chatbot(ctx):
    def check(m):     
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("chatbot")
        
    print("ChatBot On")
    await ctx.channel.send("ChatBot **On**")
    msg = await client.wait_for('message', check=check)

    if msg.content == "Hello" :
        await ctx.channel.send("Hello ,  1. How are you ? 2. What's up ?")
        msg = await client.wait_for('message', check=check)
        msg.content.lower()

        if msg.content ==  "1" or msg.content.startswith("How"):
            await ctx.channel.send("I'm fine, and you ?   1. I'm fine too 2. I'm not fine")
            msg = await client.wait_for('message', check=check)
            msg.content.lower()

            if msg.content == "1" or msg.content.startswith("I'm fi"): 
                await ctx.channel.send("Nice !")
                msg = await client.wait_for('message', check=check)
                msg.content.lower()

            elif msg.content == "2" or msg.content.startswith("I'm not fi"):
                await ctx.channel.send("Oh...")
                msg = await client.wait_for('message', check=check)
                msg.content.lower()

        elif msg.content ==  "2" or msg.content.startswith("What"):
            await ctx.channel.send("Nothing much, and you ?   1. Nothing much 2. I need something !")
            msg = await client.wait_for('message', check=check)
            msg.content.lower()
            if msg.content == "1" or msg.content.startswith("Nothing"): 
                await ctx.channel.send("ok...")
                ctx.channel.send("Chatbot **Off**")

            elif msg.content == "2" or msg.content.startswith("I need"):
                await ctx.channel.send("What do you need ?")
                msg = await client.wait_for('message', check=check)
    return
'''


@bot.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):

    if interaction.user.id == int(ID):  # type: ignore
        await bot.sync()
        print('Command tree synced.')
        await interaction.response.send_message('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')


@bot.command(name="mangaapi")
async def MangaAPI(ctx, titre: str):
    url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-xuytm/endpoint/data/v1/action/findOne"

    payload = json.dumps({
        "collection": "final_exam",
        "database": "final_exam",
        "dataSource": "Cluster0",

        "filter": {
            "Titre": titre
        }

    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': API_KEY,
        'Accept': 'application/ejson'
    }

    response_count = requests.request(
        "POST", url, headers=headers, data=payload)
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[ctx.user.id].InsertToEnd("MangaAPI")
    try:
        document = response_count.json()["document"]
        titre = document["Titre"]
        origine = document["Origine"]
        genres = document["Genres"]
        await ctx.response.send_message(f"Titre: {titre}\nOrigine: {origine}\nGenres: {genres}")
    except:
        await ctx.response.send_message(f'Manga {titre} not found')


@bot.command(name="randommangas", description="ask for a manga")
async def RandomMangas(ctx):
    import random
    url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-xuytm/endpoint/data/v1/action/findOne"
    rand = randint(1970, 2022)

    payload = json.dumps({
        "collection": "final_exam",
        "database": "final_exam",
        "dataSource": "Cluster0",
        "filter": {
            "Date de sortie": rand
        },
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': API_KEY,
        'Accept': 'application/ejson'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[ctx.user.id].InsertToEnd("MangaAPI")
    try:
        document = response.json()["document"]
        titre = document["Titre"]
        origine = document["Origine"]
        genres = document["Genres"]
        await ctx.response.send_message(f"Titre: {titre}\nOrigine: {origine}\nGenres: {genres}")
    except:
        await ctx.response.send_message(f'No Random Manga were found')

@bot.command(name="food_facts", description="Give a random fact about food")
async def Food_Quizz(ctx):
        api_key = os.getenv('APIMEAL_KEY')
        response = requests.get(f'https://api.spoonacular.com/food/trivia/random?apiKey={api_key}')
        data = response.json()
        print(data)

        if data['text']:
            question = data['text']
            await ctx.response.send_message(f"Facts : {question} ")


@bot.command(name="randommeal", description="ask for a meal")
async def RandomMeal(ctx):
    api_key = os.getenv('APIMEAL_KEY')
    response = requests.get(
        f'https://api.spoonacular.com/recipes/random?number=1&apiKey={api_key}')
    # Appel à l'API Spoonacular pour générer une entrée aléatoire
    response_appetizer = requests.get(
        f'https://api.spoonacular.com/recipes/random?number=1&tags=appetizer&apiKey={api_key}')
    data_appetizer = response_appetizer.json()

    # Appel à l'API Spoonacular pour générer un plat principal aléatoire
    response_main_course = requests.get(
        f'https://api.spoonacular.com/recipes/random?number=1&tags=main course&apiKey={api_key}')
    data_main_course = response_main_course.json()

    # Appel à l'API Spoonacular pour générer un dessert aléatoire
    response_dessert = requests.get(
        f'https://api.spoonacular.com/recipes/random?number=1&tags=dessert&apiKey={api_key}')
    data_dessert = response_dessert.json()

    if data_appetizer['recipes'] and data_main_course['recipes'] and data_dessert['recipes']:
        appetizer = data_appetizer['recipes'][0]['title']
        main_course = data_main_course['recipes'][0]['title']
        dessert = data_dessert['recipes'][0]['title']

        await ctx.response.send_message(f"Entrée : {appetizer}")
        await ctx.channel.send(f"Plat principal : {main_course}")
        await ctx.channel.send(f"Dessert : {dessert}")

@bot.command(name="searchrecipe", description="search for a recipe")
async def SearchRecipe(ctx, recipe: str):
    API_KEY = os.getenv('APIMEAL_KEY')
    response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?query={recipe}&apiKey={API_KEY}")
    data = response.json()
    if data['results']:
        for recipe in data['results']:
            await ctx.channel.send(f" ``` "+ recipe['title']+" ``` " + "\n"+recipe['image']) # type: ignore
    else:
        await ctx.response.send_message(f"No recipe found for {recipe}")

@bot.command(name="recipe_info", description="Information about a recipe")
async def RecipeInfo(ctx, recipe: str):
    API_KEY = os.getenv('APIMEAL_KEY')
    IdOfTheRecipe = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?query={recipe}&apiKey={API_KEY}")
    data = IdOfTheRecipe.json()
    if data['results']:
        for recipe in data['results']:
            Id = recipe['id'] # type: ignore
            response = requests.get(f"https://api.spoonacular.com/recipes/{Id}/information?apiKey={API_KEY}")
            data = response.json()
            if data['title']:
                title = data['title']
                await ctx.response.send_message(f" ``` "+ title+" ``` " + "\n"+data['image'])
                await ctx.channel.send(f"Temps de préparation : {data['readyInMinutes']} minutes")
                await ctx.channel.send(f"Temps de cuisson : {data['cookingMinutes']} minutes")
                await ctx.channel.send(f"Nombre de personnes : {data['servings']}")
                print(data)
                if len(data['instructions']) > 2000:
                    await ctx.channel.send(f"instructions : {data['instructions'][:2000]}")
                    await ctx.channel.send(f"instructions : {data['instructions'][2000:]}")
                
                else:
                    await ctx.channel.send(f"instructions : {data['instructions']}")
                
            else:
                await ctx.response.send_message(f"No recipe found for {recipe}")
    else:
        await ctx.response.send_message(f"No recipe found for {recipe}")
        

@bot.command(name="nutrition", description="Valeur nutritionnelle d'un aliment ou d'une recette ")
async def Nutrition(ctx, food: str):
        API_KEY = os.getenv('APIMEAL_KEY')
        # Appel à l'API Spoonacular pour obtenir les informations nutritionnelles de la recette
        response = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?query={food}&apiKey={API_KEY}')
        data = response.json()
        print(data)
        if 'results' not in data:
            await ctx.response.send_message('Aucune recette trouvée.')
            return
        else:
            if data['results']:
                recipe_id = data['results'][0]['id']

                # Appel à l'API Spoonacular pour obtenir les informations nutritionnelles détaillées
                response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json?apiKey={API_KEY}')
                nutrition_data = response.json()

                await ctx.response.send_message(f"Informations nutritionnelles pour {food}:")
                await ctx.channel.send(f"Calories : {nutrition_data['calories']}")
                await ctx.channel.send(f"Protéines : {nutrition_data['protein']}")
                await ctx.channel.send(f"Lipides : {nutrition_data['fat']}")
                await ctx.channel.send(f"Glucides : {nutrition_data['carbs']}")
            else:
                await ctx.response.send_message('Aucune recette trouvée.')
@bot.command(name="conversation", description="User Conversation")
async def UserConversation(interaction):
    if interaction.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[interaction.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[interaction.user.id].InsertToEnd("conversation")
    if MyConversation.get_value(str(interaction.user.id)) == None:
        await interaction.response.send_message("No conversation found", ephemeral=True)
    else:
        await interaction.response.send_message(MyConversation.get_value(str(interaction.user.id)), ephemeral=True)


@bot.command(name="speakabout", description="speack about X")
async def speakabout(ctx, sujet: str):
    Arbre.T.first_question()        # return to the first question
    print(Arbre.T.send_answer(sujet).lower())
    if sujet in Arbre.T.send_answer(sujet).lower():
        await ctx.response.send_message("Le bot connait ce sujet")
    else:
        await ctx.response.send_message("Le bot ne connait pas ce sujet")


@bot.command(name="chatbot", description="blabla")
async def chatbot(ctx):
    over = False
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()

    Dictionnaire_User[ctx.user.id].InsertToEnd("chatbot")
    Arbre.T.first_question()        # return to the first question
    await ctx.response.send_message(Arbre.T.get_question())

    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    msg = await client.wait_for('message', check=check)
    question_suivante = Arbre.T.send_answer(msg.content)
    while over == False:
        await ctx.followup.send(question_suivante)
        msg = await client.wait_for('message', check=check)
        question_suivante = Arbre.T.send_answer(msg.content)

        if msg.content == "reset":
            await ctx.channel.send("ChatBot reset")
            await ctx.channel.send(Arbre.T.first_question())
            question_suivante = Arbre.T.send_answer(msg.content)

        if question_suivante == "Chatbot **Off**":
            over = True
            await ctx.followup.send("Chatbot **Off**")

    print("over")

# endregion

# region Jeux


@bot.command(name="plus_ou_moins", description="Plus ou moins")
async def plus_ou_moins(ctx):
    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel

    await ctx.response.send_message("Plus ou moins choisit")
    x = randint(1, 100)
    coup = 0
    n = 0
    await ctx.channel.send("Devinez le nombre entre 1 et 100")
    while x != n:
        n = await client.wait_for('message', check=check)
        print(n.content)
        n = int(n.content)
        coup += 1
        if n < x:
            await ctx.channel.send("plus")
        elif n > x:
            await ctx.channel.send("moins")
        else:
            await ctx.channel.send("Bravo, vous avez trouvé en " + str(coup) + " coups")

    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("plus_ou_moins")

    return


@bot.command(name="pendu")
async def pendu(ctx):
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("pendu")
    await ctx.response.send_message("Pendu choisit")
    await ctx.channel.send("Devinez le mot")
    count = 0
    mot = ["banane", "pomme", "poire", "fraise", "framboise", "cerise", "abricot", "mangue", "ananas", "orange", "citron", "pamplemousse", "kiwi", "raisin", "melon", "pasteque", "peche", "prune", "mirabelle", "cerise", "cassis", "groseille",
           "mure", "myrtille", "fraise", "framboise", "cerise", "abricot", "mangue", "ananas", "orange", "citron", "pamplemousse", "kiwi", "raisin", "melon", "pasteque", "peche", "prune", "mirabelle", "cerise", "cassis", "groseille", "mure", "myrtille"]
    #mot = list(mot)
    mot = mot[randint(0, len(mot)-1)]
    mot2 = []
    life = 9
    for i in range(len(mot)):
        mot2.append("_")
    mot2 = list(mot2)
    await ctx.channel.send("il y a "+str(mot2) + " lettres")
    print(mot2)
    print(mot)

    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    while mot != mot2 and life != 0:
        print(life)
        n = await client.wait_for('message', check=check)
        n = n.content
        n = list(n)
        for i in range(len(mot)):
            if mot[i] == n[0]:
                mot2[i] = n[0]
                life += 1
                count += 1
        print(mot2)
        await ctx.channel.send(mot2)
        life -= 1
        if count == len(mot):
            break
        else:
            await ctx.channel.send("Il vous reste " + str(life) + " vies")
    if life == 0:
        await ctx.channel.send("Vous avez perdu")
    else:
        await ctx.channel.send("Bravo")


@bot.command(name="chifoumi")
async def chifoumi(ctx):
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("chifoumi")
    await ctx.response.send_message("Chifoumi choisit Pierre, Feuille ou Ciseaux ?")
    int = randint(1, 3)

    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    n = await client.wait_for('message', check=check)
    n.content = n.content.lower()
    if int == 1:
        await ctx.channel.send("Pierre")

    elif int == 2:
        await ctx.channel.send("Feuille")
    elif int == 3:
        await ctx.channel.send("Ciseaux")
    if n.content == "pierre" and int == 2:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "pierre" and int == 3:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "feuille" and int == 1:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "feuille" and int == 3:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "ciseaux" and int == 1:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "ciseaux" and int == 2:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "pierre" and int == 1:
        await ctx.channel.send("Egalité")
    elif n.content == "feuille" and int == 2:
        await ctx.channel.send("Egalité")
    elif n.content == "ciseaux" and int == 3:
        await ctx.channel.send("Egalité")
    return


# endregion


# region client event


@client.event
async def on_ready():
    print(f'{client.user} had connected to Discord!')
    # print all runnning commands that are running


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    global prefix
    time = datetime.today()  # Le bot connait l'heure a chaque message

    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete \n delete_historique \n commande_liste \n chatbot, \n mangaapi \n randommangas \n"
    if message.author == client.user:
        return

    content = MyConversation.get_value(str(message.author.id))
    if content != None:
        content.append(message.content)
        MyConversation.update_bucket([(str(message.author.id), content)])
    else:
        MyConversation._assign_buckets(
            [(str(message.author.id), [message.content])])

    if(message.content.startswith(prefix)):
        message.content = message.content[1:]
        message.content = message.content.lower()
        if message.author == client.user:
            return

        elif(message.content == "hello"):
            await message.channel.send("Bonjour ! Hi ! \n Enter ;Help for more information")
        if (message.content == "help"):
            await message.channel.send("Voici une partie des commandes : \n " + Commands + "\n \n \n prefix : "+prefix)

# endregion


client.run(TOKEN)  # type: ignore
