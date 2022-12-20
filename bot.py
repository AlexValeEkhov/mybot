import logging
from ephem import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("""Привет, дружище! Я Бот-попугай. Чем могу помочь?
    Список команд:
    /wordcount и и я посчитаю твои слова.
    /nextfullmoon выдаст дату следующего полнолуния.
    /planet покажет расположние планеты на данный момент
    /cityplay включает режим игры в города
    /calc включает режим калькулятора
    /stop возвращает режим попугая""")

modes_dict = {'/stop': 0, '/wordcount': 1, '/planet': 2, '/nextfullmoon': 3, '/cityplay': 4, '/calc': 5}
modes_text = {0: 'Режим попугая:',
 1: 'Режим подсчёта слов:',
 2: 'Поиск положения планет:', 
 3: 'Ближайшее полнолуние. Введи дату вида 2000-01-01 или слово "сегодня"',
 4: 'Игра в города:',
 5: 'Калькулятор:'}

mode = 0
def mode_control(update, context):
    text = update.message.text
    if text in modes_dict:
        global mode
        mode = modes_dict[text]
    if mode in modes_text:
       update.message.reply_text(modes_text[mode]) 
    

def talk_to_me(update, context): #возвращает пользователю его текст
    text = update.message.text
        
    if mode == 1:
        wordcount(update, context)
    elif mode == 2:
        planet_const(update, context)
    elif mode == 3:
        nextfullmoon(update, context)
    elif mode == 4:
        cityplay(update, context)
    elif mode == 5:
        calc(update, context)
    else:
        update.message.reply_text(f'Сам ты {text}!')

replace_list =['.', ',', '!', ':', ';', '?', '(', ')', '-'] # можно дополнить символами под замену.

def wordcount(update, context): # функция считает слова в сообщении ползователя
    text = update.message.text.replace('/wordcount', '')
    
    if text == "":
        update.message.reply_text('Нечего считать.')
    else:
        for symb in replace_list:
            if symb in text:
                text = text.replace(symb, ' ')
        words = text.split()
    update.message.reply_text(f'Всего слов - {len(words)}')

def planet_const(update, context): # указывает созвездие, в котором сейчас расположена планета

    planets ={                      
      "меркурий": Mercury(now()),
      "венера": Venus(now()),
      "марс": Mars(now()),
      "юпитер": Jupiter(now()),
      "сатурн": Saturn(now()),
      "уран": Uranus(now()),
      "нептун": Neptune(now()),
      "плутон": Pluto(now())
      }
  
    c = 0
    text = (update.message.text).lower()              
    find_planet = text.split()                 
    for word in find_planet:  
      for key in planets: 
        if word == key:
          print(planets[f"{word}"]) # Результат вычисления планеты выводится в консоль
          const = constellation(planets[f"{word}"]) 
          update.message.reply_text(f'Планета {(word).capitalize()} находится в созвездии {const}')
          c = 1
    if c == 0:         
        update.message.reply_text('Нет такой планеты')

def nextfullmoon(update,context): # выдает дату следующего полнолуния
    text = update.message.text
    print(text)
    if text == "сегодня":
        fullmoon = next_full_moon(now())
    else:
        text = text.replace('-', '/')
        date = Date(text)
        print(date)
        fullmoon = next_full_moon(date)
        
    update.message.reply_text(f'Дата полнолуния: {fullmoon}')


cities = ['Абакан', 'Азов', 'Арзамас', 'Вологда', 'Владимир', 'Владивосток', 'Москва', 'Магадан', 'Магнитогорск', 'Новосибирск', 'Надым', 'Находка', 'Саратов', 'Самара', 'Санкт-петербург', 'Ростов', 'Рязань', 'Рыбинск', 'Казань', 'Киров', 'Кострома']

def citycut(c):
    
    c = c.lower().replace(" ","").capitalize()
    return c

def city_find(l, c):
    for one in c:  
        if l == list(one[0]):
            return one        


def cityplay(update,context):
    citylist = cities
    city = citycut(update.message.text)
    print(city)
    #print(citylist) #
    turn = 0
    if turn == 0:
        letter = list(city[0])
    
    while city in citylist and letter == list(city[0]):
        citylist.remove(city)
        letter = list(city[-1].capitalize())
        if letter == 'ь':
            letter = list(city[-2].capitalize())
        find_city = city_find(letter, citylist)
        turn += 1
        while find_city in citylist:
            letter == list(find_city[0])
            print(find_city)
            update.message.reply_text(f'{find_city}. Ваш ход:')
            letter = list(find_city[-1])
            if letter == 'ь':
                letter = list(city[-2].capitalize())
            citylist.remove(find_city)
            return None
        else:
            update.message.reply_text('Сдаюсь...')
            return None

        print(citylist) #
    else:
        update.message.reply_text('Ты проиграл!!!')

def calc(update, context):
    calc_text = update.message.text.replace(' ','')
    mathsymb = ['/', '*', '+', '-']

    for symb in mathsymb:
        calc_text = calc_text.replace(f'{symb}', f' {symb} ')

    calc_list = calc_text.split()
    try:
        while '/' in calc_list:
            for index, value in enumerate(calc_list):
                if value =='/':
                    calc_list[index-1] = float(calc_list[index-1])/float(calc_list[index+1])
                    del calc_list[index]
                    del calc_list[index]
        while '*' in calc_list:
            for index, value in enumerate(calc_list):
                if value =='*':
                    calc_list[index-1] = float(calc_list[index-1])*float(calc_list[index+1])
                    del calc_list[index]
                    del calc_list[index]
        while '+' in calc_list:
            for index, value in enumerate(calc_list):
                if value == '+':
                    calc_list[index-1] = float(calc_list[index-1])+float(calc_list[index+1])
                    del calc_list[index]
                    del calc_list[index]
        while '-' in calc_list:
            for index, value in enumerate(calc_list):
                if value =='-':
                    calc_list[index-1] = float(calc_list[index-1])-float(calc_list[index+1])
                    del calc_list[index]
                    del calc_list[index]
        update.message.reply_text(f'Ответ: {calc_list[0]}')
    except ZeroDivisionError:
        update.message.reply_text('На ноль делить нельзя! Проверьте условия.')
    except ValueError:
        update.message.reply_text('Нет чисел, введите правильное выражение')
 

    

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('stop', mode_control))
    dp.add_handler(CommandHandler('calc', mode_control))
    dp.add_handler(CommandHandler('wordcount', mode_control))
    dp.add_handler(CommandHandler('planet', mode_control))
    dp.add_handler(CommandHandler('nextfullmoon', mode_control))
    dp.add_handler(CommandHandler('cityplay', mode_control))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()