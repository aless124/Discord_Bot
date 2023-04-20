import datetime
import time
import Liste
import Queue
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time
import asyncio
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents = intents.all()
client = discord.Client(intents=intents)


# Global Variable 
bot = app_commands.CommandTree(client)
Dictionnaire_User = {}
#Historique = Liste.doublyLinkedList()
global prefix
prefix = ";"

# Client Event

@client.event   
async def on_ready():
    await bot.sync()
    print(f'{client.user} had connected to Discord!')

# Bot Commands

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
    await ctx.channel.send(f"il est {datetime.datetime.now().strftime('%H:%M:%S')}")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
        print("User added to the dictionary")
    Dictionnaire_User[ctx.user.id].InsertToEnd("Heure")

@bot.command(name="setup",description="Setup the hello command")
async def hello_setup(ctx):
            if ctx.user.id not in Dictionnaire_User.keys():
                Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
            Dictionnaire_User[ctx.user.id].InsertToEnd("setup")
            await ctx.channel.send("Bonjour ! Hi ! \n Please choose a language \n ( French 1 , English 2 )")
            def check(m):     
                if m.content == '1':
                    Language = "Français"
                    
                elif m.content == '2':
                    Language = "English"
                else :
                    Language = "language set to English ( default) due to wrong input"
                return Language
            msg = await client.wait_for('message', check=check)
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
                return m.author.id == ctx.author.id and m.channel == ctx.channel
            
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
        Dictionnaire_User[ctx.user.id].InsertToEnd("historique")
    list_command = Dictionnaire_User[ctx.user.id].Display()

    if list_command == []:
        await ctx.channel.send("No history")
    else:

        for i in list_command:
            counter = counter + 1
            i = str(counter)+". "+i
            await ctx.channel.send(i)
    await ctx.response.send_message("Historique affiché")
   



'''
    print(Dictionnaire_User)
    if Dictionnaire_User == {}:
        await ctx.channel.send("No history")
    else:
        for cle, valeur in Dictionnaire_User.items():
            print("clé : ",cle)
            print(ctx.user.id)
          
            a = "id user :" , cle , "Valeur :" , valeur.Display()
            await ctx.channel.send(a)
'''    

@bot.command(name="delete_historique",description="Delete the history of the bot")
async def delete_historique(ctx):
    await ctx.followup.send("History deleted")
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
        await ctx.channel.send("No history")
        return 
    else:
        msg = await ctx.channel.send("Last command : " + Dictionnaire_User[ctx.user.id].DisplayLast())
    index = 0
     # React to the message with the emoji
    await msg.add_reaction(Emoji1)
    await msg.add_reaction(Emoji2)
    await msg.add_reaction(Emoji3)
    # Wait for the reaction
    await ctx.response.defer()

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

    await ctx.followup.send("Last command deleted from the History")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].delete_at_end()
        
    return
@bot.command(name="commande_liste",description="Liste des commandes")
async def commande(ctx):
    Commands = "**Help \n Hello \n Historique \n delete \n delete_historique \n hello_setup**"
    await ctx.followup.send("Liste des commandes : \n " +Commands  + "\n **prefix :** ;")
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("commande_liste")
    
    return  

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
## To Do

@bot.command(name="plus_ou_moins",description="Plus ou moins")
async def plus_ou_moins(ctx):
    def check(m):     
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    
    await ctx.channel.send("Plus ou moins choisit")
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
    await ctx.followup.send("Pendu choisit")

    
    return

@bot.command(name="chifoumi")
async def chifoumi(ctx):
    if ctx.user.id not in Dictionnaire_User.keys():
        Dictionnaire_User[ctx.user.id] = Liste.doublyLinkedList()
    Dictionnaire_User[ctx.user.id].InsertToEnd("chifoumi")
    await ctx.channel.send("Chifoumi choisit Pierre, Feuille ou Ciseaux ?")
    int = randint(1, 3)
    def check(m):     
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    n = await client.wait_for('message', check=check)
    if int == 1:
        await ctx.channel.send("Pierre")

    elif int == 2:
        await ctx.channel.send("Feuille")
    elif int == 3:
        await ctx.channel.send("Ciseaux")
    if n.content == "Pierre" and int == 2:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "Pierre" and int == 3:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "Feuille" and int == 1:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "Feuille" and int == 3:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "Ciseaux" and int == 1:
        await ctx.channel.send("Vous avez perdu")
    elif n.content == "Ciseaux" and int == 2:
        await ctx.channel.send("Vous avez gagné")
    elif n.content == "Pierre" and int == 1:
        await ctx.channel.send("Egalité")
    elif n.content == "Feuille" and int == 2:
        await ctx.channel.send("Egalité")
    elif n.content == "Ciseaux" and int == 3:
        await ctx.channel.send("Egalité")
    return

# Client Event  
    


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    global prefix
    time = datetime.datetime.today() # Le bot connait l'heure a chaque message


    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete \n delete_historique \n commande_liste \n chatbot"

    if(message.content.startswith(prefix)):
        message.content = message.content[1:]
        message.content = message.content.lower()
        if message.author == client.user:
            return  
        elif(message.content == "help"):
            if message.author.id not in Dictionnaire_User.keys():
                Dictionnaire_User[message.author.id] = Liste.doublyLinkedList()
            Dictionnaire_User[message.author.id].InsertToEnd("help")
        
            await message.channel.send(Commands)

        elif(message.content == "hello"):
            await message.channel.send("Bonjour ! Hi ! \n Enter ;Help for more information")


    


client.run(TOKEN)
