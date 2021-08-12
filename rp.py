import discord
import time

from discord import message


from config import TomlConfig

client = discord.Client()
config = TomlConfig("config.toml", "config.template.toml")

global chrono
chrono = time.time()


def get_ping(id):
    for key, values in config.ping.items():
        if values['vocal_chan'] == id:
            return values


def role(member, ping_config):
    if len(ping_config["accepte_role"]) == 0:
        return True
    for role in member.roles:
        if role.id in ping_config["accepte_role"]:
            return True
    return False


async def ping(guild, ping_config):
    global chrono
    if time.time() - chrono < 5:
        return
    else:
        channel = guild.get_channel(ping_config["alert_chan"])
        mentions = str()
        for mention in ping_config["role_ping"]:
            mentions += (f"{guild.get_role(mention).mention} ")
        await channel.send(f"{ping_config['message']} {mentions} !")
        chrono = time.time()


@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == config.guild:
        if not after.channel is None:
            ping_config = get_ping(after.channel.id)
            if not ping_config is None:
                if role(member, ping_config):
                    await ping(member.guild, ping_config)


@client.event
async def on_ready():
    print("Logged as {}!".format(client.user))

client.run(config.token, bot=config.bot)
