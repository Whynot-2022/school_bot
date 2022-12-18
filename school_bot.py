from string import Template
import telebot
import sqlite3
from datetime import datetime
import time
from threading import Thread
import schedule
from PIL import Image, ImageDraw, ImageFont
db = 'test_whynot.db'
connection_obj = sqlite3.connect(db, check_same_thread=False)
cursor_obj = connection_obj.cursor()

markup = telebot.types.ReplyKeyboardMarkup(None, True)
item1 = telebot.types.KeyboardButton('Забыл карту')
item2 = telebot.types.KeyboardButton('Потерял карту')
markup.add(item1)
markup.add(item2)

user_dict = {}
fff = set()

tconv = lambda x: time.strftime("%H:%M", time.localtime(x))  # Конвертация даты в читабельный вид

bot = telebot.TeleBot("TOKEN")


class User:
    def __init__(self, city):
        self.city = city
        keys = ['first', 'last_name', 'patronymic', 'clas', 'teacher', 'Who_teacher', 'id']
        for key in keys:
            self.key = None


now = datetime.now()
current_time = now.strftime("%H:%M")


def canteen_sending():  # Отправка в 11:00 (зав столовой)
    id = str()
    while True:
        connection_obj = sqlite3.connect(db, check_same_thread=False)
        cursor_obj = connection_obj.cursor()
        search_teacher = ''.join('\n'.join((' '.join(v) for v in cursor_obj.execute(
            "SELECT ID FROM TEST WHERE Who_teacher = 11").fetchall())))
        # connection_obj.close()
        if bool(search_teacher):
            id = search_teacher
            break
    connection_obj = sqlite3.connect(db, check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    children_lost = str('\n'.join(str(' '.join(v)) for v in cursor_obj.execute(
        "SELECT Last_Name ,First_Name, Patronymic, Class FROM TEST WHERE LOST = 'Потерял'").fetchall()))
    amount_children_lost = len(children_lost.split('\n'))
    children_forgot = str('\n'.join(str(' '.join(v)) for v in cursor_obj.execute(
        "SELECT Last_Name ,First_Name, Patronymic, Class FROM TEST WHERE LOST = 'Забыл'").fetchall()))
    amount_children_forgot = len(children_forgot.split('\n'))
    text = str()
    if len(children_lost) != 0:
        text = text + f'Потеряли карту: {amount_children_lost} человек\n' + children_lost + '\n\n'
    else:
        text = text + 'Потеряли карту: 0 человек\n\n'
    if len(children_forgot) != 0:
        text = text + f'Забыли карту: {amount_children_forgot} человек\n' + children_forgot + '\n'
    else:
        text = text + 'Забыли карту: 0 человек' + '\n'
    bot.send_message(id, text)


def teacher():  # Отправка в 11:00 (учитель)
    search_teacher1 = str()
    while True:
        connection_obj = sqlite3.connect(db, check_same_thread=False)
        cursor_obj = connection_obj.cursor()
        search_teacher = ''.join('\n'.join((' '.join(v) for v in cursor_obj.execute(
            "SELECT First_Name, Last_Name, Patronymic, Class, ID FROM TEST WHERE Who_teacher = 1").fetchall())))
        if bool(search_teacher):
            search_teacher1 = search_teacher
            break
    for one_teacher in search_teacher1.split('\n'):
        id = one_teacher.split()[4]
        clas = one_teacher.split()[3]
        name_teacher = ' '.join(one_teacher.split()[0:3])
        text = str()
        for k in clas.split(','):
            children_forgot = '\n'.join(' '.join(v) for v in cursor_obj.execute(
                f"SELECT Last_Name ,First_Name, Patronymic FROM TEST WHERE Who_teacher = 0 AND Teacher = '{name_teacher}' AND Class = '{k}' AND Lost = 'Забыл'").fetchall())
            children_lost = '\n'.join(' '.join(v) for v in cursor_obj.execute(
                f"SELECT Last_Name ,First_Name, Patronymic FROM TEST WHERE Who_teacher = 0 AND Teacher = '{name_teacher}' AND Class = '{k}' AND Lost = 'Потерял'").fetchall())
            text = text + 'Забывшие карту:\n' + children_forgot + '\n\nПотерявшие карту:\n' + children_lost + '\n\n' + 'Опоздавшие на урок (в [  ] на какой урок):\n'
            for b in cursor_obj.execute(
                    f"SELECT First_Name, Last_Name, Patronymic, Time FROM TEST WHERE Who_teacher = 0 AND Teacher = '{name_teacher}' AND Class = '{k}'").fetchall():
                try:
                    time_hour = b[3].split(':')[0]
                    time_minute = b[3].split(':')[1]
                    if datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                              16, 25, 1,
                                                                                                              1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4][5][6][7][8][9]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                15, 35,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4][5][6][7][8]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                14, 35,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4][5][6][7]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                13, 35,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4][5][6]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                12, 20,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4][5]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                11, 35,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3][4]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                10, 35,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2][3]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                9, 30,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1][2]\n'
                    elif datetime(1, 1, 1, int(time_hour), int(time_minute), 1, 1).strftime("%H:%M") > datetime(1, 1, 1,
                                                                                                                8, 30,
                                                                                                                1,
                                                                                                                1).strftime(
                        "%H:%M"):
                        text = text + ' '.join(b[0:3]) + ' [1]\n'
                    else:
                        text = text + ' '.join(b[0:3]) + '\n'
                except:
                    text = text
            bot.send_message(id, text)


