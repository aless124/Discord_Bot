
import Liste
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

Historique = Liste.doublyLinkedList()
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
        await ctx.response.send_message("You can only purge 10 messages at a time.")
        return
    elif nbr_msg < 1:
        await ctx.response.send_message("You need to purge at least one message.")
        return
    else:
        await ctx.response.defer()
        await asyncio.sleep(1) # Attente de 1 seconde pour permettre à Discord de s'adapter
        await ctx.channel.purge(limit=nbr_msg)
        await ctx.response.send_message("Deleted {nbr_msg} messages.")

    Historique.InsertToEnd("delete")

@bot.command(name="delete_historique",description="Delete the history of the bot")
async def delete_historique(ctx):
    Historique.DeleteAll()
    await ctx.response.send_message("History deleted")
    return

@bot.command(name="last_command",description="Display the last command")
async def last_command(ctx):
    await ctx.response.send_message("Last command : " + Historique.DisplayLast())
    Historique.InsertToEnd("last_command")
    return

@bot.command(name="delete_last",description="Delete the last command")
async def delete_last(ctx):
    Historique.delete_at_end()
    await ctx.response.send_message("Last command deleted from the History")
    return
@bot.command(name="commande_liste",description="Liste des commandes")
async def commande(ctx):
    Commands = "**Help \n Hello \n Historique \n delete \n delete_historique \n hello_setup**"
    await ctx.response.send_message("Liste des commandes : \n " +Commands  + "\n **prefix :** ;")
    Historique.InsertToEnd("commande_liste")
    return  

@bot.command(name="chatbot",description="activate the ChatBot mod")
async def chatbot(ctx):
    def check(m):     
        return m.author.id == ctx.user.id and m.channel == ctx.channel
    Historique.InsertToEnd("chatbot")
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

    #await ctx.response.send_message(msg.content)


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
        
    Historique.InsertToEnd("plus_ou_moins")
    return

@bot.command(name="pendu")
async def pendu(ctx):
    Historique.InsertToEnd("pendu")
    await ctx.response.send_message("Pendu choisit")
    
    return

@bot.command(name="chifoumi")
async def chifoumi(ctx):
    Historique.InsertToEnd("chifoumi")
    await ctx.response.send_message("Chifoumi choisit")
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
    global Historique
    global prefix
    Commands = "**```Basic commands :```** \n Help \n Hello \n setup \n   **```Game```** \n plus_ou_moins \n pendu \n chifoumi  \n **```Extras```** \n Historique \n delete \n delete_historique \n commande_liste \n chatbot"

    if(message.content.startswith(prefix)):
        message.content = message.content[1:]
        message.content = message.content.lower()
        if message.author == client.user:
            return  
        elif(message.content == "help"):
            Historique.InsertToEnd("Help")
            await message.channel.send(Commands)

        elif(message.content == "historique") :
            await message.channel.send(Historique.Display())  
        
        elif(message.content == "hello"):
            await message.channel.send("Bonjour ! Hi ! \n Enter ;Help for more information")
            Historique.InsertToEnd("hello")
        elif(message.content == "setup"):

            Historique.InsertToEnd("setup")
            await message.channel.send("Bonjour ! Hi ! \n Please choose a language \n ( French 1 , English 2 )")
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
                await message.channel.send(f'Merci {msg.author}! {Language} choisi !')
            elif msg.content == '2':
                Language = "English"
                await message.channel.send(f'thanks {msg.author}! {Language} choosen !')
            else :
                Language = "language set to English ( default) due to wrong input"
                await message.channel.send(f'{msg.author}! {Language} choosen !')
                Language = "English"    

            await message.channel.send("Please choose a prefix \n ( default : ; ) \n Actual prefix : " + prefix )
            def check(m):
                return m.author.id == message.author.id and m.channel == message.channel
            
            msg = await client.wait_for('message', check=check)
            
            while len(msg.content) == 1 and msg.content.isalnum():
                await message.channel.send("Le caractère entré est une lettre ou un chiffre. Vous ne pouvez choisir qu'un charactère special \n exemple : !, #, $, %, &, /, (, ), =, +, -, *, @, etc.")
                msg = await client.wait_for('message', check=check)
                time.sleep(1)

                
            prefix = msg.content
            await message.channel.send(f'Prefix set to {prefix}')
            await message.channel.send(f'Language set to {Language}')


    #await client.process_commands(message)


client.run(TOKEN)
