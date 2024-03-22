from . import post 
from flask import render_template, request, redirect, url_for, flash
import requests
from app.blueprints.main.forms import PokeForm
from flask_login import login_required, current_user
from app.models import Post, db, User


# select_pokemon_route
def poke_dic(pokemons):
    pokemon_dictionary = []
    for pokemon in pokemons:
        pokemon_dict = getPokenInfo(pokemon)
        pokemon_dictionary.append(pokemon_dict)
    return pokemon_dictionary

def getPokenInfo(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return {
            "name": data['name'].lower(),
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
        pokemon = request.form.get('pokemon').lower()
        query_poke = Post.query.filter_by(name = pokemon).first()
        if not query_poke: 
        # select_pokemon = form.select_pokemon.data
        # save pokemon here
            pokemon_go = getPokenInfo(pokemon)
            saved_pokemon = Post(name = pokemon_go['name'], base_experience = pokemon_go['base_exp'], base_hp = pokemon_go['base_hp'], ability = pokemon_go['ability'], base_attack = pokemon_go['base_attack'], base_defense = pokemon_go['base_defense'], sprite_url = pokemon_go['sprite_url'])
            saved_pokemon.save()
            flash('Pokemon Successfully Saved!')
            return render_template('select_pokemon.html', pokemon=pokemon_go)
        return render_template('select_pokemon.html', pokemon=query_poke)
    else:
        return render_template('select_pokemon.html', form=form)
    


@post.route("/catch_pokemon/<name>", methods=["GET", "POST"])
@login_required
def catch_pokemon(name):
    print(name)
    pokemon = Post.query.filter_by(name=name).first()
    if len(current_user.team.all()) < 6 and pokemon not in current_user.team:
        current_user.team.append(pokemon)
        db.session.commit()
    return redirect(url_for('post.team'))

@post.route("/remove_pokemon/<name>", methods=["GET", "POST"])
@login_required
def remove_pokemon(name):
    print(name)
    pokemon = Post.query.filter_by(name=name).first()
    current_user.team.remove(pokemon)
    db.session.commit()
    return redirect(url_for('post.team'))

@post.route("/team")
@login_required
def team():
    return render_template('team.html', team=current_user.team.all())



# pokemon_battle_route

# delete_pokemon_route

# edit_pokemon_route