def clear():
    connection_obj = sqlite3.connect(db, check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute('UPDATE TEST SET Time = null , Lost = null WHERE Who_teacher = 0')
    connection_obj.commit()
    connection_obj.close()


class Time(Thread):  # Новый поток для отправки учителям и отв по питанию в 11:00
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        schedule.every().day.at("10:50").do(teacher)
        schedule.every().day.at("10:50").do(canteen_sending)
        schedule.every().day.at("00:00").do(clear)
        while True:
            schedule.run_pending()


def db_table_val(id, name, surname, patronymic, clas, teacher, Who_teacher, Lost, Time):
    connection_obj = sqlite3.connect(db, check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(
        'INSERT INTO TEST(ID, First_Name, Last_Name, Patronymic, Class, Teacher, Who_teacher, Lost, Time) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (id, name, surname, patronymic, clas, teacher, Who_teacher, Lost, Time))
    connection_obj.commit()
    connection_obj.close()


def canteen(message):  # добавление ответ. за питание
    if not bool(cursor_obj.execute(
            f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND (Who_teacher = 1 OR Who_teacher = 11 OR Who_teacher = 0)").fetchall()):
        db_table_val(id=message.chat.id, name='Столовая', surname='0', patronymic='0', clas='0', teacher='0',
                     Who_teacher='11', Lost=None, Time=None)
        bot.send_message(message.chat.id, 'Вы добавились как ответ. за питание')
        bot.send_message(message.chat.id, 'Вы можете посмотреть кто забыл и потерял карту командой /lost')
    elif bool(cursor_obj.execute(f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND Who_teacher = 11").fetchall()):
        bot.send_message(message.chat.id, 'Вы можете посмотреть кто забыл и потерял карту командой /lost')


def add(message):  # добавление учителя в бот
    if not bool(cursor_obj.execute(
            f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND (Who_teacher = 1 OR Who_teacher = 11 OR Who_teacher = 0)").fetchall()):
        bot.send_message(message.chat.id, 'Заполните документ')
        msg = bot.send_message(message.chat.id,
                               'Напишите ФИО (Польностью)+ Класс в котором Вы классный руководитель\n\nПример:\nИванов Иван Иванович 10З')
        bot.register_next_step_handler(msg, add_teacher)
    elif bool(cursor_obj.execute(f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND Who_teacher = 1").fetchall()):
        bot.send_message(message.chat.id,
                         'Вы можете посмотреть кто забыл карту, кто потерял карту, кто опоздал на урок командой /teacher')
    else:
        bot.send_message(message.chat.id, 'Вы не учитель')
        msg = bot.send_message(message.chat.id, 'Введите ключ')
        bot.register_next_step_handler(msg, registration)


def add_teacher(message):
    us_id = message.chat.id
    us_name = message.text.split()[0]
    us_sname = message.text.split()[1]
    us_patronymic = message.text.split()[2]
    us_clas = message.text.split()[3]
    us_teacher = 0
    who = 1
    db_table_val(id=us_id, name=us_name, surname=us_sname, patronymic=us_patronymic, clas=us_clas, teacher=us_teacher,
                 Who_teacher=who, Lost=None, Time=None)
    bot.send_message(us_id, 'Вы добавлены как учитель')
    bot.send_message(message.chat.id,
                     'Вы можете посмотреть кто забыл карту, кто потерял карту, кто опоздал на урок командой /teacher')


def registration(message):
    if message.text == '0':
        start_student(message)
    elif message.text == 'imj9KzyGj5:m9T':
        add(message)
    elif message.text == 'Gz9gZFTKZT+gjC':
        canteen(message)
    else:
        msg = bot.send_message(message.chat.id, 'Введите правильный ключ')
        bot.register_next_step_handler(msg, registration)


def start_student(message):
    if not bool(cursor_obj.execute(
            f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND (Who_teacher = 1 OR Who_teacher = 11 OR Who_teacher = 0)").fetchall()):
        bot.send_message(message.chat.id, 'Заполните документ')
        msg = bot.send_message(message.chat.id, 'Имя?', )
        bot.register_next_step_handler(msg, Name)
    elif bool(cursor_obj.execute(f"SELECT ID FROM TEST WHERE ID = {message.chat.id} AND Who_teacher = 0").fetchall()):
        bot.send_message(message.chat.id, 'Хорошего пользования')
        msg = bot.send_message(message.chat.id, 'Выберите функцию', reply_markup=markup)
        bot.register_next_step_handler(msg, usually)
    else:
        bot.send_message(message.chat.id, 'Вы не ученик')
        msg = bot.send_message(message.chat.id, 'Введите ключ')
        bot.register_next_step_handler(msg, registration)


def Name(message):
    chat_id = message.chat.id
    user_dict[chat_id] = User(message.text)
    user = user_dict[chat_id]
    user.first = message.text
    msg = bot.send_message(message.chat.id, 'Фамилия?')
    bot.register_next_step_handler(msg, Patronymic)


def Patronymic(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.last_name = message.text
    msg = bot.send_message(message.chat.id, 'Отчество?')
    bot.register_next_step_handler(msg, last__name)


def last__name(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.patronymic = message.text
    msg = bot.send_message(message.chat.id, 'Класс(номер + буква)?\nПример:\n10P')
    bot.register_next_step_handler(msg, _clas)


def _clas(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.clas = message.text
    msg = bot.send_message(message.chat.id, 'Кто твой классный руководитель?\nФИО')
    bot.register_next_step_handler(msg, who_teacher)


def who_teacher(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.teacher = message.text
    d = getRegData(user, message.chat.id)
    send(d)
    start_student(message)


def send(list):
    us_id = list.split('\n')[6]
    us_name = list.split('\n')[0]
    us_sname = list.split('\n')[1]
    us_patronymic = list.split('\n')[2]
    us_clas = list.split('\n')[3]
    us_teacher = list.split('\n')[4]
    who = list.split('\n')[5]
    db_table_val(id=us_id, name=us_name, surname=us_sname, patronymic=us_patronymic, clas=us_clas, teacher=us_teacher,
                 Who_teacher=who, Lost=None, Time=None)
    bot.send_message(us_id, 'Вы добавлены как ученик')


def getRegData(user, name):
    t = Template(
        '$first_name\n$last_name\n$patronymic\n$clas\n$teacher\n$Who_teacher\n$id')
    return t.substitute({
        'first_name': user.first,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
        'clas': user.clas,
        'teacher': user.teacher,
        'Who_teacher': 0,
        'id': name
    })

@bot.message_handler(commands=['start'])
def authorization(message):
    msg = bot.send_message(message.chat.id, 'Введите ключ')
    bot.register_next_step_handler(msg, registration)

@bot.message_handler(commands=['teacher'])  # для учителя. Можно смотреть
def lost_and_forgot_teacher(message):
    teacher = ''.join('\n'.join((' '.join(v) for v in cursor_obj.execute(
        f"SELECT First_Name, Last_Name, Patronymic, Class, ID FROM TEST WHERE Who_teacher = 1 AND ID = '{message.chat.id}'").fetchall())))
    id = teacher.split()[4]
    clas = teacher.split()[3]
    name_teacher = ' '.join(teacher.split()[0:3])
    text = str()

    children_forgot = '\n'.join(' '.join(v) for v in cursor_obj.execute(
            f"SELECT Last_Name, First_Name, Patronymic FROM TEST WHERE Who_teacher = 0 AND Teacher = '{name_teacher}' AND Class = '{clas}' AND Lost = 'Забыл'").fetchall())
    children_lost = '\n'.join(' '.join(v) for v in cursor_obj.execute(
            f"SELECT Last_Name, First_Name, Patronymic FROM TEST WHERE Who_teacher = 0 AND Teacher = '{name_teacher}' AND Class = '{clas}' AND Lost = 'Потерял'").fetchall())
    text = text + 'Забывшие карту:\n' + children_forgot + '\n\nПотерявшие карту:\n' + children_lost + '\n\n'
        # if datetime(1,1,1,v[3].split(',')[0],v[3].split(',')[1],1,1).strftime("%H:%M") < datetime(1,1,1,8,30,1,1).strftime("%H:%M"))
    bot.send_message(id, text)


@bot.message_handler(commands=['lost'])  # для заведущей столовой
def lost_admin(message):
    connection_obj = sqlite3.connect(db, check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    children_lost = str('\n'.join(str(' '.join(v)) for v in cursor_obj.execute(
        "SELECT Last_Name, First_Name, Patronymic, Class FROM TEST WHERE LOST = 'Потерял'").fetchall()))
    amount_children_lost = len(children_lost.split('\n'))
    children_forgot = str('\n'.join(str(' '.join(v)) for v in cursor_obj.execute(
        "SELECT Last_Name, First_Name, Patronymic, Class FROM TEST WHERE LOST = 'Забыл'").fetchall()))
    amount_children_forgot = len(children_forgot.split('\n'))
    text = str()
    if len(children_lost) != 0:
        text = text + f'Потеряли карту: {amount_children_lost} человек\n' + children_lost + '\n\n'
    else:
        text = text + 'Потеряли карту: 0 человек\n\n'
    if len(children_forgot) != 0:
        text = text + f'Забыли карту: {amount_children_forgot} человек\n' + children_forgot + '\n'
    else:
        text = text + 'Забыли карту: 0 человек' + '\n'
    bot.send_message(message.chat.id, text)



@bot.message_handler(content_types=["text"])
def usually(message):
    connection_obj = sqlite3.connect(db, check_same_thread=False)
    cursor_obj = connection_obj.cursor()

    if message.text == 'Забыл карту':
        bot.send_message(message.chat.id,'Я надеюсь, больше ничего не забыл(а)?😅😅😅')
        bot.send_message(message.chat.id,'Можешь проходить.\nТолько покажи карточку со временем входа охраннику 👇')
        img = Image.new("RGB", (600, 600), (0, 0, 0))
        d = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('d9464-arkhip_font.ttf', 180)
        d.text((10, 200), tconv(message.date), fill=(255, 255, 255), font=myFont)
        bot.send_photo(message.chat.id, img)
        cursor_obj.execute('UPDATE TEST SET LOST = ?, Time = ? WHERE Who_teacher = 0 AND ID = ?', (
            "Забыл", str(tconv(message.date)), int(message.chat.id)))  # str(datetime.now().strftime("%H:%M"))
        connection_obj.commit()
        connection_obj.close()

    elif message.text == 'Потерял карту':
        bot.send_message(message.chat.id,'Как так???😳😳😳')
        bot.send_message(message.chat.id,'Можешь проходить.\nТолько покажи карточку со временем входа охраннику 👇')
        img = Image.new("RGB", (600, 600), (0, 0, 0))
        d = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('d9464-arkhip_font.ttf', 180)
        d.text((10, 200), tconv(message.date), fill=(255, 255, 255), font=myFont)
        bot.send_photo(message.chat.id, img)
        cursor_obj.execute('UPDATE TEST SET LOST = ?, Time = ? WHERE Who_teacher = 0 AND ID = ?',
                           ("Потерял", str(tconv(message.date)), int(message.chat.id)))
        connection_obj.commit()
        connection_obj.close()
    else:
        bot.send_message(message.chat.id,'Вы ввели что-то другое')
        authorization(message)

while True:
    try:
        Time().start()
        bot.polling(none_stop=True)
    except:
        print('Error. Restarting...')
