from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# Этапы разговора
LEVEL, TEXT, ACTION = range(3)

# Тексты и переводы
texts = {
    "easy": [
        {
            "title": "Life Like a Box of Chocolates",
            "content": "My mom always said life was like a box of chocolates. You never know what you’re gonna get. But I always tried to do the best with what I got. You have to do the best with what God gave you. And if you keep your mind on where you are going, you might just get there.",
            "translation": "Моя мама всегда говорила, что жизнь — как коробка шоколадных конфет. Никогда не знаешь, что тебе попадётся. Но я всегда старался делать лучшее из того, что у меня есть. Нужно использовать по максимуму то, что дал тебе Бог. И если ты будешь думать о том, куда идёшь, возможно, ты туда доберёшься."
        },
        {
            "title": "It’s Our Choices",
            "content": "It is not our abilities that show what we truly are. It is our choices. We all face difficult decisions in life. Sometimes, we must choose between what is right and what is easy. Remember, happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
            "translation": "Не наши способности показывают, кто мы такие на самом деле. Это наши выборы. Всем нам приходится сталкиваться с трудными решениями в жизни. Иногда нужно выбирать между тем, что правильно, и тем, что легко. Помни, счастье можно найти даже в самые тёмные времена, если только не забыть включить свет."
        }
    ],
    "medium": [
        {"title": "Rain in the Park", "content": "She was walking in the park when it started raining.", "translation": "Она гуляла в парке, когда начался дождь."},
        {"title": "Lost for Words", "content": "He didn’t know what to say.", "translation": "Он не знал, что сказать."}
    ],
    "hard": [
        {"title": "Overcoming Challenges", "content": "Despite the challenges, she managed to finish the project on time.", "translation": "Несмотря на трудности, она смогла закончить проект вовремя."},
        {"title": "Scientific Discovery", "content": "The scientist conducted a series of experiments to prove his theory.", "translation": "Учёный провёл серию экспериментов, чтобы доказать свою теорию."}
    ]
}

# Команда /start с кнопкой
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Выбрать текст", callback_data="start_text_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я твой бот для изучения английского!",
        reply_markup=reply_markup
    )

# Начало выбора текстов
async def text_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="easy"),
         InlineKeyboardButton("Medium", callback_data="medium"),
         InlineKeyboardButton("Hard", callback_data="hard")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выбери уровень сложности:",
        reply_markup=reply_markup
    )
    return LEVEL

# Обработка выбора уровня
async def choose_level(update: Update, context):
    query = update.callback_query
    await query.answer()
    level = query.data

    if level in texts:
        context.user_data['level'] = level
        text_list = texts[level]
        keyboard = [[InlineKeyboardButton(text["title"], callback_data=str(i))] for i, text in enumerate(text_list)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Выбери текст:",
            reply_markup=reply_markup
        )
        return TEXT
    else:
        await query.edit_message_text("Что-то пошло не так. Попробуй снова.")
        return ConversationHandler.END

# Обработка выбора текста
async def choose_text(update: Update, context):
    query = update.callback_query
    await query.answer()
    text_idx = int(query.data)
    level = context.user_data['level']
    selected_text = texts[level][text_idx]
    context.user_data['selected_text'] = selected_text  # Сохраняем текст для дальнейших действий
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="back_to_level"),
         InlineKeyboardButton("Перевод", callback_data="show_translation"),
         InlineKeyboardButton("Выбор слов", callback_data="select_words")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Вот твой текст:\n\n{selected_text['content']}",
        reply_markup=reply_markup
    )
    return ACTION

# Обработка действий после выбора текста
async def handle_action(update: Update, context):
    query = update.callback_query
    await query.answer()
    action = query.data
    selected_text = context.user_data['selected_text']

    if action == "back_to_level":
        keyboard = [
            [InlineKeyboardButton("Easy", callback_data="easy"),
             InlineKeyboardButton("Medium", callback_data="medium"),
             InlineKeyboardButton("Hard", callback_data="hard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Выбери уровень сложности:",
            reply_markup=reply_markup
        )
        return LEVEL
    elif action == "show_translation":
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_to_text")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Перевод:\n\n{selected_text['translation']}",
            reply_markup=reply_markup
        )
        return ACTION  # Остаёмся в ACTION для обработки кнопки "Назад"
    elif action == "select_words":
        await query.edit_message_text(
            text=f"Выбранный текст:\n\n{selected_text['content']}\n\nВведи слова или фразы, которые хочешь выучить:"
        )
        return ACTION  # Оставляем в состоянии ACTION для ввода слов
    elif action == "back_to_text":
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_to_level"),
             InlineKeyboardButton("Перевод", callback_data="show_translation"),
             InlineKeyboardButton("Выбор слов", callback_data="select_words")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Вот твой текст:\n\n{selected_text['content']}",
            reply_markup=reply_markup
        )
        return ACTION
    return ConversationHandler.END

# Обработка ввода слов
async def save_words(update: Update, context):
    words = [word.strip() for word in update.message.text.split(",")]
    # Пока просто выводим слова, можно позже сохранить в базу данных
    await update.message.reply_text(f"Ты выбрал для изучения: {', '.join(words)}")
    return ConversationHandler.END

# Основная функция
def main():
    application = Application.builder().token("7887733782:AAGbZJXB5L2qf6o-7yLIIBNNia0qeSBIAa0").build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(text_menu, pattern="start_text_menu")],
        states={
            LEVEL: [CallbackQueryHandler(choose_level)],
            TEXT: [CallbackQueryHandler(choose_text)],
            ACTION: [
                CallbackQueryHandler(handle_action),
                MessageHandler(filters=None, callback=save_words)  # Обрабатываем ввод слов
            ]
        },
        fallbacks=[]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()