# Les imports
import discord
from discord.ext import commands, tasks
import asyncio as a
import random
import os
import datetime as dt


# Le blabla du début
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="d!", intents=intents)
# slash = SlashCommand(bot, sync_commands=True)
bot.channels = []

# Début du code

# Démarrage du bot
@bot.event
async def on_ready():
    print("Bot connecté")
    ChannelID = 969714441400754186
    channel = bot.get_channel(ChannelID)
    await channel.send("Je suis ici!")
    anniversaire.start()


#   _____          _______  _____
#  |  __ \     /\ |__   __||  __ \
#  | |__) |   /  \   | |   | |__) |
#  |  _  /   / /\ \  | |   |  ___/
#  | | \ \  / ____ \ | |   | |
#  |_|  \_\/_/    \_\|_|   |_|

bot.équipes = 0
bot.tous_les_résultats = {}
point_par_ligne = {
    "RER D": 1.5,
    "RER E": 2,
    "T1": 1,
    "T2": 1,
    "T3A": 1,
    "T3B": 1,
    "T4": 2,
    "T11": 2,
}

# Nombre d'équipes
@bot.command(name="r_équipes")
@commands.has_role(969725736363622470)
async def set_équipes(ctx):
    # Variables de fonction
    guild = ctx.guild
    print(ctx.message.author)
    print(type(ctx.message.author))
    ratp_une_équipe = False
    ratp_pas_nombre = False
    # Combien d'équipes jouent
    if "thomas-carré" in ctx.channel.name:
        cb_équipes_vont_jouer = await ctx.send("Combien d'équipes vont jouer ?")

        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel

        while True:
            ask_nbre_équipes = await bot.wait_for("message", check=check_message)
            bot.équipes = ask_nbre_équipes.content
            if bot.équipes.isdigit() and bot.équipes != "1":
                bot.équipes = int(bot.équipes)
                y_aura_cb_équipes = await ctx.send(
                    "Il y aura " + str(bot.équipes) + " équipes"
                )
                break
            elif bot.équipes == "1":
                bot.ratp_une_équipe = True
                une_équipe = await ctx.send("Une équipe ? C'est chaud là mon reuf")
                embed = discord.Embed(title="", description="")
                embed.set_image(
                    url="https://c.tenor.com/LIX8OttaVncAAAAC/foss-no-bitches.gif"
                )
                no_bitches_message = await ctx.send(embed=embed)
                await a.sleep(1)
                en_vrai_man = await ctx.send("En vrai, y'en a combien ?")
            else:
                bot.ratp_pas_nombre = True
                pas_nombre = await ctx.send(":x: C'est pas un nombre ça, j'reconnais")
                combien_du_coup = await ctx.send("Mais du coup, y'en a combien ?")
        # Qui dans chaque équipe
        for didier in range(bot.équipes):
            didier += 1
            y_a_qui = await ctx.send("Qui dans l'équipe " + str(didier) + " ?")
            réponse_y_a_qui = await bot.wait_for("message", check=check_message)
            membres_content_set = réponse_y_a_qui.content
            membres_content_str = str(membres_content_set)
            membres_content_temp = membres_content_str.split(" ")
            membres_content = []
            for x in membres_content_temp:
                x = x[2:]
                x = x[:-1]
                x = int(x)
                print(x)
                noms_des_membres_pour_les_rôles = ctx.message.guild.get_member(x)
                print(noms_des_membres_pour_les_rôles)
                membres_content.append(ctx.message.guild.get_member(x))
            dict_temp = {"membres": membres_content}
            bot.tous_les_résultats[didier] = dict_temp
            bot.tous_les_résultats[didier]["y_a_qui"] = y_a_qui
            bot.tous_les_résultats[didier]["réponse_y_a_qui"] = réponse_y_a_qui
        print(bot.tous_les_résultats)
        # Créer un rôle par équipe
        didier = 0
        for didier in range(bot.équipes):
            didier = didier + 1
            await guild.create_role(
                name="Équipe " + str(didier), color=discord.Colour.random()
            )
        # Assigner les joueurs à un rôle
        didier = 0
        équipes_liste = []
        for didier in range(bot.équipes):
            didier = didier + 1
            role = discord.utils.get(ctx.guild.roles, name="Équipe " + str(didier))
            bot.tous_les_résultats[didier]["rôle"] = role
            équipes_liste.append(role)
            for x in bot.tous_les_résultats[didier]["membres"]:
                await x.add_roles(role)
        # bot.tous_les_résultats["Liste des équipes"]=équipes_liste
        await a.sleep(1)
        équipes_attribuées = await ctx.send(
            ":white_check_mark: Les équipes ont été attribuées"
        )
        # Créer une catégorie
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            # bot.tous_les_résultats["Liste des équipes"]: discord.PermissionOverwrite(read_messages=True)
        }
        didier = 0
        for didier in range(bot.équipes):
            didier += 1
            overwrites[
                bot.tous_les_résultats[didier]["rôle"]
            ] = discord.PermissionOverwrite(read_messages=True)
        bot.catégorie = await guild.create_category("Équipes", overwrites=overwrites)
        await a.sleep(1)
        catégorie_créée = await ctx.send(":white_check_mark: La catégorie a été créée")
        # Créer un channel par équipe
        didier = 0
        await a.sleep(1)
        for didier in range(bot.équipes):
            didier = didier + 1
            await a.sleep(1)
            bot.tous_les_résultats[didier]["création_channel"] = await ctx.send(
                "Création du channel textuel de l'équipe "
                + str(didier)
                + " en cours..."
            )
            sous_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                bot.tous_les_résultats[didier]["rôle"]: discord.PermissionOverwrite(
                    read_messages=True
                ),
            }
            channel = await guild.create_text_channel(
                "équipe-" + str(didier),
                category=bot.catégorie,
                overwrites=sous_overwrites,
            )
            bot.channels.append(channel)
        await a.sleep(2)
        channels_créés = await ctx.send(":white_check_mark: Channels textuels créés")
        await a.sleep(1)
        auto_suppression = await ctx.send("Tout s'auto-delete dans 5 secondes")
        await a.sleep(5)
        await ctx.message.delete()
        await cb_équipes_vont_jouer.delete()
        await ask_nbre_équipes.delete()
        await y_aura_cb_équipes.delete()
        if ratp_une_équipe == True:
            await une_équipe.delete()
            await no_bitches_message.delete()
            await en_vrai_man.delete()
        if ratp_pas_nombre == True:
            await pas_nombre.delete()
            await combien_du_coup.delete()
        for didier in range(bot.équipes):
            didier += 1
            await bot.tous_les_résultats[didier]["y_a_qui"].delete()
            await bot.tous_les_résultats[didier]["réponse_y_a_qui"].delete()
        await équipes_attribuées.delete()
        await catégorie_créée.delete()
        for didier in range(bot.équipes):
            didier += 1
            await bot.tous_les_résultats[didier]["création_channel"].delete()
        await channels_créés.delete()
        await auto_suppression.delete()

    # Si c'est pas le bon channel
    else:
        pas_bon_channel = await ctx.send(":x: Pas le bon channel")
        await a.sleep(5)
        await ctx.message.delete()
        await pas_bon_channel.delete()


