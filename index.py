import json
import time
import discord
import requests
import random

from os import remove
from qrcode import make
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from riotwatcher import LolWatcher
watcher = LolWatcher("RGAPI-25a8145c-b7d6-4312-92f1-8a8a0795c185")

prefix = "/"
bot = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True
)
slash = SlashCommand(bot, True)

@bot.event   
async def on_ready():
    print(f"Le Bot {bot.user} est connecté !")
    await bot.change_presence(
        activity=discord.Streaming(
            name=f"{prefix}aide | {len(bot.guilds)} serveurs.",
            url="https://twitch.tv/steusso"
        ))
    x = []
    for guild in bot.guilds:
        x.append(guild.id)
    print(len(x))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@slash.slash(
    name="aide",
    description="Commande d'aide si tu es perdu",
)
async def aide(
    ctx
):
    select = create_select(
        options=[
            create_select_option(
                label="League of Legends 🎇",
                value="lol",
                description="Commandes liées à League of Legends."
            ),
            create_select_option(
                label="Manga 🈹",
                value="manga",
                description="Commandes liées aux mangas."
            ),
            create_select_option(
                label="Autres 👓",
                value="other",
                description="Commandes liées à la modération."
            ),
            create_select_option(
                label="Pièces 💲",
                value="coin",
                description="Commandes liées au casino."
            )
        ],
        placeholder="Catégorie :",
        min_values=1,
        max_values=1
    )
    fait_choix = await ctx.send(f"{ctx.author.mention}, tu peux choisir la catégorie des commandes 📈 :", components=[create_actionrow(select)])
    def check(m):
        return m.author.id == ctx.author.id and m.origin_message_id == fait_choix.id
    choix_ctx = await wait_for_component(bot, components=select, check=check)
    if choix_ctx.values[0]=="lol":
        e = discord.Embed(
            title="Aide :",
            description="Commandes d'aides concernant League of Legends.",
            color=0x0bf9f4
        )
        e.add_field(
            name=f"{prefix}rank (region) (pseudo)",
            value="Commande donnant le rank d'un certain joueur en fonction se sa région.",
            inline=True
        )
        e.add_field(
            name=f"{prefix}freechamps (region)",
            value="Donne la liste des champions gratuits de la semaine (reset chaque mardi).",
            inline=True
        )
        e.set_thumbnail(
            url="https://logo-marque.com/wp-content/uploads/2020/11/League-of-Legends-Embleme.png"
        )
        e.set_footer(
            text=f"Commande demandée par {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
        await choix_ctx.send(embed=e)
    if choix_ctx.values[0]=="manga":
        e = discord.Embed(
            title="Aide :",
            description="Commandes d'aides concernant les mangas.",
            color=0xf9510b
        )
        e.add_field(
            name=f"{prefix}manga (nom_manga)",
            value="Donne des infos sur un manga choisi au préalable.",
            inline=True
        )
        e.set_thumbnail(
            url="https://www.pngall.com/wp-content/uploads/2/Manga-PNG-Clipart.png"
        )
        e.set_footer(
            text=f"Commande demandée par {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
        await choix_ctx.send(embed=e)
    if choix_ctx.values[0]=="other":
        e = discord.Embed(
            title="Aide :",
            description="Commandes d'aides concernant des commandes diverses.",
            color=0x0bf96c
        )
        e.add_field(
            name=f"{prefix}avatar (membre)",
            value="Donne l'avatar d'un membre du serveur.",
            inline=True
        )
        e.add_field(
            name=f"{prefix}qrcode (lien) (afficher_lien)",
            value="Renvoie un QRCode révelant le lien/message que vous avez défini au préalable.",
            inline=True
        )
        e.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/189/189665.png"
        )
        e.set_footer(
            text=f"Commande demandée par {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
        await choix_ctx.send(embed=e)
    if choix_ctx.values[0]=="coin":
        e = discord.Embed(
            title="Aide :",
            description="Commandes d'aides conernant le casino.",
            color=0xe5ff00
        )
        e.add_field(
            name=f"{prefix}pièces (membre)",
            value="Permet de connaître le nombres de pièces que possède un membre du serveur.",
            inline=True
        )
        e.add_field(
            name=f"{prefix}parier (mise)",
            value="Permet de miser une somme sur un lancé de 2 dés. Si la somme des dés lancés est supérieur à celle des dés lancés par le bot, vous gagnez votre mise. Sinon, vous la perdez.",
            inline=True
        )
        e.add_field(
            name=f"{prefix}give (membre) (somme)",
            value="Permet de donner une certaine somme de pièces à un autre membre du serveur.",
            inline=True
        )
        e.set_thumbnail(
            url="https://cdn-icons.flaticon.com/png/512/3592/premium/3592598.png?token=exp=1653687068~hmac=e37d865ca7da834336573732d79f645d"
        )
        e.set_footer(
            text=f"Commande demandée par {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
        await choix_ctx.send(embed=e)
    else:
        pass

@slash.slash(
    name="rank",
    description="Donne le rank d'un compte League of Legends",
    options=[
        create_option(
            name="region",
            description="La région du compte associé",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="Europe de l'Ouest",
                    value="euw1"
                ),
                create_choice(
                    name="Europe du Nord",
                    value="eun1"
                ),
                create_choice(
                    name="Brésil",
                    value="br1"
                ),
                create_choice(
                    name="Japon",
                    value="jp1"
                ),
                create_choice(
                    name="Corée",
                    value="kr"
                ),
                create_choice(
                    name="Amérique Latine",
                    value="la1"
                ),
                create_choice(
                    name="Amérique du Nord",
                    value="na1"
                ),
                create_choice(
                    name="Océanie",
                    value="oc1"
                ),
                create_choice(
                    name="Turquie",
                    value="tr1"
                ),
                create_choice(
                    name="Russie",
                    value="ru"
                )
            ]
        ),
        create_option(
            name="pseudo",
            description="Le pseudo du compte League of Legends",
            option_type=3,
            required=True
        )
    ]
)
async def rank(
    ctx,
    region : str,
    *,
    pseudo : str
):
    summoner = watcher.summoner.by_name(region, pseudo)
    name = summoner["name"]
    await ctx.send(f"✅ Joueur trouvé sous le nom de **{name}**. Veuillez patienter...")
    league = watcher.league.by_summoner(region, summoner["id"])

    length = len(league)
    queues = []
    ranks = []
    wrs = []
    totaux = []
    for i in range(length):
        queue : str = league[i]["queueType"]
        queues.append(queue)
        tier : str = league[i]["tier"]
        nb : str = league[i]["rank"]
        lp : int = league[i]["leaguePoints"]
        rank = f"{tier} {nb} {lp} LP"
        ranks.append(rank)
        win : int = league[i]["wins"]
        losses : int = league[i]["losses"]
        total : int = win + losses
        wr : int = f"{round((100*win)/total, 2)}%"
        totaux.append(total)
        wrs.append(wr)

    queues_changed = []
    with open("data.json", "r") as f:
        data = json.load(f)
        url = data[0][tier]
        for i in range(length):
            queue_changed = data[1][queues[i]]
            queues_changed.append(queue_changed)

    e = discord.Embed(
        title=f"Rank de {name} 📊 :",
        description="Rank dans les différentes queues du joueur.",
        color=0x5bcb37 
    )
    for k in range(length):
        e.add_field(
            name=f"{queues_changed[k]} 📈 :",
            value=f"{ranks[k]} • {wrs[k]} en {totaux[k]} parties.",
            inline=True
        )
    e.add_field(
        name="Mentions Légales :",
        value="Samira#2710 isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.",
        inline=False
    )
    e.set_footer(
        text=f"Commande demandée par {ctx.author}",
        icon_url=ctx.author.avatar_url
    )
    e.set_thumbnail(
        url=url
    )
    
    time.sleep(3)
    await ctx.send(embed=e)

@slash.slash(
    name="avatar",
    description="Donne l'avatar d'un compte Discord",
    options=[
        create_option(
            name="user",
            description="Utilisateur pour qui tu souhaites avoir l'avatar",
            option_type=6,
            required=True
        )
    ]
)
async def avatar(
    ctx,
    *,
    user : discord.User
):
    e = discord.Embed(
        title=f"Avatar de {user} :",
        description="Avatar de l'utilisateur sélectionné.",
        color=0x2243f4
    )
    e.set_image(
        url=user.avatar_url
    )
    e.set_footer(
        text=f"Commande demandée par {ctx.author}",
        icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=e)

@slash.slash(
    name="freechamps",
    description="Donne des informations plus globales sur un compte",
    options=[
        create_option(
            name="region",
            description="La région du compte",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="Europe de l'Ouest",
                    value="euw1"
                ),
                create_choice(
                    name="Europe du Nord",
                    value="eun1"
                ),
                create_choice(
                    name="Brésil",
                    value="br1"
                ),
                create_choice(
                    name="Japon",
                    value="jp1"
                ),
                create_choice(
                    name="Corée",
                    value="kr"
                ),
                create_choice(
                    name="Amérique Latine",
                    value="la1"
                ),
                create_choice(
                    name="Amérique du Nord",
                    value="na1"
                ),
                create_choice(
                    name="Océanie",
                    value="oc1"
                ),
                create_choice(
                    name="Turquie",
                    value="tr1"
                ),
                create_choice(
                    name="Russie",
                    value="ru"
                )
            ]
        )
    ]
)
async def freechamps(
    ctx,
    *,
    region : str
):
    rotations = watcher.champion.rotations(region)
    ids = rotations["freeChampionIds"]
    champions = []
    with open("champion.json", "r") as f:
        data = json.load(f)
        for i in range(len(ids)):
            champion = data[str(ids[i])]
            champions.append(champion)
    latest = champions[0].replace(" ", "")
    if latest=="RenataGlasc":
        latest = "Renata"
    if "'" in latest:
        latest = latest.replace("'", "")
    
    e = discord.Embed(
        title="Champions gratuits de la semaine :",
        description=f"Région séléctionnée : {region}",
        color=0x1df02c
    )
    e.add_field(
        name="Champions :",
        value=",\n".join(champions)
    )
    
    e.set_thumbnail(
        url=f"http://ddragon.leagueoflegends.com/cdn/12.5.1/img/champion/{latest}.png"
    )
    e.set_footer(
        text=f"Commande demandée par {ctx.author}",
        icon_url=ctx.author.avatar_url
    )
    e.add_field(
        name="Mentions Légales :",
        value="Samira#2710 isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.",
        inline=False
    )
    await ctx.send(embed=e)

