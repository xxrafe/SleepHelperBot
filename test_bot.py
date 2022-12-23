# import pytest
# from pytest_mock import mocker
# import telebot
# from telebot import types
# from unittest.mock import Mock
# import Sleep_helper_bot
#
#
# def test_start(mocker):
#     telebot.TeleBot.send_message = Mock()
#     types.ReplyKeyboardMarkup = Mock()
#     types.KeyboardButton = Mock()
#     message = Mock()
#     message.text = "/start"
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     sup1 = types.KeyboardButton('Привет! Кто ты? 😰')
#     markup.add(sup1)
#     Sleep_helper_bot.start(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, "Привет 🙂", reply_markup=markup)
#
#
# def test_start2_hello(mocker):
#     telebot.TeleBot.send_message = Mock()
#     types.ReplyKeyboardMarkup = Mock()
#     types.KeyboardButton = Mock()
#     message = Mock()
#     message.text = "Привет! Кто ты? 😰"
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     sup2 = types.KeyboardButton('Давай приступим!')
#     markup.add(sup2)
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id,
#                          'Я бот, созданный для улучшения сна людей. Со временем ты узнаешь что именно я умею 😁',
#                          reply_markup=markup)
#
#
# def test_start2_start(mocker):
#     telebot.TeleBot.send_message = Mock()
#     types.ReplyKeyboardMarkup = Mock()
#     types.KeyboardButton = Mock()
#     message = Mock()
#     message.text = "Давай приступим!"
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     Button1 = types.KeyboardButton('Меню')
#     markup.add(Button1)
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, 'Откройте меню, нажав на кнопку ниже', reply_markup=markup)
#
#
# def test_start2_menu(mocker):
#     telebot.TeleBot.send_message = Mock()
#     types.ReplyKeyboardMarkup = Mock()
#     types.KeyboardButton = Mock()
#     message = Mock()
#     message.text = "Меню"
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     Button1 = types.KeyboardButton('Хочу уснуть в...')
#     Button2 = types.KeyboardButton('Хочу встать в...')
#     Button3 = types.KeyboardButton('Погода')
#     Button4 = types.KeyboardButton('Информация о боте')
#     Button5 = types.KeyboardButton('Статистика')
#     Button6 = types.KeyboardButton('Узнать свой id')
#     markup.add(Button1, Button2, Button3, Button4, Button5, Button6)
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, 'Вы открыли Меню', reply_markup=markup)
#
#
# def test_start2_info(mocker):
#     telebot.TeleBot.send_message = Mock()
#     message = Mock()
#     message.text = "Информация о боте"
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, ' • хочу уснуть в.../хочу встать в... - пользователь записывает время в которое ему хотелось бы проснуться или же пойти спать, на основании полученных данных бот предлагает пользователю наилучшие варианты, основанные на фазах сна, каждая из которых длится ≈ 90 минут\n • Погода - вы указываете город, в котором вы живете, чтобы утром, когда вы просыпались вам отправлялась погода \n • Статистика - показывает сколько раз вы проснулись вовремя (ответили на утреннее сообщение) \n • Информация - показывает информацию о кнопках в меню')
#
#
# def test_start2_sleep(mocker):
#     telebot.TeleBot.send_message = Mock()
#     telebot.TeleBot.register_next_step_handler = Mock()
#     Sleep_helper_bot.sleeptime = Mock()
#     message = Mock()
#     message.text = "Хочу уснуть в..."
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, 'Напишите время, в которое вы хотите пойти спать \n(напрмер: 12:37, 0:59, 23:08)')
#     Sleep_helper_bot.bot.register_next_step_handler.assert_called_with(message, Sleep_helper_bot.sleeptime)
#
#
# def test_start2_wake(mocker):
#     telebot.TeleBot.send_message = Mock()
#     telebot.TeleBot.register_next_step_handler = Mock()
#     Sleep_helper_bot.wakeup = Mock()
#     message = Mock()
#     message.text = "Хочу встать в..."
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, 'Напишите время, в которое вы хотите встать \n(напрмер: 6:48, 8:00, 11:50)')
#     Sleep_helper_bot.bot.register_next_step_handler.assert_called_with(message, Sleep_helper_bot.wakeup)
#
#
# def test_start2_id(mocker):
#     telebot.TeleBot.send_message = Mock()
#     message = Mock()
#     message.text = "Узнать свой id"
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, f"ваш id: {message.from_user.id}")
#
#
# def test_start2_weather(mocker):
#     telebot.TeleBot.send_message = Mock()
#     telebot.TeleBot.register_next_step_handler = Mock()
#     Sleep_helper_bot.get_weather = Mock()
#     message = Mock()
#     message.text = "Погода"
#     Sleep_helper_bot.start2(message)
#     Sleep_helper_bot.bot.send_message.assert_called_with(message.chat.id, 'Введите название города')
#     Sleep_helper_bot.bot.register_next_step_handler.assert_called_with(message, Sleep_helper_bot.get_weather)