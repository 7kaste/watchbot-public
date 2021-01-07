import discord
import asyncio
import datetime
import json
import re
import urllib.request
from urllib.parse import urlparse
from discord.ext import commands

with open("DiscordAuthToken.json", "r") as readfile:
    TOKEN = json.load(readfile)["token"]

with open("W2G_API.json", "r") as readfile:
    API_KEY = json.load(readfile)["api_key"]

bot = commands.Bot(command_prefix="!")


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_youtube(url):
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(url)

    if not match:
        print('not youtube')
        return False
    print('matches youtube')
    return True

@bot.event
async def on_ready():
    print('Bot is ready. Version:')
    print(discord.__version__)
  
@bot.command()
async def watch(ctx, arg1=None):
    '''
    Enter something plz
    '''
    if arg1 == None or arg1 == '-h' or arg1 == 'h':
       await ctx.send("Enter something plz")
    else:
        # Bygg länk
        api_url="https://www.watch2gether.com/rooms/create.json"
        share_url=arg1
        
        result_url=is_url(share_url)
        
        if result_url == False:
            await ctx.send('Please send valid URL')
        else:
            result_youtube=is_youtube(share_url)
            if result_youtube == False:
                await ctx.send('Please send a YouTube link')
            else:
                body = {"share": share_url, "api_key": API_KEY}
                req = urllib.request.Request(api_url)
                req.add_header('Content-Type', 'application/json; charset=utf-8')
                json_data = json.dumps(body)
                json_data_as_bytes = json_data.encode('utf-8')
                req.add_header('Content-Length', len(json_data_as_bytes))

                response = urllib.request.urlopen(req, json_data_as_bytes)
                raw_data = response.read()
                
                encoding = response.info().get_content_charset('utf-8')
                data = json.loads(raw_data.decode(encoding))
                
                streamkey = data["streamkey"]
                
                room_url="https://www.watch2gether.com/rooms/" + streamkey
               
                reply=room_url
                
                await ctx.send(reply)
                
              
bot.run(TOKEN)
