import discord
import asyncio
import pickle
import time
import random
import sqlite3
client = discord.Client()
f = open("config","r")
fr = f.read().split("\n")
@client.event
async def on_ready():
    print("logged in as {}".format(client.user.name))
    print("____________________________________")
hep = """
**!leaderboard**
**!score <kills> <win? yes/no> <@hostname> [image]** providing an image will help with verification
**!approve <@person>**
**!decline <user>**
**!stats**
**!help**
**!setup** admin first time setup
**!editpoints <user> <kills> <wins> <games>**
"""
async def removeRoles(message):
    await client.remove_roles(message.author, discord.util.get(message.server.roles, name=fr[1][fr[1].find("intermediate: ")+len("token: ")::]))
    await client.remove_roles(message.author, discord.util.get(message.server.roles, name=fr[2][fr[2].find("experienced: ")+len("token: ")::]))
    await client.remove_roles(message.author, discord.util.get(message.server.roles, name=fr[3][fr[3].find("advance: ")+len("token: ")::]))
    await client.remove_roles(message.author, discord.util.get(message.server.roles, name=fr[4][fr[4].find("expert: ")+len("token: ")::]))
    await client.remove_roles(message.author, discord.util.get(message.server.roles, name=fr[5][fr[5].find("unbeatable: ")+len("token: ")::]))
def custom_sort(t):
    return (t[1]*4+t[2])/t[5]