@slash.slash(
    name="qrcode",
    description="Donne un QRCode pour un lien donné",
    options=[
        create_option(
            name="lien",
            description="Lien à convertir en QRCode",
            option_type=3,
            required=True
        ),

        create_option(
            name="afficher_lien",
            description="Savoir si tu veux que ton lien complet soit inclus, ou caché dans le message",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="Caché",
                    value="hide"
                ),
                create_choice(
                    name="Public",
                    value="open"
                )
            ]
        )
    ]
)
async def qrcode(
    ctx,
    lien : str,
    *,
    afficher_lien : str
):
    img = make(lien)
    img.save("test.png")

    if afficher_lien=="hide":
        e = discord.Embed(
            title="QRCode",
            description="QRCode d'un certain lien caché... Attention à ne pas tout ouvrir ! Faites attention.",
            color=0x0bf9f4
        )
    else:
        e = discord.Embed(
            title="QRCode",
            description=f"QRCode de ce [lien]({lien}) ! Attention à ne pas tout ouvrir ! Faites attention.",
            color=0x0bf9f4
        )
    file = discord.File("H:/Utilisateurs/Abdoul/Documents/Abdoul/Programmation/Kayn/test.png", filename="test.png")
    e.set_image(
        url="attachment://test.png"
    )
    e.set_footer(
        text=f"Commande demandée par {ctx.author}",
        icon_url=ctx.author.avatar_url
    )

    await ctx.send(file=file, embed=e)
    remove("test.png")

