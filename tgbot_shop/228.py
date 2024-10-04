#Импорт нужных библиотек
import telebot
import sqlite3
from telebot import types
from dotenv import dotenv_values

#Токен и конфиг бота
config=dotenv_values('.env')
bot=telebot.TeleBot(config.get('TOKEN'))

#Команда /start.Также конектим базу данных.
@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect(config.get('DB_NAME'))
    cursor = connect.cursor()

    us_id = message.chat.id
    cursor.execute(f"SELECT id FROM users WHERE id = {us_id}")
    all = cursor.fetchone()

    if all == None:
        usersss_id = message.chat.id
        balance = 25 #Деньга за регестрацию так сказать
        cursor.execute("INSERT INTO users (id, balance) VALUES(?, ?);", (usersss_id, balance))
        connect.commit()

 #Собственно меню которое вместе со стартом видит юзер
    markup=types.InlineKeyboardMarkup()
    Button1=(types.InlineKeyboardButton(text = 'Начать закуп', callback_data='menu'))
    Button2=(types.InlineKeyboardButton(text = '📝-Написать в поддержку', url='https://t.me/Akito_17'))
    Button3=(types.InlineKeyboardButton(text = '💎-Меню Средств', callback_data='menu_bal'))
    markup.row(Button1)
    markup.row(Button2,Button3)
    bot.send_message(message.chat.id, 'Привет!Ты попал в телеграм бота который продаст тебе скины и валюту из разных игр', reply_markup=markup)

#Действие после меню,а если конкретнее то выбрать категорию и вернуться в меню
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'menu')
def menu_os(callback_query: types.CallbackQuery):
    if callback_query.data == 'menu':
        markup=types.InlineKeyboardMarkup()
        Button4=(types.InlineKeyboardButton(text = '💳-Выбрать категорию', callback_data='categores'))
        Button13=(types.InlineKeyboardButton(text = '⚖️-История покупок', callback_data='history'))
        Button5=(types.InlineKeyboardButton(text = '⬅️-Назад', callback_data='back'))
        markup.row(Button4)
        markup.row(Button13,Button5)
        bot.send_message(callback_query.from_user.id,'Выберите действие!',reply_markup=markup)

#Меню баланса
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'menu_bal')
def menu_balance(callback_query: types.CallbackQuery):
    if callback_query.data == 'menu_bal':
        markup=types.InlineKeyboardMarkup()
        Button6=(types.InlineKeyboardButton(text = '💰-Мой баланс', callback_data='balance'))
        Button7=(types.InlineKeyboardButton(text = '💵-Пополнить баланс', callback_data='addbalnce'))
        Button8=(types.InlineKeyboardButton(text = '⬅️-Назад', callback_data='back'))
        markup.add(Button6,Button7,Button8)
        bot.send_message(callback_query.from_user.id,'Выберите действие!',reply_markup=markup)


#Надо бы теперь прописать кнопочки назад ибо они пока что не работают!!!
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'back')
def backs(callback_query: types.CallbackQuery):
    if callback_query.data == 'back':
            markup=types.InlineKeyboardMarkup()
            Button1=(types.InlineKeyboardButton(text = '💳-Начать закуп', callback_data='menu'))
            Button2=(types.InlineKeyboardButton(text = '📝-Написать в поддержку', url='https://t.me/Akito_17'))
            Button3=(types.InlineKeyboardButton(text = '💎-Меню Средств', callback_data='menu_bal'))
            markup.row(Button1)
            markup.row(Button2,Button3)
            bot.send_message(callback_query.from_user.id, 'Ты вернулся в меню!', reply_markup=markup)

#Собственно две категории скины и валюта(валюты не будет в данной версии кода однако его я буду дорабатывать)
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'categores')
def categore_os(callback_query: types.CallbackQuery):
    if callback_query.data == 'categores':
        markup=types.InlineKeyboardMarkup()
        Button11=(types.InlineKeyboardButton(text = 'Скины', callback_data='skins'))
        Button12=(types.InlineKeyboardButton(text = '*В разработке...*Валюта', callback_data='valuta'))
        Button5=(types.InlineKeyboardButton(text = '⬅️-Назад', callback_data='back'))
        markup.row(Button11,Button12)
        markup.row(Button5)
        bot.send_message(callback_query.from_user.id,'Выберите действие!',reply_markup=markup)

