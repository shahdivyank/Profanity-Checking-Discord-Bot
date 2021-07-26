import requests
import discord
import os

client = discord.Client()

headers = {
    'content-type': os.environ["CONTENT_TYPE"],
    'x-rapidapi-key': os.environ["KEY"],
    'x-rapidapi-host': os.environ["HOST"]
    }

url = os.environ["URL"]

TOKEN = os.environ["TOKEN"]

def check_profanity(text):
    payload = "censor-character=*&content=" + text
    response = requests.request("POST", url, data = payload, headers = headers)
    contains_profanity = response.text.split(",")[1].split(":")[1]
    return contains_profanity

owner = None

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if check_profanity(message.content):
        await message.channel.purge(limit = 1)

        msg = "NOTICE: Your latest message:\t'" + str(message.content) + "'\tis suspected to " \
        "contain profanity! Further violations will result in action from the server owner. If you " \
        "believe this was a mistake, please contact the server owner for clarification"
        await message.author.send(msg)

client.run(TOKEN)
