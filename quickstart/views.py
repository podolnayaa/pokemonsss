from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import random
import requests
from .models import Fight
from django.db.models import F

Pokemons = []
selected_enemy = 0
rounds = 0
now_page = 8
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
    global now_page
    global start
    BASE_URL = 'https://pokeapi.co/api/v2/pokemon'

    if(start == True):
        for i in range(1,8):
            response = requests.get(f"{BASE_URL}/{i}").json()
            Pokemons.append(Pokemon(response['name'],
                                    response['sprites']['other']['dream_world']['front_default'],
                                    response['stats'][0]['base_stat'],
                                    response['stats'][1]['base_stat'],
                                    response['stats'][-1]['base_stat'],))
        start = False


    paginator = Paginator(Pokemons, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if (page_obj.number == paginator.page_range[-1]):
        for i in range(now_page,now_page+7):
            response = requests.get(f"{BASE_URL}/{i}").json()
            Pokemons.append(Pokemon(response['name'],
                                    response['sprites']['other']['dream_world']['front_default'],
                                    response['stats'][0]['base_stat'],
                                    response['stats'][1]['base_stat'],
                                    response['stats'][-1]['base_stat'],))
        now_page = now_page+6
    #print(len(Pokemons))

    paginator = Paginator(Pokemons, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {'page_obj': page_obj})



def show_pokemon(request, name):
    for i in range(len(Pokemons)):
        if (Pokemons[i].name == name):
            print(name)
            return render(request, "poke.html", context = {"Pokemon": Pokemons[i]})


def poke_fights(request, name):
    global selected_enemy
    global rounds
    global my_point
    global enemy_point

    if request.method == 'POST':
        fight = Fight.objects.all().last()
        my_point = fight.fighter_f
        enemy_point = fight.fighter_s

        if (my_point > 0 and enemy_point > 0 ):
            textt = "hhhh"
            hit = (int)(request.POST.get("hit"))
            random_index = random.randint(0, 10)

            choosed_poke = []
            choosed_names = []
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
                rounds = rounds-1
            else:


                fight.fighter_f = fight.fighter_f - choosed_poke[1].attack
                print(fight.fighter_f)
                my_point = fight.fighter_f
                enemy_point = fight.fighter_s

                fight.save()
                textt = "Выйграл боец компьютера"
                rounds = rounds-1


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
        rounds = 3
        my_point = 0
        enemy_point = 0

        choosed_poke = []
        choosed_names = []
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
        print(rounds)
        return render(request, 'poke_fights.html', {"Pokemons": choosed_poke, "Names": choosed_names, "Hps":choosed_hp, "Attacks":choosed_attack,  "Result":"Здесь будет выведен результат каждого раунда",} )

    return 0