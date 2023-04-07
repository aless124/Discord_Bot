
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents = intents.all()
client = discord.Client(intents=intents)


# Global Variable 
bot = app_commands.CommandTree(client)

Historique = []
prefix = ";"

# Client Event

@client.event   
async def on_ready():
    await bot.sync()
    print(f'{client.user} had connected to Discord!')


# Bot Commandx


@bot.command(name="delete")

async def delete(ctx,nbr_msg : int):
    
    if nbr_msg>10:
        await ctx.send("You can only purge 10 message")
        return
    elif nbr_msg<1:
        await ctx.send("You can't purge less than one message")
        return
    
    await ctx.channel.purge(limit = nbr_msg)
    Historique.append("Delete")

@bot.command(name="delete_historique")
async def delete_historique(ctx):
    global Historique
    Historique = []
    await ctx.response.send_message("History deleted")
    return
@bot.command(name="commande_liste")
async def commande(ctx):
    global Historique
    Commands = "**Help \n Hello \n Historique \n delete \n delete_historique \n hello_setup**"
    await ctx.response.send_message("Liste des commandes : \n " +Commands  + "\n prefix : **;**")
    Historique.append("commande_liste")

    return

@bot.command(name="ChatBot")
async def chatbot(ctx):
    Historique.append("ChatBot")
    await ctx.response.send_message("ChatBot **On**")
    def check(m):     
        return m.author == ctx.author and m.channel == ctx.channel
    
    msg = await client.wait_for('message', check=check)
    await ctx.response.send_message(msg.content)
    

    return
## To Do

@bot.command(name="plus_ou_moins")
async def plus_ou_moins(ctx):
    Historique.append("plus_ou_moins")
    await ctx.response.send_message("Plus ou moins choisit")
    return

@bot.command(name="pendu")
async def pendu(ctx):
    Historique.append("pendu")
    await ctx.response.send_message("Pendu choisit")
    return

@bot.command(name="chifoumi")
async def chifoumi(ctx):
    Historique.append("chifoumi")
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
    Commands = ["Help","Hello","Historique","delete","delete_historique","hello_setup"]

    if(message.content.startswith(prefix)):
        message.content = message.content[1:]
        message.content = message.content.lower()
        if message.author == client.user:
            return  
        elif(message.content == "help"):
            Historique.append("Help")
            await message.channel.send(Commands)

        elif(message.content == "historique") :
            Historique.append(message.content)
            await message.channel.send(Historique)  
        
        elif(message.content == "hello"):
            await message.channel.send("Bonjour ! Hi ! \n Enter ;Help for more information")
            Historique.append("Hello")
        elif(message.content == "hello_setup"):

            Historique.append(message.content)
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

    #await client.process_commands(message)


client.run(TOKEN)
