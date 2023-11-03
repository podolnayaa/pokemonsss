from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import random
import requests
from .models import Fight

from django.core.mail import send_mail
from django.core.validators import validate_email
from django import forms
from .forms import MailForm

import ftplib
import datetime

from django.core.cache import cache

Pokemons = []
selected_enemy = 0
rounds = 0
now_pok = 3
start = True
my_point = 0
enemy_point = 0



class Pokemon():
    def __init__(self, name, image, hp, attack, speed):
        self.name = name
        self.image = image
        self.hp = hp
        self.attack = attack
        self.speed = speed


def index(request):
    global start
    global now_pok
    BASE_URL = 'https://pokeapi.co/api/v2/pokemon'


    # Получаем список объектов для вывода на странице
    if start == True:
        for i in range(1,2):
            response = requests.get(f"{BASE_URL}/{i}").json()
            Pokemons.append(Pokemon(response['name'],
                                    response['sprites']['other']['dream_world']['front_default'],
                                    response['stats'][0]['base_stat'],
                                    response['stats'][1]['base_stat'],
                                    response['stats'][-1]['base_stat'],))
        start = False
        cache_key = f"my_model_page_None"
        cache.set(cache_key, Pokemons )

    print(start)
    # Создаем пагинатор с 10 объектами на странице
    paginator = Paginator(Pokemons, 6)

    # Получаем номер запрошенной страницы из GET-параметров
    page_number = request.GET.get('page')
    if (page_number is None):
        page_number = 1

    # Получаем объекты для текущей страницы
    page_obj = paginator.get_page(page_number)

    print("PAGE NUMBER:", page_number)
    # Проверяем, есть ли кеш для текущей страницы
    cache_key = f"my_model_page_{page_obj.number}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        # Если есть кеш, то используем его данные для вывода на странице
        print("CACHED_DATA")
        #page_obj.object_list = cached_data
    else:
        # Если кеша нет, то получаем данные и сохраняем их в кеш
        print("YES")
        Pokemons_new = []
        for i in range(now_pok,now_pok+6):
            response = requests.get(f"{BASE_URL}/{i}").json()
            Pokemons_new.append(Pokemon(response['name'],
                                response['sprites']['other']['dream_world']['front_default'],
                                response['stats'][0]['base_stat'],
                                response['stats'][1]['base_stat'],
                                response['stats'][-1]['base_stat'],))

        now_pok+=6
        print("ID следующего покемона:", now_pok)
        for i in range(len(Pokemons_new)):
            Pokemons.append(Pokemons_new[i])

        cache_key = f"my_model_page_{page_number}"
        cache.set(cache_key, Pokemons_new)
        #page_obj.object_list = Pokemons_new

    # Выводим объекты на страницу
    print(len(Pokemons))
    # Создаем пагинатор с 10 объектами на странице
    paginator = Paginator(Pokemons, 6)

    # Получаем объекты для текущей страницы
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {'page_obj': page_obj})



def show_pokemon(request, name):
    for i in range(len(Pokemons)):
        if (Pokemons[i].name == name):
            print(name)
            return render(request, "poke.html", context = {"Pokemon": Pokemons[i]})


def poke_fights(request, name):
    global selected_enemy
    global my_point
    global enemy_point

    if request.method == 'POST':
        fight = Fight.objects.all().last()
        my_point = fight.fighter_f
        enemy_point = fight.fighter_s

        if (my_point > 0 and enemy_point > 0 ):
            hit = (int)(request.POST.get("hit"))
            random_index = random.randint(0, 10)

            choosed_poke = []

            for i in range(len(Pokemons)):
                if (Pokemons[i].name == name):
                    choosed_poke.append(Pokemons[i])
                    break

            choosed_poke.append(Pokemons[selected_enemy])
            choosed_names = [p.name for p in choosed_poke]
            choosed_attack = [p.attack for p in choosed_poke]
            choosed_hp = [p.hp for p in choosed_poke]

            fight = Fight.objects.all().last()
            print("FIGHT")

            if ((hit%2==1 and random_index%2==1) or (hit%2==0 and random_index%2==0)):


                fight.fighter_s = fight.fighter_s - choosed_poke[0].attack
                print(fight.fighter_s)
                my_point = fight.fighter_f
                enemy_point = fight.fighter_s
                fight.save()
                textt = "Выйграл боец игрока"

            else:


                fight.fighter_f = fight.fighter_f - choosed_poke[1].attack
                print(fight.fighter_f)
                my_point = fight.fighter_f
                enemy_point = fight.fighter_s

                fight.save()
                textt = "Выйграл боец компьютера"



            return render(request, 'poke_fights.html', {"Pokemons": choosed_poke, "Names": choosed_names, "Hps":choosed_hp, "Attacks":choosed_attack, "Result": textt } )
        else:
            fight = Fight.objects.all().last()
            fight.fighter_f = my_point
            fight.fighter_s = enemy_point
            fight.save()

            if(my_point>enemy_point):
                return render(request, 'end.html', {"End": "Бой завершен, победа за Вами!"} )
            else:
                return render(request, 'end.html', {"End": "Бой завершен, победа за Компьютером!"} )




    else: #если мы просто выводим файт

        my_point = 0
        enemy_point = 0

        choosed_poke = []

        for i in range(len(Pokemons)):
            if (Pokemons[i].name == name):
                choosed_poke.append(Pokemons[i])
                break

        selected_enemy = random.randint(0, len(Pokemons) - 1)

        while(Pokemons[selected_enemy].name==choosed_poke[0].name):
            selected_enemy = random.randint(0, len(Pokemons) - 1)
        choosed_poke.append(Pokemons[selected_enemy])
        choosed_names = [p.name for p in choosed_poke]
        choosed_attack = [p.attack for p in choosed_poke]
        choosed_hp = [p.hp for p in choosed_poke]

        fight = Fight(fighter_f=choosed_poke[0].hp, fighter_s=choosed_poke[1].hp)
        fight.save()

        return render(request, 'poke_fights.html', {"Pokemons": choosed_poke, "Names": choosed_names, "Hps":choosed_hp, "Attacks":choosed_attack,  "Result":"Здесь будет выведен результат каждого раунда",} )

    return 0

