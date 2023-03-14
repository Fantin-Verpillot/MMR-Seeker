import discord
import requests
from urllib.parse import quote

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('/mmr'):
        arguments = message.content.split('/mmr ')
        name = arguments[1] if len(arguments) > 1 else message.author.name
        encodedName = quote(name)
        url = f'https://euw.whatismymmr.com/api/v1/summoner?name={encodedName}'
        response = requests.get(url)
        json_data = response.json()

        if "error" in json_data:
            result = f'Désolé, je n\'ai trouvé aucun joueur portant le pseudo **{name} (EUW)**.\n\n'
            result += ":bulb: Pour chercher un joueur spécifique, utilise le commande `/mmr {pseudo}`."
        else:
            result = f':bar_chart: Estimation de MMR pour **{name} (EUW)** :\n\n'

            if json_data["ranked"]["avg"]:
                result += f':small_blue_diamond: Ranked : **{str(json_data["ranked"]["avg"])}** ({json_data["ranked"]["closestRank"]} - top {str(100 - round(json_data["ranked"]["percentile"]))}%)\n'

            if json_data["normal"]["avg"]:
                result += f':small_blue_diamond: Normal : **{str(json_data["normal"]["avg"])}** ({json_data["normal"]["closestRank"]} - top {str(100 - round(json_data["normal"]["percentile"]))}%)\n'

            if json_data["ARAM"]["avg"]:
                result += f':small_blue_diamond: ARAM : **{str(json_data["ARAM"]["avg"])}** ({json_data["ARAM"]["closestRank"]} - top {str(100 - round(json_data["ARAM"]["percentile"]))}%)\n'

        await message.channel.send(result)

    elif client.user in message.mentions:
        await message.channel.send(f'Hello {message.author.mention}, je suis bien là :blush:')

client.run('DISCORD_BOT_TOKEN')
