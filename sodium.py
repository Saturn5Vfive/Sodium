import base64
import ctypes
import threading

import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from pyfiglet import Figlet
import hashlib
import discord
import random
import string
import json
from discord.ext import commands
import requests
import os
import unicodedata
import time
import datetime
import re

intents = discord.Intents.default()
intents.all()
client = commands.Bot(command_prefix="~", self_bot=True, fetch_offline_members = False, intents=intents)
yellow = '\033[1;33m'

last = []
webhooks = []
whname = ""
whimg = ""
whcont = ""
sniper = False

codeRegex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
print(f"{yellow}░██████╗░█████╗░██████╗░██╗██╗░░░██╗███╗░░░███╗")
print(f"{yellow}██╔════╝██╔══██╗██╔══██╗██║██║░░░██║████╗░████║")
print(f"{yellow}╚█████╗░██║░░██║██║░░██║██║██║░░░██║██╔████╔██║")
print(f"{yellow}░╚═══██╗██║░░██║██║░░██║██║██║░░░██║██║╚██╔╝██║")
print(f"{yellow}██████╔╝╚█████╔╝██████╔╝██║╚██████╔╝██║░╚═╝░██║")
print(f"{yellow}╚═════╝░░╚════╝░╚═════╝░╚═╝░╚═════╝░╚═╝░░░░░╚═╝")
print(f"{yellow}Sodium selfbot made by saturn5Vfive#3541")
print(f"{yellow}Signing into token...")
conreader = open("config.json", "r")
content = conreader.read()
conreader.close()
config = json.loads(content)
token = config["token"]

def ddembed(title, content):
    str = "```ini\n"
    titl = "[" + title + "]\n\n"
    str = str + titl
    for line in content:
        linestr = line[1:]
        if line.startswith("|"):
            str += "[" + linestr + "]\n"
        elif line.startswith("$"):
            str += "[] " + linestr + " []"
        else:
            str += line

    str += "```"
    return str

#sussy
def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def sha1sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def md5sum(filename):
    h  = hashlib.md5()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def sodiumguild():
    for guild in client.guilds:
        if guild.name == "Sodium [" + client.user.name + "]":
            return guild

def results():
    guild = sodiumguild()
    for channel in guild.text_channels:
        if channel.name == "results":
            return channel


def results():
    guild = sodiumguild()
    for channel in guild.text_channels:
        if channel.name == "results":
            return channel


def logger():
    guild = sodiumguild()
    for channel in guild.text_channels:
        if channel.name == "logging":
            return channel

def naembed(titlez, contentz):
   eobj = discord.Embed(title=titlez, description=contentz, colour=0xffe345)
   eobj.set_thumbnail(url="https://cdn.discordapp.com/attachments/908215400913846272/916541602934169640/logo.png")
   return eobj


def nasimple(contentz):
    return naembed("Sodium", contentz)


def flood(ip):
    for i in range(10):
        r = requests.get(ip)


