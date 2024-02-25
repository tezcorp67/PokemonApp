from . import post 
from flask import render_template, request, redirect, url_for, flash
import requests
from app.blueprints.main.forms import PokeForm
from flask_login import login_required, current_user
from app.models import Post, db


# select_pokemon_route
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
            "name": data['name'].title(),
            "ability": data['abilities'][0]['ability']['name'],
            "base_exp": data['base_experience'],
            "sprite_url": data['sprites']['front_shiny'],
            "base_hp": data['stats'][0]['base_stat'],
            "base_attack": data['stats'][1]['base_stat'],
            "base_defense": data['stats'][2]['base_stat']

        }
    
@post.route('/select_pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit:
        pokemon = request.form.get('pokemon')
        pokemon_go = getPokenInfo(pokemon)
        # select_pokemon = form.select_pokemon.data
        # save pokemon here
        saved_pokemon = Post(pokemon_go['name'], pokemon_go['base_exp'], pokemon_go['base_hp'], pokemon_go['ability'], pokemon_go['base_attack'], pokemon_go['base_defense'], pokemon_go['sprite_url'])
        saved_pokemon.save()
        flash('Pokemon Successfully Saved!')

        return render_template('pokemon.html', pokemon=pokemon_go)
    else:
        return render_template('select_pokemon.html', form=form)

# pokemon_battle_route

# delete_pokemon_route

# edit_pokemon_route