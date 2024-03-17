from . import main 
from flask import render_template, request
import requests
from . import main 
from .forms import PokeForm



@main.route('/')
def home():
    return render_template('home.html')

# @main.route('/user/<name>')
# def user(name):
#     return f'Hello {name}'

def poke_dic(pokemons):
    pokemon_dictionary = []
    for pokemon in pokemons:
        pokemon_dict = getPokenInfo(pokemon)
        pokemon_dictionary.append(pokemon_dict)
    return pokemon_dictionary

def getPokenInfo(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return {
            "name": data['name'],
            "ability": data['abilities'][0]['ability']['name'],
            "base_exp": data['base_experience'],
            "sprite_url": data['sprites']['back_default']
        }
    
@main.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokeForm()
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        pokemon_go = getPokenInfo(pokemon)
        return render_template('pokemon.html', pokemon=pokemon_go)
    else:
        return render_template('pokemon.html', form=form)
    

