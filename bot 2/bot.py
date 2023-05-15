import discord
from discord.ext import commands
from historique import CommandHistory
from conv import Node
import json 
import youtube_dl
import random 
import asyncio
#import openai




gif_yes = "https://tenor.com/fr/view/jotaro-kujo-yes-jojo-distorted-anime-gif-17239598"
gif_no = "https://tenor.com/fr/view/jojo-no-no-no-nah-nope-its-a-no-gif-17161746"
#gif_lol = "https://tenor.com/fr/view/hacker-pc-meme-matrix-codes-gif-16730883"

# Initialisation des variables de conversation
conversation_active = False
current_node = None
root = Node("Aimez-vous la programations ?")
gif_lol = "https://tenor.com/fr/view/hacker-pc-meme-matrix-codes-gif-16730883"




# Création des intents pour le bot
intents = discord.Intents.all()
intents.members = True
user_histories = {}


# Création de l'objet bot avec le préfixe de commande et les intents
bot = commands.Bot(command_prefix='$', intents=intents)
#gif_lol = "https://tenor.com/fr/view/hacker-pc-meme-matrix-codes-gif-16730883"



####################################### partie historique #####################################
# Création d'instances des modules personnalisés pour le bot
bot.history = CommandHistory()


ignored_commands = ["$lastcmd", "$next", "$prev", "$hist", "$clearcmd"]


# Définition d'un événement pour quand le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} le Bot est pret ")
    # await send_motivation_quote() #teste de l'envoi de la citation

# Définition d'une commande pour supprimer les messages en masse(limitation à 10)
@bot.command(name="clearmsg")
async def delete(ctx):
    await ctx.channel.purge(limit=15)

# Commande servant de test
@bot.command("name=do it")
async def focus(ctx):
    await ctx.send("Restez concentré ta grand mère")


@bot.event
async def on_command_completion(ctx):
    if ctx.message.content not in ignored_commands:
        bot.history.add_command(ctx.message.content)

# Commande pour afficher l'historique des commandes
@bot.command(name="hist")
async def history(ctx):
    commands = bot.history.get_all_commands()
    if commands == "Pas d'historique":
        await ctx.send("Aucune commande dans l'historique.")
    else:
        commands_str = "\n".join(commands)
        await ctx.send(f"Voici toutes les commandes que vous avez entrées :\n```{commands_str}```")

# Commande pour afficher la dernière commande
#@bot.command(name="cmd")
#async def last_command(ctx):
 #   last_cmd = bot.history.get_last_command()
  #  if last_cmd == "Pas d'historique":
   #     await ctx.send("Aucune commande dans l'historique.")
    #else:
    #    await ctx.send(f"Dernière commande : {last_cmd}")

# Commande pour revenir en arrière dans l'historique des commandes
@bot.command(name="prev")
async def back(ctx):
    command = bot.history.move_backward()
    if command:
        await ctx.send(f"Dernière commande : {command}")
    else:
        await ctx.send("Début de l'historique atteint.")

# Commande pour avancer dans l'historique des commandes
@bot.command(name="next")
async def forward(ctx):
    command = bot.history.move_forward()
    if command:
        await ctx.send(f"Dernière commande : {command}")
    else:
        await ctx.send("Fin de l'historique atteint.")

# Commande pour effacer l'historique des commandes
@bot.command(name="clearcmd")
async def clear_history(ctx):
    bot.history.clear()
    await ctx.send("L'historique a été supprimé.")

    


@bot.event
async def on_command(ctx):
    user_id = ctx.author.id
    if user_id not in user_histories:
        user_histories[user_id] = CommandHistory()

    command_name = ctx.message.content.split()[0]
    if command_name not in ignored_commands:
        user_histories[user_id].add_command(ctx.message.content)
################################################ partie sondage #####################################