@client.event
async def on_message(message):
    global sniper, whname
    global webhooks
    global last
    if ("discord.gift" in message.content) and sniper:
        eff = codeRegex.search(message.content)
        if eff:
            nitrocode = eff.group(2)
            if len(nitrocode) < 16:
                return
            result = requests.post(f'https://discordapp.com/api/v6/entitlements/gift-codes/{nitrocode}/redeem', json={'channel_id': str(message.channel.id)}, headers={'authorization': token, 'user-agent': 'Mozilla/5.0'})
            if 'This gift has been redeemed already' in str(result.content):
                await logger().send(embed=nasimple(f"Sniper:\nTried to snipe `{nitrocode}`, code already redeemed"))
            elif 'nitro' in str(result.content):
                await logger().send(embed=nasimple(f"Sniper:\nCode Successfully sniped! `{nitrocode}`"))
            elif 'Unknown Gift Code' in str(result.content):
                await logger().send(embed=nasimple(f"Sniper:\nInvalid code `{nitrocode}`"))
    if not message.content.startswith("~"):
        return
    if message.author.id != client.user.id:
        george = False
        for item in config["whitelist"]:
            if item == message.author.id:
                george = True
        if not george:
            return
        if george:
            await logger().send(embed=naembed("Sodium", f"Executor: `{message.author.name}`\nCommand: `{message}`"))
    await message.delete()
    if config["delete-embeds"]:
        for item in last:
            await item.delete()
    last.clear()
    arr = message.content.split(" ")
    if arr[0] == "~help":
        if len(arr) < 2:
            embed = naembed("Sodium", "Categories:\n\nhelp raid - give help on raid commands\nhelp misc - misc commands\nhelp minecraft - minecraft related commands\nhelp tools - epic tools\nhelp moderation - moderation commands\nsetup - setup the selfbot")
            a = await message.channel.send(embed=embed)
            last.append(a)
        else:
            if arr[1] == "raid":
                embed = naembed("Sodium",
                                "Raid:\n\nspam [amount] - spam the message\ndelete [c/r/e/w] - delete channels, roles, emojis, or webhooks\ncreate [c/r/e] [text/file] - create channels, roles, or emojis\neveryone - ping everyone bypass\nformat - format the server\nclear - clear the chat")
                a = await message.channel.send(embed=embed)
                last.append(a)
            elif arr[1] == "misc":
                embed = naembed("Sodium",
                                "Misc:\n\nascii [text] - make text big\nrandom [unicode/ascii] [amount] - print some random stuff\nrepeat [amount] [string] - repeat a string an amount\nsniper [enable/disable] - enable or disable discord nitro sniper\nhide [normal text] | [hidden text] - hide some text\nnitro [link] - create a fake nitro message\nstream [link] [text] - fake streaming on twitch\nstatus [playing/watching/listening] [text] - set your discord status\nlog [text] - log some text to the logging channel\nspmove [amount] - spam leave and join the vc you are currently connected to\navatar [mention] - get a users avatar")
                a = await message.channel.send(embed=embed)
                last.append(a)
            elif arr[1] == "minecraft":
                embed = naembed("Sodium",
                                "Minecraft:\n\nfind [username] - find a user on minehut\nserver [server] - get server information\nplugins [server] - get server plugins\nplayers [server] - get the players on a server\nusername [username] - get a minecraft username info")
                a = await message.channel.send(embed=embed)
                last.append(a)
            elif arr[1] == "tools":
                embed = naembed("Sodium",
                                "Tools:\n\nlookup [ip] - lookup an ip\nuser [mention] - get user data\nhook [add/clear/view/spam/send] [content] - manage webhooks\ntokenpart [userid] - get partial token of a user\nbencode [text] - base64encode text\nbdecode [text] - base64decode text\nhash [text/file] - get the hash of a string or a file\nshorten [link] - shorten a url\nreverse [string] - reverse a string")
                a = await message.channel.send(embed=embed)
                last.append(a)
            elif arr[1] == "moderation":
                embed = naembed("Sodium",
                                "Moderation:\n\nban [mention] - ban a member\nkick [mention] - kick a member\ndelete [mention] [amount] - delete a amount of messages from a user\npurge [amount] - purge the chat\nspurge [amount] [user] - purges from a specific person")
                a = await message.channel.send(embed=embed)
                last.append(a)

    if arr[0] == "~kick":
        user = message.mentions[0]
        await user.kick()
        a = await message.channel.send(embed=nasimple("Kicked " + arr[1]))
        last.append(a)
    if arr[0] == "~ban":
        user = message.mentions[0]
        await user.ban()
        a = await message.channel.send(embed=nasimple("Banned " + arr[1]))
        last.append(a)
    if arr[0] == "~purge":
        async for msg in message.channel.history(limit=int(arr[1])):
            await msg.delete()
        a = await message.channel.send(embed=nasimple("Purge Completed!"))
        last.append(a)
    if arr[0] == "~spurge":
        async for msg in message.channel.history(limit=int(arr[1])):
            if msg.author == message.mentions[0]:
                await msg.delete()
        a = await message.channel.send(embed=nasimple("Purge Completed!"))
        last.append(a)
    if arr[0] == "~quit":
        await message.channel.send(embed=nasimple("Quitting..."))
        quit()
    if arr[0] == "~reverse":
        if (len(arr) < 2):
            return
        if (len(arr) >= 2):
            arr[0] = ""
            total = " ".join(arr)
            rev = total[::-1]
            emb = nasimple(f"Reverse: `{rev}`")
            a = await message.channel.send(embed=emb)
            last.append(a)
    if arr[0] == "~username":
        if len(arr) < 2:
            return
        try:
            minecraftuser = requests.get("https://api.mojang.com/users/profiles/minecraft/" + arr[1])
            te = minecraftuser.text
            jso = json.loads(te)
            name = jso.get("name")
            uuid = jso.get("id")
            msgtot = ""
            pastusers = requests.get("https://api.mojang.com/user/profiles/" + str(uuid) + "/names")
            dump = pastusers.text
            element = json.loads(dump)
            for pastuser in element:
                j = pastuser["name"]
                msgtot += "`" + j + "`" + "\n"
            body = nasimple(arr[1])
            body.add_field(name="Description", value="Username: " + name + "\n" + "UUID: " + str(uuid))
            body.add_field(name="Past Usernames", value=msgtot)
            a = await message.channel.send(embed=body)
            last.append(a)
        except Exception as e:
            a = await message.channel.send(embed=nasimple("Invalid Username"))
            last.append(a)
    if arr[0] == "~avatar":
        if len(arr) < 2:
            return
        try:
            user = message.mentions[0]
            if not user:
                a = await message.channel.send(embed=nasimple("Mention someone in your message to get their avatar"))
                last.append(a)
                return
            emb = nasimple("Avatar of " + user.name)
            emb.set_image(url=user.avatar_url)
            a = await message.channel.send(embed=emb)
            last.append(a)
        except Exception as e:
            a = await message.channel.send(embed=nasimple("Mention someone in your message to get their avatar"))
            last.append(a)
    if arr[0] == "~find":
        try:
            serverlistr = requests.get("https://api.minehut.com/servers")
            servertext = serverlistr.text
            serverjson = json.loads(servertext)
            serverlist = serverjson.get("servers")
            minecraftuser = requests.get("https://api.mojang.com/users/profiles/minecraft/" + arr[1])
            te = minecraftuser.text
            jso = json.loads(te)
            target = jso.get("id")
            tid = "NONETYPE"
            for server in serverlist:
                serverplayerdata = server["playerData"]
                serverplayers = serverplayerdata["players"]
                for player in serverplayers:
                    strippedplayer = player.replace("-", "")
                    if strippedplayer == target:
                        tid = server["name"]
                        break
            if tid == "NONETYPE":
                a = await message.channel.send(embed=nasimple(f"Player `{arr[1]}` was not found on any servers"))
                last.append(a)
            else:
                a = await message.channel.send(embed=nasimple(f"Player `{arr[1]}` was found on `{tid}`"))
                last.append(a)
        except Exception as e:
            a = await message.channel.send(embed=nasimple(f"Player `{arr[1]}` was not found on any servers"))
            last.append(a)
    if arr[0] == "~server":
        try:
            msgtotal = ""
            mhserver = requests.get("https://api.minehut.com/server/" + arr[1] + "?byName=true")
            serverjson = mhserver.text
            pj = json.loads(serverjson)
            mainserver = pj.get("server")
            root = pj.get("server").get("server_properties")
            response = requests.get(
                "https://merchandise-service-prod.superleague.com/merchandise/v1/merchandise/products/?populateVersions=true")  # cache requests
            pluginstext = response.text
            pluginsjson = json.loads(pluginstext)
            plugins = pluginsjson["products"]
            serverplugman = pj["server"]["installed_content"]
            pluglist = ""
            for plugin in serverplugman:
                for serverplugin in plugins:
                    if serverplugin["sku"] == plugin["content_id"]:
                        pluglist += serverplugin["title"] + "\n"
            body = naembed(arr[1], mainserver.get("motd"))
            body.add_field(name="Information\n",
                           value="**Players**: " + str(mainserver.get("activePlayers")) + "/" + str(
                               mainserver.get("maxPlayers")) + "\n" + "**Online**: " + str(
                               mainserver.get("online")) + "\n" + "**Suspended**: " + str(mainserver.get("suspended")))
            body.add_field(name="Properties\n",
                           value="**Plan**: " + str(mainserver.get("activeServerPlan")) + "\n" + "**Software**: " + str(
                               root.get("server_version_type")) + "\n" + "**CommandBlocks**: " + str(
                               root.get("enable_command_block")) + "\n" + "**HostileMobs**: " + str(
                               root.get("spawn_mobs")) + "\n" + "**PassiveMobs**: " + str(
                               root.get("spawn_animals")) + "\n" + "**Seed**: " + str(
                               root.get("level_seed")) + "\n" + "**World Name**: " + str(
                               root.get("level_name")) + "\n" + "**Nether**: " + str(mainserver.get("allow_nether")))
            body.add_field(name="Plugins", value="PlayerServer\n" + pluglist)
            a = await message.channel.send(embed=body)
            last.append(a)
        except Exception as e:
            a = await message.channel.send(embed=nasimple("Server Not Found"))
            last.append(a)
    if arr[0] == "~players":
        try:
            primer = nasimple("Fetching players on " + arr[1] + " [This takes a while]")
            await message.channel.send(embed=primer)
            serverlistr = requests.get("https://api.minehut.com/servers")
            servertext = serverlistr.text
            serverjson = json.loads(servertext)
            serverlist = serverjson.get("servers")
            compnames = ""
            found = False
            for server in serverlist:
                if server["name"].lower().strip("\n").strip() == arr[1].lower().strip("\n").strip(" "):
                    found = True
                    poi = server["playerData"]
                    players = poi["players"]
                    for player in players:
                        minecraftrequest = requests.get("https://api.mojang.com/user/profiles/" + player + "/names")
                        mctext = minecraftrequest.text
                        mcjson = json.loads(mctext)
                        nameobject = mcjson[(len(mcjson) - 1)]
                        compnames = compnames + "`" + nameobject["name"] + "`" + "\n"
                    embedd = naembed("Players on " + arr[1], compnames)
                    a = await message.channel.send(embed=embedd)
                    last.append(a)
            if not found:
                a = await message.channel.send(embed=nasimple("Server Not Found"))
                last.append(a)
                return
        except Exception as e:
            a = await message.channel.send(embed=nasimple("Server Not Found"))
            last.append(a)
    if arr[0] == "~plugins":
        try:
            msgtotal = ""
            mhserver = requests.get("https://api.minehut.com/server/" + arr[1] + "?byName=true")
            serverjson = mhserver.text
            pj = json.loads(serverjson)
            mainserver = pj.get("server")
            root = pj.get("server").get("server_properties")
            response = requests.get(
                "https://merchandise-service-prod.superleague.com/merchandise/v1/merchandise/products/?populateVersions=true")  # cache requests
            pluginstext = response.text
            pluginsjson = json.loads(pluginstext)
            plugins = pluginsjson["products"]
            serverplugman = pj["server"]["installed_content"]
            pluglist = ""
            for plugin in serverplugman:
                for serverplugin in plugins:
                    if serverplugin["sku"] == plugin["content_id"]:
                        pluglist += serverplugin["title"] + "\n"
            body = naembed(f"Plugins on {arr[1]}", f"PlayerServer\n{pluglist}")
            a = await message.channel.send(embed=body)
            last.append(a)
        except Exception as e:
            a = await message.channel.send(embed=nasimple("Server Not Found"))
            last.append(a)
    if arr[0] == "~clear":
        for i in range(4):
            newlines = "\n"
            for i in range(1900):
                newlines += "\n"
            await message.channel.send("᲼" + newlines + "᲼")
    if arr[0] == "~format":
        if len(arr) < 5:
            return
        arr[0] = ""
        arr[1] = ""
        arr[2] = ""
        arr[3] = ""
        joiner = " ".join(arr)
        eb = nasimple("Editing Guild")
        msi = await message.channel.send(embed=eb)
        last.append(msi)
        await message.guild.edit(name=arr[2], desc=joiner, icon=open(arr[3], 'rb').read())
    if arr[0] == "~create":
        server = message.channel.guild
        if arr[1] == "c":
            if len(arr) > 3:
                custom = arr[3]
                amount = 0
                try:
                    amount = int(arr[2])
                except:
                    return
                for i in range(amount):
                    await server.create_text_channel(custom)
                    time.sleep(0.3)
            else:
                amount = 0
                try:
                    amount = int(arr[2])
                except:
                    return
                for i in range(amount):
                    await server.create_text_channel("MOLED")
                    time.sleep(0.3)
        if arr[1] == "r":
            if len(arr) > 3:
                custom = arr[3]
                amount = 0
                try:
                    amount = int(arr[2])
                except:
                    return
                for i in range(amount):
                    await server.create_role(name=custom)
                    time.sleep(0.3)
            else:
                amount = 0
                try:
                    amount = int(arr[2])
                except:
                    return
                for i in range(amount):
                    await server.create_role(name="MOLED")
                    time.sleep(0.3)
    if arr[0] == "~everyone":
        pings = []
        membes = []
        async for msg in message.channel.history(limit=150):
            if not msg.author in membes:
                pings.append("<@" + str(msg.author.id) + ">")
                membes.append(msg.author)
        pingstring = ""
        for ping in pings:
            pingstring += ping + " "
        if len(pingstring) > 1900:
            return
        ping = await message.channel.send(f"@everyone ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ {pingstring}")
    if arr[0] == "~delete":
        server = message.channel.guild
        if arr[1] == "c":
            for channel in server.text_channels:
                try:
                    await channel.delete()
                    time.sleep(0.1)
                except:
                    pass
            for channel in server.voice_channels:
                try:
                    await channel.delete()
                    time.sleep(0.1)
                except:
                    pass
            for channel in server.stage_channels:
                try:
                    await channel.delete()
                    time.sleep(0.1)
                except:
                    pass
            for category in server.categories:
                try:
                    await category.delete()
                    time.sleep(0.1)
                except:
                    pass
            await server.create_text_channel("text")
        if arr[1] == "r":
            for role in server.roles:
                try:
                    await role.delete()
                    time.sleep(0.1)
                except:
                    pass
        if arr[1] == "e":
            for emoji in server.emojis:
                try:
                    await emoji.delete()
                    time.sleep(0.1)
                except:
                    pass
        if arr[1] == "w":
            for webhook in server.integrations:
                try:
                    await webhook.delete()
                    time.sleep(0.1)
                except:
                    pass
    if arr[0] == "~spam":
        for i in range((int(arr[1]))):
            chois = []
            for j in range(50):
                chois.append("{} " + "[" + random.choice(config["insults"]).upper() + "] {}\n")
            emb = ddembed(config["raid"]["heading"], chois)
            await message.channel.send(
                f"@everyone " + config["raid"]["body"] + "\n" + config["raid"]["image_url"] + "\n" + emb)
            time.sleep(1)
    if arr[0] == "~nitro":
        if len(arr) < 2:
            return
        nitro = discord.Embed(title="Nitro Gift", description="Click Me To Redeem!", url=arr[1])
        nitro.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/911695673626353804/914439333648412682/download.png")
        await message.channel.send("https://discord.com/gift/RRGBAN50GKNTBAY", embed=nitro)
    if arr[0] == "~hide":
        arr[0] = ""
        strin = " ".join(arr)
        before, after = strin.split("|")
        await message.channel.send(
            f"{before}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ {after}")
    if arr[0] == "~spmove":
        cc = message.author.voice.channel
        if cc is None:
            return
        amount = 0
        try:
            amount = int(arr[1])
        except:
            return
        msi = await message.channel.send(embed=nasimple("Spamming moves"))
        last.append(msi)
        for _ in range(amount):
            for voiceclient in client.voice_clients:
                await voiceclient.disconnect()
            await cc.connect()
    if arr[0] == "~sniper":
        if sniper:
            sniper = False
        else:
            sniper = True
        ams = await message.channel.send(embed=nasimple(f"Toggled Sniper\nSniper is now `{str(sniper)}`"))
        last.append(ams)
    if arr[0] == "~log":
        arr[0] = ""
        await logger().send(embed = nasimple(" ".join(arr)))
    if arr[0] == "~repeat":
        for i in range(int(arr[1])):
            arr[0] = ""
            arr[1] = ""
            the = " ".join(arr)
            await message.channel.send(the)
    if arr[0] == "~random":
        if arr[1] == "unicode":
            unicodes = ["𧟝", "𡤻", "龗", "鱻", "爩", "䴑", "䰱", "䯂", "𪈾", "䶫", "䴒", "䖇", "齾", "䨺", "齉", "靐", "齉", "䲜",
                        "龘", "䨻", "𪚥", "你", "好", "们", "里", "的", "嗨", "我", "嗨", "我", "很", "们", "这", "上", "为", "里"]
            the = ""
            for i in range(int(arr[2])):
                the += random.choice(unicodes)
            a = await message.channel.send(embed=nasimple(the))
            last.append(a)
        if arr[1] == "ascii":
            letters = string.ascii_letters
            the = ""
            for i in range(int(arr[2])):
                the += random.choice(letters)
            a = await message.channel.send(embed=nasimple(the))
            last.append(a)
    if arr[0] == "~ascii":
        arr[0] = ""
        tex = " ".join(arr)
        f = Figlet(font="slant")
        returner = f.renderText(tex)
        await message.channel.send(f"```{returner}```")
    if arr[0] == "~hash":
        if len(message.attachments) > 0:
            try:
                await message.attachments[0].save("hashable")
                em = nasimple("File Hash")
                em.add_field(name="Sha1", value=sha1sum("hashable"), inline=False)
                em.add_field(name="Sha256", value=sha256sum("hashable"), inline=False)
                em.add_field(name="Md5", value=md5sum("hashable"), inline=False)
                ams = await message.channel.send(embed=em)
                last.append(ams)
            except:
                a = await message.channel.send(embed=nasimple("Error While Hashing file"))
                last.append(a)
        else:
            arr[0] = ""
            l = "".join(arr)
            em = nasimple("Text Hash")
            em.add_field(name="Sha1", value=hashlib.sha1(l.encode('ascii')).hexdigest(), inline=False)
            em.add_field(name="Sha256", value=hashlib.sha256(l.encode('ascii')).hexdigest(), inline=False)
            em.add_field(name="Md5", value=hashlib.md5(l.encode('ascii')).hexdigest(), inline=False)
            ams = await message.channel.send(embed=em)
            last.append(ams)
    if arr[0] == "~bdecode":
        try:
            base = base64.b64decode(arr[1].encode('ascii')).decode('ascii')
            ams = await message.channel.send(embed=nasimple(f"Result: `{base}`"))
            last.append(ams)
        except:
            ams = await message.channel.send(embed=nasimple(f"Result: `Could Not Decode Base64`"))
            last.append(ams)
    if arr[0] == "~bencode":
        ams = await message.channel.send(embed=nasimple(f"Result: `{base64.b64encode(arr[1].encode('ascii')).decode('ascii')}`"))
        last.append(ams)
    if arr[0] == "~tokenpart":
        partone = base64.b64encode(arr[1].encode('ascii')).decode('ascii')
        ams = await message.channel.send(embed=nasimple(f"Token: `{partone}.XXXX.XXXXXXXXXXXXXXXX`"))
        last.append(ams)
    if arr[0] == "~hook":
        if len(arr) < 2:
            a = await message.channel.send(embed=nasimple("Please use ~hook [add/clear/view/spam/send/content/avatar/username/multisend] [content/amount]"))
            last.append(a)
            return

        if arr[1] == "add":
            webhooks.append(arr[2])
            a = await message.channel.send(embed=nasimple("Added Webhook"))
            last.append(a)


        if arr[1] == "clear":
            webhooks.clear()
            a = await message.channel.send(embed=nasimple("cleared embeds"))
            last.append(a)

        if arr[1] == "username":
            arr[0] = ""
            arr[1] = ""
            lol = "".join(arr)
            whname = lol.strip()
            b = await message.channel.send(embed=nasimple(f"Webhook Name : `{lol.strip()}`"))
            last.append(b)

        if arr[1] == "content":
            arr[0] = ""
            arr[1] = ""
            lol = "".join(arr)
            whcont = lol.strip()
            b = await message.channel.send(embed=nasimple(f"Webhook Content : `{lol.strip()}`"))
            last.append(b)

        if arr[1] == "avatar":
            lol = arr[2]
            whname = lol.strip()
            b = await message.channel.send(embed=nasimple(f"Webhook Avatar : `{lol.strip()}`"))
            last.append(b)


        if arr[1] == "view":
            a = nasimple("Webhooks")
            for web in webhooks:
                a.add_field(name="Webhook", value=web, inline=True)
            b = await message.channel.send(embed=a)
            last.append(b)

        if arr[1] == "multisend":
            ams = await message.channel.send(embed=nasimple(f"Firing Webhooks ({arr[2]}x)"))
            last.append(ams)
            for i in range(int(arr[2])):
                for webhook in webhooks:
                    webhookinstance = DiscordWebhook(url=webhook, rate_limit_retry=True)
                    webhookinstance.set_content(whcont)
                    webhookinstance.username = whname
                    webhookinstance.avatar_url = whimg
                    webhookinstance.execute()

        if arr[1] == "send":
            ams = await message.channel.send(embed=nasimple("Firing Webhooks"))
            last.append(ams)
            for webhook in webhooks:
                webhookinstance = DiscordWebhook(url=webhook, rate_limit_retry = True)
                webhookinstance.set_content(whcont)
                webhookinstance.username = whname
                webhookinstance.avatar_url = whimg
                webhookinstance.execute()

        if arr[1] == "spam":
            for i in range(int(arr[2])):
                for webhook in webhooks:
                    webhookinstance = DiscordWebhook(url=webhook)
                    embed = DiscordEmbed(title=config["raid"]["heading"], description=config["raid"]["body"],
                                         color=0xab6c3c)
                    for j in range(15):
                        embed.add_embed_field(name=str(j), value=random.choice(config["insults"]), inline=False)
                    time.sleep(0.2)
                    embed.set_image(url=config["raid"]["image_url"])
                    embed.set_thumbnail(url=config["raid"]["image_url"])
                    embed.set_url(url=config["raid"]["url"])
                    webhookinstance.set_content("@everyone")
                    webhookinstance.add_embed(embed)
                    webhookinstance.avatar_url = config["raid"]["image_url"]
                    webhookinstance.username = config["raid"]["heading"]
                    resp = webhookinstance.execute()
                    if resp.status_code == 429:
                        time.sleep(20)

    if arr[0] == "~user":
        try:
            user = message.mentions[0]
        except:
            user = message.author

        avi = user.avatar_url

        if isinstance(user, discord.Member):
            role = user.top_role.name
            if role == "@everyone":
                role = "N/A"
            voice_state = None if not user.voice else user.voice.channel
            em = naembed(user.name, "")
            em.add_field(name='User ID', value=user.id, inline=True)
            if isinstance(user, discord.Member):
                em.add_field(name='Nick', value=user.nick, inline=True)
                em.add_field(name='Status', value=user.status, inline=True)
                em.add_field(name='In Voice', value=voice_state, inline=True)
                em.add_field(name='Game', value=user.activity, inline=True)
                em.add_field(name='Highest Role', value=role, inline=True)
            em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
            if isinstance(user, discord.Member):
                em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
            em.set_image(url=avi)
            returner = await message.channel.send(embed=em)
            last.append(returner)
    if arr[0] == "~lookup":
        if len(arr) < 2:
            ams = await message.channel.send(embed=nasimple("Please Provide an ip for lookup"))
            last.append(ams)
            return
        ip = arr[1]
        resp = requests.get(f'https://ipinfo.io/{ip}/json')
        if "Wrong ip" in resp.text:
            return
        else:
            loaded = json.loads(resp.text)
            eb = nasimple("IP Lookup")
            eb.add_field(name=f'IP', value=f'{ip}', inline=True)
            eb.add_field(name=f'City', value=f'{loaded["city"]}', inline=True)
            eb.add_field(name=f'Region', value=f'{loaded["region"]}', inline=True)
            eb.add_field(name=f'Country', value=f'{loaded["country"]}', inline=True)
            eb.add_field(name=f'Location', value=f'{loaded["loc"]}', inline=True)
            eb.add_field(name=f'Postal', value=f'{loaded["postal"]}', inline=True)
            eb.add_field(name=f'Timezone', value=f'{loaded["timezone"]}', inline=True)
            ams = await message.channel.send(embed=eb)
            last.append(ams)
    if arr[0] == "~shorten":
        if len(arr) < 1:
            return
        try:
            params = {
                "access_token": "757c24db53fac6a6a994439da41bdbbe325dfb99",
                "longUrl": arr[1]
            }
            r = requests.get("https://api-ssl.bitly.com/v3/shorten", params=params)
            j = json.loads(r.text)
            ams = await message.channel.send(
                embed=nasimple("Shortened Url").add_field(name="Url", value=j["data"]["url"],
                                                                                   inline=False).add_field(
                    name="Original", value=j["data"]["long_url"], inline=False))
            last.append(ams)
        except Exception as e:
            ams = await message.channel.send(embed=nasimple("Could not shorten URL"))
            last.append(ams)
    if arr[0] == "~setup":
        a = await message.channel.send(embed=naembed("Sodium", "Setting up the server..."))
        last.append(a)
        await client.create_guild(name="Sodium [" + client.user.name + "]", icon=open("assets/logo.png", 'rb').read())
        time.sleep(7)
        sodium = sodiumguild()
        for _ in sodium.text_channels:
            await _.delete()
        time.sleep(0.5)
        for _ in sodium.voice_channels:
            await _.delete()
        time.sleep(0.5)
        for _ in sodium.categories:
            await _.delete()
        time.sleep(0.5)
        await sodium.create_text_channel(name="Results")
        await sodium.create_text_channel(name="Commands")
        await sodium.create_text_channel(name="Logging")
        time.sleep(0.3)
        await logger().send(embed = naembed("Sodium", "Set up the server"))




@client.event
async def on_ready():
    print(f"{yellow}Signed into token!, type ~help to get commands")



client.run(token, bot=False)
