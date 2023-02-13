import discord, json, asyncio, re, random, aiohttp
from discord.ext import commands
from blagues_api import BlaguesAPI

with open("./config.json") as f:
    config = json.load(f)

class conf():
    token = config["token"]
    prefix = config["prefix"]
    owner_id = config["owner_id"]
    blagues_token = config["blagues_token"]
    gif_token = config["gif_token"]

class colors():
    red = discord.Colour.from_rgb(255, 0, 0)
    green = discord.Colour.from_rgb(57, 209, 36)
    blue = discord.Colour.from_rgb(0, 73, 255)
    orange = discord.Colour.from_rgb(255, 133, 0)
    purple = discord.Colour.from_rgb(143, 0, 255)

daryl_intents = discord.Intents.all()
daryl_activity  = discord.Activity(type=discord.ActivityType.playing, name="d$help")

daryl = commands.Bot(command_prefix=conf.prefix, description="Daryl", activity=daryl_activity ,intents=daryl_intents)

owner_id = conf.owner_id
token = conf.token

daryl.remove_command("help")

@daryl.event
async def on_ready():
    print(f"Connected has {daryl.user}")

@daryl.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        arguments_message = f":warning: {ctx.author.mention} Commande Incorrecte, d$help pour afficher la liste des commandes"
        await ctx.send(arguments_message, delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        permissions_messages = f":x: {ctx.author.mention} Tu n'as pas la permission de faire cela"
        await ctx.send(permissions_messages, delete_after=5)

@daryl.command(name="Owner")
async def Owner(ctx):
    if ctx.author.id == owner_id:
        embed = discord.Embed(title="Bonjour, mon créateur :)", description=" ", color=colors.purple)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Seul mon créateur est autorisé à éxécuter cette commande !", description=" ", color=colors.red)
        await ctx.send(embed=embed)

@daryl.command(name="ServersCount")
async def ServersCount(ctx):
    count = len(daryl.guilds)
    
    if ctx.author.id == owner_id:
        ServersCount_embed = discord.Embed(title=f"Je suis actuellement sur {count} serveur(s)", color=colors.purple)
        
        await ctx.send(embed=ServersCount_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command(name="Token")
async def Token(ctx):
    bot_token = token

    if ctx.author.id == owner_id:
        token_mp_embed = discord.Embed(title=f"Voici mon token :\n\n``{bot_token}``", description=" ", color=colors.purple)

        await ctx.message.delete()
        await ctx.author.send(embed=token_mp_embed)
    else:
        not_owner_embed = discord.Embed(title="Seul le créateur du bot peut exécuter cette commande", color=colors.red)
        
        await ctx.send(embed=not_owner_embed, delete_after=5)

@daryl.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Liste des commandes" ,color=colors.blue)
    embed.add_field(name=" ", value="**Commandes de bases :**\n\n**d$ping :** *Jouer au Ping Pong*\n**d$serverinfos :** *Afficher les information du serveur*\n**d$welcome :** *Souhaiter la bienvenue à un membre*", inline=False)
    embed.add_field(name=" ", value="**Modération :**\n\n**d$ban MEMBRE RAISON :** *Bannir un membre*\n**d$unban MEMBRE :** *Débannir un membre*\n**d$bans :** *Afficher la liste des membres bannis*\n**d$kick MEMBRE RAISON :** *Expulser un membre*\n**d$mute MEMBRE ROLE TEMPS RAISON :** *Réduire au silence un membre*\n**d$unmute MEMBRE :** *Rétablir la vois d'un membre*\n**d$warn MEMBRE RAISON :** *Avertir un membre*\n**d$unwarn MEMBRE NOM_DU_WARN :** *Retirer un avertissement à un  membre*\n**d$warns MEMBRE :** *Afficher les avertissements d'un membre*\n**d$clear NOMBRE :** *Supprimer des messages*\n**d$rename MEMBRE PSEUDO :** *Renommer un membre*\n**d$roleadd MEMBRE ROLE :** *Ajouter un rôle à un membre*\n**d$roledel MEMBRE ROLE :** *Retirer un rôle à un membre*", inline=False)
    embed.add_field(name=" ", value="**Fun :**\n\n**d$cat :** *Envoir une image de chat aléatoire*\n**d$dog :** *Envoie une image de chien aléatoire*\n**d$gif MOT :** *Envoie un gif en rapport avec le mot entré*\n**d$joke :** *Je vous fait une blague*", inline=False)
    embed.add_field(name=" ", value="**Autres :**\n\n**d$embed \"MESSAGE\" :** *Envoyer un embed*\n**d$say \"MESSAGE\" :** *Envoyer un message avec le bot*\n**d$rolereact_add ROLE EMOJI ID_MESSAGE :** *Ajouter un rôle réaction*\n**d$rolereact_del ID_MESSAGE :** *Supprimer les rôles réactions*", inline=False)
    embed.add_field(name=" ", value="**Credits :**\n\nBot crée par PenTaist#4560\n\nhttps://pentaist.tk/\nhttps://github.com/PenTaist\n\nhttps://daryl-bot.tk/\nhttps://github.com/PenTaist/Daryl", inline=False)
    embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    await ctx.send(embed=embed)

@daryl.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="Pong !", description=" ", color=colors.blue)
    await ctx.send(embed=embed, delete_after=3)

@daryl.command(name="serverinfos")
async def serverinfos(ctx):
    server = ctx.guild
    server_name = server.name
    server_description = server.description

    if server_description is None:
        server_description = "Le serveur n'as pas de description"
    
    members = 0
    bots = 0
    
    for member in server.members:
        if member.bot:
            bots += 1
        elif not member.bot:
            members += 1
    
    total_members = bots + members
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)

    embed = discord.Embed(title=f"Informations du serveur \"{server_name}\"", description=" ", color=colors.blue)
    embed.add_field(name="Description :", value=server_description, inline=False)
    embed.add_field(name=" ", value=f"**Membres :** {members}")
    embed.add_field(name=" ", value=f"**Bots :** {bots}")
    embed.add_field(name=" ", value=f"**Total :** {total_members}", inline=False)
    embed.add_field(name=" ", value=f"**Salons textuels :** {text_channels}")
    embed.add_field(name=" ", value=f"**Salons vocaux :** {voice_channels}")
    embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    await ctx.send(embed=embed)

