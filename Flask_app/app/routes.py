from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from .forms import LoginForm, SignUpForm, PokeForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


@app.route('/')
def home():
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

        queried_user = User.quety.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Welcome {queried_user.username}!' 'info')
            login_user(queried_user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username email or password')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username, email, password)
        new_user.save()
        flash('Success! Thank you for Signing Up', 'success')
        return redirect(url_for('login'))
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