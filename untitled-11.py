from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "8455830105:AAE9U4tFswn4ZaWyYnMny58u2PctnJ_Kdew"

CITIES = {
    "Торжок": {...},   # ← вставь словари отсюда
    "Удомля": {...},
    "Старица": {...},
    "Осташков": {...},
    "Вышний Волочёк": {...}
}


# --- Главное меню ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐ Рекомендуемый маршрут", callback_data="recommended")],
        [InlineKeyboardButton("🎲 Случайный маршрут", callback_data="random")],
        [InlineKeyboardButton("🏙 Выбрать город", callback_data="choose_city")]
    ]
    await update.message.reply_text("Спасибо, что выбрали наш бот! Выберите подходящий Вам вариант из списка и получите маршрут своей мечты:", reply_markup=InlineKeyboardMarkup(keyboard))


# --- Обработка кнопок ---
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # 1. Случайный маршрут
    if data == "random":
        route = random.sample(list(CITIES.keys()), 5)
        text = "🎲 *Случайный маршрут:*\n" + " → ".join(route)
        await query.edit_message_text(text, parse_mode="Markdown")
        return

    # 2. Рекомендуемый маршрут
    if data == "recommended":
        text = "⭐ *Рекомендуемый маршрут:*\nТоржок → Осташков → Вышний Волочёк"
        await query.edit_message_text(text, parse_mode="Markdown")
        return

    # 3. Выбрать город — вывод списка
    if data == "choose_city":
        keyboard = [[InlineKeyboardButton(name, callback_data=f"city:{name}")] for name in CITIES]
        keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back_to_menu")])
        await query.edit_message_text("Выберите город:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # 4. Карточка города
    if data.startswith("city:"):
        city = data.split(":")[1]
        keyboard = [
            [InlineKeyboardButton("🏛 Достопримечательности", callback_data=f"sights:{city}")],
            [InlineKeyboardButton("🍽 Где поесть", callback_data=f"food:{city}")],
            [InlineKeyboardButton("🚌 Как добраться", callback_data=f"transport:{city}")],
            [InlineKeyboardButton("⬅ Назад", callback_data="choose_city")]
        ]
        await query.edit_message_text(f"Город: *{city}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    # 5. Внутренние разделы карточки города
    for section in ("sights", "food", "transport"):
        if data.startswith(section):
            city = data.split(":")[1]
            text = CITIES[city][section]
            keyboard = [
                [InlineKeyboardButton("⬅ Назад", callback_data=f"city:{city}")]
            ]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

    # 6. Возврат в главное меню
    if data == "back_to_menu":
        await start(update, context)
        return


# --- Запуск приложения ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Бот запущен!")
app.run_polling()
