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
        query_poke = Post.query.filter(Post.name == pokemon).first()
        if not query_poke: 
        # select_pokemon = form.select_pokemon.data
        # save pokemon here
            pokemon_go = getPokenInfo(pokemon)
            saved_pokemon = Post(name = pokemon_go['name'], base_exp = pokemon_go['base_exp'], base_hp = pokemon_go['base_hp'], ability = pokemon_go['ability'], base_attack = pokemon_go['base_attack'], base_defense = pokemon_go['base_defense'], sprite_url = pokemon_go['sprite_url'])
            saved_pokemon.save()
            flash('Pokemon Successfully Saved!')
            return render_template('pokemon.html', pokemon=pokemon_go)
        return render_template('pokemon.html', pokemon=query_poke)
    else:
        return render_template('select_pokemon.html', form=form)
    
# post.route('/add_team/<user_id>')
# @login_required
# def add_team(user_id):
#     user = User.query.get(user_id)
#     current_user.team.append(user)
#     db.session.commit()
#     flash(f'Added Pokemon')
#     return redirect(url_for('main.connect'))

# post.route('/remove_team/<user_id>')
# @login_required
# def remove_team(user_id):
#     user = User.query.get(user_id)
#     current_user.team.remove(user)
#     db.session.commit()
#     flash(f'Removed Pokemon')
#     return redirect(url_for('main.connect'))

# @post.route('/select_pokemon', methods=['GET', 'POST'])
# @login_required
# def select_pokemon():
#     form = PokeForm()
#     if form.validate_on_submit():
#         pokemon_name = form.poke_search.data
#         if len(current_user.team) < 6:
#             add_pokemon_to_team(pokemon_name)
#         else:
#             flash('Team already full!')
#         return redirect(url_for('main.connect'))
#     return render_template('select_pokemon.html', form=form, user=current_user)


# def add_pokemon_to_team(pokemon_name):
#     pokemon = Post.query.filter_by(name=pokemon_name).first()
#     if not pokemon:
#         pokemon = get_poken_info(pokemon_name)
#         save_pokemon(pokemon)
#     current_user.team.append(pokemon)
#     db.session.commit()
#     flash(f'Added {pokemon_name} to your team!')

# def remove_pokemon_to_team(pokemon_name):
#     pokemon = Post.query.filter_by(name=pokemon_name).first()
#     if not pokemon:
#         pokemon = get_poken_info(pokemon_name)
#         save_pokemon(pokemon)
#     current_user.team.remove(pokemon)
#     db.session.commit()
#     flash(f'Removed {pokemon_name} from your team!')


# def get_poken_info(pokemon_name):
#     pokemon_info = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/').json()
#     return pokemon_info


# def save_pokemon(pokemon_info):
#     saved_pokemon = Post(
#         name=pokemon_info['name'],
#         base_exp=pokemon_info['base_experience'],
#         base_hp=pokemon_info['stats'][0]['base_stat'],
#         ability=pokemon_info['abilities'][0]['ability']['name'],
#         base_attack=pokemon_info['stats'][1]['base_stat'],
#         base_defense=pokemon_info['stats'][2]['base_stat'],
#         sprite_url=pokemon_info['sprites']['front_default']
#     )
#     saved_pokemon.save()


# pokemon_battle_route

# delete_pokemon_route

# edit_pokemon_route