# Au cas où j'éteins par erreur
@bot.command(name="r_set")
@commands.has_role(969725736363622470)
async def set(ctx):
    # Variables de fonction
    def check_message(message):
        return message.author == ctx.author and message.channel == ctx.channel
    # Combien d'équipes
    if "thomas-carré" in ctx.channel.name:
        combien = await ctx.send("Ah, là y'a pas d'équipes. Y'en avait combien ?")
        nbre_équipes_message = await bot.wait_for("message", check=check_message)
        try:
            nbre_équipes = int(nbre_équipes_message.content)
        except ValueError:
            troll = await ctx.send("Espèce de petit troll, tu dois recommencer la commande maintenant :face_with_raised_eyebrow:")
            await a.sleep(5)
            await ctx.message.delete()
            await combien.delete()
            await nbre_équipes_message.delete()
            await troll.delete()
            return
        bot.équipes = nbre_équipes
        check_pour_troll = discord.utils.get(ctx.message.guild.roles, name="Équipe " + str(bot.équipes))
        if check_pour_troll == None:
            troll = await ctx.send("Espèce de petit troll, tu dois recommencer la commande maintenant :face_with_raised_eyebrow:")
            await a.sleep(5)
            await ctx.message.delete()
            await combien.delete()
            await nbre_équipes_message.delete()
            await troll.delete()
        else:
            good = await ctx.send(":white_check_mark: C'est bon")
            await a.sleep(5)
            await ctx.message.delete()
            await combien.delete()
            await nbre_équipes_message.delete()
            await good.delete()