#Скины
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'skins')
def skin(callback_query: types.CallbackQuery):
    if callback_query.data == 'skins':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text = 'Arcana на Crystal Maiden', callback_data='buy_skin_1'))
        markup.add(types.InlineKeyboardButton(text = 'Arcana на Pudge', callback_data='buy_skin_2'))
        markup.add(types.InlineKeyboardButton(text = 'Arcana на Shadow Fiend', callback_data='buy_skin_3'))
        markup.add(types.InlineKeyboardButton(text = 'Arcana на Phantom Assasin', callback_data='buy_skin_4'))
        markup.add(types.InlineKeyboardButton(text = '⬅️-Назад', callback_data='buy_skin_5'))
        bot.send_message(callback_query.from_user.id,'Выберите скин!',reply_markup=markup)

#Тут пойдут несколько кнопок которые с бд выводят инфу о товаре и возможность купить)
@bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith( 'buy_skin'))
def hero_info(callback_query: types.CallbackQuery):
     if callback_query.data.startswith( 'buy_skin'):
        uesr_id=callback_query.message.from_user.id
        items_id = callback_query.data.split("_")[2]
       
        connect = sqlite3.connect(config.get('DB_NAME'))
        curs = connect.cursor()
        query=f'SELECT name, desc, price FROM items WHERE id={items_id}'
        curs.execute(query)
        data = curs.fetchone()
        item_name, item_desc, item_price= data
        # bot.send_photo(callback_query.message.chat.id, f"Название: {item_name}\nОписание: {item_desc}\nЦена: {item_price}")
        bot.send_message(callback_query.message.chat.id, f"Название: {item_name}\nОписание: {item_desc}\nЦена: {item_price}")

         
                

# @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'pud')
# def balancer(callback_query: types.CallbackQuery):
#      if callback_query.data == 'pud':
        

# @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'sf')
# def balancer(callback_query: types.CallbackQuery):
#      if callback_query.data == 'sf':
        

# @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'pha')
# def balancer(callback_query: types.CallbackQuery):
#      if callback_query.data == 'pha':
        

#Непосредственно нам нужно знать наш баланс.
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'balance')
def balancer(callback_query: types.CallbackQuery):
    if callback_query.data == 'balance':
        connect = sqlite3.connect(config.get('DB_NAME'))
        cursor = connect.cursor()
        id_u = callback_query.from_user.id
        cursor.execute(f'SELECT balance FROM users WHERE id = {id_u}')
        vsego = cursor.fetchone()
        if vsego:
            balance = vsego[0]
            bot.send_message(callback_query.message.chat.id, f'На данный момент у тебя столько копеек: {balance}')
        else:
            bot.send_message(callback_query.message.chat.id, 'Пользователя нет в базе данных,зарегестрируйся!')

#Функция пополнения и также само пополнение
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'addbalance')
def balancer(callback_query: types.CallbackQuery):
    if callback_query.data == 'addbalance':
        conn = sqlite3.connect(config.get('DB_NAME'))
        curs = conn.cursor()
        id_u = callback_query.from_user.id

        curs.execute(f'SELECT balance FROM users WHERE id = {id_u}')
        vsego = curs.fetchone()
        if vsego:
            balance = vsego[0]
            bot.send_message(callback_query.message.chat.id, f'Счёт: {balance}')
            bot.send_message(callback_query.message.chat.id, f'Введите сумму пополнения:')
            bot.register_next_step_handler(callback_query.message.chat.id, addmoney)
        else:
            bot.send_message(callback_query.message.chat.id, 'Такой юзер не найден')

def addmoney(message):
    try:
        summa_popolnaniya = int(message.text)
        id_u = message.from_user.id
        connect = sqlite3.connect(config.get('DB_NAME'))
        cursor = connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE id = {id_u}')
        vsego = cursor.fetchone()
        if vsego:
            balance = vsego[0]
            if summa_popolnaniya > 0 and summa_popolnaniya <= 5000:
                balance_add_money = balance + summa_popolnaniya
                cursor.execute(f'UPDATE users SET balance = {balance_add_money} WHERE id = {id_u}')
                connect.commit()
                connect.close()
                bot.send_message(message.chat.id, f'Текущий счёт: {balance_add_money}')
            elif summa_popolnaniya < 0:
                bot.send_message(message.chat.id, 'Слишком мало деняг')
            elif summa_popolnaniya > 5000:
                bot.send_message(message.chat.id, 'Слишком много деняг за один раз')           
        else:
            connect.close()
            bot.send_message(message.chat.id, 'Такого юзера не найдено он пропал куда-то')
    except ValueError:
        bot.send_message(message.chat.id, 'Данные буквы не цифры так что твой счёт такой же')


#Сделаем цикл с помощью которого бот работает постоянно
bot.polling(none_stop=True)