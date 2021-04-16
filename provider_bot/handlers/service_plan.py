from provider_bot.root import app
from provider_bot.bot_db import get_user_data, get_service_plan
from provider_bot.vocalizer import vocalized_name
from provider_bot.utils.state_logger import logged
from provider_bot.utils.aggressive import aggressive_filter


@app.handle(intent='change_service_plan')
@logged
@aggressive_filter
def change_service_plan(request, responder):
    for e in request.entities:
        if e['type'] == 'service_plan':
            selected_plan = e['value'][0]
    if not responder.frame.get('verified', False):
        responder.params.target_dialogue_state = 'verify_service_number'
        responder.frame['return_to'] = change_service_plan
        responder.reply(f"Сначала пройдите верификацию. Введите 8 цифр вашего договора.")
    else:
        responder.frame['user'] = get_user_data(request.context['username'])
        responder.frame['service_plan'] = get_service_plan(responder.frame['user']['service_plan_id'])
        responder.params.target_dialogue_state = 'change_service_plan_selection'
        responder.reply(f"Сейчас ваш тарифный план: {responder.frame['service_plan']['name']}." +
                        f" На какой тарифный план вы хотите перейти?")


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def change_service_plan_selection(request, responder):
    if request.intent == 'abort':
        responder.reply("Понятно. Чем еще мы можем вам помочь?")
        return
    if request.intent == 'clarify':
        responder.frame['service_plan_clarify_counter'] = responder.frame.get('service_plan_clarify_counter', 0) + 1
        if responder.frame['service_plan_clarify_counter'] == 1:
            responder.reply("- Смидл Спорт HD Pro +100 (319 грн)\n- Смидл Power Time Pro +200 (399 грн)\n- Premium HD +200 (459 грн)")
        else:
            responder.reply("Смидл Спорт HD Pro +100\n- Интернет до 100 Мбит/с\n- Более 70 каналов\n- 10 HD каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европы UEFA")
            responder.reply("Смидл Power Time Pro +200\n- Интернет до 200 Мбит/с\n- Более чем 140 каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европы UEFA")
            responder.reply("Premium HD +200\n- Интернет до 200 Мбит/с\n- Более чем 160 каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европи UEFA\n- оборудование в количестве 5 шт. включено")
            responder.frame['service_plan_clarify_counter'] = 0
        responder.params.target_dialogue_state = 'change_service_plan_selection'
        return
    if request.intent == 'specify_service_plan':
        selected_plan = None
        for e in request.entities:
            if e['type'] == 'service_plan':
                selected_plan = e['value'][0]
        if selected_plan and selected_plan['id'] != responder.frame['service_plan']['id']:
            responder.frame['selected_service_plan'] = get_service_plan(selected_plan['id'])
            responder.params.target_dialogue_state = 'change_service_plan_confirm'
            responder.reply("Вы хотите изменить ваш тарифный план с " +
                            f"{responder.frame['service_plan']['name']} на " +
                            f"{responder.frame['selected_service_plan']['name']}?")
            return
    responder.frame['change_service_plan_selection_count'] = responder.frame.get('change_service_plan_selection_count', 0) + 1
    if responder.frame['change_service_plan_selection_count'] < 3:
        responder.params.target_dialogue_state = 'change_service_plan_selection'
        responder.reply(f"Сейчас ваш тарифний план {responder.frame['service_plan']['name']}." +
                        f" На какой тарифный план вы хотите перейти?")
        return
    else:
        responder.frame['change_service_plan_selection_count'] = 0
        responder.reply(f"{vocalized_name(request.context['username'])}, ожидайте соединения, пожалуйста.")


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def change_service_plan_confirm(request, responder):
    if request.intent == 'abort':
        responder.reply('Понятно. Чем еще мы можем вам помочь?')
        return
    if request.intent == 'confirmation':
        responder.params.target_dialogue_state = 'change_service_plan_changed'
        responder.reply(f"Стоимость нового тарифного плана составит" +
                        f" {responder.frame['selected_service_plan']['price']}. " +
                        f"Вы подтверждаете переход на тарифный план " +
                        f"{responder.frame['selected_service_plan']['name']}?")
        return
    else:
        responder.frame['change_service_plan_confirm_count'] = responder.frame.get('change_service_plan_confirm_count', 0) + 1
        if responder.frame['change_service_plan_confirm_count'] < 3:
            responder.params.target_dialogue_state = 'change_service_plan_confirm'
            responder.reply("Вы хотите изменить ваш тарифный план с " +
                            f"{responder.frame['service_plan']['name']} на " +
                            f"{responder.frame['selected_service_plan']['name']}?")
            return
        else:
            responder.frame['change_service_plan_confirm_count'] = 0
            responder.reply(f"{vocalized_name(request.context['username'])}, ожидайте соединения, пожалуйста.")


