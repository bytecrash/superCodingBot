import logging
import helper
import json
from datetime import datetime, timedelta
import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from queue import Queue
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from threading import Thread
from telegram import ParseMode
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, ConversationHandler, MessageHandler, RegexHandler, Updater,Filters,CallbackQueryHandler
from configparser import ConfigParser
import bs4 as bs
import html5lib
import time
import urllib.error
import urllib.request
from urllib import parse
import sqlite3
import random
from xlsxwriter.workbook import Workbook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
config = ConfigParser()
config.read('config.ini')
TOKEN = config.get('telegram','bot_token')
HACKERRANK_API_KEY = config.get('hackerrank','api_key')
CLIST_USER_NAME = config.get('clist','username')
CLIST_API_KEY = config.get('clist','api_key')
mount_point=config.get('openshift','persistent_mount_point')
compiler = helper.HackerRankAPI(api_key=HACKERRANK_API_KEY)
adminlist=str(config.get('telegram','admin_chat_id')).split(',')
# FOR CONVERSATION HANDLERS
NAME,JUDGE,HANDLE,SELECTION,HOLO,SOLO,POLO,XOLO,REMOVER,UPDA,QSELCC,LANG,CODE,DECODE,TESTCASES,RESULT,OTHER,FILE,FILETEST,GFG1,GFG2,GFG3,DB,CF,SCHED,REMNOTI,QSELCF,SUBSEL,SUBCC,SUBCF,UNSUB,MSG=range(32)
# CLASS FOR FLOOD PROTECTION
class Spam_settings:
    def __init__(self):
        self.limits = {1: 3, 5: 7, 10: 10, 15: 13, 30: 20}  # max: 3 updates in 1 second, 7 updates in 5 seconds etc
        self.timeout_start = 10
        self.timeout_factor = 5
        self.factors = {}
        self.timeouts = {}
        self.times = {}

    def new_message(self, chat_id):
        update_time = time.time()
        if chat_id not in self.timeouts:
            self.timeouts.update({chat_id: 0})
            self.times.update({chat_id: [update_time]})
            self.factors.update({chat_id: 1})
        else:
            if self.timeouts[chat_id] > update_time:
                return self.timeouts[chat_id] - update_time
            for limit in self.limits:
                amount = 1
                for n, upd_time in enumerate(self.times[chat_id]):
                    if update_time - upd_time < limit:
                        amount += 1
                    else:
                        if amount > self.limits[limit]:
                            self.timeouts[chat_id] = update_time + self.timeout_start * (self.factors[chat_id])
                            self.factors[chat_id] *= self.timeout_factor
                            text = "You are timeouted by the flood protection system of this bot. Try again in {0} seconds.".format(
                                self.timeouts[chat_id] - update_time)

                            return text
        self.times[chat_id].insert(0, update_time)
        return 0

    def wrapper(self, func):  # only works on functions, not on instancemethods
        def func_wrapper(bot, update, *args2):
            timeout = self.new_message(update.effective_chat.id)
            if not timeout:
               return func(bot, update, *args2)
            elif isinstance(timeout, str):
                print("timeout")
                # Only works for messages (+Commands) and callback_queries (Inline Buttons)
                if update.callback_query:
                    bot.edit_message_text(chat_id=update.effective_chat.id,
                                          message_id=update.effective_message.message_id,
                                          text=timeout)
                elif update.message:
                    bot.send_message(chat_id=update.effective_chat.id, text=timeout)

        return func_wrapper


timeouts = Spam_settings()



# COMMAND HANDLER FUNCTION FOR /start COMMAND
@timeouts.wrapper
def start(bot, update):
    update.message.reply_text(
        'welcome!\nOnly one person can register through one telegram id\nHere are the commands\nEnter /cancel at any time to cancel operation\nEnter /randomcc to get a random question from codechef\nEnter /randomcf to get a random question from codeforces\nEnter /geeksforgeeks to get topics from geeks for geeks\nEnter /register to go to register menu to register your handle to the bot\nEnter /unregister to go to unregister menu to unregister from the bot\nEnter /ranklist to go to ranklist menu to get ranklist\nEnter /ongoing to get a list of ongoing competitions\nEnter /upcoming to get a list of upcoming competitions\nEnter /compiler to compile and run\nEnter /subscribe to get question of the day everyday\nEnter /unsubscribe to unsubscribe from question of the day\nEnter /update to initialise updating of your info\n Automatic updation of all data will take place every day\n To see all the commands enter /help any time.\n\nORIGINAL CREATOR @gotham13121997\nORIGINAL source code https://github.com/Gotham13121997/superCodingBot')


