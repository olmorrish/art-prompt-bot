import discord
import os
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client() #register a client

@client.event 
async def on_ready(): #called when bot is ready to start
  print('We have logged in as {0.user}'.format(client))
  game = discord.Game("%help")
  await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
  if(message.author == client.user):
    return
  
  if(message.content.startswith('%')):
    messagewords = message.content.split()

    # %help
    if(messagewords[0] == "%help"):
      await message.channel.send("Supported commands:"
        + "\n   %suggest <word or phrase> ---> Add a word to the list."
        + "\n   %list ---> See the current list."
        + "\n   %remove <index number> ---> Remove a word from the list.")

    # %suggest
    if(messagewords[0] == '%suggest' and len(messagewords) > 1):
      suggestion_word = ''
      for msg_word in messagewords[1:]:
        suggestion_word += msg_word + " ";
      suggestion_word = suggestion_word[:len(suggestion_word)-1]
      add_word(suggestion_word, message.author.display_name)
      await message.channel.send('Your suggestion has been added.')

    # %list
    if(messagewords[0] == '%list'):

      if "words" in db.keys():
        db_words = db["words"]
      else:
        db["words"] = [] #init if not existing
      if "suggestors" in db.keys():
        db_suggestors = db["suggestors"]
      else:
        db["suggestors"] = []

      listoutput = 'Words in current list:'
      for i in range(len(db_words)):
        listoutput += '\n [' + str(i) + ']  - - -  '
        listoutput += '**\"' + db_words[i] + '\"**'
        listoutput += '  - - -  (suggested by ' + str(db_suggestors[i]) + ')'
      listoutput += "\n Words are selected at random from this list and removed when selected (this order has no impact)."
      await message.channel.send(listoutput)

    # %remove
    if(messagewords[0] == "%remove" and len(messagewords) > 1):
      index = messagewords[1]
      if(str.isnumeric(index)):
        deleted_word = delete_word(int(index))
        await message.channel.send("Word \"" + deleted_word + "\" has been removed.")

    # %clear
    if(messagewords[0] == "%clear"):
        db["words"] = []
        db["suggestors"] = []
        await message.channel.send("All suggestions have been deleted.")

    # %current
    # %newword
    # %extension
    # %days

def add_word(new_word, new_suggestor):
  if "words" in db.keys():
    db_words = db["words"]
    db_words.append(str.upper(new_word))
    db["words"] = db_words #save the altered data
  else:
    db["words"] = [new_word] #init if not existing
  
  if "suggestors" in db.keys():
    db_suggestors = db["suggestors"]
    db_suggestors.append(new_suggestor)
    db["suggestors"] = db_suggestors #save the altered data
  else:
    db["suggestors"] = [new_suggestor] #init if not existing

def delete_word(index):
  db_words = db["words"]
  db_suggestors = db["suggestors"]
  if len(db_words) > index and len(db_suggestors) > index:
    ret = db_words[index]
    del db_words[index]
    del db_suggestors[index]
    db["words"] = db_words
    db["suggestors"] = db_suggestors
    return ret
    
def select_new_word():
    db_words = db["words"]
    db_suggestors = db["suggestors"]

keep_alive()
client.run(os.environ['envtoken'])
