import configparser
import logging
import logging.config

from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded


# loads the config.cfg file, useful to seperate the configuration from the code
config = configparser.ConfigParser(allow_no_value=True, interpolation=None)
config.read("config.cfg", encoding="utf-8")

# sets up logging
logging.config.fileConfig("logging.cfg")
logger = logging.getLogger("discord")

# setup for bot prefixes
config_prefixes = config["Bot"]["Prefixes"].split(",")
config_dm_prefixes = config_prefixes.copy()
for x in config["Bot"]["DM_Prefixes"].split(","):
    config_dm_prefixes.append(x)


def get_prefix(client, message):
    prefixes = config_prefixes

    # switch to dm_prefixes if message is a dm
    if not message.guild:
        prefixes = config_dm_prefixes

    return commands.when_mentioned_or(*prefixes)(client, message)


# this creates the bot
bot = commands.Bot(
    command_prefix=get_prefix,
    description=config["Bot"]["Description"],
    owner_id=int(config["Bot"]["Owner"]),
    case_insensitive=config._convert_to_boolean(
        config["Bot"]["Case_Insensitive"])
)

# event at bot startup
# https://discordpy.readthedocs.io/en/stable/api.html?highlight=on_ready#discord.on_ready

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} - {bot.user.id}')
    print(f'Logged in as {bot.user} - {bot.user.id}')
    try:
        for cog in config["Cogs"]:
            bot.load_extension(f"{config['Bot']['Cogdir']}.{cog}")
    except ExtensionAlreadyLoaded as e:
        logger.warning(f"Extension already loaded: {e}")

# run the bot, needs to be the last call
# https://discordpy.readthedocs.io/en/stable/api.html?highlight=run#discord.Client.run
bot.run(config["Bot"]["Token"], bot=True, reconnect=True)