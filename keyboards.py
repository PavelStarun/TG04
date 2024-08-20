from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/links")],
    [KeyboardButton(text="📞 Записаться"), KeyboardButton(text="🏠 Посмотреть список")],
], resize_keyboard=True)


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет")],
    [KeyboardButton(text="Пока")],
], resize_keyboard=True)


inline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/watch?v=f9VbU_pCh8w")],
    [InlineKeyboardButton(text="Музыка", url="https://www.youtube.com/watch?v=1NrPcrWaMLo")],
    [InlineKeyboardButton(text="Новости", callback_data='news')],
])




test = ["Новости погоды", "Новости спорта", "Новости"]

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   keyboard.add(InlineKeyboardButton(text="Новости погоды", url="https://www.gismeteo.by/news/"))
   keyboard.add(InlineKeyboardButton(text="Новости спорта", url="https://www.championat.com/news/1.html"))
   keyboard.add(InlineKeyboardButton(text="Новости", url="https://myfin.by/article/zhizn/v-novoj-borovoj-otkrylas-skola-talantov-za-20-mln-smotrim-cto-vnutri-31780"))
   keyboard.add(InlineKeyboardButton(text="Новость о школе", url="https://myfin.by/article/zhizn/v-novoj-borovoj-otkrylas-skola-talantov-za-20-mln-smotrim-cto-vnutri-31780"))
   return keyboard.adjust(2).as_markup()