@bot.command(name="sondage")
async def create_poll(ctx, question, *options):
    # Vérifier que le nombre d'options est valide
    if len(options) < 2 or len(options) > 10:
        await ctx.send("Le sondage doit avoir entre 2 et 10 options.")
        return

    # Créer le message du sondage
    poll_message = f"Sondage : {question}\n\n"
    for i, option in enumerate(options, start=1):
        poll_message += f"{i}. {option}\n"

    # Envoyer le message du sondage
    poll = await ctx.send(poll_message)

    # Ajouter les réactions pour voter sur les options
    for i in range(len(options)):
        await poll.add_reaction(f"{i+1}\N{COMBINING ENCLOSING KEYCAP}")

    await ctx.message.delete()  # Supprimer la commande du sondage

    # Répondre avec un message confirmant la création du sondage
    await ctx.send("Le sondage a été créé ! Utilisez les réactions pour voter !")
#################################### partie conv #################################""

@bot.command(name="conv")
async def start_conversation(ctx):
    global conversation_active, current_node
    if conversation_active:
        await ctx.send("Une conversation est déjà en cours. Utilisez la commande $reset pour recommencer.")
    else:
        conversation_active = True
        current_node = root

        embed = discord.Embed(title="Conversation avec Adonis 2.0",)
        embed.description = current_node.question

        await ctx.send(embed=embed)

@bot.command(name="reset")
async def reset_conversation(ctx):
    global conversation_active, current_node
    if not conversation_active:
        await ctx.send("Aucune conversation en cours. Utilisez la commande $start_conversation pour commencer.")
    else:
        conversation_active = False
        current_node = root

        embed = discord.Embed(title="Conversation réinitialisée", color=discord.Color.blue())
        await ctx.send(embed=embed)
@bot.event
async def on_message(message):
    global conversation_active, current_node

    if message.author == bot.user:
        return

    if conversation_active:
        if message.content.lower() == "oui":
            if current_node.yes_node:
                current_node = current_node.yes_node
                await message.channel.send(current_node.question)
                await message.channel.send(gif_yes)  
            else:
                await message.channel.send("Oh, ça sent le futur développeur ça!")
                await message.channel.send(gif_yes)  
                conversation_active = False
        elif message.content.lower() == "non":
            if current_node.no_node:
                current_node = current_node.no_node
                await message.channel.send(current_node.question)
                await message.channel.send(gif_no) 
            else:
                await message.channel.send("Ah, moi aussi ")
                await message.channel.send(gif_no)  

    await bot.process_commands(message)  


############################################ partie info bot ##########################################################


# Événement pour quand le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} est en ligne !")
    print(f"ID du bot : {bot.user.id}")

# Commande pour afficher les informations du bot
@bot.command(name="info")
async def bot_info(ctx):
    embed = discord.Embed(title="Informations du Bot")
    embed.add_field(name="Nom", value=bot.user.name, inline=False)
    embed.add_field(name="ID", value=bot.user.id, inline=False)
    embed.add_field(name="Commentaire", value="Sah je sais pas quoi mettre comme info a part que c'est un projet quoi", inline=False)
    embed.add_field(name="Version de discord.py", value=discord.__version__, inline=False)
    embed.add_field(name="Créateur", value="Lénu-san#5439", inline=False)
    
    embed.set_thumbnail(url=bot.user.avatar.url)
    await ctx.send(embed=embed)

