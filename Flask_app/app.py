from flask import Flask, request, render_template
import requests


app = Flask(__name__)

@app.route('/')
def hello_thieves():
    return "<p> Hello Thieves!! </p>" 

@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return f'{email} {password}'
    else:
        return render_template('login.html')
    
def poke_dic(pokemons):
    pokemon_dictionary = []
    for pokemon in pokemons:
        pokemon_dict = getPokenInfo(pokemon)
        pokemon_dictionary.append(pokemon_dict)
        # print(f"Name: {pokemon_dict['name']} \nAbility: {pokemon_dict['abilitiy']} \nBase Experience: {pokemon_dict['base_exp']}\n Sprite: {pokemon_dict['sprite_url']}\n")
    return pokemon_dictionary

def getPokenInfo(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        # pokemon_dict = poke_dic(data)
        # print(f"Name: {pokemon_dict['name']} \nAbility: {pokemon_dict['abilities'][0]['ability']['name']} \nBase Experience: {pokemon_dict['base_xp']}\n")
        return {
            "name": data['name'],
            "abilitiy": data['abilities'][0]['ability']['name'],
            "base_exp": data['base_experience'],
            "sprite_url": data['sprites']['back_default']
        }
    

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemons = requests.form.get('pokemon')
        poke_dic(pokemons)
        return render_template('pokemon.html', pokemons=pokemons)
    else:
        return render_template('pokemon.html')




#         }
#     return {}

# poke_dic([5,1])

# @app.route('/pokemon', methods=['GET', 'POST'])
# def pokemon():
#     if requests.method == 'POST':
#         return 'Something'
#     else:
#         return render_template('login.html')