# Calcul des points
@bot.command(name="r_arrêts")
@commands.has_role(969725736363622470)
async def arrêts(ctx):
    if "thomas-carré" in ctx.channel.name:
        # Variables de fonction
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        pas_drôle_check = False
        # Si pas encore d'équipe
        if bot.équipes == 0:
            faire_r_équipes = await ctx.send(":warning: Attention, il faut définir un nombre d'équipes puis réessayer la commande")
            await a.sleep(5)
            await faire_r_équipes.delete()
        # Détermination
        else:
            départ_question = await ctx.send("Quelle est la station de départ ?")
            départ_message = await bot.wait_for("message", check=check_message)
            départ = départ_message.content
            arrivée_question = await ctx.send("Quelle est la station d'arrivée ?")
            arrivée_message = await bot.wait_for("message", check=check_message)
            arrivée = arrivée_message.content
            liste_arrêts = []
            # print(départ, arrivée)
            read_arrêts_lignes = open(os.path.join(os.path.dirname(__file__), "liste-arrêts-Paris-intramuros.txt"), "r", encoding="utf-8")
            for x in read_arrêts_lignes:
                x = x[:-1]
                if not départ in x and not arrivée in x:
                    liste_arrêts.append(x)
            # print(liste_arrêts)
            read_arrêts_lignes.close()
            cb_arrêt_question = await ctx.send("Combien d'arrêts imposés ?")
            cb_arrêt_message = await bot.wait_for("message", check=check_message)
            cb_arrêt = cb_arrêt_message.content
            cb_arrêt_int = int(cb_arrêt)
            liste_arrêts_choisis = []
            if cb_arrêt_int == 1:
                pas_drôle = await ctx.send("Vous êtes pas drôles")
                pas_drôle_check = True
            if cb_arrêt_int >= 2:
                for roger in range(bot.équipes):
                    roger +=1
                    for didier in range(cb_arrêt_int):
                        # dict_temp={}
                        didier+=1
                        while True:
                            arrêt_choisi = "".join(random.choices(liste_arrêts))
                            if arrêt_choisi in liste_arrêts_choisis:
                                pass
                            else:
                                liste_arrêts_choisis.append(arrêt_choisi)
                                channel = discord.utils.get(ctx.guild.channels, name="équipe-" + str(roger))
                                arrêts_chosis_message = await channel.send(arrêt_choisi)
                                # dict_temp["arrêts_choisis_message"] = arrêts_chosis_message
                                # bot.tous_les_résultats[didier] = dict_temp
                                break
            arrêts_envoyés = await ctx.send("Vos arrêts imposés ont été envoyés dans vos channels respectifs")
            await a.sleep(3)
            await ctx.message.delete()
            await départ_question.delete()
            await départ_message.delete()
            await arrivée_question.delete()
            await arrivée_message.delete()
            await cb_arrêt_question.delete()
            await cb_arrêt_message.delete()
            if pas_drôle_check == True:
                await pas_drôle.delete()
            else:
                await arrêts_envoyés.delete()



