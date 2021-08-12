import discord
import time


from config import TomlConfig

client = discord.Client()
config = TomlConfig("config.toml", "config.template.toml")

global chrono
chrono = time.time()


def role(member):
    for role in member.roles:
        if role.id == config.sans_papier:
            return True
    return False


async def ping(guild):
    global chrono
    if time.time() - chrono < 5:
        print("ok")
        return
    else:
        role = guild.get_role(config.role_ping)
        channel = guild.get_channel(config.alert_chan)
        await channel.send(f"Un Sans Papier s'est connecté dans le channel {role.mention} !")
        chrono = time.time()


@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == config.guild:
        if (not after.channel is None) and after.channel.id == config.vocal_chan:
            if role(member):
                await ping(member.guild)


@client.event
async def on_ready():
    print("Logged as {}!".format(client.user))

client.run(config.token, bot=config.bot)
