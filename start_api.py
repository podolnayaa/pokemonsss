import requests
BASE_URL = 'https://pokeapi.co/api/v2'
response = requests.get(f"{BASE_URL}/pokemon/ditto")
print(response.json())