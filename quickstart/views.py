from django.http import HttpResponse
from django.shortcuts import render
import requests
pokemon_names = []
def index(request):

    BASE_URL = 'https://pokeapi.co/api/v2'
    response = requests.get(f"{BASE_URL}/pokemon?limit=100000&offset=0").json()

    for r in response["results"]:
        pokemon_names.append(r["name"])

    return render(request, "index.html", {'pokemons' : pokemon_names})

def search_pokemons(request):
    if request.method == 'GET':
        query = request.GET.get('pokemon')
        pokemon_namess = []
        for p in pokemon_names:
            if query in p:
                pokemon_namess.append(p)
        return render(request, "index.html", {'pokemons' : pokemon_namess})