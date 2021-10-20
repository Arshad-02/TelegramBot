import os
import telebot
import pafy
import random
import time
import youtube_dl
from telebot import types
from keep_alive import keep_alive 
import urllib.request
import re
import wikipedia

API_KEY = secret.TOKEN
bot = telebot.TeleBot(API_KEY)
telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60

responses = [
"It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]

roll_die = ["1","2","3","4","5","6"]

options = ["Paper", "Rock", "Scissors"]

stickers = ["CAACAgIAAxkBAAIH-GFkWlHh4EGC0xkqmdsIJkCYBQaYAAJeAQACEBptItNORzH8jWOyIQQ","CAACAgIAAxkBAAIH-mFkWyPU3xEgH5GPRApGL2yiUlb5AAJjAQACEBptImu6AmhfaYu5IQQ","CAACAgIAAxkBAAIH_WFkW1AfCGynFkc8Mt2ud-BtaObDAAJZAQACEBptIh2VbDlfzkAfIQQ","CAACAgIAAxkBAAIIBGFkW8XdNT6PahbjZ-EnheHF3ftgAAJhAQACEBptIu-IjH2qmk0HIQQ","CAACAgIAAxkBAAIIB2FkXAfwr2fwHYWNVPquNxR5iVRWAAJuAQACEBptIqZdn9Atu9XsIQQ"]


text_messages = {
    'welcome':
        u'Please welcome {name}!\n\n'
        u'This chat is intended for bot testing and discussion.\n'
        u'I hope you enjoy your stay here!'}

@bot.message_handler(commands = ["help","start"])
def greet(message):
  bot.reply_to(message,"Hello I am Alfred,\n1️⃣. I can download audio from youtube videos, You can do that by sharing the video link with me.\n2️⃣. You can now search for youtube videos right from telegram by texting Alfred <video name>. \n3️⃣. Added 8ball, to use just text 8ball <your question>.\n4️⃣.Rock Paper Scissor.\n5️⃣.Image searcher source:Wikipedia use Wimg <topic>\n🏳️‍🌈As alfred is in early stage of development,we only support youtube links with a maximum duration of 5 mins.Sooner in the future there will be support for video downloads from multiple platforms and many more exciting features, soo stay tuned.")
    
#Check cmd

def check_ws(message):
  request = message.text.split()
  if len(request) < 2 or request[0] not in "ws":
    return False
  else:
    return True

@bot.message_handler(func=check_ws)
def wiki_search(message):
  pass

#basic_url = https://youtu.be/E-7RhUMBzi8 or https://www.youtube.com/watch?v=vC-ZjwxBnMg
#(basic_url.split("/")[2]) = youtu.be or www.youtube.com

def yt_downloader(query,message):
  try:
    text = query.message.text
    chat_id = message.chat.id
    bot.send_message(chat_id,"Downloading audio may take some time, ⌛ ￣へ￣ " )
    video = pafy.new(text)
    vid_big = video.bigthumb
    best_audio = video.getbestaudio(preftype='m4a')
    check_length = int(video.duration.split(":")[1])
    hr_check = int(video.duration.split(":")[0])
    if check_length < 6 and hr_check == 0:
      best_audio.download(filepath = "music") 
      vid_loc = f'''music/{video.title}.m4a'''
      audio = open(vid_loc, 'rb')
      if message.chat.type == "private":
        bot.send_audio(chat_id,audio,duration = video.duration, performer = video.author, title = video.title,thumb = vid_big)
      if message.chat.type == "group":
        bot.send_audio(chat_id,audio,duration = video.duration, performer = video.author, title = video.title,thumb = vid_big)
    else:
        bot.send_message(chat_id,f"Audio duration greater then 5 mins, duration: {check_length}")
  except:
    bot.send_message(chat_id,"Something went wrong")

yt_basic = ["youtu.be","www.youtube.com"]
def check_yt(message):
  request = message.text.split("/")
  if len(request) < 4 or request[2] not in yt_basic:
    return False
  else:
    return True

@bot.message_handler(func = check_yt)
def yt_search(message):
  chat_id = message.chat.id
  keyboard = types.InlineKeyboardMarkup()
  b1 =(types.InlineKeyboardButton("Download",callback_data = "download"))
  b2 =(types.InlineKeyboardButton("Cancel",callback_data = "cancel" ))
  keyboard.row(b1,b2)
  #send link as text in markup and get query.msg.text
  edit = bot.send_message(chat_id,message.text,reply_markup = keyboard)
  def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    yt_downloader(query,message)
 
  @bot.callback_query_handler(func=lambda call: True)
  def iq_callback(query):
    data = query.data
    if data.startswith('download'):
      get_ex_callback(query)
      bot.send_message(chat_id,"Appreciate your patience")    
    elif data.startswith("cancel"):
      bot.answer_callback_query(query.id)
      bot.send_message(chat_id,"Thank you (╯‵□′)╯︵┻━┻ ")
    else:
      bot.reply_to(edit,"Something went wrong")

def yt_searcher(message):
  request = message.text.split()
  if len(request) < 2 or request[0] not in "Alfred":
    return False
  else:
    return True
@bot.message_handler(func = yt_searcher)
def yt_get(message): 
  video = message.text.split("Alfred ",1)[1]
  chat_id = message.chat.id
  video = video.replace(" ","+")
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + video)
  video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
  keyboard = types.InlineKeyboardMarkup()
  b1 =(types.InlineKeyboardButton("Download",callback_data = "download_yt"))
  b2 =(types.InlineKeyboardButton("Cancel",callback_data = "cancel_yt" ))
  keyboard.row(b1,b2)
  bot.send_message(chat_id,"https://www.youtube.com/watch?v="+ video_ids[0],reply_markup = keyboard)
  def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    yt_downloader(query,message)
  @bot.callback_query_handler(func=lambda call: True)
  def iq_callback(query):
    data = query.data
    if data.startswith('download_yt'):
      get_ex_callback(query)
      bot.send_message(chat_id,"Appreciate your patience")    
    elif data.startswith("cancel_yt"):
      bot.answer_callback_query(query.id)
      bot.send_message(chat_id,"Thank you (╯‵□′)╯︵┻━┻ ")
    else:
      bot.send_message(chat_id,"Something went wrong")