# COMMAND HANDLER FUNCTION FOR /help COMMAND
@timeouts.wrapper
def help(bot, update):
    update.message.reply_text(
        'Only one person can register through one telegram id\nHere are the commands\nEnter /register to go to register menu to register your handle to the bot\nEnter /cancel at any time to cancel operation\nEnter /randomcc to get a random question from codechef\nEnter /randomcf to get a random question from codeforces\nEnter /geeksforgeeks to get topics from geeks for geeks\nEnter /unregister to go to unregister menu to unregister from the bot\nEnter /ranklist to go to ranklist menu to get ranklist\nEnter /ongoing to get a list of ongoing competitions\nEnter /upcoming to get a list of upcoming competitions\nEnter /compiler to compile and run\nEnter /subscribe to get question of the day everyday\nEnter /unsubscribe to unsubscribe from question of the day\nEnter /update to initialise updating of your info\n Automatic updation of all data will take place every day\n To see all the commands enter /help any time.\n\nORIGINAL CREATOR @gotham13121997\nORIGINAL source code https://github.com/Gotham13121997/superCodingBot')


# FUNCTION FOR LOGGING ALL KINDS OF ERRORS
@timeouts.wrapper


# FUNCTION FOR SENDING THE RANDOM QUESTION TO USER ACCORDING TO HIS CHOICE

# END OF CONVERSATION HANDLER FOR GETTING RANDOM QUESTION FROM CODECHEF


# START OF CONVERSATION HANDLER FOR REGISTERING THE USERS HANDLES
@timeouts.wrapper


# FUNCTION FOR GETTING THE NAME AND ASKING ABOUT WHICH JUDGE USER WANTS TO REGISTER THEIR HANDLE FOR


# FUNCTION FOR GETTING THE ONLINE JUDGE AND ASKING FOR HANDLE


