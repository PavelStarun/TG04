import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN, WEATHER_API_KEY
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
import keyboards as kb


bot = Bot(token=TOKEN)
dp = Dispatcher()


logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
        ''')

    conn.commit()
    conn.close()


init_db()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Привет!', reply_markup=kb.main)

@dp.message(Command("help"))
async def help(message: Message, state: FSMContext):
    await message.answer('Я бот для учета учеников школы. Вот мои команды', reply_markup=kb.menu)


@dp.message(F.text == "Привет")
async def hello(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}! Если нужна помощь нажми /help')

@dp.message(F.text == "Пока")
async def goodbye(message: Message):
    await message.answer(f'До свидания, {message.from_user.full_name}!')



@dp.message(Command("links"))
async def links(message: Message):
    await message.answer('Развлеки себя',reply_markup=kb.inline_menu)


@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
   await callback.answer("Новости подгружаются")
   await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())



@dp.message(Command("sign_up") or F.text == "📞 Записаться")
async def sign_up(message: Message, state: FSMContext):
    await message.answer("Привет, как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"{message.text}, сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком классе ты учишься?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def city(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
        (user_data['name'], user_data['age'], user_data['grade'])
    )
    conn.commit()
    conn.close()

    await message.answer(f"Студент {user_data['name']} с класса {user_data['grade']} добавлен в список.")
    await state.clear()


@dp.message(Command("all") or F.text == "🏠 Посмотреть список")
async def all_data(message: Message):
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    all_students = cur.fetchall()
    conn.close()

    if all_students:
        response = "Данные всех учеников:\n"
        for student in all_students:
            response += f"ID: {student[0]}, Имя: {student[1]}, Возраст: {student[2]}, Класс: {student[3]}\n"
        await message.answer(response)
    else:
        await message.answer("Нет данных учеников.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())