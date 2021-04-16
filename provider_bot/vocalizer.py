from provider_bot.bot_db import get_user

vocal_dict = {'Андрій': 'Андрію', 'Артем': 'Артеме', 'Арсеній': 'Арсенію',
              'Антон': 'Антоне', 'Артур': 'Артуре', 'Анатолій': 'Анатолію',
              'Адам': 'Адаме', 'Адріан': 'Адріане', 'Альберт': 'Альберте',
              'Альфред': 'Альфреде', 'Аристарх': 'Аристарху', 'Аркадій': 'Аркадію',
              'Аарон': 'Аароне', 'Абрам': 'Абраме', 'Армен': 'Армене', 'Арсен': 'Арсене',
              'Архип': 'Архипе', 'Афанасій': 'Афанасію', 'Богдан': 'Богдане',
              'Борис': 'Борисе', 'Борислав': 'Бориславе', 'Броніслав': 'Броніславе',
              'Володимир': 'Володимире', 'Владислав': 'Владиславе', 'Вадим': 'Вадиме',
              'Валентин': 'Валентине', 'Валерій': 'Валерію', 'Вальдемар': 'Вальдемаре',
              'Варфоломій': 'Варфоломію', 'Василь': 'Василю', 'Веніамін': 'Веніаміне',
              'Віктор': 'Вікторе', 'Вільгельм': 'Вільгельме', 'Віталій': 'Віталію',
              'Владлен': 'Владлене', 'Влас': 'Власе', 'Всеволод': 'Всеволоде',
              'В’ячеслав': 'В’ячеславе', 'Веремій': 'Веремію', 'Гліб': 'Глібе',
              'Гаврило': 'Гавриле', 'Гаррі': 'Гаррі', 'Геворг': 'Геворгу',
              'Геннадій': 'Геннадію', 'Генріх': 'Генріху', 'Георгій': 'Георгію',
              'Герман': 'Германе', 'Гордій': 'Гордію', 'Григорій': 'Григорію',
              'Гнат': 'Гнате', 'Денис': 'Денисе', 'Дмитро': 'Дмитре',
              'Данило': 'Даниле', 'Давид': 'Давиде', 'Даніель': 'Даніелю',
              'Дарій': 'Дарію', 'Демид': 'Демиде', "Дем’ян": "Дем’яне",
              'Добриня': 'Добрине', 'Домінік': 'Домініку', 'Едгар': 'Едгаре',
              'Едуард': 'Едуарде', 'Ельдар': 'Ельдаре', 'Еміль': 'Емілю',
              'Еммануїл': 'Еммануїле', 'Ерік': 'Еріку', 'Ернест': 'Ернесте',
              'Єгор': 'Єгоре', 'Євген': 'Євгене', 'Євдоким': 'Євдокиме',
              'Єлизар': 'Єлизаре', 'Єлисей': 'Єлисею', 'Захар': 'Захаре',
              'Ілля': 'Ілле', 'Іван': 'Іване', 'Ібрагім': 'Ібрагіме',
              'Ігор': 'Ігорю', 'Ісус': 'Ісусе', 'Іларіон': 'Іларіоне',
              'Ільдар': 'Ільдаре', 'Інокентій': 'Інокентію', 'Іскандер': 'Іскандере',
              'Ісмаїл': 'Ісмаїле', 'Йосип': 'Йосипе', 'Кирило': 'Кириле',
              'Каміль': 'Камілю', 'Карен': 'Карене', 'Карім': 'Каріме',
              'Клим': 'Климе', 'Костянтин': 'Костянтине', 'Крістіан': 'Крістіане',
              'Кузьма': 'Кузьмо', 'Лаврентій': 'Лаврентію', 'Лев': 'Леве',
              'Леон': 'Леоне', 'Леонард': 'Леонарде', 'Леонід': 'Леоніде',
              'Левко': 'Левку', 'Лука': 'Луко', "Лук’ян": "Лук’яне", 'Микола': 'Миколо',
              'Матвій': 'Матвію', 'Марк': 'Марку', 'Михайло': 'Михайле', 'Максим': 'Максиме',
              'Микита': 'Микито', 'Марік': 'Марік', 'Май': 'Маю', 'Макар': 'Макаре',
              'Марат': 'Марате', 'Марсель': 'Марселю', 'Мартін': 'Мартіне', 'Мілан': 'Мілане',
              'Мирон': 'Мироне', 'Мирослав': 'Мирославе', 'Митрофан': 'Митрофане',
              'Мстислав': 'Мстиславе', 'Мурат': 'Мурате', 'Назар': 'Назаре',
              'Натан': 'Натане', 'Нестор': 'Несторе', 'Олександр': 'Олександре',
              'Олексій': 'Олексію', 'Овсій': 'Овсію', 'Омелян': 'Омеляне',
              'Олег': 'Олеже', 'Оскар': 'Оскаре', 'Остап': 'Остапе', 'Павло': 'Павле',
              'Петро': 'Петре', 'Платон': 'Платоне', 'Потап': 'Потапе', 'Прохор': 'Прохоре',
              'Роман': 'Романе', 'Радик': 'Радику', 'Радомир': 'Радомире', 'Рафаель': 'Рафаелю',
              'Ренат': 'Ренате', 'Річард': 'Річарде', 'Роберт': 'Роберте',
              'Родіон': 'Родіоне', 'Ролан': 'Ролане', 'Ростислав': 'Ростиславе',
              'Руслан': 'Руслане', 'Рустам': 'Рустаме', 'Степан': 'Степане', 'Сава': 'Саво',
              'Савелій': 'Савелію', 'Саїд': 'Саїде', 'Самір': 'Саміре', 'Самсон': 'Самсоне',
              'Самуїл': 'Самуїле', 'Святослав': 'Святославе', 'Севастян': 'Севастяне',
              'Семен': 'Семене', 'Серафим': 'Серафиме', 'Сергій': 'Сергію',
              'Симон': 'Симоне', 'Соломон': 'Соломоне', 'Спартак': 'Спартаку',
              'Станіслав': 'Станіславе', 'Тимофій': 'Тимофію', 'Тагір': 'Тагіре',
              'Тамерлан': 'Тамерлане', 'Тарас': 'Тарасе', 'Теодор': 'Теодоре',
              'Тигран': 'Тигране', 'Тимур': 'Тимуре', 'Тихон': 'Тихоне', 'Трохим': 'Трохиме',
              'Умар': 'Умаре', 'Устин': 'Устине', 'Федір': 'Федоре', 'Фарід': 'Фаріде',
              'Фелікс': 'Феліксе', 'Філіп': 'Філіпе', 'Фома': 'Фомо', 'Харитон': 'Харитоне',
              'Юхим': 'Юхиме', 'Юліан': 'Юліане', 'Юлій': 'Юлію', 'Юрій': 'Юрію',
              'Ярослав': 'Ярославе', 'Яків': 'Якове', 'Ян': 'Яне', 'Яромир': 'Яромире',

              'Аврора': 'Авроро', 'Агата': 'Агато', 'Аглая': 'Аглає', 'Агнія': 'Агніє',
              'Аделіна': 'Аделіно', 'Адель': 'Адель', 'Адріана': 'Адріано', 'Азалія': 'Азаліє',
              'Аїда': 'Аїдо', 'Айгуль': 'Айгуль', 'Аксінья': 'Аксіньє', 'Алевтина': 'Алевтино',
              'Олександра': 'Олександро', 'Олена': 'Олено', 'Аліна': 'Аліно', 'Аліса': 'Алісо',
              'Алія': 'Аліє', 'Алла': 'Алло', 'Алсу': 'Алсу', 'Альбіна': 'Альбіно',
              'Альфія': 'Альфіє', 'Амелія': 'Амеліє', 'Аміна': 'Аміно',
              'Анастасія': 'Анастасіє', 'Ангеліна': 'Ангеліно',
              'Анжела': 'Анжело', 'Аніта': 'Аніто',
              'Анна': 'Анно', 'Антоніна': 'Антоніно', 'Анфіса': 'Анфісо',
              'Аріадна': 'Аріадно', 'Аріана': 'Аріано', 'Аріна': 'Аріно',
              'Ася': 'Асю', 'Белла': 'Белло', 'Валентина': 'Валентино',
              'Валерія': 'Валеріє', 'Варвара': 'Варваро', 'Василина': 'Василино',
              'Венера': 'Венеро', 'Віра': 'Віро', 'Вероніка': 'Вероніко',
              'Вікторія': 'Вікторіє', 'Віолетта': 'Віолетто',
              'Владлена': 'Владлено', 'Галина': 'Галино', 'Гузель': 'Гузель',
              'Гульназ': 'Гульназ', 'Гульнара': 'Гульнаро', 'Дана': 'Дано',
              'Дарина': 'Дарино', "Дар'я": "Дар'є", 'Діана': 'Діано', 'Діна': 'Діно',
              'Дінара': 'Дінаро', 'Домініка': 'Домініко', 'Єва': 'Єво',
              'Євангеліна': 'Євангеліно', 'Євдокія': 'Євдокіє', 'Катерина': 'Катерино',
              'Єлизавета': 'Єлизавето', 'Єсенія': 'Єсеніє', 'Жанна': 'Жанно', 'Заріна': 'Заріно',
              'Зінаїда': 'Зінаїдо', 'Злата': 'Злато', 'Зоя': 'Зоє', 'Зульфія': 'Зульфіє',
              'Іванна': 'Іванно', 'Ізабелла': 'Ізабелло', 'Ілона': 'Ілоно', 'Інга': 'Інго',
              'Інеса': 'Інесо', 'Інна': 'Інно', 'Іраїда': 'Іраїдо', 'Ірина': 'Ірино',
              'Камілла': 'Камілло', 'Каріма': 'Карімо', 'Каріна': 'Каріно',
              'Кароліна': 'Кароліно', 'Кіра': 'Кіро', 'Христина': 'Христино',
              'Ксенія': 'Ксеніє', 'Лада': 'Ладо', 'Лана': 'Лано', 'Лариса': 'Ларисо',
              'Лаура': 'Лауро', 'Лейла': 'Лейло', 'Ліана': 'Ліано', 'Лідія': 'Лідіє',
              'Ліліана': 'Ліліано', 'Лілія': 'Ліліє', 'Ліна': 'Ліно', 'Лія': 'Ліє',
              'Луїза': 'Луїзо', 'Любов': 'Любове', 'Людмила': 'Людмило', 'Мадіна': 'Мадіно',
              'Майя': 'Майє', 'Маліка': 'Маліко', 'Маргарита': 'Маргарито', 'Маріанна': 'Маріанно',
              'Марина': 'Марино', 'Марія': 'Маріє', 'Марта': 'Марто', "Мар'ям": "Мар'ям",
              'Меланія': 'Меланіє', 'Міла': 'Міло', 'Мілана': 'Мілано', 'Мілена': 'Мілено',
              'Мирослава': 'Мирославо', 'Надія': 'Надіє', 'Наталія': 'Наталіє', 'Ніка': 'Ніко',
              'Ніна': 'Ніно', 'Оксана': 'Оксано', 'Олеся': 'Олесю', 'Олівія': 'Олівіє',
              'Ольга': 'Ольго', 'Пелагея': 'Пелагеє', 'Поліна': 'Поліно', 'Рада': 'Радо',
              'Раїса': 'Раїсо', 'Регіна': 'Регіно', 'Рената': 'Ренато', 'Римма': 'Риммо',
              'Роза': 'Розо', 'Роксана': 'Роксано', 'Руфіна': 'Руфіно', 'Сабіна': 'Сабіно',
              'Сабрина': 'Сабрино', 'Світлана': 'Світлано', 'Серафима': 'Серафимо',
              'Сніжана': 'Сніжано', 'Софія': 'Софіє', 'Стелла': 'Стелло', 'Стефанія': 'Стефаніє',
              'Таїсія': 'Таїсіє', 'Тамара': 'Тамаро', 'Тетяна': 'Тетяно', 'Уляна': 'Уляно',
              'Фаріда': 'Фарідо', 'Фатіма': 'Фатімо', 'Елеонора': 'Елеоноро', 'Еліна': 'Еліно',
              'Ельза': 'Ельзо', 'Ельміра': 'Ельміро', 'Емілія': 'Еміліє', 'Емма': 'Еммо',
              'Юлія': 'Юліє', 'Яна': 'Яно'}

def vocalize(name):
    return name

def vocalized_name(username):
    user = get_user(username)
    if user['first_name']:
        return vocalize(user['first_name'])
    else:
        return username