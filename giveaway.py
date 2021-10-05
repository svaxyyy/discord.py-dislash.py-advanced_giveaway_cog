import discord
from discord.ext import commands
from dislash import *
import json
import datetime
import random
import asyncio


class roster(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.win_color = 0xfff305
        self.pending_color = 0x1fff22
        self.error_color = 0xff191c

    
    @slash_command(name = "giveaway", description = "start a giveaway")
    async def giveaway(self, inter):

        


        with open("database/json/giveaways.json", "r") as file:
            JSON = json.load(file)

        def check(inter):
            return inter.author == inter.author and inter.author != inter.author.bot and inter.author != self.client.user 
            
        def convert(time):
            pos = ["s","m","h","d"]

            time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2


            return val * time_dict[unit]

        def convertStamp(seconds):
            return datetime.timedelta(seconds=seconds)


        currentId = int(JSON["id"])
        newId = (int(currentId) + 1)
        currentTime = datetime.datetime.utcnow()
   
        embed = discord.Embed(
            title="Giveaway🎉",
            description="What is the Giveaway award?"
        ).set_author(
            name=inter.author.name + "#" + inter.author.discriminator,
            icon_url=str(inter.author.avatar_url)
        )
        embed.timestamp = currentTime
        await inter.send(embed=embed)


        msg1 = await self.client.wait_for("message",check=check)

        embed = discord.Embed(
            title="Giveaway🎉",
            description="What should be the giveaway duration?\n> 1s or 1m or 1h or 1d"
        ).set_author(
            name=inter.author.name + "#" + inter.author.discriminator,
            icon_url=str(inter.author.avatar_url)
        )
        embed.timestamp = currentTime
        await inter.send(embed=embed)


        msg2 = await self.client.wait_for("message",check=check)
        time = convert(msg2.content)
        if time == -1:
            await inter.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
            return
        elif time == -2:
            await inter.send(f"The time must be an integer. Please enter an integer next time. Integer is a number")
            return  
        
        embed = discord.Embed(
            title="Giveaway🎉",
            description="In which channel should i send the giveaway? just mention it with `#textchannel`."
        ).set_author(
            name=inter.author.name + "#" + inter.author.discriminator,
            icon_url=str(inter.author.avatar_url)
        )

        embed.timestamp = datetime.datetime.utcnow()

        await inter.send(embed=embed)


        msg3 = await self.client.wait_for("message",check=check)

        channelId = msg3.channel_mentions[0].id

        embed = discord.Embed(
            title="Giveaway🎉",
            description="How much winners should the giveaway have? Please tell me the number."
        ).set_author(
            name=inter.author.name + "#" + inter.author.discriminator,
            icon_url=str(inter.author.avatar_url)
        )

        embed.timestamp = datetime.datetime.utcnow()

        await inter.send(embed=embed)


        msg5 = await self.client.wait_for("message",check=check)

        winnersint = int(msg5.content)
        while True:
            if winnersint == 0:
                await inter.send(embed=embed)
                msg5 = await self.client.wait_for("message",check=check)
            else:
                break

        embed = discord.Embed(
            title="Giveaway🎉",
            description=f"> {msg1.content}"
        ).set_author(
            name="Giveaway pending 🟩")
        embed.set_footer(text="Ends ")
        embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
        embed.add_field(name="Entrants", value=f"• `🟢0` People joined the giveaway\n• `🔺0` total entrants\n• `🔻0` entrants left", inline=False)
        embed.add_field(name="Winner(s)", value=f"`👑{winnersint}`",inline=False)
        embed.color = self.pending_color
        msg4 = await inter.send(embed=embed)

        await msg4.add_reaction("🎉")

        giveawayObject = {
            "giveawayid" : int(newId),
            "winners" : int(winnersint),
            "msgid" : int(msg4.id),
            "giveawayContent" : str(msg1.content),
            "endTimestamp" : int(time), #int to datetime
            "entrants" : int(0),
            "totalentrants" : int(0),
            "giveawayChannelid" : int(channelId)
        }

        JSON["giveaways"].append(giveawayObject)

        with open("database/json/giveaways.json", "w") as file:
            json.dump(JSON, file, indent=4)


        await asyncio.sleep(time)


        channel = self.client.get_channel(channelId)
        new_msg = await channel.fetch_message(msg4.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        with open("database/json/giveaways.json", "r") as file:
            JSON = json.load(file)
        try:
            final = winnersint - 1
            users[final]
        except:
            embed = discord.Embed(
                title="Giveaway🎉",
                description=f"> {msg1.content}"
            ).set_author(
                name="Giveaway error 🟥")

            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="❌Error❌", value=f"> You placed a to high winner number please put it lower next time. Finished the giveaway🟥",inline=False)
            embed.color = self.error_color
            await msg4.edit(embed=embed)
            await msg4.clear_reactions()

            await asyncio.sleep(5)
            index = 0
            for obj in JSON["giveaways"]:
                
                if obj["msgid"] == msg4.id:
                    del JSON["giveaways"][index]
                else:
                    index += 1

            with open("database/json/giveaways.json", "w") as file:
                json.dump(JSON, file, indent=4)
            return

        string = ""
        winners = []
        for i in range(winnersint):
            while True:
                winner = random.choice(users)
                if not winner in winners:
                    winners.append(winner)
                    string += f"<@{winner.id}> "
                    break

                    

        
        
        
        with open("database/json/giveaways.json", "r") as file:
            JSON = json.load(file)

        for giveaway in JSON["giveaways"]:
            
            if (int(msg4.id) == int(giveaway["msgid"])):
                Entrants = giveaway["entrants"]
                giveaway["totalentrants"] += 1
                TOTAL = giveaway["totalentrants"]
                final = giveaway["totalentrants"] - giveaway["entrants"]
                LEFT = final
                CONTENT = giveaway["giveawayContent"]
                WINNERS = giveaway["winners"]
                embed = discord.Embed(
                    title="Giveaway Ended🎉 ",
                    description=f"> {CONTENT} "
                ).set_author(
                    name="Giveaway ended 🟨")
                embed.set_footer(text="Ended")
                embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
                embed.add_field(name="Entrants", value=f"• `🟢{Entrants}` People joined the giveaway\n• `🔺{TOTAL}` total entrants\n• `🔻{LEFT}` entrants left the giveaway", inline=False)
                embed.add_field(name="Winner(s)", value=f"`👑{WINNERS}`\n\n> {string}",inline=False)
                embed.color = self.win_color
                await msg4.edit(embed=embed)
                await msg4.clear_reactions()




        await asyncio.sleep(5)
        index = 0
        for obj in JSON["giveaways"]:
            
            if obj["msgid"] == msg4.id:
                del JSON["giveaways"][index]
            else:
                index += 1

        with open("database/json/giveaways.json", "w") as file:
            json.dump(JSON, file, indent=4)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):


        
        color = 0x2f3136
        channel = self.client.get_channel(payload.channel_id)
        user =  self.client.get_user(payload.user_id)
        guild = self.client.get_guild(payload.guild_id)
        message = await channel.fetch_message(payload.message_id)
        with open("database/json/giveaways.json", "r") as file:
            JSON = json.load(file)

        

        user = await self.client.fetch_user(payload.user_id)

        if user.bot:
            return

        if (str(payload.emoji) == "🎉"):
            for giveaway in JSON["giveaways"]:

                
                if (int(message.id) == int(giveaway["msgid"])):
                    giveaway["entrants"] +=1
                    giveaway["totalentrants"] += 1
                    with open("database/json/giveaways.json", "w") as file:
                        json.dump(JSON, file, indent=4)
                    Entrants = giveaway["entrants"]
                    TOTAL = giveaway["totalentrants"]
                    final = TOTAL - giveaway["entrants"]
                    LEFT = final
                    CONTENT = giveaway["giveawayContent"]
                    WINNERS = giveaway["winners"]
                    currentrants = Entrants 
                    embed = discord.Embed(
                        title="Giveaway🎉",
                        description=f"> {CONTENT} "
                    ).set_author(
                        name="Giveaway pending 🟩")
                    embed.set_footer(text="Ends ")
                    embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=giveaway["endTimestamp"])
                    embed.add_field(name="Entrants", value=f"• `🟢{currentrants}` People joined the giveaway\n• `🔺{TOTAL}` total entrants\n• `🔻{LEFT}` entrants left the giveaway", inline=False)
                    embed.add_field(name="Winner(s)", value=f"`👑{WINNERS}`",inline=False)
                    embed.color = self.pending_color
                    await message.edit(embed=embed)
                    await user.send(f"> **You sucessfully joined the giveaway! in {channel.mention}**")
                    

        with open("database/json/giveaways.json", "w") as file:
            json.dump(JSON, file, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> print("ws"):


        
        color = 0x2f3136
        channel = self.client.get_channel(payload.channel_id)
        user =  self.client.get_user(payload.user_id)
        guild = self.client.get_guild(payload.guild_id)
        message = await channel.fetch_message(payload.message_id)
        with open("database/json/giveaways.json", "r") as file:
            JSON = json.load(file)

        

        user = await self.client.fetch_user(payload.user_id)

        if user.bot:
            return

        if (str(payload.emoji) == "🎉"):
            for giveaway in JSON["giveaways"]:
                Entrants = giveaway["entrants"]
                currentrants = Entrants - 1
                if (int(message.id) == int(giveaway["msgid"])):
                    giveaway["entrants"] -=1
                    with open("database/json/giveaways.json", "w") as file:
                        json.dump(JSON, file, indent=4)
                    Entrants = giveaway["entrants"]
                    TOTAL = giveaway["totalentrants"]
                    final = TOTAL - giveaway["entrants"]
                    LEFT = final
                    CONTENT = giveaway["giveawayContent"]
                    WINNERS = giveaway["winners"]
                    currentrants = Entrants 
                    embed = discord.Embed(
                        title="Giveaway🎉",
                        description=f"> {CONTENT} "
                    ).set_author(
                        name="Giveaway pending 🟩")
                    embed.set_footer(text="Ends ")
                    embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=giveaway["endTimestamp"])
                    embed.add_field(name="Entrants", value=f"• `🟢{currentrants}` People joined the giveaway\n• `🔺{TOTAL}` total entrants\n• `🔻{LEFT}` entrants left the giveaway", inline=False)
                    embed.add_field(name="Winner(s)", value=f"`👑{WINNERS}`",inline=False)
                    embed.color = self.pending_color
                    await message.edit(embed=embed)
                    await user.send(f"> **You sucessfully joined the giveaway! in {channel.mention}**")
                    

        with open("database/json/giveaways.json", "w") as file:
            json.dump(JSON, file, indent=4)


def setup(client):
    client.add_cog(roster(client))