# FUNCTION FOR GETTING THE HANDLE AND REGISTERING IT IN DATABASE
# ALL THE MAGIC BEGINS HERE

    user = str(update.message.from_user.id)
    handle1 = update.message.text
    name1 = user_data['name']
    code1 = user_data['code']
    if code1 == 'HE':
        # IF HACKEREARTH
        opener = urllib.request.build_opener()
        # SCRAPING DATA FROM WEBPAGE
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            sauce = opener.open('https://www.hackerearth.com/@' + handle1)
            print('used')
            soup = bs.BeautifulSoup(sauce, 'html5lib')
            stri = "HACKEREARTH\n"
            for i in soup.find_all('a', {"href": "/users/" + handle1 + "/activity/hackerearth/#user-rating-graph"}):
                stri = stri + i.text + "\n"
            for i in soup.find_all('a', {"href": "/@" + handle1 + "/followers/"}):
                stri = stri + i.text + "\n"
            for i in soup.find_all('a', {"href": "/@" + handle1 + "/following/"}):
                stri = stri + i.text + "\n"
            vals = stri
        except urllib.error.URLError as e:
            # IF URL NOT FOUND THE ID IS WRONG
            update.message.reply_text('wrong id')
            user_data.clear()
            return ConversationHandler.END
    elif code1 == 'HR':
        # IF HACKERRANK
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            sauce = opener.open('https://www.hackerrank.com/' + handle1 + '?hr_r=1')
            soup = bs.BeautifulSoup(sauce, 'html5lib')
            try:
                soup.find('script', {"id": "initialData"}).text
            except AttributeError:
                update.message.reply_text('wrong id')
                user_data.clear()
                return ConversationHandler.END
            # I HAVE NO IDEA WHAT I HAVE DONE HERE
            # BUT IT SEEMS TO WORK
            s = soup.find('script', {"id": "initialData"}).text
            i = s.find("hacker_id", s.find("hacker_id", s.find("hacker_id") + 1) + 1)
            i = parse.unquote(s[i:i + 280]).replace(",", ">").replace(":", " ").replace("{", "").replace("}",
                                                                                                         "").replace(
                '"', "").split(">")
            s1 = "HACKERRANK\n"
            for j in range(1, 10):
                s1 = s1 + i[j] + "\n"
            vals = s1
        except urllib.error.URLError as e:
            update.message.reply_text('wrong id')
            user_data.clear()
            return ConversationHandler.END
    elif code1 == 'CC':
        # IF CODECHEF
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            sauce = opener.open('https://www.codechef.com/users/' + handle1)
            soup = bs.BeautifulSoup(sauce, 'html5lib')
            try:
                soup.find('a', {"href": "http://www.codechef.com/ratings/all"}).text
            except AttributeError:
                update.message.reply_text('wrong id')
                user_data.clear()
                return ConversationHandler.END
            try:
                s1 = soup.find('span', {"class": "rating"}).text + "\n"
            except AttributeError:
                s1 = ""
            s = "CODECHEF" + "\n" + s1 + "rating: " + soup.find('a', {
                "href": "http://www.codechef.com/ratings/all"}).text + "\n" + soup.find('div', {
                "class": "rating-ranks"}).text.replace(" ", "").replace("\n\n", "").strip('\n')
            vals = s
        except urllib.error.URLError as e:
            update.message.reply_text('wrong id')
            user_data.clear()
            return ConversationHandler.END
    elif code1 == 'SP':
        # IF SPOJ
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            sauce = opener.open('http://www.spoj.com/users/' + handle1 + '/')
            soup = bs.BeautifulSoup(sauce, 'html5lib')
            try:
                soup.find('div', {"class": "col-md-3"}).text
            except AttributeError:
                update.message.reply_text('wrong id')
                user_data.clear()
                return ConversationHandler.END
            s = soup.find('div', {"class": "col-md-3"}).text.strip('\n\n').replace("\t", "").split('\n')
            s = s[3].strip().split(":")
            s = "SPOJ\n" + s[0] + "\n" + s[1].strip(" ") + "\n" + soup.find('dl', {
                "class": "dl-horizontal profile-info-data profile-info-data-stats"}).text.replace("\t", "").replace(
                "\xa0", "").strip('\n')
            vals = s
        except urllib.error.URLError as e:
            update.message.reply_text('wrong id')
            user_data.clear()
            return ConversationHandler.END
    elif code1 == 'CF':
        # IF CODEFORCES
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            sauce = opener.open('http://codeforces.com/profile/' + handle1)
            soup = bs.BeautifulSoup(sauce, 'html5lib')
            try:
                soup.find('img', {"alt": "User\'\'s contribution into Codeforces community"}).text
            except AttributeError:
                update.message.reply_text('wrong id')
                user_data.clear()
                return ConversationHandler.END
            s = soup.find_all('span', {"style": "font-weight:bold;"})
            if len(s) == 0:
                s2 = ""
            else:
                s2 = "contest rating: " + s[0].text + "\n" + "max: " + s[1].text + s[2].text + "\n"
            s1 = "CODEFORCES\n" + s2 + "contributions: " + soup.find('img', {"alt": "User\'\'s contribution into Codeforces community"}).nextSibling.nextSibling.text
            vals = s1
        except urllib.error.URLError as e:
            update.message.reply_text('wrong id')
            user_data.clear()
            return ConversationHandler.END
    else:
        return ConversationHandler.END
    # CONNECTING TO DATABASE
    conn = sqlite3.connect(mount_point+'coders1.db')
    c = conn.cursor()
    # STORING THE PROFILE INFO IN datas TABLE
    # STORING HANDLES IN handles TABLE
    c.execute("INSERT OR IGNORE INTO datas (id, name, " + code1 + ") VALUES (?, ?, ?)", (user, name1, vals))
    c.execute("INSERT OR IGNORE INTO handles (id, name, " + code1 + ") VALUES (?, ?, ?)", (user, name1, handle1))
    if c.rowcount == 0:
        c.execute("UPDATE datas SET " + code1 + " = (?) , name= (?) WHERE id = (?) ", (vals, name1, user))
        c.execute("UPDATE handles SET " + code1 + " = (?) , name= (?) WHERE id = (?) ", (handle1, name1, user))
    if code1=='HE':
        try:
            rat=vals.split('\n')
            if(rat[1]=="Rating"):
                rat2=rat[2].strip(" ").strip("\n")
                c.execute("INSERT OR IGNORE INTO priority (id, HE) VALUES(?, ?)", (user, rat2))
                if(c.rowcount==0):
                    c.execute("UPDATE  priority SET HE = (?) WHERE id = (?) ", (rat2, user))
        except:
            pass
    elif code1=='HR':
        try:
            rat=vals.split('\n')
            rat2=rat[1].split(" ")[1].strip(" ").strip("\n")
            c.execute("INSERT OR IGNORE INTO priority (id, HR) VALUES(?, ?)", (user, rat2))
            if (c.rowcount == 0):
                c.execute("UPDATE  priority SET HR = (?) WHERE id = (?) ", (rat2, user))
        except:
            pass
    elif code1=='CF':
        try:
            rat=vals.split("\n")
            if "contest rating:"in rat[1]:
                rat2=rat[1].split(" ")[2].strip(" ").strip("\n")
                c.execute("INSERT OR IGNORE INTO priority (id, CF) VALUES(?, ?)", (user, rat2))
                if (c.rowcount == 0):
                    c.execute("UPDATE  priority SET CF = (?) WHERE id = (?) ", (rat2, user))
        except:
            pass
    elif code1=='CC':
        try:
            rat=vals.split("\n")
            if not "rating" in rat[1]:
                rat2=rat[2].split(" ")[1].strip(" ").strip("\n")
                c.execute("INSERT OR IGNORE INTO priority (id, CC) VALUES(?, ?)", (user, rat2))
                if (c.rowcount == 0):
                    c.execute("UPDATE  priority SET CC = (?) WHERE id = (?) ", (rat2, user))
        except:
            pass
    elif code1=='SP':
        c.execute("INSERT OR IGNORE INTO priority (id) VALUES(?)", (user,))

    conn.commit()
    # BELOW LINES ARE USED TO CREATE XLMX FILES OF ALL SORTS OF RANKLIST
    # SO WHEN USER ASKS FOR RANKLIST THERE IS NO DELAY
    workbook = Workbook(mount_point+'all.xlsx')
    worksheet = workbook.add_worksheet()
    format = workbook.add_format()
    format.set_align('top')
    format.set_text_wrap()
    mysel = c.execute("SELECT datas.name, datas.HE, datas.HR, datas.SP, datas.CF, datas.CC FROM datas INNER JOIN priority ON datas.id=priority.id ORDER BY CAST(priority.CF AS FLOAT) DESC, CAST(priority.CC AS FLOAT) DESC, CAST(priority.HR AS FLOAT) DESC, CAST(priority.HE AS FLOAT) DESC")
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j], format)
            worksheet.set_row(i, 170)
    worksheet.set_column(0, 5, 40)
    workbook.close()
    workbook = Workbook(mount_point + code1 + ".xlsx")
    worksheet = workbook.add_worksheet()
    format = workbook.add_format()
    format.set_align('top')
    format.set_text_wrap()
    if(code1=='SP'):
        mysel = c.execute("SELECT name, " + code1 + " FROM datas")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, row[j], format)
                worksheet.set_row(i, 170)
        worksheet.set_column(0, 5, 40)
        workbook.close()
    else:
        mysel = c.execute("SELECT datas.name, datas." + code1 + " FROM datas INNER JOIN priority ON datas.id=priority.id ORDER BY CAST(priority."+code1+" AS FLOAT) DESC")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, row[j], format)
                worksheet.set_row(i, 170)
        worksheet.set_column(0, 5, 40)
        workbook.close()
    conn.close()
    update.message.reply_text("Succesfully Registered")
    update.message.reply_text(name1 + "    \n" + vals)
    user_data.clear()
    return ConversationHandler.END