@daryl.command(name="welcome")
async def welcome(ctx, member: discord.Member):
    embed = discord.Embed(title=":tada: Bienvenue !", description=f"**{ctx.author.mention} souhaite la bienvenue à {member.mention} !**", color=colors.blue)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLM5ZxKmpk7nwf8H2zQIctCoL7_dsI27J5OA&usqp=CAU")
    await ctx.send(embed=embed)

@daryl.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason = "Aucune raison fournie"):
        author = ctx.author

        mp_ban_embed = discord.Embed(title=f"Vous avez été bannis de \"{ctx.guild}\"", color=colors.red)
        mp_ban_embed.add_field(name=" ", value=f"Raison : {reason}", inline=False)
        mp_ban_embed.add_field(name=" ", value=f"**Modérateur :** {ctx.author}", inline=False)

        embed = discord.Embed(title=f"{user} à été bannis par {author}", color=colors.red)
        embed.add_field(name="raison :", value=f"{reason}")

        if ctx.author.top_role <= user.top_role:
            top_role_message = "Impossible de ban cet utilisateur !"
            top_role_embed = discord.Embed(title=top_role_message, color=colors.red)
            top_role_embed.add_field(name=" ", value=f"*Commande exécutée par {author}*", inline=False)
            await ctx.send(embed=top_role_embed)

        await user.send(embed=mp_ban_embed)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(embed=embed)

@daryl.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            unban_embed = discord.Embed(title=f"{user} à été débannis par {ctx.author}", color=colors.green)
            await ctx.guild.unban(user)
            await ctx.send(embed=unban_embed)

