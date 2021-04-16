from datetime import datetime, timedelta

from provider_bot.root import app
from provider_bot.bot_db import get_user_data, get_service_plan, set_credit_flag
from provider_bot.utils.state_logger import logged
from provider_bot.utils.aggressive import aggressive_filter


@app.handle(intent='get_credit')
@logged
@aggressive_filter
def get_credit(request, responder):
    responder.frame['user'] = get_user_data(request.context['username'])
    if responder.frame['user']['credit']:
        responder.reply('Услуга "Кредит доверия" уже подключена. Чем еще можем вам помочь?')
        return
    if request.intent == 'abort':
        responder.reply('Возможно у вас есть еще какие-то вопросы?')
        return
    if request.intent in ['confirmation', 'get_credit', 'repeat', 'clarify']:
        responder.params.target_dialogue_state = 'turn_on_credit'
        responder.reply('С услугой "Кредит доверия" вы можете восстановить поставку интернета сразу, '
                        'а заплатить на протяжении 10 дней. Желаете подключить эту услугу сейчас?')
        return
    else:
        responder.reply("Извините, я вас не поняла. Чем еще мы можем вам помочь?")
        return


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def turn_on_credit(request, responder):
    if request.intent == 'abort':
        responder.reply("Понятно. Чем еще мы можем вам помочь?")
        return
    if request.intent in ['confirmation', 'clarify']:
        if not responder.frame.get('verified', False):
            responder.params.target_dialogue_state = 'verify_service_number'
            responder.frame['return_to'] = turn_on_credit_continue
            responder.reply("Сначала пройдите верификацию. Введите 8 цифр вашего договора.")
            return
        else:
            turn_on_credit_continue(request, responder)
            return
    if request.intent == 'repeat':
        get_credit(request, responder)
        return
    else:
        responder.frame['credit_count'] = responder.frame.get('credit_count', 0) + 1
        if responder.frame['credit_count'] < 3:
            responder.params.target_dialogue_state = 'turn_on_credit'
            responder.reply('Извините, я вас не поняла.')
            return
        else:
            responder.frame['credit_count'] = 0
            responder.reply('Извините, я вас не поняла. Чем еще мы можем вам помочь?')
            return


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def turn_on_credit_continue(request, responder):
    responder.frame['user'] = get_user_data(request.context['username'])
    responder.frame['service_plan'] = get_service_plan(responder.frame['user']['service_plan_id'])
    responder.params.target_dialogue_state = 'turn_on_credit_processing'
    responder.reply(f'Мы можем выдать вам кредит на сумму {responder.frame["service_plan"]["price"]}' +
                    f' до {str(datetime.now() + timedelta(days=10))[:10]}.' +
                    f'Оплатить {abs(responder.frame["user"]["balance"]) + responder.frame["service_plan"]["price"]} грн '
                    f'нужно на протяжении 10 дней. ' +
                    f'Вас устраивают такие условия?')


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def turn_on_credit_processing(request, responder):
    if request.intent == 'confirmation':
        set_credit_flag(responder.frame['user']['id'], True)
        responder.reply('Услуга "Кредит доверия" подключена.')
        return
    if request.intent == 'abort':
        responder.reply('Понятно. Чем еще мы можем вам помочь?')
        return
    if request.intent == 'repeat':
        turn_on_credit_continue(request, responder)
        return
    else:
        responder.frame['credit_process_count'] = responder.frame.get('credit_process_count', 0) + 1
        if responder.frame['credit_process_count'] < 3:
            responder.frame['user'] = get_user_data(request.context['username'])
            responder.frame['service_plan'] = get_service_plan(responder.frame['user']['service_plan_id'])
            responder.params.target_dialogue_state = 'turn_on_credit_processing'
            responder.reply(f'Мы можем выдать вам кредит на сумму {responder.frame["service_plan"]["price"]}' +
                    f' до {str(datetime.now() + timedelta(days=10))[:10]}.' +
                    f'Оплатить {abs(responder.frame["user"]["balance"]) + responder.frame["service_plan"]["price"]} грн '
                    f'нужно на протяжении 10 дней. ' +
                    f'Вас устраивают такие условия?')
            return
        else:
            responder.frame['credit_process_count'] = 0
            responder.reply('Извините, я вас не поняла. Чем еще мы можем вам помочь?')
            return