# END OF CONVERSATION HANDLER FOR REGISTERING THE USERS HANDLES


# START OF CONVERSATION HANDLER FOR COMPILING AND RUNNING
@timeouts.wrapper
def compilers(bot, update):
    keyboard = [[InlineKeyboardButton("C++", callback_data='cppcomp1'),
                 InlineKeyboardButton("Python", callback_data='pythoncomp1')],
                [InlineKeyboardButton("C", callback_data='ccomp1'),
                 InlineKeyboardButton("Java", callback_data='javacomp1')],
                [InlineKeyboardButton("Python3", callback_data='python3comp1'),
                 InlineKeyboardButton("Java8", callback_data='java8comp1')],
                [InlineKeyboardButton("Other", callback_data='othercomp1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select the language', reply_markup=reply_markup)
    return LANG


# FUNCTION TO GET THE PROGRAMMING LANGUAGE
def lang(bot, update, user_data):
    query = update.callback_query
    val = query.data
    val=str(val).replace("comp1","")
    if val == "other":
        # IF USER CHOOSES OTHER
        s1 = ""
        for i in compiler.supportedlanguages():
            s1 = s1 + i + ","
        bot.edit_message_text(text="enter the name of language\n" + s1, chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return OTHER
    else:
        # ELSE ASKING WETHER HE WANTS TO SEND SOURCE CODE OR A .TXT FILE
        user_data['lang'] = val
        keyboard = [[InlineKeyboardButton("Enter Source Code", callback_data='codeso1'),
                     InlineKeyboardButton("Send a .txt file", callback_data='fileso1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text="please select", reply_markup=reply_markup, chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return CODE


# FUNCTION TO GET THE SOURCE CODE OR .TXT FILE AS INPUT
def code(bot, update, user_data):
    query = update.callback_query
    val = query.data
    val=str(val).replace("so1","")
    if val == "code":
        bot.edit_message_text(text="please enter your code\nPlease make sure that the first line is not a comment line",
                              chat_id=query.message.chat_id, message_id=query.message.message_id)
        return DECODE
    elif val=="file":
        bot.edit_message_text(text="please send your .txt file\nMaximum size 2mb", chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return FILE
    else:
        return ConversationHandler.END


# FUNCTION TO GET TESTCASE FILE
def filetest(bot, update, user_data):
    file_id = update.message.document.file_id
    file_id = update.message.document.file_id
    file_size = update.message.document.file_size
    if file_size > 2097152:
        update.message.reply_text("FILE SIZE GREATER THAN 2 MB")
        return ConversationHandler.END
    newFile = bot.get_file(file_id)
    newFile.download('test.txt')
    with open('test.txt', 'rt') as f:
        source = f.read()
    s1 = (str(user_data['code'])).replace("«", "<<").replace("»", ">>")
    result = compiler.run({'source': s1,
                           'lang': user_data['lang'],
                           'testcases': [source]
                           })
    output = result.output
    time1 = result.time
    memory1 = result.memory
    message1 = result.message
    if time1 is not None:
        time1 = time1[0]
    if memory1 is not None:
        memory1 = memory1[0]
    if output is not None:
        output = output[0]
    else:
        output = ""
    markup = ReplyKeyboardRemove()
    if (len(output) <= 2897):
        update.message.reply_text("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
            memory1) + "\nMessage: " + str(message1), reply_markup=markup)
    else:
        with open("out.txt", "w") as text_file:
            text_file.write("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
                memory1) + "\nMessage: " + str(message1))
        bot.send_document(chat_id=update.message.chat_id, document=open('out.txt', 'rb'), reply_markup=markup)
        os.remove('out.txt')
    user_data.clear()
    os.remove('test.txt')
    return ConversationHandler.END


# FUNCTION TO DOWNLOAD THE FILE SENT AND EXTRACT ITS CONTENTS
def filer(bot, update, user_data):
    file_id = update.message.document.file_id
    file_size=update.message.document.file_size
    if file_size > 2097152:
        update.message.reply_text("FILE SIZE GREATER THAN 2 MB")
        return ConversationHandler.END
    newFile = bot.get_file(file_id)
    newFile.download('abcd.txt')
    with open('abcd.txt', 'r') as f:
        source = f.read()
    user_data['code'] = source
    custom_keyboard = [['#no test case', '#send a .txt file']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keybord=True)
    update.message.reply_text(
        'Please send test cases together as you would do in online ide\nIf you dont want to provide test cases select #no test case\n I you want to send test cases as .txt file select #send a .txt file',
        reply_markup=reply_markup)
    # REMOVING THE FILE AFTER PROCESS IS COMPLETE
    os.remove('abcd.txt')
    return TESTCASES


# FUNCTION TO GET THE SOURCE CODE SENT BY USER
def decode(bot, update, user_data):
    user_data['code'] = update.message.text
    custom_keyboard = [['#no test case', '#send a .txt file']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keybord=True)
    update.message.reply_text(
        'Please send test cases together as you would do in online ide\nIf you dont want to provide test cases select #no test case\n I you want to send test cases as .txt file select #send a .txt file',
        reply_markup=reply_markup)
    return TESTCASES


# FUNCTION TO GET THE TEST CASES FROM THE USER
def testcases(bot, update, user_data):
    s = update.message.text
    markup = ReplyKeyboardRemove()
    if s == "#send a .txt file":
        update.message.reply_text("Please send your testcases as a .txt file\nMaximum size 2mb", reply_markup=markup)
        return FILETEST
    if s == "#no test case":
        # CONVERTING UNICODE CHARACTER TO DOUBLE GREATER THAN OR LESS THAN
        # WEIRD
        s1 = (str(user_data['code'])).replace("«", "<<").replace("»", ">>")
        # USING COMPILER FUNCTION FROM helper.py script
        result = compiler.run({'source': s1,
                               'lang': user_data['lang']
                               })
        # GETTING OUTPUT FROM result CLASS in helper.py script
        output = result.output
        time1 = result.time
        memory1 = result.memory
        message1 = result.message
        if time1 is not None:
            time1 = time1[0]
        if memory1 is not None:
            memory1 = memory1[0]
        if output is not None:
            output = output[0]
        else:
            output = ""
        if (len(output) <= 2897):
            update.message.reply_text("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
                memory1) + "\nMessage: " + str(message1), reply_markup=markup)
        else:
            with open("out.txt", "w") as text_file:
                text_file.write("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
                    memory1) + "\nMessage: " + str(message1))
            bot.send_document(chat_id=update.message.chat_id, document=open('out.txt', 'rb'), reply_markup=markup)
            os.remove('out.txt')
    else:
        # AGAIN THE SAME DRILL
        s1 = (str(user_data['code'])).replace("«", "<<").replace("»", ">>")
        result = compiler.run({'source': s1,
                               'lang': user_data['lang'],
                               'testcases': [s]
                               })
        output = result.output
        time1 = result.time
        memory1 = result.memory
        message1 = result.message
        if time1 is not None:
            time1 = time1[0]
        if memory1 is not None:
            memory1 = memory1[0]
        if output is not None:
            output = output[0]
        else:
            output = ""
        if (len(output) <= 2897):
            update.message.reply_text("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
                memory1) + "\nMessage: " + str(message1), reply_markup=markup)
        else:
            with open("out.txt", "w") as text_file:
                text_file.write("Output:\n" + str(output) + "\n" + "Time: " + str(time1) + "\nMemory: " + str(
                    memory1) + "\nMessage: " + str(message1))
            bot.send_document(chat_id=update.message.chat_id, document=open('out.txt', 'rb'), reply_markup=markup)
            os.remove('out.txt')
    user_data.clear()
    return ConversationHandler.END


# FUNCTION FOR THE CASE WHERE USER HAD SELECTED OTHER
def other(bot, update, user_data):
    s = update.message.text
    user_data['lang'] = s
    keyboard = [[InlineKeyboardButton("Enter Source Code", callback_data='code'),
                 InlineKeyboardButton("Send a file", callback_data='file')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("please select", reply_markup=reply_markup)
    return CODE


# END OF CONVERSATION HANDLER FOR COMPILING AND RUNNING

# START OF CONVERSATION HANDLER FOR GEEKS FOR GEEKS


# FUNCTION TO SHOW SUBMENU 1

    query = update.callback_query
    val = query.data
    val=str(val).replace("gfg1","")
    val=val+".json"
    user_data['gfg'] = val
    if (val == "Algorithms.json"):
        keyboard = [[InlineKeyboardButton("Analysis of Algorithms", callback_data='Analysis of Algorithmsgfg2'),
                     InlineKeyboardButton("Searching and Sorting", callback_data='Searching and Sortinggfg2')],
                    [InlineKeyboardButton("Greedy Algorithms", callback_data='Greedy Algorithmsgfg2'),
                     InlineKeyboardButton("Dynamic Programming", callback_data='Dynamic Programminggfg2')],
                    [InlineKeyboardButton("Strings and Pattern Searching",
                                          callback_data='Strings and Pattern Searchinggfg2'),
                     InlineKeyboardButton("Backtracking", callback_data='Backtrackinggfg2')],
                    [InlineKeyboardButton("Geometric Algorithms", callback_data='Geometric Algorithmsgfg2'),
                     InlineKeyboardButton("Mathematical Algorithms", callback_data='Mathematical Algorithmsgfg2')],
                    [InlineKeyboardButton("Bit Algorithms", callback_data='Bit Algorithmsgfg2'),
                     InlineKeyboardButton("Randomized Algorithms", callback_data='Randomized Algorithmsgfg2')],
                    [InlineKeyboardButton("Misc Algorithms", callback_data='Misc Algorithmsgfg2'),
                     InlineKeyboardButton("Recursion", callback_data='Recursiongfg2')],
                    [InlineKeyboardButton("Divide and Conquer", callback_data='Divide and Conquergfg2')]]
    elif (val == "DS.json"):
        keyboard = [[InlineKeyboardButton("Linked Lists", callback_data='Linked Listsgfg2'),
                     InlineKeyboardButton("Stacks", callback_data='Stacksgfg2')],
                    [InlineKeyboardButton("Queue", callback_data='Queuegfg2'),
                     InlineKeyboardButton("Binary Trees", callback_data='Binary Treesgfg2')],
                    [InlineKeyboardButton("Binary Search Trees",
                                          callback_data='Binary Search Treesgfg2'),
                     InlineKeyboardButton("Heaps", callback_data='Heapsgfg2')],
                    [InlineKeyboardButton("Hashing", callback_data='Hashinggfg2'),
                     InlineKeyboardButton("Graphs", callback_data='Graphsgfg2')],
                    [InlineKeyboardButton("Advanced Data Structures", callback_data='Advanced Data Structuresgfg2'),
                     InlineKeyboardButton("Arrays", callback_data='Arraysgfg2')],
                    [InlineKeyboardButton("Matrix", callback_data='Matrixgfg2')]]
    elif (val == "GATE.json"):
        keyboard = [[InlineKeyboardButton("Operating Systems", callback_data='Operating Systemsgfg2'),
                     InlineKeyboardButton("Database Management Systems", callback_data='Database Management Systemsgfg2')],
                    [InlineKeyboardButton("Automata Theory", callback_data='Automata Theorygfg2'),
                     InlineKeyboardButton("Compilers", callback_data='Compilersgfg2')],
                    [InlineKeyboardButton("Computer Networks",
                                          callback_data='Computer Networksgfg2'),
                     InlineKeyboardButton("GATE Data Structures and Algorithms",
                                          callback_data='GATE Data Structures and Algorithmsgfg2')]]
    elif (val == "Interview.json"):
        keyboard = [[InlineKeyboardButton("Payu", callback_data='Payugfg2'),
                     InlineKeyboardButton("Adobe", callback_data='Adobegfg2')],
                    [InlineKeyboardButton("Amazon", callback_data='Amazongfg2'),
                     InlineKeyboardButton("Flipkart", callback_data='Flipkartgfg2')],
                    [InlineKeyboardButton("Google",
                                          callback_data='Googlegfg2'),
                     InlineKeyboardButton("Microsoft", callback_data='Microsoftgfg2')],
                    [InlineKeyboardButton("Snapdeal", callback_data='Snapdealgfg2'),
                     InlineKeyboardButton("Zopper-Com", callback_data='Zopper-Comgfg2')],
                    [InlineKeyboardButton("Yahoo", callback_data='Yahoogfg2'),
                     InlineKeyboardButton("Cisco", callback_data='Ciscogfg2')],
                    [InlineKeyboardButton("Facebook", callback_data='Facebookgfg2'),
                     InlineKeyboardButton("Yatra.Com", callback_data='Yatra.Comgfg2')],
                    [InlineKeyboardButton("Symantec", callback_data='Symantecgfg2'),
                     InlineKeyboardButton("Myntra", callback_data='Myntragfg2')],
                    [InlineKeyboardButton("Groupon", callback_data='Groupongfg2'),
                     InlineKeyboardButton("Belzabar", callback_data='Belzabargfg2')],
                    [InlineKeyboardButton("Paypal", callback_data='Paypalgfg2'),
                     InlineKeyboardButton("Akosha", callback_data='Akoshagfg2')],
                    [InlineKeyboardButton("Linkedin", callback_data='Linkedingfg2'),
                     InlineKeyboardButton("Browserstack", callback_data='Browserstackgfg2')],
                    [InlineKeyboardButton("Makemytrip", callback_data='Makemytripgfg2'),
                     InlineKeyboardButton("Infoedge", callback_data='Infoedgegfg2')],
                    [InlineKeyboardButton("Practo", callback_data='Practogfg2'),
                     InlineKeyboardButton("Housing-Com", callback_data='Housing-Comgfg2')],
                    [InlineKeyboardButton("Ola-Cabs", callback_data='Ola-Cabsgfg2'),
                     InlineKeyboardButton("Grofers", callback_data='Grofersgfg2')],
                    [InlineKeyboardButton("Thoughtworks", callback_data='Thoughtworksgfg2'),
                     InlineKeyboardButton("Delhivery", callback_data='Delhiverygfg2')],
                    [InlineKeyboardButton("Taxi4Sure", callback_data='Taxi4Suregfg2'),
                     InlineKeyboardButton("Lenskart", callback_data='Lenskartgfg2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(text="Please select", reply_markup=reply_markup, chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    return GFG2


# FUNCTION TO SHOW SUBMENU 2

    query = update.callback_query
    try:
        val = query.data
        val=str(val).replace("gfg3","")
        with open(user_data['gfg'], encoding='utf-8') as data_file:
            data = json.load(data_file)
        se = data["Advanced Data Structures"][val]
        s = ""
        for i in se:
            s = s + '<a href="' + se[i] + '">' + i + '</a>\n\n'
        bot.edit_message_text(text=val + "\n\n" + s, chat_id=query.message.chat_id,
                              message_id=query.message.message_id, parse_mode=ParseMode.HTML)
    except:
        return ConversationHandler.END
    user_data.clear()
    return ConversationHandler.END


# END OF CONVERSATION HANDLER FOR GEEKS FOR GEEKS

# GLOBAL VARIABLES STORE THE PREVIOUS DATA TEMPORARILY IN CASE THE WEBPAGE IS BEING MAINTAINED


# MAIN SETUP FUNCTION
def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        # CONVERSATION HANDLER FOR REGISTERING
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('register', register)],
            allow_reentry=True,
            states={

                NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],

                JUDGE: [CallbackQueryHandler(judge, pass_user_data=True,pattern=r'\w*reg1\b')],

                HANDLE: [MessageHandler(Filters.text, handle, pass_user_data=True)]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR GETTING RANKLIST
        conv_handler1 = ConversationHandler(
            entry_points=[CommandHandler('ranklist', ranklist)],
            allow_reentry=True,
            states={

                SELECTION: [CallbackQueryHandler(selection,pattern=r'\w*sel1\b')],

                HOLO: [CallbackQueryHandler(holo,pattern=r'\w*list6\b')],

                SOLO: [CallbackQueryHandler(solo,pattern=r'\w*list7\b')],

                POLO: [MessageHandler(Filters.text, polo, pass_user_data=True)],

                XOLO: [CallbackQueryHandler(xolo, pass_user_data=True,pattern=r'\w*list8\b')]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR UNREGISTERING
        conv_handler2 = ConversationHandler(
            entry_points=[CommandHandler('unregister', unregister)],
            allow_reentry=True,
            states={

                REMOVER: [CallbackQueryHandler(remover,pattern=r'\w*rem2\b')]

            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR UPDATING
        conv_handler3 = ConversationHandler(
            entry_points=[CommandHandler('update', updatesel)],
            allow_reentry=True,
            states={

                UPDA: [CallbackQueryHandler(updasel,pattern=r'\w*upd5\b')]

            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR COMPILING AND RUNNING
        conv_handler4 = ConversationHandler(
            entry_points=[CommandHandler('compiler', compilers)],
            allow_reentry=True,
            states={

                LANG: [CallbackQueryHandler(lang, pass_user_data=True,pattern=r'\w*comp1\b')],
                CODE: [CallbackQueryHandler(code, pass_user_data=True,pattern=r'\w*so1\b')],
                DECODE: [MessageHandler(Filters.text, decode, pass_user_data=True)],
                TESTCASES: [MessageHandler(Filters.text, testcases, pass_user_data=True)],
                OTHER: [MessageHandler(Filters.text, other, pass_user_data=True)],
                FILE: [MessageHandler(Filters.document, filer, pass_user_data=True)],
                FILETEST: [MessageHandler(Filters.document, filetest, pass_user_data=True)]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR GETTING A RANDOM QUESTION FROM CODECHEF
        conv_handler5 = ConversationHandler(
            entry_points=[CommandHandler('randomcc', randomcc)],
            allow_reentry=True,
            states={

                QSELCC: [CallbackQueryHandler(qselcc,pattern=r'\w*cc1\b')]

            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR GEEKS FOR GEEKS
        conv_handler6 = ConversationHandler(
            entry_points=[CommandHandler('geeksforgeeks', gfg)],
            allow_reentry=True,
            states={

                GFG1: [CallbackQueryHandler(gfg1, pass_user_data=True,pattern=r'\w*gfg1\b')],

                GFG2: [CallbackQueryHandler(gfg2, pass_user_data=True,pattern='^.*gfg2.*$')],

                GFG3: [CallbackQueryHandler(gfg3, pass_user_data=True,pattern='^.*gfg3.*$')]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR REPLACING SQLITE DATABASE
        conv_handler7 = ConversationHandler(
            entry_points=[CommandHandler('senddb', getDb)],
            allow_reentry=True,
            states={
                DB: [MessageHandler(Filters.document, db)]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR GETTING UPCOMING COMPETITIONS
        conv_handler8 = ConversationHandler(
            entry_points=[CommandHandler('upcoming', upcoming)],
            allow_reentry=True,
            states={

                SCHED: [CallbackQueryHandler(remind,pattern=r"^[0-9]*$")]

            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR REMOVING CONTEST REMINDERS
        conv_handler9 = ConversationHandler(
            entry_points=[CommandHandler('dontRemindMe', removeRemind)],
            allow_reentry=True,
            states={
                REMNOTI: [CallbackQueryHandler(remnoti,pattern=r'^.*notiplz.*$')]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER FOR GETTING RANDOM QUESTION FROM CODEFORCES
        conv_handler10 = ConversationHandler(
            entry_points=[CommandHandler('randomcf', randomcf)],
            allow_reentry=True,
            states={

                QSELCF: [CallbackQueryHandler(qselcf,pattern=r'\w*cf1\b')]

            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # ADMIN CONVERSATION HANDLER TO REPLACE CODEFORCES JSON FILE
        conv_handler11 = ConversationHandler(
            entry_points=[CommandHandler('sendcf', getCf)],
            allow_reentry=True,
            states={
                CF: [MessageHandler(Filters.document,cf)]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER TO SUBSCRIBE TO QUESTION OF THE DAY
        conv_handler12 = ConversationHandler(
            entry_points=[CommandHandler('subscribe', subscribe)],
            allow_reentry=True,
            states={
                SUBSEL:[CallbackQueryHandler(subsel,pattern=r'\w*sub3\b')],
                SUBCC:[CallbackQueryHandler(subcc,pattern=r'\w*cc2\b')],
                SUBCF: [CallbackQueryHandler(subcf,pattern=r'\w*cf2\b')]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        # CONVERSATION HANDLER TO UNSUBSCRIBE FROM QUESTION OF THE DAY
        conv_handler13 = ConversationHandler(
            entry_points=[CommandHandler('unsubscribe', unsubsel)],
            allow_reentry=True,
            states={
                UNSUB: [CallbackQueryHandler(unsub,pattern=r'\w*unsub4\b')]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )
        dp.add_handler(conv_handler)
        dp.add_handler(conv_handler1)
        dp.add_handler(conv_handler2)
        dp.add_handler(conv_handler3)
        dp.add_handler(conv_handler4)
        dp.add_handler(conv_handler5)
        dp.add_handler(conv_handler6)
        dp.add_handler(conv_handler7)
        dp.add_handler(conv_handler8)
        dp.add_handler(conv_handler9)
        dp.add_handler(conv_handler10)
        dp.add_handler(conv_handler11)
        dp.add_handler(conv_handler12)
        dp.add_handler(conv_handler13)
        dp.add_handler(CommandHandler('help', help))
        dp.add_handler(CommandHandler('givememydb', givememydb))
        dp.add_handler(CommandHandler('getcfjson', getcfjson))
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CommandHandler('ongoing', ongoing))
        dp.add_handler(CommandHandler('adminhandle', adminhandle))
        dp.add_handler(CommandHandler('adminud', adminupdate))
        dp.add_handler(CommandHandler('adminuq', admqupd))
        dp.add_handler(CommandHandler('adminrestart', restart))
        # log all errors
        dp.add_error_handler(error)
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