################################################################ pierre papier ciseaux #####################################


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def jeux(ctx):
    # Envoyez un message pour proposer un choix
    message = await ctx.send("Choisissez votre coup :")
    await message.add_reaction("✊")  # Pierre
    await message.add_reaction("✋")  # Papier
    await message.add_reaction("✌️")  # Ciseaux

    # Fonction pour vérifier la réaction de l'utilisateur
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✊", "✋", "✌️"]

    try:
        # Attendez la réaction de l'utilisateur pendant 60 secondes
        reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)

        # Obtenez le choix de l'utilisateur
        choix = ""
        if str(reaction.emoji) == "✊":
            choix = "pierre"
        elif str(reaction.emoji) == "✋":
            choix = "papier"
        elif str(reaction.emoji) == "✌️":
            choix = "ciseaux"

        # Générez le choix de l'ordinateur
        choix_ordi = random.choice(['pierre', 'papier', 'ciseaux'])

        # Déterminez le gagnant
        if choix == choix_ordi:
            resultat = "C'est une égalité !"
        elif (choix == 'pierre' and choix_ordi == 'ciseaux') or (choix == 'papier' and choix_ordi == 'pierre') or (choix == 'ciseaux' and choix_ordi == 'papier'):
            resultat = "Vous avez gagné !"
        else:
            resultat = "Vous avez perdu !"

        # Envoyez le résultat dans le canal Discord
        await ctx.send(f"Vous avez choisi : {choix}\nL'ordinateur a choisi : {choix_ordi}\n{resultat}")

    except asyncio.TimeoutError:
        await ctx.send("Le temps de réponse est écoulé. Veuillez réessayer.")

############################################### Chat GPT ############################################################


# # Définir le token du modèle ChatGPT d'OpenAI
# openai.api_key = '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'  # Remplacez par votre clé d'API ChatGPT

# @bot.event
# async def on_ready():
#     print(f'Connecté en tant que {bot.user.name}')

# @bot.command()
# async def gpt(ctx, *, message):
#     # Appeler l'API ChatGPT pour obtenir une réponse
#     response = openai.Completion.create(
#         engine='text-davinci-003',  # Utilisez le moteur "text-davinci-003" pour ChatGPT
#         prompt=message,
#         max_tokens=50,  # Nombre maximal de tokens pour la réponse
#         n=1,  # Générer une seule réponse
#         stop=None,  # Arrêter la réponse à la fin de la phrase
#         temperature=0.7  # Contrôler le niveau d'aléatoire de la réponse
#     )

#     # Récupérer la réponse générée par ChatGPT
#     reply = response.choices[0].text.strip()

#     # Envoyer la réponse dans le canal Discord
#     await ctx.send(reply)

# ne marche pas apparement probleme au niveau du payement lol ducoup j'ai delete la cle vu que ca sert a rien snif ...


# #################################################### partie music ####################################################


#     # Événement pour quand le bot est prêt
# @bot.event
# async def on_ready():
#     print(f"{bot.user.name} est en ligne !")

# # Commande pour jouer de la musique
# @bot.command(name="play")
# async def play_music(ctx, url):
#     # Vérification du salon vocal
#     if ctx.author.voice is None or ctx.author.voice.channel is None:
#         await ctx.send("Vous devez être connecté à un salon vocal pour utiliser cette commande.")
#         return

#     # Récupération du salon vocal de l'utilisateur
#     channel = ctx.author.voice.channel

#     # Connexion au salon vocal
#     voice_client = await channel.connect()

#     # Configuration de youtube_dl pour la lecture audio
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }

#     # Téléchargement et lecture de la musique depuis le lien YouTube
#    
#        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=False)
#         url2 = info['formats'][0]['url']
#         voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('Fin de la lecture'))

#     await ctx.send(f"En train de jouer la musique de {url}")

# # Commande pour arrêter la musique et déconnecter le bot
# @bot.command(name="stop")
# async def stop_music(ctx):
#     # Vérification si le bot est connecté à un salon vocal
#     if ctx.voice_client is None:
#         await ctx.send("Je ne suis pas connecté à un salon vocal.")
#         return

#     # Arrêt de la lecture et déconnexion du salon vocal
#     await ctx.voice_client.disconnect()

    
    
    
bot.run("MTA5MTMzNDc4MjUyNjQyMzEyNA.G3zT9y.ttu30r9dXoCHpCVnmKwfyfmyPl1BNmzQlWBDXQ")


