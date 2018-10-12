#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import logging
from intent_processing import get_location_recommendation
from yelp import search_yelp
import geopy.distance

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LOCATION, BUSINESS_CHOICE, RESULT = range(3)

# It's ugly but it's a 2 hours challenge


locations_dict = {
    # user : {lattitude: , longitude: }
}

btypes_dict = {

}

results_dict = {

}

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hi! I am the Elca Challenge Bot.'
        'I am going to show you some places. '
        'To start, send me a location.'
    )

    user = update.message.from_user

    logger.info("Started conversationg with {}".format(user.id))

    return LOCATION


def location(bot, update):

    user = update.message.from_user

    logger.info("Receiving location from {}".format(user.id))

    user_location = update.message.location

    if user_location is None:
        update.message.reply_text(
            "Uh-oh, it looks like you didn't send me a location :( Let's try again !")
        logger.info("Invalid location from {}".format(user.id))

        return LOCATION

    update.message.reply_text("Great ! What would you like to do ?")

    logger.info("Received location {} from {}".format(user_location, user.id))

    locations_dict[user.id] = user_location

    return BUSINESS_CHOICE


def business_choice(bot, update):
    user = update.message.from_user

    # retrieve user location from locations_dict[user.id]

    btype = get_location_recommendation(update.message.text)

    btypes_dict[user.id] = btype

    update.message.reply_text(
        "Great, you're looking for a {}. Let's look at what we have near you.".format(btype[0]))

    logger.info(
        "Received business type intent {} from user {}".format(btype[0], user.id))

    user = update.message.from_user

    loc = locations_dict[user.id]

    result = search_yelp(business_type=btypes_dict[user.id], location=loc)

    results_dict[user.id] = result

    l1 = (loc["latitude"], loc["longitude"])

    update.message.reply_text("Ok, so here is what I found: ",
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("{}, ({})".format(
                                      x["name"],
                                      geopy.distance.distance(
                                          l1, (x["location"][0], x["location"][1]))
                                  ), callback_data=x["name"])] for x in result
                              ]))

    logger.info(result)

    return ConversationHandler.END


def menu_actions(bot, update):

    logger.info(update)

    user = update.callback_query.message.chat.id
    query = update.callback_query

    for result in results_dict[user]:
        if result["name"] == query.data:
            bot.send_venue(user,
                           latitude=result["location"][0],
                           longitude=result["location"][1],
                           title=result["name"],
                           address=result["display_address"]
                           )

    bot.send_message(user, "Thank you for trying our bot !")

    return ConversationHandler.END


def result(bot, update):

    pass


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Oups, I think something really wrong happened.')

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("API TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            LOCATION: [MessageHandler(Filters.text | Filters.location, location)],
            BUSINESS_CHOICE: [MessageHandler(Filters.text, business_choice)],
            RESULT: [MessageHandler(Filters.text, menu_actions)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]

    )

    # on different commands - answer in Telegram
    dp.add_handler(conv_handler)

    dp.add_handler(CallbackQueryHandler(menu_actions))

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