@slash.slash(
    name="manga",
    description="Informations sur un manga souhaité",
    options=[
        create_option(
            name="nom",
            description="Nom du manga souhaité",
            option_type=3,
            required=True
        )
    ]
)
async def manga(
    ctx,
    *,
    nom : str
):
    response = requests.get(f"https://kitsu.io/api/edge//anime?filter[text]={nom}")
    data = response.json()["data"]
    option=[]
    for i in range(10):
        synopsis = str(data[i]["attributes"]["synopsis"])
        if len(synopsis)>50:
            synopsis = f"{synopsis[:22]}..."
        else:
            pass
        name = str(data[i]["attributes"]["canonicalTitle"])
        if len(name)>25:
            name = f"{name[:22]}..."
        else:
            pass
        option.append(
            create_select_option(
                label=name,
                value=str(i),
                description=synopsis[:50]
            )
        )
    select = create_select(
        options=option,
        placeholder="Le manga :",
        min_values=1,
        max_values=1
    )
    fait_choix = await ctx.send(f'{ctx.author.mention}, tu peux choisir le manga de ton choix parmi cette liste comprenant les mangas se rapprochant le plus du nom "**{nom}**". 🌟', components=[create_actionrow(select)])
    def check(m):
        return m.author.id == ctx.author.id and m.origin_message_id == fait_choix.id
    choix_ctx = await wait_for_component(bot, components=select, check=check)
    value = int(choix_ctx.values[0])
    data = data[value]
    type_manga = data["type"]
    data = data["attributes"]
    title_en = data["canonicalTitle"]
    title_jp = data["titles"]["ja_jp"]
    trailer = data["youtubeVideoId"]
    synopsis = data["synopsis"]
    img = data["posterImage"]["original"]
    note = data["averageRating"]
    startDate = data["startDate"]
    endDate = data["endDate"]
    nb_episodes = data["episodeCount"]
    duree_episodes = data["episodeLength"]
    e = discord.Embed(
        title=f"Informations sur {title_en} :",
        description=f"Trailer [**ici**](https://youtube.com/watch?v={trailer}) ; Nom japonais : **{title_jp}**",
        color=0x0bf911
    )
    e.add_field(
        name="Synopsis",
        value=synopsis[:1021]+"...",
        inline=False
    )
    e.add_field(
        name="Note sur 100 :",
        value=f"{note}%"
    )
    e.add_field(
        name="Le manga a commencé :",
        value=startDate
    )
    e.add_field(
        name="Le manga s'est terminé :",
        value=endDate
    )
    e.add_field(
        name="Nombre d'épisodes :",
        value=nb_episodes
    )
    e.add_field(
        name="Durée d'un épisode :",
        value=f"{duree_episodes} minutes."
    )
    e.add_field(
        name="Type :",
        value=type_manga
    )
    e.set_thumbnail(
        url=img
    )
    e.set_footer(
        text=f"Commande demandée par {ctx.author}",
        icon_url=ctx.author.avatar_url
    )
    await choix_ctx.send(embed=e)

