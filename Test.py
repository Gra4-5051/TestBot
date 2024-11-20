import telebot, re, pyodbc
from telebot import types
bot = telebot.TeleBot('5334003111:AAHu_zRzft82AlxIMkUo11QE7t8Gu5PxhOU')
grz = ''
FIO_customer = ''
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=GRA4;"
                      "Database=TEST;"
                      "UID=test;"
                      "PWD=12345")
cursor = cnxn.cursor()
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Какое ФИО у клиента?")
        bot.register_next_step_handler(message, get_customer)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_customer(message):
    global FIO_customer
    FIO_customer = message.text
    bot.send_message(message.from_user.id, 'Какой номер добавить? (Водить номер латиницей в формате A123BC123)')
    bot.register_next_step_handler(message, get_dat)

def get_dat(message):
    global grz
    regex = re.compile(r"^[ABEKMHOPCTYX]\d{3}[ABEKMHOPCTYX]{2}\d{2,3}")
    grz = message.text
    check_grz = regex.match(grz)
    if check_grz == None:
        bot.send_message(message.from_user.id, f'Не верный формат')
        get_customer(message)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'ФИО клиента: '+str(FIO_customer)+'\nНомер автомобиля: '+grz+'\nВерно?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
        cursor.execute('INSERT INTO TESTINGBOT (STR1TEST, STR2TEST) values(?, ?)', grz, FIO_customer)
        cnxn.commit()
    elif call.data == "no":
        keyboard = types.ReplyKeyboardMarkup()
        key_again = types.KeyboardButton('/reg')
        keyboard.add(key_again)
        question = 'Начнем с начала : )'
        bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)