@daryl.command(name="bans")
@commands.has_permissions(ban_members=True)
async def bans(ctx):
    guild = ctx.guild
    bans = await guild.bans()

    if bans == []:
        no_bans_embed = discord.Embed(title="La liste des membres bannis est vide", color=colors.blue)
        no_bans_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
        
        await ctx.send(embed=no_bans_embed)
        return
    else:
        for ban in bans:
            bans_embed = discord.Embed(title="Liste des membres bannis", description=f"{ban.user.name}#{ban.user.discriminator}", color=colors.blue)
            bans_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

            await ctx.send(embed=bans_embed)

@daryl.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason = "Aucune raison fournie"):
    kick_embed = discord.Embed(title=f"{member} à été expulsé(e) du serveur", color=colors.red)
    kick_embed.add_field(name="Auteur :", value=f"{ctx.author}")
    kick_embed.add_field(name="raison :", value=f"{reason}")
    
    mp_kick_embed = discord.Embed(title=f"Vous avez été expulsé(e) de \"{ctx.guild}\"", color=colors.red)
    mp_kick_embed.add_field(name=" ", value=f"Raison : {reason}", inline=False)
    mp_kick_embed.add_field(name=" ", value=f"**Modérateur :** {ctx.author}", inline=False)
    
    if ctx.author.top_role <= member.top_role:
        top_role_embed = discord.Embed(title="Impossible d'expulser cet utilisateur !", color=colors.red)
        top_role_embed.add_field(name=" ", value=f"*Commande executée par {ctx.author}*", inline=False)
        await ctx.send(embed=top_role_embed)
        return

    await member.send(embed=mp_kick_embed)
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(embed=kick_embed)
    return

@daryl.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: str, *, reason: str):
    mute_role_name = "Muted"
    mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)

    if not mute_role:
        mute_role = await ctx.guild.create_role(name=mute_role_name)
    
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, add_reactions=False, connect=False)

    await member.add_roles(mute_role, reason=reason)

    mute_embed = discord.Embed(title=f"{member} à été réduis au silence", color=colors.red)
    mute_embed.add_field(name="Raison  : ", value=reason)
    mute_embed.add_field(name="Durée  : ", value=f"{duration}")
    mute_embed.add_field(name="Modérateur :", value=ctx.author, inline=False)

    mp_mute_embed = discord.Embed(title=f"Vous avez été réduis au silence", color=colors.red)
    mp_mute_embed.add_field(name="Durée :", value=f"{duration}", inline=False)
    mp_mute_embed.add_field(name="Raison :", value=reason, inline=False)
    mp_mute_embed.add_field(name="Modérateur :", value=ctx.author, inline=False)

    await member.send(embed=mp_mute_embed)
    await ctx.send(embed=mute_embed)

    match = re.match("([0-9]+)([smh])", duration)

    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        if unit == "s":
            duration = amount
        elif unit == "m":
            duration = amount * 60
        elif unit == "h":
            duration = amount * 60 * 60
    else:
        embed = discord.Embed(title="Durée non valide !", description=" ", color=colors.red)
        await ctx.send(embed=embed, delete_after=5)
        return

    await asyncio.sleep(duration)

    await member.remove_roles(mute_role, reason="Fin de la durée de mute")

@daryl.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role_name = "Muted"
    mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)

    unmute_embed = discord.Embed(title=f"{member} à retrouvé sa voix", color=colors.green)
    unmute_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    await member.remove_roles(mute_role)
    await ctx.send(embed=unmute_embed)

def load_warnings():
    try:
        with open("warnings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("warnings.json", "w") as f:
            json.dump({}, f)
        return {}

def save_warnings(warnings):
    with open("warnings.json", "w") as f:
        json.dump(warnings, f)

warnings = load_warnings()

@daryl.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, user: discord.User, *, reason = "Aucune raison fournie"):
    user_id = str(user.id)
    
    if user_id in warnings:
        warnings[user_id]["count"] += 1
        warnings[user_id]["reasons"].append(reason)
    else:
        warnings[user_id] = {"count": 1, "reasons": [reason]}
    
    save_warnings(warnings)
    
    mp_warn_embed = discord.Embed(title="Vous avez reçus un avertissement !", description=" ", color=colors.red)
    mp_warn_embed.add_field(name="Serveur :", value=ctx.guild.name, inline=False)
    mp_warn_embed.add_field(name="Modérateur :", value=ctx.author.mention, inline=False)
    mp_warn_embed.add_field(name="Raison :", value=reason, inline=False)

    warn_embed = discord.Embed(title=" ", description=f"**{user.mention} as été avertis par {ctx.author.mention}**", color=colors.red)
    warn_embed.add_field(name="Raison :", value=reason, inline=False)
    warn_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    await ctx.send(embed=warn_embed)
    await user.send(embed=mp_warn_embed)