@app.handle(targeted_only=True)
@logged
@aggressive_filter
def change_service_plan_changed(request, responder):
    if request.intent == 'abort':
        responder.reply('Понятно. Чем еще мы можем вам помочь?')
        return
    if request.intent == 'confirmation':
        responder.reply("Ваш тарифный план изменен. Чем еще мы можем вам помочь? ")
        return
    else:
        responder.frame['change_service_plan_changed_count'] = responder.frame.get('change_service_plan_changed_count', 0) + 1
        if responder.frame['change_service_plan_changed_count'] < 3:
            responder.params.target_dialogue_state = 'change_service_plan_changed'
            responder.reply(f"Стоимость нового тарифного плана составит" +
                        f" {responder.frame['selected_service_plan']['price']}. " +
                        f"Вы подтверждаете переход на тарифный план " +
                        f"{responder.frame['selected_service_plan']['name']}?")
            return
        else:
            responder.frame['change_service_plan_confirm_count'] = 0
            responder.reply(f"{vocalized_name(request.context['username'])}, ожидайте соединения, пожалуйста.")
        return


@app.handle(intent='stop_service')
@logged
@aggressive_filter
def stop_service(request, responder):
    responder.reply("Подождите, мы соединим вас со специалистом по подобным вопросам.")


@app.handle(intent='service_plan_description')
@logged
@aggressive_filter
def service_plan_description(request, responder):
    if request.intent == 'service_plan_description':
        responder.frame['user'] = get_user_data(request.context['username'])
        responder.frame['service_plan'] = get_service_plan(responder.frame['user']['service_plan_id'])
        responder.reply(f"Ваш тарифный план: {responder.frame['service_plan']['name']}.\n" +
                        f"{responder.frame['service_plan']['description']}\n" +
                        f"Стоимость составляет {responder.frame['service_plan']['price']} "
                        f"гривен в месяц.")
        responder.params.target_dialogue_state = 'service_plan_description'
        return
    if request.intent == 'clarify':
        responder.frame['service_plan_description_clarify_counter'] = responder.frame.get('service_plan_description_clarify_counter', 0) + 1
        if responder.frame['service_plan_description_clarify_counter'] == 1:
            responder.reply(
                "- Смидл Спорт HD Pro +100 (319 грн)\n- Смидл Power Time Pro +200 (399 грн)\n- Premium HD +200 (459 грн)")
        else:
            responder.reply(
                "Смидл Спорт HD Pro +100\n- Интернет до 100 Мбит/с\n- Более 70 каналов\n- 10 HD каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европы UEFA")
            responder.reply(
                "Смидл Power Time Pro +200\n- Интернет до 200 Мбит/с\n- Более чем 140 каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европы UEFA")
            responder.reply(
                "Premium HD +200\n- Интернет до 200 Мбит/с\n- Более чем 160 каналов\n- Дополнительная услуга Смидл Футбол+: прямые трансляции всех матчей Лиги Чемпионов и Лиги Европи UEFA\n- оборудование в количестве 5 шт. включено")
            responder.frame['service_plan_description_clarify_counter'] = 0
        responder.params.target_dialogue_state = 'service_plan_description'
        return
    if request.intent == 'change_service_plan':
        change_service_plan(request, responder)
        return
    else:
        responder.reply('Чем еще мы можем вам помочь?')
        return