# Reset
@bot.command(name="r_reset")
@commands.has_role(969725736363622470)
async def reset(ctx):
    message_du_reset = await ctx.send("On sort le lance-flamme ?")
    await message_du_reset.add_reaction("✅")
    await message_du_reset.add_reaction("❌")

    def check_emoji(reaction, user):
        return (
            ctx.message.author == user
            and message_du_reset.id == reaction.message.id
            and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
        )

    reaction, user = await bot.wait_for("reaction_add", check=check_emoji)
    # Si je veux reset
    if reaction.emoji == "✅":
        while True:
            if bot.équipes != 0:
                for x in range(bot.équipes):
                    x = x + 1
                    role = discord.utils.get(
                        ctx.message.guild.roles, name="Équipe " + str(x)
                    )
                    await role.delete()
                for didier in range(bot.équipes):
                    await bot.channels[didier].delete()
                await bot.catégorie.delete()
                finito_pipo = await ctx.send("Reset terminé :thumbsup:")
                await a.sleep(5)
                await ctx.message.delete()
                await message_du_reset.delete()
                try:
                    await erreur.delete()
                except UnboundLocalError:
                    await finito_pipo.delete()
                    break
                await ask_nbre_équipes.delete()
                await finito_pipo.delete()
                break
            else:
                # Si le bot a redémarré entre temps
                erreur = await ctx.send(
                    "Ah, là y'a pas d'équipes. Y'en avait combien ?"
                )

                def check_message(message):
                    return (
                        message.author == ctx.author and message.channel == ctx.channel
                    )

                ask_nbre_équipes = await bot.wait_for("message", check=check_message)
                # Voir si c'est un chiffre
                try:
                    bot.équipes = int(ask_nbre_équipes.content)
                except ValueError:
                    troll = await ctx.send(
                        "Espèce de petit troll, tu dois recommencer la commande maintenant :face_with_raised_eyebrow:"
                    )
                    await a.sleep(5)
                    await ctx.message.delete()
                    await message_du_reset.delete()
                    await erreur.delete()
                    await ask_nbre_équipes.delete()
                    await troll.delete()
                    break
                # Voir si le jeu a même pas encore commencé
                check_pour_troll = discord.utils.get(
                    ctx.message.guild.roles, name="Équipe " + str(bot.équipes)
                )
                if check_pour_troll == None:
                    troll = await ctx.send(
                        "Espèce de petit troll, tu dois recommencer la commande maintenant :face_with_raised_eyebrow:"
                    )
                    await a.sleep(5)
                    await ctx.message.delete()
                    await message_du_reset.delete()
                    await erreur.delete()
                    await ask_nbre_équipes.delete()
                    await troll.delete()
                    break
                didier = 0
                for didier in range(bot.équipes):
                    didier = didier + 1
                    channel = discord.utils.get(
                        ctx.guild.channels, name="équipe-" + str(didier)
                    )
                    bot.channels.append(channel)
                bot.catégorie = discord.utils.get(ctx.guild.categories, name="Équipes")

    else:
        arabe = await ctx.send("Ah (-rabe)")
        await a.sleep(5)
        await ctx.message.delete()
        await message_du_reset.delete()
        await arabe.delete()


#   _____        _             _ _                   _                          _          
#  |  __ \      | |           | ( )                 (_)                        (_)         
#  | |  | | __ _| |_ ___    __| |/  __ _ _ __  _ __  ___   _____ _ __ ___  __ _ _ _ __ ___ 
#  | |  | |/ _` | __/ _ \  / _` |  / _` | '_ \| '_ \| \ \ / / _ \ '__/ __|/ _` | | '__/ _ \
#  | |__| | (_| | ||  __/ | (_| | | (_| | | | | | | | |\ V /  __/ |  \__ \ (_| | | | |  __/
#  |_____/ \__,_|\__\___|  \__,_|  \__,_|_| |_|_| |_|_| \_/ \___|_|  |___/\__,_|_|_|  \___|

# Dictionnaire des anniversaires
bday_txt = open(os.path.join(os.path.dirname(__file__), "anniversaires_filtrés.txt"), "r", encoding="utf-8")
bday_read = bday_txt.read()
bday_txt.close()
bday_dictionnary = {}
liste_bday = bday_read.split("\n")
index_bday = 0
while index_bday != len(liste_bday):
    bday_date = liste_bday[index_bday]
    index_bday+=1
    bday_name = liste_bday[index_bday]
    index_bday+=1
    try:
        bday_dictionnary[bday_date].append(bday_name)
    except KeyError:
        bday_dictionnary[bday_date] = [bday_name]


# Envoyer un message pour les anniversaires
@tasks.loop(hours=24)
async def anniversaire():
    ctx = bot.get_channel(1000525423429554337)
    maintenant = dt.datetime.now()
    date_du_jour = maintenant.strftime("%m%d")
    if date_du_jour in bday_dictionnary:
        for bday in bday_dictionnary[date_du_jour]:
            await ctx.send(bday + " fête son anniversaire !")

@anniversaire.before_loop
async def before_anniversaire():
    for _ in range(60*60*24):
        if dt.datetime.now().hour == 0:
            print('Les anniversaires arrivent !')
            return
        await a.sleep(1)

# À mettre à la toute fin
token_txt = open(os.path.join(os.path.dirname(__file__), "bot token.txt"), "r", encoding="utf-8")
token = token_txt.read()
token_txt.close()
bot.run(token)