@daryl.command(name="unwarn")
@commands.has_permissions(ban_members=True)
async def unwarn(ctx, user: discord.User, *, reason: str):
    user_id = str(user.id)

    if user_id in warnings:
        if reason in warnings[user_id]["reasons"]:
            warnings[user_id]["reasons"].remove(reason)
            warnings[user_id]["count"] -= 1
            if warnings[user_id]["count"] == 0:
                warnings.pop(user_id, None)
            
            save_warnings(warnings)
            
            unwarn_embed = discord.Embed(title=" ", description=f"Avertissement pour **{reason}** retiré à {user.mention}", color=colors.green)
            unwarn_embed.add_field(name=" ", value=f"Modérateur : {ctx.author.mention}")

            await ctx.send(embed=unwarn_embed)
        else:
            unwarn_embed = discord.Embed(title=" ", description=f"Avertissement pour **{reason}** introuvable pour {user.mention}", color=colors.red)

            await ctx.send(embed=unwarn_embed, delete_after=5)
    else:
        unwarn_embed = discord.Embed(title=" ", description=f"{user.mention} n'a aucun avertissement", color=colors.red)

        await ctx.send(embed=unwarn_embed, delete_after=5)

@daryl.command(name="warns")
@commands.has_permissions(ban_members=True)
async def warns(ctx, user: discord.User):
    user_id = str(user.id)

    if user_id in warnings:
        warn_count = warnings[user_id]["count"]
        reason_list = "\n".join(warnings[user_id]["reasons"])

        warns_embed = discord.Embed(title=" ", description=f"**Voici la liste des avertissements de {user.mention} :**", color=colors.blue)
        warns_embed.add_field(name=" ", value=f"\n\n{reason_list}", inline=False)
        warns_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
        
        await ctx.send(embed=warns_embed)
    else:
        warns_embed = discord.Embed(title=" ", description=f"**{user.mention} n'a aucuns avertissements**", color=colors.blue)
        warns_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

        await ctx.send(embed=warns_embed, delete_after=5)

@daryl.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount >= 1 and amount <= 1000:
        await ctx.channel.purge(limit=amount+1)

        if amount == 1:
            text_embed = f"{amount} message a été supprimé"
        elif amount > 1:
            text_embed = f"{amount} messages ont été supprimés"

        clear_embed = discord.Embed(title=text_embed, color=colors.green)

        await ctx.send(embed=clear_embed, delete_after=5)
        await ctx.message.delete()
    else:
        await ctx.send(f":warning: {ctx.author.mention} veuillez indiquez un nombre entre 1 et 1000 !")

