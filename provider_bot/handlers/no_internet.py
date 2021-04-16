from provider_bot.root import app
from provider_bot.bot_db import get_user_data
from provider_bot.utils.state_logger import logged
from provider_bot.utils.aggressive import aggressive_filter


@app.handle(intent='no_internet')
@logged
@aggressive_filter
def no_internet(request, responder):
    if not responder.frame.get('verified', False):
        responder.params.target_dialogue_state = 'verify_service_number'
        responder.frame['return_to'] = no_internet
        responder.reply(f"Сначала пройдите верификацию. Введите 8 цифр вашего договора.")
    else:
        user = get_user_data(request.context['username'])
        balance = user['balance']
        repair = user['repair']
        if balance < 0:
            reply = f'Последняя оплата на ваш счет была произведена' + \
                    f' {user["last_payment_date"]} в размере {user["last_payment_amount"]} грн.' + \
                    f'Сейчас ваша задолженность составляет {abs(balance)} грн.' \
                    f'Оплатите, пожалуйста, {abs(balance)} грн, чтоб восстановить услугу интернета.\n\n'
            if not user['credit']:
                reply += f'Хотите ли вы узнать об услуге "Кредит доверия"?'
                responder.params.target_dialogue_state = 'get_credit'
            responder.reply(reply)
        elif repair:
            responder.reply('У вас не работает интернет из-за технических неисправностей.'
                            ' Наши специалисты решат эту проблему как можно скорее.'
                            ' Можем ли мы вам еще чем-то помочь?')
        else:
            responder.reply("Подождите, мы соединим вас с оператором!")
