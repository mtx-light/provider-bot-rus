from datetime import datetime, timedelta

from provider_bot.root import app
from provider_bot.bot_db import get_user_data, call_home_service
from provider_bot.utils.state_logger import logged
from provider_bot.utils.aggressive import aggressive_filter

parsing_format = "%Y-%m-%dT%H:%M"
def parse_date(date):
    day = datetime.strptime(date[:16], parsing_format)
    hour = datetime.strptime(date[:16], parsing_format)
    return (day, hour)

def in_days_constraint(date, days):
    day, _ = parse_date(date)
    limit = datetime.now() + timedelta(days=days)
    return day <= limit

def show_balance(request, responder):
    if responder.frame['with_balance']:
        responder.frame['with_balance'] = False
        balance = get_user_data(request.context['username'])['balance']
        responder.reply(f"Ваш баланс: {balance}")

def verify(request, responder, return_to):
    if not responder.frame.get('verified', False):
        responder.params.target_dialogue_state = 'verify_service_number'
        responder.frame['return_to'] = return_to
        responder.reply(f"Сначала пройдите верификацию. Введите 8 цифр вашего договора.")
        return True
    return False

@app.handle(intent='home_service')
@logged
@aggressive_filter
def home_service(request, responder):
    responder.frame['with_balance'] = False
    balance_and_home_service(request, responder)

@app.handle(intent='balance_and_home_service')
@logged
@aggressive_filter
def balance_and_home_service(request, responder):
    if request.intent == 'balance_and_home_service':
        responder.frame['with_balance'] = True
    day = None
    for e in request.entities:
        if e['type'] == 'sys_time' and e['role'] == 'day':
            day = e['value'][0]['value']
    hour = None
    for e in request.entities:
        if e['type'] == 'sys_time' and e['role'] == 'hour':
            hour = e['value'][0]['value']
    if (day and in_days_constraint(day, 10)) or responder.frame.get('balance_and_home_service_day'):
        if not responder.frame.get('balance_and_home_service_day'):
            responder.frame['balance_and_home_service_day'] = day
        if hour or responder.frame.get('balance_and_home_service_hour'):
            if not responder.frame.get('balance_and_home_service_hour'):
                responder.frame['balance_and_home_service_hour'] = hour
            balance_and_home_service_hour(request, responder)
            return
        else:
            if verify(request, responder, balance_and_home_service):
                return
            show_balance(request, responder)
            responder.params.target_dialogue_state = 'balance_and_home_service_hour'
            responder.reply('На который час вы желаете вызвать мастера?')
            return

    if verify(request, responder, balance_and_home_service):
        return
    else:
        if request.intent in ['balance_and_home_service', 'verification', 'home_service']:
            show_balance(request, responder)
            responder.reply("Вы желаете оставить заявку на вызов мастера домой?")
            responder.params.target_dialogue_state = 'balance_and_home_service'
            return
        if request.intent == 'abort':
            responder.frame['balance_and_home_service_day'] = None
            responder.frame['balance_and_home_service_hour'] = None
            responder.reply("Понятно. Чем еще мы можем вам помочь?")
            return
        if request.intent == 'confirmation':
            responder.reply("На какой день вы желаете вызвать мастера?")
            responder.params.target_dialogue_state = 'balance_and_home_service_day'
            return
        else:
            responder.frame['balance_and_home_service_count'] = responder.frame.get('balance_and_home_service_count', 0) + 1
            if responder.frame['balance_and_home_service_count'] < 3:
                responder.params.target_dialogue_state = 'balance_and_home_service'
                responder.reply("Извините, я вас не поняла. Вы желаете оставить заявку на вызов мастера домой?")
                return
            else:
                responder.frame['balance_and_home_service_count'] = 0
                responder.reply("Извините, пожалуйста, я вас не поняла. Чем еще мы можем вам помочь?")
                return