def poke_fast_fight(request, name):
    global rounds
    if request.method == 'GET':
        rounds = 0

        text = []
        choosed_poke = []

        for i in range(len(Pokemons)):
            if (Pokemons[i].name == name):
                choosed_poke.append(Pokemons[i])
                break

        selected_enemy = random.randint(0, len(Pokemons) - 1)

        while(Pokemons[selected_enemy].name==choosed_poke[0].name):
            selected_enemy = random.randint(0, len(Pokemons) - 1)
        choosed_poke.append(Pokemons[selected_enemy])

        fight = Fight(fighter_f=choosed_poke[0].hp, fighter_s=choosed_poke[1].hp)
        while(fight.fighter_f > 0 and fight.fighter_s > 0):
            random_index_f = random.randint(0, 10)
            random_index_s = random.randint(0, 10)

            if ((random_index_s%2==1 and random_index_f%2==1) or (random_index_f%2==0 and random_index_s%2==0)):
                fight.fighter_s = fight.fighter_s - choosed_poke[0].attack
                text.append("В раунде выйграл боец игрока")
                rounds +=1
                fight.save()
                fight = Fight.objects.all().last()

            else:

                fight.fighter_f = fight.fighter_f - choosed_poke[1].attack
                text.append("В раунде выйграл боец компьютера")
                rounds +=1
                fight.save()
                fight = Fight.objects.all().last()


        fight.save()

        mailform = MailForm()
        return render(request, 'fast_end.html', {"End": text, "Form": mailform, "Flag": 1} )

    else:
        fight = Fight.objects.all().last()
        new_mail = request.POST.get("email")

        subject = 'Результат боя №'+str(fight.fightid)
        if fight.fighter_f <=0:
            message = "Победа Компьютера!"+"\n"+"Всего раундов: "+str(rounds)\
                      +"\n"+"Оставшееся здоровье персонажа Игрока: "+ str(fight.fighter_f)+"\n"\
                      +"Оставшееся здоровье персонажа Компьютера: "+str(fight.fighter_s)+"\n"
        else:
            message = "Победа Игрока!"+"\n"+"Всего раундов: "+str(rounds) \
                      +"\n"+"Оставшееся здоровье персонажа Игрока: "+str(fight.fighter_f)+"\n" \
                      +"Оставшееся здоровье персонажа Компьютера: "+ str(fight.fighter_s)+"\n"

        recipient_list = [new_mail]

        send_mail(subject, message, recipient_list=recipient_list, from_email="")

        mailform = MailForm()
        return render(request, 'fast_end.html', {"End": ["Письмо отправлено!"], "Form": mailform, "Flag": 0 } )
    return 0

def convert_to_markdown(checkbox1, checkbox2, checkbox3, poke):

    result = f"# Имя покемона: {poke.name}\n\n"
    if checkbox1:
        result += f"Аттака: {poke.attack}\n\n"

    if checkbox2:
        result += f"Здоровье: {poke.hp}\n\n"

    if checkbox3:
        result += f"Скорость: {poke.speed}\n\n"
    return result

def poke_save_info(request, name):
    if request.method == 'GET':
        choosed_poke =0

        for i in range(len(Pokemons)):
            if (Pokemons[i].name == name):
                choosed_poke = Pokemons[i]
                break
        return render(request, 'ftp_sending.html', {"P": choosed_poke} )

    else:
        checkbox1 = request.POST.get('checkbox1')
        checkbox2 = request.POST.get('checkbox2')
        checkbox3 = request.POST.get('checkbox3')

        choosed_poke =0

        for i in range(len(Pokemons)):
            if (Pokemons[i].name == name):
                choosed_poke = Pokemons[i]
                break

        current_date = datetime.datetime.now().strftime('%Y%m%d')
        markdown_text = convert_to_markdown(checkbox1, checkbox2, checkbox3, choosed_poke)
        print(markdown_text)

        FTP_HOST = "127.0.0.1"
        FTP_USER = "Svetik"
        FTP_PASS = "12345"

        # connect to the FTP server
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        # force UTF-8 encoding
        ftp.encoding = "utf-8"

        file_list_fol = ftp.nlst()
        if current_date in file_list_fol:

            file_list = ftp.nlst(current_date)
            filename = str(name)+"_pokemon.md"
            if filename in file_list:
                print(f'Файл уже существует')
            else:
                ftp.cwd(current_date)
                with open(filename, "wb") as file:

                    file.write(markdown_text.encode())
                ftp.storbinary(f"STOR {filename}", open(filename, 'rb'))

        else:

            ftp.mkd(current_date)
            ftp.cwd(current_date)
            filename = str(name)+"_pokemon.md"

            with open(filename, "wb") as file:

                file.write(markdown_text.encode())


            ftp.storbinary(f"STOR {filename}", open(filename, 'rb'))


        ftp.quit()

        return render(request, "poke.html", context = {"Pokemon": choosed_poke })


    return 0