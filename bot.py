from _socket import if_nameindex

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import requests
#import telepot
import time
import urllib3
import json
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# proxy_url = "http://proxy.server:3128"

# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

def start(bot, update):
    update.message.reply_text('Hi I\'m GitMan!\n These are List Of My Works:\n 1.Use /pic And Username to See the Picture.\n 2.Use /page And Username to Get the User Github Page.\n 3.Use /followcount for get Number of Users followers and following.\n 4.Use /followers to see Users followers.\n 5.Use /following to see Users following.\n 6.Use /repo to see Users Repos.')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bot, update):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

# def help(bot, update):
#     update.message.reply_text("Help!")

def user_pic(bot, update, args):
    if args:
        temp_txt = ' '.join(args)
        js_pic = requests.get('https://api.github.com/users/' + temp_txt)
        js_obj = js_pic.json()
        if 'message' in js_obj:
            bot.send_message(chat_id=update.message.chat_id, text='`Username is invalid`', parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='<b>{0}</b>'.format(js_obj['login']), parse_mode=telegram.ParseMode.HTML)
            bot.send_photo(chat_id=update.message.chat_id, photo=js_obj['avatar_url'])

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')

def user_page(bot, update, args):
    if args:
        temp_txt = ''.join(args)
        js_page = requests.get('https://api.github.com/users/' + temp_txt)
        js_obj = js_page.json()
        if 'message' in js_obj:
            bot.send_message(chat_id=update.message.chat_id, text='`Username is invalid`', parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='<i>Github Page: </i> <a href="{0}">{1}</a>'.format(js_obj['html_url'], js_obj['html_url']), parse_mode=telegram.ParseMode.HTML)
        # bot.send_message(chat_id=update.message.chat_id, text='<a href="{}"><b><i>Github Page</b></i></a>'.format(js_obj['html_url']), parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')

# def user_repos(bot, update, args):
#     if args:
#         temp_txt =

def user_follow(bot, update, args):
    if args:
        temp_txt = ''.join(args)
        js_page = requests.get('https://api.github.com/users/' + temp_txt)
        js_obj = js_page.json()
        bot.send_message(chat_id=update.message.chat_id, text='<b>Number Of Followers: {0}</b>\nUse /followers to see followers.\n<b>Number Of Following: {1}</b>\nUse /following to see following.'.format(js_obj['followers'], js_obj['following']), parse_mode=telegram.ParseMode.HTML)

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')

def user_followers(bot, update, args):
    if args:
        temp_txt = ''.join(args)
        js_page = requests.get('https://api.github.com/users/' + temp_txt + '/followers')
        js_obj = js_page.json()
        if js_obj:
            bot.send_message(chat_id=update.message.chat_id, text='<b>Followers: </b>', parse_mode=telegram.ParseMode.HTML)
            count = 1
            for i in js_obj:
                bot.send_message(chat_id=update.message.chat_id, text='{0}- <i>{1}</i>'.format(count, i['login']), parse_mode=telegram.ParseMode.HTML)
                count += 1
        else:
            bot.send_message(chat_id=update.message.chat_id, text='`There is no follower!`', parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')

def user_following(bot, update, args):
    if args:
        temp_txt = ''.join(args)
        js_page = requests.get('https://api.github.com/users/' + temp_txt + '/following')
        js_obj = js_page.json()
        if js_obj:
            bot.send_message(chat_id=update.message.chat_id, text='<b>Following: </b>', parse_mode=telegram.ParseMode.HTML)
            count = 1
            for i in js_obj:
                bot.send_message(chat_id=update.message.chat_id, text='{0}- <i>{1}</i>'.format(count, i['login']), parse_mode=telegram.ParseMode.HTML)
                count += 1
        else:
            bot.send_message(chat_id=update.message.chat_id, text='`There is no following!`', parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')

def user_repo(bot, update, args):
    if args:
        temp_txt = ''.join(args)
        js_page = requests.get('https://api.github.com/users/' + temp_txt + '/repos')
        js_page2 = requests.get('https://api.github.com/users/' + temp_txt)
        js_obj2 = js_page2.json()
        js_obj = js_page.json()
        if 'message' in js_obj:
            bot.send_message(chat_id=update.message.chat_id, text='`Username is invalid`', parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='<b>Number of Repos: </b>{}'.format(js_obj2['public_repos']), parse_mode=telegram.ParseMode.HTML)
            count = 1
            for i in js_obj:
                bot.send_message(chat_id=update.message.chat_id, text='{0}- <i>{1}</i>'.format(count, i['name']), parse_mode=telegram.ParseMode.HTML)
                count += 1
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please Enter a Username!')


def main():
    TOKEN = "432666119:AAGbNIuTpNZ2sJG4-9MDeETQN1N6uOFN0tU"
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://gitman.herokuapp.com/" + TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    # dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("pic", user_pic, pass_args=True))
    dp.add_handler(CommandHandler("page", user_page, pass_args=True))
    dp.add_handler(CommandHandler("followcount", user_follow, pass_args=True))
    dp.add_handler(CommandHandler("followers", user_followers, pass_args=True))
    dp.add_handler(CommandHandler("following", user_following, pass_args=True))
    dp.add_handler(CommandHandler("repo", user_repo, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