@app.handle(targeted_only=True)
@logged
@aggressive_filter
def balance_and_home_service_day(request, responder):
    if request.intent == 'abort':
        responder.frame['balance_and_home_service_day'] = None
        responder.frame['balance_and_home_service_hour'] = None
        responder.reply("Понятно. Чем еще мы можем вам помочь?")
        return
    day = None
    for e in request.entities:
        if e['type'] == 'sys_time' and e['role'] == 'day':
            day = e['value'][0]['value']
    hour = None
    for e in request.entities:
        if e['type'] == 'sys_time' and e['role'] == 'hour':
            hour = e['value'][0]['value']
    if verify(request, responder, balance_and_home_service_day):
        return
    if (not day or not in_days_constraint(day, 10)) and not responder.frame.get('balance_and_home_service_day'):
        responder.frame['balance_and_home_service_day_count'] = responder.frame.get('balance_and_home_service_day_count', 0) + 1
        if responder.frame['balance_and_home_service_day_count'] < 3:
            future_date_limit = datetime.now() + timedelta(days=10)
            responder.params.target_dialogue_state = 'balance_and_home_service_day'
            responder.reply(f'Повторите, пожалуйста, на какой день вы желаете вызвать мастера?' +
                            f' Вы можете выбрать день начиная с завтра до {str(future_date_limit)[:10]}')
            return
        else:
            responder.frame['balance_and_home_service_day_count'] = 0
            responder.reply('Ожидайте соединения с оператором.')
            return
    else:
        if hour:
            show_balance(request, responder)
            if not responder.frame.get('balance_and_home_service_day'):
                responder.frame['balance_and_home_service_day'] = day
            if not responder.frame.get('balance_and_home_service_hour'):
                responder.frame['balance_and_home_service_hour'] = hour
            responder.params.target_dialogue_state = 'balance_and_home_service_confirm'
            responder.reply(f'Вы желаете вызвать мастера на {str(day)[:10]} {str(hour)[11:16]}?')
        else:
            if not responder.frame.get('balance_and_home_service_day'):
                responder.frame['balance_and_home_service_day'] = day
            responder.params.target_dialogue_state = 'balance_and_home_service_hour'
            responder.reply('На который час вы желаете вызвать мастера?')
            return

@app.handle(targeted_only=True)
@logged
@aggressive_filter
def balance_and_home_service_hour(request, responder):
    if request.intent == 'abort':
        responder.frame['balance_and_home_service_day'] = None
        responder.frame['balance_and_home_service_hour'] = None
        responder.reply("Понятно. Чем еще мы можем вам помочь?")
        return
    hour = None
    for e in request.entities:
        if e['type'] == 'sys_time' and e['role'] == 'hour':
            hour = e['value'][0]['value']
    if verify(request, responder, balance_and_home_service_hour):
        return
    if not hour and not responder.frame.get('balance_and_home_service_hour'):
        responder.frame['balance_and_home_service_hour_count'] = responder.frame.get('balance_and_home_service_hour_count', 0) + 1
        if responder.frame['balance_and_home_service_hour_count'] < 3:
            responder.params.target_dialogue_state = 'balance_and_home_service_hour'
            responder.reply('Повторите, пожалуйста, на который час вы желаете вызвать мастера? Например: 17:00')
            return
        else:
            responder.frame['balance_and_home_service_hour_count'] = 0
            responder.reply('Ожидайте соединения с оператором.')
            return
    else:
        show_balance(request, responder)
        if not responder.frame.get('balance_and_home_service_hour'):
            responder.frame['balance_and_home_service_hour'] = hour
        else:
            hour = responder.frame['balance_and_home_service_hour']
        day = responder.frame['balance_and_home_service_day']
        responder.params.target_dialogue_state = 'balance_and_home_service_confirm'
        responder.reply(f'Вы хотите вызвать мастера на {str(day)[:10]} {str(hour)[11:16]}?')
        return

@app.handle(targeted_only=True)
@logged
@aggressive_filter
def balance_and_home_service_confirm(request, responder):
    if verify(request, responder, balance_and_home_service_confirm):
        return
    if request.intent == 'abort':
        responder.reply('На какой день вы желаете вызвать мастера?')
        responder.params.target_dialogue_state = 'balance_and_home_service_day'
        return
    if request.intent == 'confirmation':
        responder.frame['user'] = get_user_data(request.context['username'])
        day = responder.frame['balance_and_home_service_day']
        hour = responder.frame['balance_and_home_service_hour']
        call_home_service(responder.frame['user']['id'], day, hour)
        responder.frame['balance_and_home_service_day'] = None
        responder.frame['balance_and_home_service_hour'] = None
        responder.reply(f'Заявку на вызов мастера на {str(day)[:10]} {str(hour)[11:16]} создано.\nОжидайте звонка от мастера.')
        responder.reply('Чем еще можем вам помочь?')
        return
    else:
        responder.frame['balance_and_home_service_confirm_count'] = responder.frame.get('balance_and_home_service_confirm_count', 0) + 1
        if responder.frame['balance_and_home_service_confirm_count'] < 3:
            day = responder.frame['balance_and_home_service_day']
            hour = responder.frame['balance_and_home_service_hour']
            responder.params.target_dialogue_state = 'balance_and_home_service_confirm'
            responder.reply(f'Повторите, пожалуйста, вы хотите вызвать мастера на {str(day)[:10]} {str(hour)[11:16]}?')
            return
        else:
            responder.frame['balance_and_home_service_confirm_count'] = 0
            responder.reply('Ожидайте соединения с оператором.')
            return