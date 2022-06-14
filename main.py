import os
import discord
from discord.ext import commands
from discord.ext import tasks
import random
from keep_alive import keep_alive
import aiohttp
import pickle
import random
import time

token = os.environ['token']
client = discord.Client()
client = commands.Bot(command_prefix="$")
client.remove_command("help")

roasts = open("responses/roasts.txt").read().splitlines()
compliments = open("responses/compliments.txt").read().splitlines()


@client.event
async def on_ready():
    automeme.start()
    print("I'm in")
    print(client.user)
    await client.change_presence(activity=discord.Game(name="Skimming Canoe"))


@client.command()
async def update(ctx):
    await ctx.channel.send(
        "Online should be out 15th June, but there may be delays")


@client.command()
async def roll(ctx, user: discord.User):
    await user.send(
        "https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713"
    )


@client.command()
async def invite(ctx):
    await ctx.channel.send("https://discord.com/invite/TVDHT3HZ")


@client.command()
async def about(ctx):
    await ctx.channel.send(
        "Skimming Canoe is a fast paced game about collecting coins and dodging rocks"
    )


@client.command()
async def message(ctx, user: discord.User, *, msg):
    await user.send(
        "Somebody in the Skimming Canoe server wanted to tell you this: " +
        msg)


@tasks.loop(minutes=5)
async def automeme():
    channel = client.get_channel(985084449261764688)
    embed = discord.Embed(title="", description="")
    done = False
    while not done:
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://www.reddit.com/r/dankmemes/new.json?sort=new'
                ) as r:
                    res = await r.json()
                    embed.set_image(url=res['data']['children'][random.randint(
                        0, 25)]['data']['url'])
                    await channel.send(embed=embed)
                    done = True
        except:
            done = False


@client.command
async def socials(ctx):
    await ctx.channel.send('''Contact and Follow us!
[Our website (this page lol)](https://gomango99.github.io/SkimmingCanoe/)

[Download on itch.io](https://pjgamedev.itch.io/skimmingcanoe)

[Join our Discord](https://discord.gg/ATJNEkuu8m)

[Find updates on Insta](https://instagram.com/skimming.canoe?igshid=YmMyMTA2M2Y=)

[Exclusive vids on YouTube](https://youtube.com/channel/UCSMJJ6kpW2QSiofhUECsNXg)'''
                           )


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Jeremy Help Page")
    embed.add_field(name="$update",
                    value="Tells you when the next update should be out",
                    inline=False)
    embed.add_field(name="$socials",
                    value="Lists the websites Skimming Canoe is part of",
                    inline=False)
    embed.add_field(name="$roll @victim",
                    value="Rickrolls that user in a DM",
                    inline=False)
    embed.add_field(name="$message @recipient [your_message]",
                    value="I will DM that user your message",
                    inline=False)
    embed.add_field(name="$help", value="Displays this message", inline=True)
    embed.add_field(name="$about",
                    value="Tells you about Skimming Canoe",
                    inline=True)
    embed.add_field(name="$creator",
                    value="Tells you about GoMango99, the bot creator",
                    inline=True)
    await ctx.channel.send(embed=embed)


@client.command()
async def creator(ctx):
    embed = discord.Embed(
        title="I was programmed by Gomango",
        description=
        "Join his Discord and subscribe to his YouTube channnel: \n https://discord.com/invite/rFWUtj5jjt \n https://youtube.com/channel/UCVIy7tBdlmAvMGd9kvoMV3w",
        color=0xfefb41)
    embed.set_author(name="GoMango99")
    await ctx.channel.send(embed=embed)


@client.command()
async def question(ctx):
    if (random.randint(1, 2) == 1):
        await ctx.channel.send("Yes")
    else:
        await ctx.channel.send("No")


@client.command()
async def roast(ctx, user: discord.User):
    await ctx.channel.send(user.mention + "," + random.choice(roasts))


@client.command()
async def compliment(ctx, user: discord.User):
    await ctx.channel.send(user.mention + ", " + random.choice(compliments))


@client.command()
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                'https://www.reddit.com/r/dankmemes/new.json?sort=new') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            await ctx.send(embed=embed)


@client.event
async def on_message_delete(message):

    role = False
    for r in message.guild.roles:
        if r.mention in message.content:
            role = True
    if "@everyone" in message.content or "@here" in message.content:
        role = True
    if len(message.mentions) == 0 and not role:
        return
    else:
        print(message.author.name)
        ghostping = discord.Embed(title=f'GHOSTPING',
                                  color=0xFF0000,
                                  timestamp=message.created_at)
        ghostping.add_field(name='**Name:**',
                            value=f'{message.author} ({message.author.id})')
        ghostping.add_field(name='**Message:**', value=f'{message.content}')
        ghostping.set_thumbnail(
            url=
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXtzZMvleC8FG1ExS4PyhFUm9kS4BGVlsTYw&usqp=CAU'
        )
        try:
            await message.channel.send(embed=ghostping)
        except discord.Forbidden:
            try:
                await message.author.send(embed=ghostping)
            except discord.Forbidden:
                return max


data_filename = "data.pickle"


class Data:
    def __init__(self, wallet, bank):
        self.wallet = wallet
        self.bank = bank


@client.command()
async def work(ctx):
    member_data = load_member_data(ctx.author.id)

    member_data.wallet += 1
    await ctx.channel.send("You earned 1 coin!")

    save_member_data(ctx.author.id, member_data)


