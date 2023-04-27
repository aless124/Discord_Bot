#region import

from datetime import datetime, timedelta
import time
import classe.Liste as Liste
import classe.Queue as Queue
import classe.Arbre as Arbre
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time
import asyncio
from random import randint
import json

#endregion


#region variable
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID = os.getenv('DISCORD_ID')
intents = discord.Intents.default()
intents = intents.all()
client = discord.Client(intents=intents)


# Global Variable 
bot = app_commands.CommandTree(client)
Dictionnaire_User = {}
FILENAME = "Projet_DiscordBotPy\json\data.json"
global prefix
prefix = ";"
SaveArbre = Arbre.T


#endregion

#region Json

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


## test
# Enregistrer des données
'''
my_data = {"users": ["Alice", "Bob", "Charlie","test"]}
save_data(my_data)
# Charger des données
loaded_data = load_data()
print(loaded_data)  # {'users': ['Alice', 'Bob', 'Charlie']}
'''
#endregion




#region app command
# Bot Commands

@bot.command(name="savedata",description="Save the data in the json file")
async def savedata(ctx):
    await ctx.response.send_message("Saving data...")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Data = {ctx.user.id : Dictionnaire_User[ctx.user.id].Display()}
    save_data(Data)
    await ctx.channel.send("Data saved !")

@bot.command(name="savedataauto",description="save data during a certain time")
async def save_data_auto(ctx,hour_of_ending:int,day_of_ending:int):
    Hour = datetime.now().strftime('%H')
    Jour = datetime.now().strftime('%d')
    Jour = int(Jour)

    await ctx.response.send_message("Saving data")

    while day_of_ending != Jour :
        if ctx.user.id not in Dictionnaire_User.keys():
            Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
            print("User added to the dictionary")

        Data = {ctx.user.id : Dictionnaire_User[ctx.user.id].Display()}
        save_data(Data)
        await asyncio.sleep(10)
        
    if day_of_ending == Jour:
        while int(Hour) != int(hour_of_ending): 
            if ctx.user.id not in Dictionnaire_User.keys():
                Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
                print("User added to the dictionary")

            Data = {ctx.user.id : Dictionnaire_User[ctx.user.id].Display()}
            save_data(Data)
            await asyncio.sleep(10)

    await ctx.channel.send("Data saved !")

@bot.command(name="loaddata",description="Load the data from the json file")
async def loaddata(ctx):
    await ctx.response.send_message("Loading data...")
    Data = load_data()
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
 
    for i in Data[str(ctx.user.id)]:
        Dictionnaire_User[ctx.user.id].InsertToEnd(i)

    await ctx.channel.send("Data loaded !")

    
@bot.command(name="delete")
async def delete(ctx, nbr_msg: int):
    nbr_msg += 1 # On ajoute 1 pour compter le message de la commande
    if nbr_msg > 11:
        await ctx.followup.send("You can only purge 10 messages at a time.")
        return
    elif nbr_msg < 1:
        await ctx.followup.send("You need to purge at least one message.")
        return
    else:
        await ctx.response.defer()
        await asyncio.sleep(1) # Attente de 1 seconde pour permettre à Discord de s'adapter
        await ctx.channel.purge(limit=nbr_msg)
        #await ctx.chan.send_message("Deleted {nbr_msg} messages.")
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

@bot.command(name="setup",description="Setup the hello command")
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
            else :
                Language = "language set to English ( default) due to wrong input"
                await ctx.channel.send(f'{msg.author}! {Language} choosen !')
                Language = "English"    

            await ctx.channel.send("Please choose a prefix \n ( default : ; ) \n Actual prefix : " + prefix )
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


@bot.command(name="historique",description="Display the history of the bot")
async def historique(ctx): 
    counter = 0
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    list_command = Dictionnaire_User[ctx.user.id].Display()

    if list_command == None:
        await ctx.response.send_message("No history")
    else:
        for i in list_command:
            counter = counter + 1
            i = str(counter)+". "+i
            await ctx.channel.send(i)
        await ctx.response.send_message("Historique affiché")
   



@bot.command(name="delete_historique",description="Delete the history of the bot")
async def delete_historique(ctx):
    await ctx.response.send_message("History deleted")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].DeleteAll()
    

    return

@bot.command(name="last_command",description="Display the last command")
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
    
        reaction,user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.user and str(reaction.emoji) == Emoji2)
    # If the reaction is the same as the emoji, display last command +1
        if str(reaction.emoji) == Emoji2:
            await ctx.channel.send("Last command : " + Dictionnaire_User[ctx.user.id].DisplayOne(index))
            index = index + 1
        if str(reaction.emoji) == Emoji3:
            await ctx.channel.send("End of History")
            break
        
    Dictionnaire_User[ctx.user.id].InsertToEnd("last_command")
    return  

@bot.command(name="delete_last",description="Delete the last command")
async def delete_last(ctx):

    await ctx.response.send_message("Last command deleted from the History")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].delete_at_end()
    return

@bot.command(name="commande_liste",description="Liste des commandes")
async def commande(ctx):
    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete  ( delete X previous msg )\n delete_historique \n commande_liste \n chatbot \n"
    await ctx.response.send_message("Liste des commandes : \n " +Commands  + "\n \n \n prefix : **;**")
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

    if interaction.user.id == int(ID): # type: ignore
        await bot.sync()
        print('Command tree synced.')
        await interaction.response.send_message('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@bot.command(name="speakabout",description="speack about X")
async def speakabout(ctx,sujet:str):
    Arbre.T.first_question()        # return to the first question
    py = "python"
    
    if py in Arbre.T.send_answer(sujet).lower():   
        await ctx.response.send_message("Le bot connait ce sujet")
    else:
        await ctx.response.send_message("Le bot ne connait pas ce sujet")


@bot.command(name="chatbot",description="blabla")
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
        
        if msg.content == "reset" :
            await ctx.channel.send("ChatBot reset")
            await ctx.channel.send(Arbre.T.first_question())
            question_suivante = Arbre.T.send_answer(msg.content)

        if question_suivante == "Chatbot **Off**":
            over = True
            await ctx.followup.send("Chatbot **Off**")

    print("over")

#endregion

#region Jeux

@bot.command(name="plus_ou_moins",description="Plus ou moins")
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
    mot = "test"
    mot = list(mot)
    mot2 = []
    life = 9
    for i in range(len(mot)):
        mot2.append("_")
    mot2 = list(mot2)
    await ctx.channel.send("il y a "+str(mot2)  + " lettres")
    print(mot2)
    print(mot)
    def check(m):
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    while mot != mot2 or life != 0:
        n = await client.wait_for('message', check=check)
        n = n.content
        n = list(n)
        for i in range(len(mot)):
            if mot[i] == n[0]:
                mot2[i] = n[0]
        print(mot2)
        await ctx.channel.send(mot2)
        life -= 1
        await ctx.channel.send("Il vous reste " + str(life) + " vies")
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
    n.content =     n.content.lower()
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


#endregion


#region client event


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
    time = datetime.today() # Le bot connait l'heure a chaque message


    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete \n delete_historique \n commande_liste \n chatbot"

    if(message.content.startswith(prefix)):
        message.content = message.content[1:]
        message.content = message.content.lower()
        if message.author == client.user:
            return  


        elif(message.content == "hello"):
            await message.channel.send("Bonjour ! Hi ! \n Enter ;Help for more information")

#endregion
    


client.run(TOKEN)  # type: ignore