@slash.slash(
    name="puanteur",
    description="Donne le pourcentage de puanteur d'un membre",
    options=[
        create_option(
            name="member",
            description="Membre dont on souhaite connaître la puanteur",
            option_type=6,
            required=True
        )
    ]
)
async def puanteur(
    ctx,
    *,
    member : discord.Member
):
    nb = random.randint(0, 100)
    await ctx.send(f"{member.mention}, ton indice de puanteur est de {nb}%.")

@slash.slash(
    name="pièces",
    description="Voir combien tu ou quelqu'un a d'argent",
    options=[
        create_option(
            name="member",
            description="Le membre en question",
            option_type=6,
            required=True
        )
    ]
)
async def pièces(
    ctx,
    *,
    member : discord.Member
):
    with open("coins.json", "r") as f:
        data = json.load(f)
        try:
            nb = data[str(member.id)]
        except KeyError:
            await ctx.send(f"{member.mention} n'est pas enregistré dans ma base de donnée, ou bien c'est un bot 🤖.")
    await ctx.send(f"{member.mention} a **{nb}** pièces :coin:.")

@slash.slash(
    name="parier",
    description="Mise ton argent dans un jeu de dé",
    options=[
        create_option(
            name="mise",
            description="La mise que tu souhaites placer dans ce pari",
            option_type=4,
            required=True
        )
    ]
)
async def parier(
    ctx,
    *,
    mise : int
):
    member = ctx.author
    with open("coins.json", "r") as f:
        data = json.load(f)
        try:
            nb = data[str(member.id)]
        except KeyError:
            await ctx.send(f"{member.mention} n'est pas enregistré dans ma base de donnée, ou bien c'est un bot 🤖.")
    if mise>nb or mise<=0:
        await ctx.send(f"Soit tu as mis une mise négative, sois tu veux parier plus de pièces que tu n'en as, sois raisonnable ! {ctx.author.mention}, tu as **{nb}** :coin: pièces.")
    else:
        if mise>round(1/2*nb):
            await ctx.send(f"{ctx.author.mention}, tu ne peux pas miser plus de la moitié de tes pièces, sois raisonnable 💲 ! Tu as **{nb}** :coin: pièces, tu ne peux pas miser plus de **{round(1/2*nb)}** :coin: pièces.")
        else:
            message = await ctx.send(f"{member.mention} lance les dés...")
            lancer_1 = random.randint(1, 6)
            lancer_2 = random.randint(1, 6)
            lancer_3 = random.randint(1, 6)
            lancer_4 = random.randint(1, 6)
            time.sleep(3)
            await message.edit(content=f"{member.mention} a lancé les dés et a obtenu un **{lancer_1}**, et un **{lancer_2}**.")
            time.sleep(3)
            await message.edit(content=f"L'opposant de {member.mention} a lancé les dés et a obtenu un **{lancer_3}**, et un **{lancer_4}**.")
            time.sleep(3)
            if lancer_1+lancer_2>lancer_3+lancer_4:
                if lancer_1==lancer_2:
                    with open("coins.json", "r+") as f:
                        data = json.load(f)
                        data[str(member.id)] = nb + mise*2
                        f.seek(0)
                        json.dump(data, f)
                        f.truncate()
                    await message.edit(content=f"{member.mention} a fait un **double** ! Tu gagnes deux fois ta mise de **{mise}** pièces :coin:, soit **{mise*2}** :coin: pièces !")
                else:
                    with open("coins.json", "r+") as f:
                        data = json.load(f)
                        data[str(member.id)] = nb + mise
                        f.seek(0)
                        json.dump(data, f)
                        f.truncate()
                    await message.edit(content=f"{member.mention} a gagné **{mise}** pièces :coin:.")
            if lancer_1+lancer_2<lancer_3+lancer_4:
                await message.edit(content=f"{member.mention} a perdu **{mise}** pièces :coin:.")
                with open("coins.json", "r+") as f:
                    data = json.load(f)
                    data[str(member.id)] = nb - mise
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
            if lancer_1+lancer_2==lancer_3+lancer_4:
                await message.edit(content=f"{member.mention} garde sa mise de **{mise}** pièces :coin:, tu restes à **{nb}** pièces..")