@client.command()
async def deposit(ctx, amt):
    member_data = load_member_data(ctx.author.id)
    try:
        amt = int(amt)
    except:
        await ctx.channel.send(
            f"{ctx.author.mention}, you need to deposit a positive whole number"
        )
    if amt > member_data.wallet:
        await ctx.channel.send(
            f"{ctx.author.mention}, you don't have that much money to deposit!"
        )
    elif amt < 0:
        await ctx.channel.send(
            f"{ctx.author.mention}, you need to deposit a positive whole number"
        )
    else:
        member_data.wallet -= amt
        member_data.bank += amt
        await ctx.channel.send(
            f"{ctx.author.mention}, sucrssfully deposited {amt} into bank!")
        save_member_data(ctx.author.id, member_data)


@client.command()
async def bal(message):
    member_data = load_member_data(message.author.id)

    embed = discord.Embed(title=f"{message.author.display_name}'s Balance")
    embed.add_field(name="Wallet", value=str(member_data.wallet))
    embed.add_field(name="bank", value=str(member_data.bank))

    await message.channel.send(embed=embed)


@client.command()
async def gamble(ctx, amt):
    member_data = load_member_data(ctx.author.id)
    try:
        amt = int(amt)
    except:
        await ctx.channel.send(
            f"{ctx.author.mention}, you need to gamble a whole number")
    if amt > member_data.wallet:
        await ctx.channel.send(
            f"{ctx.author.mention}, you don't have that much money to gamble away!"
        )
    elif amt < 50 or amt > 1000:
        await ctx.channel.send(
            f"{ctx.author.mention}, you need to gamble at least 50 and at most 1000"
        )
    else:
        amt = int(amt)
        member_data.wallet -= amt
        icons = ["🍒", "🍋", "🍊", "🫐", "🛎️", "〰️", "7️⃣"]
        results = await ctx.channel.send("???")
        msg = ""
        for i in range(0, 3):
            num = random.random()
            result = 0
            result = int(num > 0.5)
            if (result == 0):
                result = int(num > 0.3) * 2
            if (result == 0):
                result = int(num > 0.1) * 3
            if (result == 0):
                result = int(num > 0.06) * 4
            if (result == 0):
                result = int(num > 0.029) * 5
            if (result == 0):
                result = int(num > 0.01) * 6
            if (result == 0):
                result = int(num > 0.001) * 7
            msg += icons[result - 1]
            print(icons[result - 1])
        await results.edit(content=msg)
        if (msg == "🍒🍒🍒"):
            await ctx.channel.send(
                f"{ctx.author.mention}, you got triple cherries, thats {amt*5} to your wallet!"
            )
            member_data.wallet += amt * 5
        if (msg == "🍋🍋🍋"):
            await ctx.channel.send(
                f"{ctx.author.mention}, you got triple lemons, thats {amt*10} to your wallet!"
            )
            member_data.wallet += amt * 10
        if (msg == "🍊🍊🍊"):
            await ctx.channel.send(
                f"Cool {ctx.author.mention}, you got triple oranges, thats {amt*20} to your wallet!"
            )
            member_data.wallet += amt * 10
        if (msg == "🫐🫐🫐"):
            await ctx.channel.send(
                f"{ctx.author.mention}, you got triple plums, thats {amt*50} to your wallet!"
            )
            member_data.wallet += amt * 50
        if (msg == "🛎🛎🛎"):
            await ctx.channel.send(
                f"{ctx.author.mention}, you got triple bell, thats {amt*100} to your wallet!"
            )
            member_data.wallet += amt * 100
        if (msg == "➖➖➖"):
            await ctx.channel.send(
                f"{ctx.author.mention}, you got triple bar, thats {amt*200} to your wallet!"
            )
            member_data.wallet += amt * 200
        if (msg == "7️⃣7️⃣7️⃣"):
            await ctx.channel.send(
                f"WOW {ctx.author.mention}, you got the JACKPOT! Thats 1,000,000 to your wallet!"
            )
            member_data.wallet += 1000000
        elif("7️⃣" in msg):
          ctx.channel.send(f"{ctx.author.mention}, you didn't get any matches. but I'm impressed that you got a 7! I'm not meant to do this, but here's {amt*10} for the impressive 7!!!")
          member_data.wallet += amt*10
        else:
          ctx.channel.send(f"Too bad, {ctx.author.mention}!! You didn't win anything. Better luck next time")
        save_member_data(ctx.author.id, member_data)


@client.command()
async def grant(ctx, user: discord.User, wallet: int, bank: int):
    if ctx.author.id == 737691407191507015:
        await ctx.channel.send(f"{user.mention}, it's your lucky day! You have been chosen to be gifted {wallet} to your wallet, and {bank} to your bank!")
    member_data = load_member_data(user.id)
    member_data.wallet += wallet
    member_data.bank += bank

    save_member_data(user.id, member_data)


def load_data():
    if os.path.isfile(data_filename):
        try:
            with open(data_filename, "rb") as file:
                return pickle.load(file)
        except EOFError:
            return dict()
    else:
        return dict()


def replace(s, index, c):
    chars = list(s)
    chars[index] = c
    res = "".join(chars)
    return res


def load_member_data(member_ID):
    data = load_data()

    if member_ID not in data:
        return Data(0, 0)

    return data[member_ID]


def save_member_data(member_ID, member_data):
    data = load_data()

    data[member_ID] = member_data

    with open(data_filename, "wb") as file:
        pickle.dump(data, file)


keep_alive()
client.run(token)
keep_alive()
client.run(token)()