@client.event
async def on_message(message):
    d = sqlite3.connect("{}.db".format(str(message.server.id)))
    c = d.cursor()
    c.execute("SELECT * FROM rm WHERE user = ?",(message.author.id,))
    dlata = c.fetchall()
    #stuffs
    try:
        sa  = data[z][1]*4+data[z][2]/data[z][5]
        if sa >=10:
            removeRoles(message)
            await client.add_roles(message.author, discord.util.get(message.server.roles, name=fr[5][fr[5].find("unbeatable: ")+len("unbeatable: ")::]))
        elif sa >=8 and sa <10:
            removeRoles(message)
            await client.add_roles(message.author, discord.util.get(message.server.roles, name=fr[4][fr[4].find("expert: ")+len("expert: ")::]))
        elif sa >=6 and sa <8:
            removeRoles(message)
            await client.add_roles(message.author, discord.util.get(message.server.roles, name=fr[3][fr[3].find("advance: ")+len("advance: ")::]))
        elif sa >=4 and sa <6:
            removeRoles(message)
            await client.add_roles(message.author, discord.util.get(message.server.roles, name=fr[2][fr[2].find("experienced: ")+len("experienced: ")::]))
        elif sa >=2 and sa <4:
            removeRoles(message)
            client.add_roles(message.author, discord.util.get(message.server.roles, name=fr[1][fr[1].find("intermediate: ")+len("intermediate: ")::]))
    except:
        None
    #commands
    if message.content =="!stats":
        d = sqlite3.connect("{}.db".format(str(message.server.id)))
        c = d.cursor()
        x = message.content.split(" ")
        c.execute("SELECT * FROM rm WHERE user = ?",(message.author.id,))
        data = c.fetchall()
        z= 0
        await client.send_message(message.channel,"Wins: {} \n Games: {} \n Kills: {} \n Score: {} \n Average Score: {}".format(str(data[z][1]),str(data[z][3]),str(data[z][2]),str((data[z][1]*4+data[z][2])),str((data[z][1]*4+data[z][2])/data[z][5])))
    if message.content =="!leaderboard":
        d = sqlite3.connect("{}.db".format(str(message.server.id)))
        c = d.cursor()
        x = message.content.split(" ")
        c.execute("SELECT * FROM rm ")
        data = c.fetchall()
        data.sort(key=custom_sort)
        l = []
        em = discord.Embed(title="", description="",color=0x00ff00)
        for z in range(0,26):
            try:
                l.append([data[z][4],"\t Wins: {} \n \t Games: {} \n \t Kills: {} \n \t Score: {} \n \t Average Score: {}".format(str(data[z][1]),str(data[z][3]),str(data[z][2]),str((data[z][1]*4+data[z][2])),str((data[z][1]*4+data[z][2])/data[z][5]))])
        
            except:
                None
        print(l)
        l.reverse()
        for c,z in enumerate(l):
            em.add_field(name=str(c+1)+") "+z[0], value=z[1], inline=False)
        em.set_author(name="Leaderboard")
        await client.send_message(message.channel, embed=em)
    if message.content.startswith("!decline"):
        d = sqlite3.connect("{}.db".format(str(message.server.id)))
        c = d.cursor()
        x = message.content.split(" ")
        c.execute("SELECT * FROM urm WHERE user = ?",(x[1][2:-1],))
        data = c.fetchall()
        g= 0
        for y in data:
            if message.author.id == y[3][2:-1] and fr[6][fr[6].find("host: ")+len("host: ")::] in [y.id for y in message.author.roles]:
                c.execute("DELETE FROM urm WHERE user = ? AND host =?",(x[1][2:-1],y[3]))
                d.commit()
        await client.send_message(message.channel,"{} Your score has been processed, and has been declined. This may be due to your command having a false score input or missing an image.".format(x[1]))
    if message.content.startswith("!approve "):
        d = sqlite3.connect("{}.db".format(str(message.server.id)))
        c = d.cursor()
        x = message.content.split(" ")
        c.execute("SELECT * FROM urm WHERE user = ?",(x[1][2:-1],))
        #await client.send_message(message.channel,)
        data = c.fetchall()
        g= 0
        for y in data:
            if message.author.id == y[3][2:-1] and fr[6][fr[6].find("host: ")+len("host: ")::] in [y.id for y in message.author.roles]:
                c.execute("SELECT * FROM rm WHERE user = ?",(x[1][2:-1],))
                g = c.fetchall()
                m=0
                c.execute("SELECT * FROM rm WHERE user = ?",(x[1][2:-1],))
                g = c.fetchall()
                try:
                    c.execute("SELECT * FROM rm WHERE user = ?",(x[1][2:-1],))
                    g = c.fetchall()
                    m=0
                    if y[1] =="yes":
                        m+=1
                    try:
                        c.execute("UPDATE rm SET wins = ? WHERE user = ?",(g[0][1]+m,x[1][2:-1] ))
                        d.commit()
                        c.execute("UPDATE rm SET kills = ? WHERE user = ?",(g[0][2]+y[2],x[1][2:-1] ))
                        d.commit()
                        c.execute("UPDATE rm SET games = ? WHERE user = ?",(g[0][3]+1,x[1][2:-1] ))
                        d.commit()
                        c.execute("UPDATE rm SET aproves = ? WHERE user = ?",(g[0][5]+1,x[1][2:-1] ))
                        d.commit()
                    except:
                        c.execute("INSERT INTO rm (user,wins,kills,games,name,aproves) VALUES (?,?,?,?,?,?)",(x[1][2:-1],m,y[2],1,y[4],1))
                        d.commit()
                except:
                    None
                #try:
                print(x[1][2:-1])
                c.execute("DELETE FROM urm WHERE user = ? AND host =?",(x[1][2:-1],y[3]))
                d.commit()
                #except:
                    #None
            await client.send_message(message.channel,"{} Your score has been processed, and has been approved".format(x[1]))
    if message.content.startswith("!help"):
        await client.send_message(message.channel,hep)
    if message.content.startswith("!points "):
        x = message.content.split(" ")
        d = sqlite3.connect("{}.db".format(str(message.server.id)))
        c = d.cursor()
        try:
            c.execute("DELETE FROM urm Where user = ?",(str(message.author.id),))
            d.commit()
        except:
            None
        try:
            c.execute("INSERT INTO urm (user,win,kills,host,name) VALUES (?,?,?,?,?)",(str(message.author.id),x[2],int(x[1]),x[3],str(message.author.name)))
            d.commit()
            await client.send_message(message.channel,"```Your score is now being proccessed, please wait.```")
        except:
            await client.send_message(message.channel,"```please add the proper peramiters. !help```")
    if message.content == "!setup":
        if message.author.server_permissions.administrator:
            d = sqlite3.connect("{}.db".format(str(message.server.id)))
            c = d.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS urm (user TEXT,win TEXT,kills INT,host TEXT,name TEXT)")#unregistered messages
            c.execute("CREATE TABLE IF NOT EXISTS rm (user TEXT ,wins INT,kills INT,games INT, name TEXT,aproves INT)")#registered messages
            await client.send_message(message.channel,"```thank you for registering!```")
    if message.content.startswith("!editscore"):
        if message.author.server_permissions.administrator:
            x = message.content.split(" ")
            d = sqlite3.connect("{}.db".format(str(message.server.id)))
            c = d.cursor()
            c.execute("SELECT * FROM rm WHERE user = ?",(x[1][2:-1],))
            g = c.fetchall()
            c.execute("UPDATE rm SET kills = ? WHERE user = ?",(g[0][2]+int(x[2]),x[1][2:-1] ))
            d.commit()
            c.execute("UPDATE rm SET wins = ? WHERE user = ?",(g[0][1]+int(x[3]),x[1][2:-1] ))
            d.commit()
            c.execute("UPDATE rm SET games = ? WHERE user = ?",(g[0][3]+int(x[4]),x[1][2:-1] ))
            d.commit()
    if message.content.startswith("!clearpoints"):
        if message.author.server_permissions.administrator:
            x = message.content.split(" ")
            d = sqlite3.connect("{}.db".format(str(message.server.id)))
            c = d.cursor()
            c.execute("UPDATE rm SET kills = ? WHERE user = ?",(0,x[1][2:-1] ))
            d.commit()
            c.execute("UPDATE rm SET wins = ? WHERE user = ?",(0,x[1][2:-1] ))
            d.commit()
            c.execute("UPDATE rm SET games = ? WHERE user = ?",(0,x[1][2:-1] ))
            d.commit()
            await client.send_message(message.channel, "cleared!")
x = fr[0][fr[0].find("token: ")+len("token: ")::]
client.run(x)
#*looks up regex* not know what it is
