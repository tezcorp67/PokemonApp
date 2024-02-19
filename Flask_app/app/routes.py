from flask import request, render_template
import requests
from app import app
from .forms import LoginForm, SignUpForm, PokeForm


@app.route('/')
def hello_thieves():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        return f'{username} {email} {password}'
    else:
        return render_template('signup.html', form=form)
    
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
    
@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokeForm()
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        pokemon_go = getPokenInfo(pokemon)
        return render_template('pokemon.html', pokemon=pokemon_go)
    else:
        return render_template('pokemon.html', form=form)