@slash.slash(
    name="give",
    description="Donne des pièces à quelqu'un",
    options=[
        create_option(
            name="member",
            description="Le membre auquel tu souhaites envoyer des pièces",
            option_type=6,
            required=True
        ),
        create_option(
            name="somme",
            description="La somme que tu souhaites donné",
            option_type=4,
            required=True
        )
    ]
)
async def give(
    ctx,
    *,
    member : discord.Member,
    somme : int
):
    with open("coins.json", "r") as f:
        data = json.load(f)
        nb = data[str(ctx.author.id)]
        nb2 = data[str(member.id)]
    if somme>nb or somme<=0:
        await ctx.send(f"Soit tu as mis une valeur négative, sois tu veux donner plus de pièces que tu n'en as, sois raisonnable ! {ctx.author.mention}, tu as **{nb}** :coin: pièces.")
    else:
        with open("coins.json", "r+") as f:
            data = json.load(f)
            data[str(ctx.author.id)] = nb - somme
            data[str(member.id)] = nb2 + somme
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        await ctx.send(f"{ctx.author.mention}, tu avais **{nb}** :coin: pièces et tu en as désormais **{nb-somme}** :coin:. Quant à toi {member.mention}, on t'a généreusement donné **{somme}** :coin: pièces, tu en as désormais **{nb2+somme}** :coin:.")

@slash.slash(
    name="classement",
    description="Classement de ceux qui ont le plus de pièces",
    options=[]
)
async def classement(
    ctx
):
    with open("coins.json", "r") as f:
        data = json.load(f)
        ids = []
        msgs = []
        for i in range(len(data)):
            id = list(data)[i]
            ids.append(id)
            if data[id]==200:
                pass
            else:
                msg = f"<@{id}> • {data[id]} :coin:"
                msgs.append(msg)
    e = discord.Embed(
        title="Classement 📊 :",
        description="Les joueurs n'ayant que 200 pièces ne sont pas ajoutés.",
        color=0x09ff00
    )
    e.add_field(
        name="Noms :",
        value="\n".join(msgs),
        inline=True
    )
    e.set_footer(
            text=f"Commande demandée par {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
    await ctx.send(embed=e)

bot.run("")
