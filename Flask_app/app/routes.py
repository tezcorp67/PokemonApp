from flask import request, render_template
import requests
from app import app
from .forms import PokeForm


@app.route('/')
def hello_thieves():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    else:
        return render_template('login.html', form=form)
    
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
            "abilitiy": data['abilities'][0]['ability']['name'],
            "base_exp": data['base_experience'],
            "sprite_url": data['sprites']['back_default']
        }
    

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        getPokenInfo(pokemon)
        return render_template('pokemon.html', pokemon=pokemon)
    else:
        return render_template('pokemon.html')