def eightball(message):
  request = message.text.split()
  if len(request) < 1 or request[0] not in "8ball":
    return False
  else:
    return True

@bot.message_handler(func = eightball)
def eightrun(message):
  bot.reply_to(message,random.choice(responses))

def die_roll(message):
  request = message.text.split()
  if len(request) > 1 or request[0] not in "Roll":
    return False
  else:
    return True

@bot.message_handler(func = die_roll)
def dice_handler(message):
  bot.reply_to(message,random.choice(roll_die))

def rps_check(message):
  request = message.text.split()
  if len(request) > 1 or request[0] not in options:
    return False
  else:
    return True

@bot.message_handler(func = rps_check)
def mini_game(message):
  choice = random.choice(options)
  user_choice = message.text
  def rps(user_choice,choice):
    if (user_choice == "Rock" and choice == "Scissors") or (user_choice == "Paper" and choice == "Rock") or (user_choice == "Scissors" and choice == "Paper"):
        return True  
  if user_choice == choice:
      bot.reply_to(message,f"It's a tie, Your choice : {user_choice}\n my choice :{choice}")
  elif rps(user_choice,choice):
      bot.reply_to(message,f"You Won, Your choice :{user_choice}\n my choice :{choice}")
  else:
      bot.reply_to(message,f"You lose, Your choice :{user_choice}\n my choice :{choice}")

def img_search(message):
  request = message.text.split()
  if len(request) < 1 or request[0] not in "Wimg":
    return False
  else:
    return True

@bot.message_handler(func = img_search)
def get_img(message):
    try:
        wiki_img = message.text.split("Wimg ", 1)[1]
        img_s = ":" + wiki_img + ":"
        bot.reply_to(message,"Processing your request....")
        no = random.randrange(0, 9)
        img = wikipedia.page(img_s).images[no]
        check = img.split(".")[-1]
        num = 0
        while check != "jpg":
            img = wikipedia.page(img_s).images[num]
            num+=1
            check = img.split(".")[-1]
            if check == "png":
                break
            if check == "jpg":
                break
            if num > 6:
                img = "https://bitsofco.de/content/images/2018/12/broken-1.png"
                break
        bot.send_photo(message.chat.id,img)
    except:
        bot.reply_to(message,"Bad request")

@bot.message_handler(content_types = ["stickers","sticker"])
def sticker(message):
    bot.reply_to(message,message.sticker.file_id)

@bot.message_handler(commands = ["sticker"])
def sticker_send(message):
    bot.send_sticker(message.chat.id,random.choice(stickers))


print("bot is now active")
keep_alive()
bot.infinity_polling(skip_pending = True)
