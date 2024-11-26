from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,  ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json

#Load config
with open('config.json', 'r') as config:
    config = json.load(config)
    token = config['token']
    

# Funktion für den Startbefehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tasten definieren
    keyboard = [
        ["Trading", "Stats"],  # Erste Reihe mit zwei Tasten
        ["Info", "Help"],             # Zweite Reihe mit einer Taste
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    # Nachricht mit Menü senden
    await update.message.reply_text("Wähle eine Option:", reply_markup=reply_markup)
    
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Buttons definieren
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='option_1')],
        [InlineKeyboardButton("Option 2", callback_data='option_2')],
        [InlineKeyboardButton("Option 3", callback_data='option_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Nachricht mit Menü senden
    await update.message.reply_text("Wähle eine Option:", reply_markup=reply_markup)

# Funktion für beliebige Nachrichten
#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await update.message.reply_text(f"Du hast gesagt: {update.message.text}")

# Funktion für unbekannte Befehle
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Diesen Befehl kenne ich nicht. 😅")
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat.id
    message_id = update.message.id
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print('Fehler beim loeschen', str(e))
        
    if user_message == "Trading":
        # Buttons definieren
        keyboard = [
        [InlineKeyboardButton("Switch Trading Mode", callback_data='switch_mode')],
        [InlineKeyboardButton("Option 2", callback_data='option_2')],
        [InlineKeyboardButton("Option 3", callback_data='option_3')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Nachricht mit Menü senden
        await update.message.reply_text("Wähle eine Option:", reply_markup=reply_markup)
        
    elif user_message == "Option 2":
        await update.message.reply_text("Du hast *Option 2* gewählt!", parse_mode='Markdown')
    elif user_message == "Option 3":
        await update.message.reply_text("Du hast *Option 3* gewählt!", parse_mode='Markdown')
    else:
        await update.message.reply_text("Unbekannte Option.")
    
# Callback-Funktion für Button-Klicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Antwortet auf den Klick, um "Ladesymbol" zu entfernen

    # Aktion basierend auf der Auswahl
    if query.data == 'option_1':
        await query.edit_message_text("Du hast *Option 1* gewählt!", parse_mode='Markdown')
    elif query.data == 'option_2':
        await query.edit_message_text("Du hast *Option 2* gewählt!", parse_mode='Markdown')
    elif query.data == 'option_3':
        await query.edit_message_text("Du hast *Option 3* gewählt!", parse_mode='Markdown')
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Verfügbare Befehle:
    /start - Startet den Bot
    /help - Zeigt diese Hilfe
    """
    await update.message.reply_text(help_text)


def main():

    # Bot-Anwendung erstellen
    application = Application.builder().token(token).build()

    # Handler für Befehle hinzufügen
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("help", help))
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Bot starten
    application.run_polling()

if __name__ == "__main__":
    main()

    
