from provider_bot.root import app
from provider_bot.bot_db import get_user_data
from provider_bot.vocalizer import vocalized_name
from provider_bot.utils.state_logger import logged
from provider_bot.utils.aggressive import aggressive_filter

@app.handle(default=True)
@logged
@aggressive_filter
def default(request, responder):
    """This is a default handler."""
    responder.reply('Прошу прощения?')


@app.handle(intent='thanks')
@logged
@aggressive_filter
def thanks(request, responder):
    responder.reply(['Пожалуйста.', 'Всегда рада помочь.'])


@app.handle(intent='small_talk')
@logged
@aggressive_filter
def small_talk(request, responder):
    responses = ['Я бы с удовольствием с вами пообщалась, но могу помочь только с услугами компании "Смидл".',
                 'Я могу помочь вам с такими вопросами:\n- проверить баланс\n- вызов мастера на дом\n- изменение тарифного плана\n- описание вашего тарифного плана\n- услуга "Кредит доверия"\n- проверка проблем с работой интернета.',
                 'К сожалению, я не смогу ответить на это.',
                 'Я понимаю, что вам интересно со мной поиграть, но я не лучший собеседник, если дело не касается услуг компании "Смидл"',
                 'Что ж, если будут вопросы по услугам компании "Смидл" - обращайтесь.']
    responder.frame['small_talk_cycle'] = responder.frame.get('small_talk_cycle', 0)
    responder.reply(responses[responder.frame['small_talk_cycle']])
    responder.frame['small_talk_cycle'] += 1
    if responder.frame['small_talk_cycle'] >= len(responses):
        responder.frame['small_talk_cycle'] = 0

@app.handle(intent='competence')
@logged
@aggressive_filter
def competence(request, responder):
    responder.reply('Я могу помочь вам с такими вопросами:\n- проверить баланс\n- вызов мастера на дом\n- изменение тарифного плана\n- описание вашего тарифного плана\n- услуга "Кредит доверия"\n- проверка проблем с работой интернета.')

@app.handle(intent='confirmation')
@logged
@aggressive_filter
def confirmation(request, responder):
    responder.reply(['Чем именно я могу вам помочь?',
                     'Сформулируйте, пожалуйста, ваш запрос.'])


@app.handle(intent='greet')
@logged
@aggressive_filter
def welcome(request, responder):
    responder.frame['greeted'] = responder.frame.get('greeted', False)
    username = get_user_data(request.context['username'])['username']
    if not responder.frame['greeted']:
        responder.frame['greeted'] = True
        if username:
            responder.reply(f'Приветствую, {vocalized_name(username)}!')
        else:
            responder.reply('Приветствую!')
    else:
        responder.reply([f'Слушаю вас',
                         f'Да-да, я вас слушаю',
                         f'Да, {vocalized_name(username)}, чем могу вам помочь?'])


@app.handle(intent='abort')
@logged
@aggressive_filter
def abort(request, responder):
    responder.reply("Буду рада вам помочь, если возникнут проблемы.")


@app.handle(intent='goodbye')
@logged
@aggressive_filter
def goodbye(request, responder):
    responder.reply(['До свидания!', 'До встречи!', "На связи!", "Прощайте!"])


@app.handle(intent='suicide')
@logged
@aggressive_filter
def suicide(request, responder):
    responder.reply("Мы готовы вас выслушать, подождите минутку.")

@app.handle(intent='clarify')
@logged
@aggressive_filter
def clarify(request, responder):
    responder.reply(['Что именно вас интересует?',
                     'Сформулируйте, пожалуйста, ваш запрос.',
                     'Чем именно я могу вам помочь?'])