@daryl.command(name="rename")
@commands.has_permissions(manage_nicknames=True)
async def rename(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

    rename_embed = discord.Embed(title=f"Le pseudo de {member} à été changé", color=colors.green)
    rename_embed.add_field(name="Nouveau pseudo :", value=nick, inline=True)
    rename_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    
    await ctx.send(embed=rename_embed)

@daryl.command(name="roleadd")
@commands.has_permissions(manage_roles=True)
async def roleadd(ctx, user : discord.Member, *, role : discord.Role):
    addrole_embed = discord.Embed(title=f"{user} à reçu le rôle {role}", color=colors.green)
    addrole_embed.add_field(name="Rôle :", value=role, inline=False)
    addrole_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    addrole_error_embed = discord.Embed(title=f"Je ne peut pas ajouter le rôle {role} pour l'utilisateur {user} !", color=colors.red)
    addrole_error_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    
    if role.position > ctx.author.top_role.position:
        return await ctx.send(embed=addrole_error_embed)
    if role.position == ctx.author.top_role.position:
        return await ctx.send(embed=addrole_error_embed)
    
    await user.add_roles(role)
    await ctx.send(embed=addrole_embed)

@daryl.command(name="roledel")
@commands.has_permissions(manage_roles=True)
async def roledel(ctx, user : discord.Member, *, role : discord.Role):
    delrole_embed = discord.Embed(title=f"{user} à perdus le rôle {role}", color=colors.red)
    delrole_embed.add_field(name="Rôle :", value=role, inline=False)
    delrole_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    delrole_error_embed = discord.Embed(title=f"Je ne peut pas retirer le rôle {role} pour l'utilisateur {user} !", color=colors.red)
    delrole_error_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    if role.position > ctx.author.top_role.position:
        return await ctx.send(embed=delrole_error_embed)
    if role.position == ctx.author.top_role.position:
        return await ctx.send(embed=delrole_error_embed)

    await user.remove_roles(role)
    await ctx.send(embed=delrole_embed)

@daryl.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      dogjson = await request.json()
   embed = discord.Embed(title="Ho un chat !", color=colors.purple)
   embed.set_image(url=dogjson['link'])
   embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
   await ctx.send(embed=embed)

@daryl.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
   embed = discord.Embed(title="Coucou le chien !", color=colors.purple)
   embed.set_image(url=dogjson['link'])
   embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
   await ctx.send(embed=embed)

@daryl.command(pass_context=True)
async def gif(ctx, *, search):
    api_key = conf.gif_token

    embed = discord.Embed(colour=colors.purple)
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={api_key}')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
        embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={api_key}&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
        embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)
    await session.close()
    await ctx.send(embed=embed)

@daryl.command(name="joke")
async def joke(ctx):
    blagues_token = conf.blagues_token
    blagues = BlaguesAPI(blagues_token)
    blague = await blagues.random()

    embed = discord.Embed(title="J'en ai une bonne !", color=colors.purple)
    embed.add_field(name="Blague :", value=f"{blague.joke}", inline=False)
    embed.add_field(name="Réponse :", value=f"{blague.answer}", inline=False)
    embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    await ctx.send(embed=embed)

@daryl.command(name="embed")
async def embed(ctx, message):
    embed = discord.Embed(title=" ", description=f"**{message}**", color=colors.purple)
    await ctx.send(embed=embed)

@daryl.command(name="say")
async def say(ctx, message):
    await ctx.send(message)

@daryl.command(name="rolereact_add")
@commands.has_permissions(manage_roles=True)
@commands.has_permissions(add_reactions=True)
async def rolereact_add(ctx, role: discord.Role, emoji: str, message_id: int):
    rr_add_embed = discord.Embed(title=f"Le rôle {role} à été assigné à la réaction {emoji}", color=colors.green)
    rr_add_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    message = await ctx.channel.fetch_message(message_id)
    await message.add_reaction(emoji)

    @daryl.event
    async def on_raw_reaction_add(payload):
        if payload.message_id == message_id and payload.emoji.name == emoji:
            guild = daryl.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            
            await member.add_roles(role)

    @daryl.event
    async def on_raw_reaction_remove(payload):
        if payload.message_id == message_id and payload.emoji.name == emoji:
            guild = daryl.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            
            await member.remove_roles(role)
    
    await ctx.send(embed=rr_add_embed, delete_after=5)

@daryl.command(name="rolereact_del")
@commands.has_permissions(manage_messages=True)
@commands.has_permissions(add_reactions=True)
async def rolereact_del(ctx, message_id: int):
    rr_del_embed = discord.Embed(title="Toutes les réactions ont été supprimés", color=colors.green)
    rr_del_embed.add_field(name=" ", value=f"*Commande exécutée par {ctx.author}*", inline=False)

    message = await ctx.channel.fetch_message(message_id)
    reactions = message.reactions

    for reaction in reactions:
        async for user in reaction.users():
            await reaction.remove(user)
            await ctx.send(embed=rr_del_embed, delete_after=5)

daryl.run(token)