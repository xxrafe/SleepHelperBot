import telebot
import requests
import datetime
from datetime import timedelta
from config import open_weather_token
from telebot import types
from time import sleep

bot = telebot.TeleBot('5989218895:AAEN6XlBADjGF0nn559G6twzn2xtcnl51Eg')
wakeup_count = 0
days_count = 0
time_wake1, time_wake2, time_sleep1, time_sleep2 = '', '', '', ''
city = ''


@bot.message_handler(commands=['start'])
def start(message):
    '''
    После команды: (/start) бот отправляет сообщение 'Привет 🙂'
    псоле чего у пользователя появляется кнопка: 'Привет! Кто ты? 😰'
    :param message: str
    :return: str
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    sup1 = types.KeyboardButton('Привет! Кто ты? 😰')
    markup.add(sup1)
    bot.send_message(message.chat.id, 'Привет 🙂', reply_markup=markup)


@bot.message_handler()
def start2(message):
    '''
    На сообщение 'Привет! Кто ты? 😰' бот отправляет сообщение:
    'Я бот, созданный для улучшения сна людей. Со временем ты узнаешь что именно я умею 😁'
    После чего для пользователя появляется кнопка: 'Давай приступим!' нажав на которую
    появлется кнопка 'Меню' и сообщение от бота: 'Откройте меню, нажав на кнопку ниже'
    После нажатия на кнопку 'Меню' в чате с бото закрепляются 8 кнопок с различными
    функциями:'Хочу уснуть в...,'Хочу встать в...,Погода,Информация о боте,Узнать свой id,
    фото о стадии сна и интересные факты о сне.
    Нажимая на какую-либо из кнопок пользователь отправляет сообщение соответсвующее названию кнопки,
    после чего через (elif message.text == (...)) бот начинает обращаться к написанным ниже фунциям и выводить
    пользователю различную информацию в соответствии с тем на какую кнопку нажал пользователь, то есть
    какой текст пользователь отправил боту.
    :param message: str
    :return: str
    '''
    if message.text == 'Привет! Кто ты? 😰':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        sup2 = types.KeyboardButton('Давай приступим!')
        markup.add(sup2)
        bot.send_message(message.chat.id,
                         'Я бот, созданный для улучшения сна людей. Со временем ты узнаешь что именно я умею 😁',
                         reply_markup=markup)

    elif message.text == 'Давай приступим!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        Button1 = types.KeyboardButton('Меню')
        markup.add(Button1)
        bot.send_message(message.chat.id, 'Откройте меню, нажав на кнопку ниже', reply_markup=markup)

    elif message.text == 'Меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        Button1 = types.KeyboardButton('Хочу уснуть в...')
        Button2 = types.KeyboardButton('Хочу встать в...')
        Button3 = types.KeyboardButton('Погода')
        Button4 = types.KeyboardButton('Информация о боте')
        Button5 = types.KeyboardButton('Статистика')
        Button6 = types.KeyboardButton('Узнать свой id')
        Button7 = types.KeyboardButton('фото о стадии сна')
        Button8 = types.KeyboardButton('интересные факты о сне')

        markup.add(Button1, Button2, Button3, Button4, Button5, Button6, Button7, Button8)
        bot.send_message(message.chat.id, 'Вы открыли Меню', reply_markup=markup)

    elif message.text == 'Информация о боте':
        bot.send_message(message.chat.id,
                         ' • хочу уснуть в.../хочу встать в... - пользователь записывает время в которое ему хотелось бы проснуться или же пойти спать, на основании полученных данных бот предлагает пользователю наилучшие варианты, основанные на фазах сна, каждая из которых длится ≈ 90 минут\n'
                         ' • Погода - вы указываете город, в котором вы живете, чтобы утром, когда вы просыпались вам отправлялась погода \n '
                         ' • Статистика - показывает сколько раз вы проснулись вовремя (ответили на утреннее сообщение) \n '
                         ' • Информация - показывает информацию о кнопках в меню\n'
                         ' • Узнай свой id - отправляет пользователю его id\n'
                         ' • Фото о стадиях и фазах сна - бот отправляет пользователю фото, кратко рассказывающую о различных фазах сна и чем они отличаются друг от друга\n'
                         ' • Интересные факты о сне - бот отправляет пользователю занимательные факты о сне')


    elif message.text == 'Хочу уснуть в...':
        bot.send_message(message.chat.id,
                         'Напишите время, в которое вы хотите пойти спать \n(напрмер: 12:37, 0:59, 23:08)')
        bot.register_next_step_handler(message, sleeptime)

    elif message.text == 'Хочу встать в...':
        bot.send_message(message.chat.id, 'Напишите время, в которое вы хотите встать \n(напрмер: 6:48, 8:00, 11:50)')
        bot.register_next_step_handler(message, wakeup)

    elif message.text == 'Узнать свой id':
        bot.send_message(message.chat.id, f"Ваш id: {message.from_user.id}")

    elif message.text == 'Погода':
        bot.send_message(message.chat.id, 'Напишите в каком городе вы хотите узнать погоду')
        bot.register_next_step_handler(message, get_weather)

    elif message.text == 'фото о стадии сна':
        photo = open('1.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif message.text == 'интересные факты о сне':
        bot.send_message(message.chat.id, '1. Люди проводят во сне треть своей жизни\n'
                                          '2. Официальный рекорд по времени пребывания без сна принадлежит Рэнди Гарднеру. В 1965 году, когда ему было 17 лет, он смог продержаться без сна и каких-либо стимуляторов 11 дней\n'
                                          '3. Недостаток сна ведет к снижению продолжительности жизни, а также другим проблемам, таким как переедание, ухудшение иммунитета, раздражительность и ухудшение внимания. А постоянный недостаток сна повышает шанс развития сердечно-сосудистых заболеваний\n'
                                          '4. Глухонемые люди иногда говорят во сне при помощи языка жестов\n'
                                          '5. До изобретения будильников в больших городах были люди, работа которых было будить людей по утрам. Они подходили с длинной такой палкой к окнам клиента и стучали по подоконнику, пока клиент не проснется. Но потом появились будильники и все эти люди остались без работы. То есть получается будильники погубили целую бизнес отрасль\n'
                                          '6.Невозможно чихнуть, пока вы спите\n'
                                          '7. Коала спит 20 часов в сутки\n'
                                          '8. Во время Первой мировой войны венгерский солдат Пауль Керн получил пулевое ранение в голову. Пулю вытащили, но Пауль потерял способность спать. Дело в том, что пуля уничтожила часть его нервной системы и часть лобной доли его головного мозга. Обычно такое ранение смертельно, но Паулю удалось выжить. Но это привело к тому, что до конца жизни он не чувствовал боли, утомление и не мог и не хотел спать. Он утверждал, что чувствует себя отлично, работал и даже завел семью. Так он прожил без сна 40 лет, пока не умер\n'
                                          '9. Люди, выросшие на черно-белом телевидении, видят в основном черно-белые сны\n'
                                          '10. В древней Греции сны считались посланиями богов\n'
                                          '11. Около 10% -50% детей в возрасте от 3 до 6 лет испытывают ночные кошмары')

    elif message.text == 'Статистика':
        bot.send_message(message.chat.id, f'Вы вовремя проснулись {wakeup_count} дней из {days_count}')


def get_weather(message):
    '''
    Выводит погоду в городе, выбранном пользователем
    :param message: str
    :return: str
    '''
    city = message.text

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода..."

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        bot.send_message(message.chat.id, f"---{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---\n"
                                          f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                          f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                          f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                          f"Хорошего дня!")

    except Exception as ex:
        bot.send_message(message.chat.id, "Проверьте название города")


def wakeup(message):
    '''
    В функцию передается время в котрое пользователь хотел бы пойти спать и на основе фаз сна
    пользователю предлагаются лучшие варианты для того что бы уснуть (каждая из фаз сна длится
    примерно 90 минут, конкретнее можно узнать вызвав каманду 'фото' в меню)
    :param message: str
    :return str
    '''
    s = str(message.text)
    s = prov(s)
    x = s.split(':')
    if (x[0].isdigit() == True) and (x[1].isdigit() == True):
        if (int(x[0]) >= 0) and (int(x[0]) <= 23) and (int(x[1]) >= 0) and (int(x[1]) <= 59):
            w = timedelta(hours=int(x[0]), minutes=int(x[1]))
            q = str(w - timedelta(hours=6))

            if len(q) > 12:
                q = q[6:]
            d = str(w - timedelta(hours=7, minutes=30))

            if len(d) > 12:
                d = d[6:]
            p = str(w - timedelta(hours=9))

            if len(p) > 12:
                p = p[6:]
            bot.send_message(message.chat.id, 'Если вы хотите проснуться в ' + s + ', то вам стоит лечь в: \n' + check(q[:-3]) + '\n' + check(d[:-3]) + '\n' + check(p[:-3]))
        else:
            bot.send_message(message.chat.id, 'Время введено не коректно, повторите попытку')
    else:
        bot.send_message(message.chat.id, 'Введеное вами значение не является числом, повторите попытку')

def sleeptime(message):
    '''
    В функцию передается время в котрое пользователь хотел бы проснуться и на основе фаз сна
    пользователю предлагаются лучшие варианты для того что бы проснуться (каждая из фаз сна длится
    примерно 90 минут, конкретнее можно узнать вызвав каманду 'фото' в меню)
    :param message:
    :return: str
    '''
    s = str(message.text)
    s = prov(s)
    time_sleep1 = s
    x = s.split(':')
    if (x[0].isdigit() == True) and (x[1].isdigit() == True):
        if (int(x[0]) >= 0) and (int(x[0]) <= 23) and (int(x[1]) >= 0) and (int(x[1]) <= 59):
            w = timedelta(hours=int(x[0]), minutes=int(x[1]))
            q = str(w + timedelta(hours=6))
            if len(q) > 12:
                q = q[6:]
            d = str(w + timedelta(hours=7, minutes=30))

            if len(d) > 12:
                d = d[6:]
            p = str(w + timedelta(hours=9))

            if len(p) > 12:
                p = p[6:]
            bot.send_message(message.chat.id,
                             'Если вы хотите лечь в ' + s + ', то лучшим временем что бы проснуться бeдует: \n' + check(
                                 q[:-3]) + '\n' + (check(d[:-3]) + '\n' + check(p[:-3])))
            bot.register_next_step_handler(message, save_time_wake)
            bot.send_message(message.chat.id, time_wake1)
            alarm(message, time_sleep1, time_wake1)
            bot.send_message(message.chat.id, 'Ваше время сохранено!')
        else:
            bot.send_message(message.chat.id, 'Время введено не коректно, повторите попытку')
    else:
        bot.send_message(message.chat.id, 'Введеное вами значение не является числом, повторите попытку')


def check(s):
    '''
    Проверяет: если первый символ строки ','
    тогда функция возвращает строку без первого сивола
    то есть без ','
    Если же первым символом ',' не является,
    то возвращает стоку и том же виде, какой она и была
    передана в функцию
    :param s: str
    :return: str
    '''
    if s[0] == ',':
        return s[1:]
    else:
        return s


def prov(s):
    '''
    Если в строке не встречается ':'
    тогда в конец строки добавляется '345'
    Если же ':' есть в строке, которую передают в функцию
    тогда функция возвращает строку, переданную в нее
    :param s: str
    :return: str
    '''
    if ':' in s:
        return s
    elif ':' not in s:
        s = s + ':34'


def save_time_wake(message):
    '''
    сохраняет время пробуждения пользователя
    :param message: str
    :return: str
    '''
    global time_wake1
    time_wake1 = message.text


def save_time_sleep(message):
    '''
    сохраняет время когда пользователь идет спать
    :param message: str
    :return: str
    '''
    global time_sleep2
    time_sleep2 = message.text


def alarm(message, time_sleep, time_wake):
    '''
    аналагбудильника: отправляет сообщение пользователю, когда ему нужно вставать:'Вам пора просыпаться!'
    а когда ложиться: 'Вам пора ложиться спать!'
    :param message: str
    :param time_sleep: str
    :param time_wake: str
    :return: str
    '''
    markup = types.ReplyKeyboardMarkup()
    Button = types.KeyboardButton(text='Я проснулся!')
    markup.add(Button)
    while True:
        time_now = datetime.datetime.now()
        if (str(time_now.hour) == time_sleep[:2]) and (str(time_now.minute) == time_sleep[-2:]):
            bot.send_message(message.chat.id, 'Вам пора ложиться спать!')
            break
    while True:
        if (str(time_now.hour) == time_wake[:2]) and (str(time_now.minute) == time_wake[-2:]):
            bot.send_message(message.chat.id, 'Вам пора просыпаться!', reply_markup=markup)
            sleep(60 * 5)
            bot.register_next_step_handler(message.chat.id, wakeup_answer)
            break


def wakeup_answer(message):
    '''
    отвечает пользователю на утреннее сообщение: 'Доброе утро!\nВот погода на сегодняшний день:'
    если пользователь пишет: 'Я проснулся!'
    и пишет  'Доброе утро!, к сожалению вы не проснулись 😔\nВот погода на сегодняшний день:'
    если пользователь не ответил на сообщение
    в обоих случаях отправляет погоду пользователю
    :param message: str
    :return: str
    '''
    global days_count, wakeup_count, city
    if message.text == 'Я проснулся!':
        bot.send_message(message.chat.id, 'Доброе утро!\nВот погода на сегодняшний день:')
        wakeup_count += 1
    else:
        bot.send_message(message.chat.id,
                         'Доброе утро!, к сожалению вы не проснулись 😔\nВот погода на сегодняшний день:')
    days_count += 1
    get_weather(city)


bot.polling(none_stop=True)