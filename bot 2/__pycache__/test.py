# Commande pour afficher la dernière commande
@bot.command()
async def last_command(ctx):
    last_cmd = await command_history.get_latest_command()
    if last_cmd:
        await ctx.send(f"Last command: {last_cmd}")
    else:
        await ctx.send("No commands in history.")

# Commande pour afficher toutes les commandes d'un utilisateur
@bot.command()
async def user_commands(ctx):
    author = ctx.author
    user_commands = await command_history.get_user_commands(author)
    if user_commands:
        response = "\n".join(user_commands)
    else:
        response = "No commands found for this user."
    await ctx.send(response)

# Commande pour se déplacer vers la commande précédente
@bot.command()
async def previous_command(ctx):
    command = await command_history.move_to_previous_command()
    if command:
        await ctx.send(f"Previous command: {command}")
    else:
        await ctx.send("No previous command available.")

# Commande pour se déplacer vers la commande suivante
@bot.command()
async def next_command(ctx):
    command = await command_history.move_to_next_command()
    if command:
        await ctx.send(f"Next command: {command}")
    else:
        await ctx.send("No next command available.")

# Commande pour vider l'historique des commandes
@bot.command()
async def clear_history(ctx):
    await command_history.clear_history()
    await ctx.send("Command history cleared.")

# Lancement du bot
bot.run("MTA5MTMzNDc4MjUyNjQyMzEyNA.G3zT9y.ttu30r9dXoCHpCVnmKwfyfmyPl1BNmzQlWBDXQ")
