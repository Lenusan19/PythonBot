import discord 
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix="zebi", intents = intents)

@client.command(name="del")
async def delete(ctx, number):
    await ctx.channel.purge(limit=int(number))



@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_typing(channel, user, when):
     await channel.send(user.name+"en train de ```rediger MeinKampf```")

@client.even
async def on_member_join(member):
    general_channel = client.get_channel(1091343630473646191)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)

@client.event
async def on_message(message):
  if message.author == client.user:
    return 

  if message.content.startswith("wsh"):
    await message.channel.send("```Ca dit quoi l'équipe ?```")
    



client.run("MTA5MTMzNDc4MjUyNjQyMzEyNA.G1I6mh.Xm8y9VNSeZiXcM06SI-8Nvq5PiQFQKG2r5HOJA")