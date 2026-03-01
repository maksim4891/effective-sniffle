import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Включим логирование (чтобы видеть ошибки)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8531942383:AAFu4rifYUFqyK-inpt37g3U_zjyBHcNhOQ"  # Вставьте сюда токен от @BotFather

# Список каналов для проверки (username каналов или ID каналов)
# Можно использовать username (например: "@channel_name") или числовой ID
REQUIRED_CHANNELS = [
    "3397655252",  # Замените на ваши каналы
    "3605865013",
    "2153595243",
]

# Ссылки, которые бот будет выдавать после успешной проверки
REWARD_LINKS = [
    "https://t.me/+MTODS129dwtiYzBi",
    #"https://t.me/your_channel_5",
    #"https://t.me/your_channel_6",
]
# ===============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    
    # Проверяем подписку
    not_subscribed = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            # Получаем информацию о статусе участника в канале
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            
            # Если пользователь не подписан (статус left, kicked или banned)
            if member.status in ['left', 'kicked', 'banned']:
                not_subscribed.append(channel)
        except Exception as e:
            logger.error(f"Ошибка при проверке канала {channel}: {e}")
            # Если не можем проверить (бот не админ или канал не существует)
            not_subscribed.append(channel)
    
    if not not_subscribed:
        # Пользователь подписан на все каналы - выдаем ссылки
        links_text = "Спасибо за подписку! Вот ваши ссылки:\n\n"
        for i, link in enumerate(REWARD_LINKS, 1):
            links_text += f"{i}. {link}\n"
        
        await update.message.reply_text(links_text)
    else:
        # Пользователь не подписан - показываем кнопки для подписки
        keyboard = []
        for channel in not_subscribed:
            # Создаем кнопку для перехода на канал
            button = InlineKeyboardButton(
                text=f"Подписаться", 
                url=f"https://t.me/+z99KZL11SVE5NmJi"
            )
            keyboard.append([button])
        
        # Добавляем кнопку для повторной проверки
        keyboard.append([InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subscription")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Для получения ссылок необходимо подписаться на следующие каналы:",
            reply_markup=reply_markup
        )

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка подписки при нажатии на кнопку"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Проверяем подписку
    not_subscribed = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked', 'banned']:
                not_subscribed.append(channel)
        except Exception as e:
            logger.error(f"Ошибка при проверке канала {channel}: {e}")
            not_subscribed.append(channel)
    
    if not not_subscribed:
        # Успешно подписан - выдаем ссылки
        links_text = "Спасибо за подписку! Вот ваши ссылки:\n\n"
        for i, link in enumerate(REWARD_LINKS, 1):
            links_text += f"https://t.me/+MTODS129dwtiYzBi\n"
        
        await query.edit_message_text(links_text)
    else:
        # Всё еще не подписан
        await query.edit_message_text(
            "Вы ещё не подписались на все каналы.\n"
            "Пожалуйста, подпишитесь и нажмите кнопку еще раз."
        )
        # Можно вернуть клавиатуру с кнопками подписки
        # Для простоты просто показываем текст

def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(8518419152:AAGPzH55IICyIIFqpCcvZXXgm2ZfZntCLgU).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_subscription"))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
