from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove 
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sqlite3
import datetime

date_t = datetime.datetime.today()

date_t = date_t.strftime("%d.%m.%Y (%H:%M)")

db = sqlite3.connect('tasks.sqlite')

c = db.cursor()

c.execute("""DROP TABLE tasks""")

c.execute("""CREATE TABLE tasks (
    id integer primary key autoincrement,
    fullname varchar,
    chin varchar,
    task varchar,
    status varchar,
    corpus varchar,
    date varchar,
    usid integer
)""")

TOKEN = '5763371808:AAHb57W1PDdQ5KvevvkESnU_in0Yy0Ed98M'

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb.add(KeyboardButton('Добавить задачу'))
kb.add(KeyboardButton('Посмотреть мои задачи'))

kbc = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kbc.add(KeyboardButton('1')).insert(KeyboardButton('2')).insert(KeyboardButton('3'))

kbs = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kbs.add(KeyboardButton('Ожидает выполнения')).insert(KeyboardButton('В работе')).insert(KeyboardButton('Выполнена'))

class FSMTask(StatesGroup):
    add_t = State()
    add_c = State()

class FSMUpdate(StatesGroup):
    up_t = State()
    up_s = State()

class FSMChin(StatesGroup):
    add_chin = State()

# class FSMStatus(StatesGroup):

chin = 'unknown'

@dp.message_handler(commands=['start'], state=None)
async def pro(message: types.Message):

    await FSMChin.add_chin.set()
    await message.answer("Введите должность")

@dp.message_handler(state=FSMChin.add_chin)
async def pro_n(message: types.Message, state: FSMContext):
    global chin

    await state.update_data(chin=message.text)

    data_ch = await state.get_data()

    chin = message.text

    # c.execute("INSERT INTO tasks (chin) VALUES (?)", (message.text,))
    # db.commit()

    await state.finish()
    await message.answer("Выберите действие", reply_markup=kb)


# Добавление задачи


@dp.message_handler(Text('Добавить задачу'), state=None)
async def add_task(message: types.Message):

    await FSMTask.add_t.set()
    await message.answer('Введите задачу', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=FSMTask.add_t)
async def add_task_n(message: types.Message, state: FSMContext):

    await state.update_data(task=message.text)

    await FSMTask.next()
    await message.answer('Введите номер корпуса', reply_markup=kbc)

@dp.message_handler(state=FSMTask.add_c)
async def add_task_c(message: types.Message, state: FSMContext):
    await state.update_data(corpus=message.text)

    data_t = await state.get_data()

    c.execute("INSERT INTO tasks (fullname, chin, task, status, corpus, date, usid) VALUES(?, ?, ?, 'Ожидает выполнения', ?, ?, ?)", (message.from_user.username, chin, data_t['task'], data_t['corpus'], date_t, message.from_user.id))
    db.commit()

    await state.finish()
    await message.answer('Задача добавлена', reply_markup=kb)


# Обновление статуса


@dp.message_handler(commands=['update'])
async def update_task(message: types.Message):
    await message.answer('Введите ID задачи')

    await FSMUpdate.up_t.set()


@dp.message_handler(state=FSMUpdate.up_t)
async def update_task_status(message: types.Message, state: FSMContext):
    
    await state.update_data(id=message.text)
    await message.answer('Введите статус', reply_markup=kbs)

    await FSMUpdate.next()

@dp.message_handler(state=FSMUpdate.up_s)
async def update_task_status_name(message: types.Message, state:FSMContext):
    await state.update_data(status=message.text)
    await message.answer('Статус обновлен', reply_markup=kb)
    data = await state.get_data()

    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], data['id']))
    db.commit()

    c.execute("SELECT * FROM tasks WHERE id = ?", (data['id']))
    items = c.fetchall()
    for el in items:
        await bot.send_message(chat_id=el[7], text=f"""
        <s>📋</s>
<b> Задание: </b> {el[2]} 
<b> Корпус: </b> {el[4]}
<b> Статус: </b> {el[3]}""", parse_mode='HTML')

    await state.finish()


# Вывод всех заданий


@dp.message_handler(commands=['show'])
async def show_task(message: types.Message):
    c.execute("SELECT * FROM tasks")
    items = c.fetchall()
    for el in items:
        await message.answer(f"""
        <s>📋</s>
<b> ID: </b> {el[0]} 
<b> Имя: </b> {el[1]}
<b> Должность: </b> {el[2]}
<b> Задание: </b> {el[3]} 
<b> Категория: </b> {el[5]}
<b> Статус: </b> {el[4]}
<b> Дата: </b> {el[6]}""", parse_mode='HTML')


# Вывод заданий пользователя

@dp.message_handler(Text('Посмотреть мои задачи'))
async def show_my_tasks(message: types.Message):
    cc = message.from_user.id
    c.execute("SELECT * FROM tasks WHERE usid = ?", [(message.from_user.id)])
    items = c.fetchall()
    for el in items:
        await message.answer(f"""
        <s>📋</s>
<b> Задание: </b> {el[3]} 
<b> Статус </b> {el[4]}""", parse_mode='HTML')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

db.close()