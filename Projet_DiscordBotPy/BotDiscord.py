
import Liste
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time
import asyncio

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
        print(ctx)
        await ctx.response.send_message("Deleted {nbr_msg} messages.")

    Historique.InsertToEnd("delete")

@bot.command(name="delete_historique")
async def delete_historique(ctx):
    Historique.DeleteAll()
    await ctx.response.send_message("History deleted")
    return
@bot.command(name="delete_last")
async def delete_last(ctx):
    Historique.delete_at_end()
    await ctx.response.send_message("Last command deleted from the History")
    return
@bot.command(name="commande_liste")
async def commande(ctx):
    Commands = "**Help \n Hello \n Historique \n delete \n delete_historique \n hello_setup**"
    await ctx.response.send_message("Liste des commandes : \n " +Commands  + "\n prefix : **;**")
    Historique.InsertToEnd("commande_liste")
    return  

@bot.command(name="chatbot")
async def chatbot(ctx):
    Historique.InsertToEnd("chatbot")
    await ctx.response.send_message("ChatBot **On**")
    print("ChatBot On")
    def check(m):     
        return m.author.id == ctx.user.id and m.channel == ctx.channel
        #return m.channel == ctx.channel
    msg = await client.wait_for('message', check=check)
    print(msg.content)
    if msg.content == "Hello" :
        await ctx.response.send_message("Hello")
        msg = await client.wait_for('message', check=check)
    elif msg.content == "How are you ?":
        await ctx.response.send_message("I'm fine, and you ?")
        msg = await client.wait_for('message', check=check)
        if msg.content == "I'm fine too":
            await ctx.response.send_message("Nice !")
            msg = await client.wait_for('message', check=check)
    await ctx.response.send_message(msg.content)


    return
## To Do

@bot.command(name="plus_ou_moins")
async def plus_ou_moins(ctx):
    Historique.InsertToEnd("plus_ou_moins")
    await ctx.response.send_message("Plus ou moins choisit")
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
