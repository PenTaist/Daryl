import aiohttp, json, random, discord
from discord.ext import commands
from blagues_api import BlaguesAPI

bot_token = "TOKEN DU BOT"
owner_id = ID DU CREATEUR DU BOT

description = 'Coded by PenTaist#4560\n\nPréfixe : **d$**'
intents = discord.Intents().all()
activity = discord.Activity(type=discord.ActivityType.playing, name="d$help | v1.1")
daryl = commands.Bot(command_prefix='d$', description=description, intents=intents, activity=activity)
daryl.remove_command('help')

class colors():
    red = discord.Color.red()
    blue = discord.Color.blue()
    green = discord.Color.green()
    yellow = discord.Color.yellow()
    purple = discord.Color.purple()

@daryl.event
async def on_ready():
    print(f"Logged in as {daryl.user}")

@daryl.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        arguments_message = "Commande Incorrecte !"
        arguments_embed = discord.Embed(title=arguments_message, color=colors.red)
        await ctx.send(embed=arguments_embed, delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        permissions_messages = "Tu n'a pas les permissions requises !"
        permissions_embed = discord.Embed(title=permissions_messages, color=colors.red)
        await ctx.send(embed=permissions_embed, delete_after=5)

@daryl.command()
async def owner(ctx):
    if ctx.author.id == owner_id:
        owner_embed = discord.Embed(title="Bonjour, mon créateur", color=colors.purple)
        await ctx.send(embed=owner_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command()
async def ServersCount(ctx):
    if ctx.author.id == owner_id:
        count = len(daryl.guilds)
        ServersCount_embed = discord.Embed(title=f"Je suis actuellement sur {count} serveur(s)", color=colors.purple)
        await ctx.send(embed=ServersCount_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command()
async def say(ctx, *, message):
    if ctx.author.id == owner_id:
        await ctx.message.delete()
        say_embed = discord.Embed(title=f"{message}", color=colors.purple)
        await ctx.send(embed=say_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command()
async def token(ctx):
    if ctx.author.id == owner_id:
        token = str(bot_token)
        token_mp_embed = discord.Embed(title=f"Voici mon token :\n\n``{token}``")
        token_embed = discord.Embed(title="Mon token vous as été envoyé en MP", color=colors.purple)
        await ctx.message.delete()
        await ctx.author.send(embed=token_mp_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command()
async def help(ctx):
    help_embed = discord.Embed(title="**PAGE D'AIDE**", color=colors.blue)
    help_embed.add_field(name="**Commandes de bases :**", value="d$ping : *Jouer au ping pong ;)*\nd$ServerInfos : *Afficher les infos du serveur*\nd$welcome MEMBER : *Souhaiter la bienvenue à un membre*", inline=False)
    help_embed.add_field(name="Modération", value="d$ban MEMBRE RAISON : *Bannir un membre* (hors bots)\nd$unban MEMBRE : *Débannir un membre (membre#1234)*\nd$kick MEMBRE RAISON : *Expulser un membre* (hors bots)\nd$clear NUMBER : *Effacer des messages*\nd$rename MEMBRE NOM : *Renommer un membre*\nd$role_add MEMBRE RÔLE : *Ajouter un rôle à un membre*\nd$role_remove MEMBRE RÔLE : *Supprimer un rôle à un membre*", inline=False)
    help_embed.add_field(name="Fun", value="d$cat : *Envoyer une image de chat aléatoire*\nd$dog : *Envoyer une image de chien aléatoire*\nd$gif MOT : *Envoyer un gif en rapport avec le mot entré (mot en minuscules)*\nd$joke : *Je vous fait une blague*", inline=False)
    help_embed.add_field(name="Credits :", value="made by PenTaist#4560\nhttps://daryl-bot.tk/", inline=False)
    await ctx.send(embed=help_embed)

@daryl.command()
async def ping(ctx):
    ping_embed = discord.Embed(title='Pong !', color=colors.blue)
    await ctx.send(embed=ping_embed)

@daryl.command()
async def ServerInfos(ctx):
    server = ctx.guild
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    description = server.description
    number_of_members = server.member_count
    if server.description == None:
        description = "Le serveur n'a pas encore de description"
    serverinfos_embed = discord.Embed(title='Infos du serveur :', color=colors.blue)
    serverinfos_embed.add_field(name='Nom du serveur :',value=f'{server}', inline=True)
    serverinfos_embed.add_field(name='Nombre de membres :', value=f'{number_of_members}', inline=True)
    serverinfos_embed.add_field(name='Description du serveur :', value=f'{description}', inline=False)
    serverinfos_embed.add_field(name='Salons textuels :', value=f'{text_channels}', inline=True)
    serverinfos_embed.add_field(name='Salons vocaux :', value=f'{voice_channels}', inline=True)
    await ctx.send(embed=serverinfos_embed)

@daryl.command()
async def welcome(ctx, member: discord.Member):
    welcome_embed = discord.Embed(title=f'Bienvenue {member} !', color=colors.green)
    await ctx.send(embed=welcome_embed)

@daryl.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    mp_ban_embed = discord.Embed(title=f"Vous avez été ban de {ctx.guild}", color=colors.red)
    mp_ban_embed.add_field(name="Ban par :", value=f"{ctx.author}", inline=False)
    mp_ban_embed.add_field(name="Raison :", value=f"{reason}", inline=False)
    if reason == None:
        no_reason_embed = discord.Embed(title="Veuillez spécifier la raison !", color=colors.red)
        no_reason_embed.add_field(name="Utilisation :", value="d$ban MEMBRE RAISON", inline=False)
        await ctx.send(embed=no_reason_embed)
        return
    if ctx.author.top_role < user.top_role:
        no_permissions_embed = discord.Embed(title="Impossible de ban cet utilisateur !", color=colors.red)
        await ctx.send(embed=no_permissions_embed)
        return
    ban_embed = discord.Embed(title=f"{user} à été ban par {ctx.author}", color=colors.green)
    ban_embed.add_field(name="Raison :", value=f"{reason}")
    await user.send(embed=mp_ban_embed)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(embed=ban_embed)
    return

@daryl.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unban_embed = discord.Embed(title=f"Le membre {user} à été débannis par {ctx.author}", color=colors.green)
            await ctx.send(embed=unban_embed)
            return

    error_embed = discord.Embed(title=f"Ce membre n'as pas été trouvé dans la liste des membres bannis !", color=colors.red)
    await ctx.send(embed=error_embed)
    return

@daryl.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    kick_embed = discord.Embed(title=f"{member} à été kick par {ctx.author}", color=colors.green)
    kick_embed.add_field(name="Raison :", value=f"{reason}")
    mp_kick_embed = discord.Embed(title=f"Vous avez été kick de {ctx.guild}", color=colors.red)
    mp_kick_embed.add_field(name="Kick par :", value=f"{ctx.author}", inline=False)
    mp_kick_embed.add_field(name="Raison :", value=f"{reason}", inline=False)
    if ctx.author.top_role <= member.top_role:
        top_role_embed = discord.Embed(title="Impossible de kick cet utilisateur !", color=colors.red)
        await ctx.send(embed=top_role_embed)
        return
    if reason==None:
        no_reason_embed = discord.Embed(title="Veuillez spécifier la raison !", color=colors.red)
        no_reason_embed.add_field(name="Utilisation", value="d$kick MEMBRE RAISON")
        await ctx.send(embed=no_reason_embed)
        return
    await member.send(embed=mp_kick_embed)
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(embed=kick_embed)
    return

@daryl.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    clear_embed = discord.Embed(title=f"{amount} message(s) ont étés supprimés", color=colors.green)
    await ctx.send(embed=clear_embed, delete_after=5)
    await ctx.message.delete()

@daryl.command()
@commands.has_permissions(manage_nicknames=True)
async def rename(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    rename_embed = discord.Embed(title=f"{ctx.author} à changé le pseudo de {member}", color=colors.green)
    rename_embed.add_field(name="Nouveau pseudo :", value=nick, inline=True)
    await ctx.send(embed=rename_embed)

@daryl.command()
@commands.has_permissions(manage_roles=True)
async def role_add(ctx, user : discord.Member, *, role : discord.Role):
    addrole_embed = discord.Embed(title=f"{ctx.author} à ajouté un rôle à {user}", color=colors.green)
    addrole_embed.add_field(name="Rôle :", value=role, inline=False)
    addrole_error_embed = discord.Embed(title=f"Vous ne pouvez pas ajouter le rôle {role} pour l'utilisateur {user} !", color=colors.red)
    if role.position > ctx.author.top_role.position:
        return await ctx.send(embed=addrole_error_embed)
    await user.add_roles(role)
    await ctx.send(embed=addrole_embed)

@daryl.command()
@commands.has_permissions(manage_roles=True)
async def role_remove(ctx, user : discord.Member, *, role : discord.Role):
    delrole_embed = discord.Embed(title=f"{ctx.author} à retiré un rôle à {user}", color=colors.red)
    delrole_embed.add_field(name="Rôle :", value=role, inline=False)
    delrole_error_embed = discord.Embed(title=f"Vous ne pouvez pas retirer le rôle {role} pour l'utilisateur {user} !", color=colors.red)
    if role.position > ctx.author.top_role.position:
        return await ctx.send(embed=delrole_error_embed)
    await user.remove_roles(role)
    await ctx.send(embed=delrole_embed)

@daryl.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
   embed = discord.Embed(title="Wouaf !", color=colors.purple)
   embed.set_image(url=dogjson['link'])
   await ctx.send(embed=embed)

@daryl.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      dogjson = await request.json()
   embed = discord.Embed(title="Coucou le chat !", color=colors.purple)
   embed.set_image(url=dogjson['link'])
   await ctx.send(embed=embed)

@daryl.command(pass_context=True)
async def gif(ctx, *, search):
    giphy_token = "TOKEN GIPHY"
    embed = discord.Embed(colour=discord.Colour.purple())
    session = aiohttp.ClientSession()
    if search == '':
        response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={giphy_token}')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={giphy_token}&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
    await session.close()
    await ctx.send(embed=embed)

@daryl.command()
async def joke(ctx):
    blagues_api_token = "TOKEN BLAGUES API"
    blagues = BlaguesAPI(blagues_api_token)
    blague = await blagues.random()
    embed = discord.Embed(title="Quelqu'un à commandé une blague ?", color=colors.purple)
    embed.add_field(name="Blague :", value=f"{blague.joke}", inline=False)
    embed.add_field(name="Réponse :", value=f"{blague.answer}", inline=False)
    await ctx.send(embed=embed)

daryl.run(bot_token)
