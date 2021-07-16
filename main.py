import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client=discord.Client()
#list of words that the bot will respond to....
sad_words = ["sad","despressed","mean","I suck", "I'm trying","Man, I'm bad at this", "I'll never", "unhappy","miserable", "angry","depressing", "I wish","I'm stupid","I'm dumb","I'm a dumbass","hopeless","tragic"]

thank_bot = ["thanks, Courage Bot","good Bot Courage","thanks Courage!","thanks Courage","thanks, Courage", "good bot","Good Bot","Best Bot","best Bot","good bot","best bot","best boi","thanks, Courage Bot","good bot","thanks courage","Thanks"]

Hello = ["OwO", "0w0","Hi Courage!", "Hello Courage","Hi Courage","Hey Shanique's Bot","owo"]

Hello_responses = ["OwO", "0w0","Hi!","Hi","Hey Friend","owo"]

starter_encouragements = [ "Cheer Up!","Hang in there!","You are a good person!", "You deserve nice things!", "This bot thinks that you are Great!", "Go for a walk and have some pizza and juice, you might feel a bit better after that.","Be kind to yourself!","Things will get better in time.","You are smart,just give yourself time and grace.","Go and have some water and eat a piece of fruit, you might feel a bit better after that."]


if "responding" not in db.keys():
  db["responding"] = True

#Helper Function to return quote from affirmations API
def get_quote():
  response = requests.get( "https://affirmations.dev")
  json_data = json.loads(response.text)
  quote = json_data["affirmation"]
  return quote

#Helper Function to return picture form dog API   
def get_dog():
  response2 = requests.get("https://api.thedogapi.com/v1/images/search")
  json_data2 =json.loads(response2.text)
  dog_picture = json_data2[0]['url']
  return dog_picture

#allows users to update responses from discord
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

#allows users to delete responses from discord
def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements  

@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$nice'):
    quote=get_quote();
    await message.channel.send(quote)

  if db["responding"]:

    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  #Adding New encouraging words
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New Encouraging Message Added!")

  #Remove Phrases from encouraging message
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index =int(msg.split("$del ",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  #thanks Courage!
  if any(word in msg for word in thank_bot):
    dog_picture = get_dog();
    await message.channel.send(dog_picture)

  #Responses to Hello Courage
  if any(word in msg for word in Hello):
    await message.channel.send(random.choice(Hello_responses))
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower()=="true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is Off.")

keep_alive()
client.run(os.getenv('TOKEN'))