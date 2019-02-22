#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Bojan"
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Bojan"

from flask import render_template, request, redirect, url_for, session
from app import app
from app.game import GaleGame

@app.route('/')
@app.route('/index')
def index():
    '''index'''
    table = session.get('table', None)
    player = session.get('player', None)
    #set default player
    if not player:
        player = 'blue'
    game = GaleGame(table=table, cp=player)
    session['table'] = game.table
    session['player'] = game.current_player
    return render_template('index.html', table=game.table,
        player=game.current_player)

@app.route('/move', methods=['POST'])
def move():
    '''move'''
    if request.method == 'POST':
        move = request.form['move-button']
        player = session.get('player', None)
        table = session.get('table', None)
        game = GaleGame(table=table, cp=player)
        if game.move(move):
            return render_template('index.html', table=game.table,
                player=game.current_player, win=game.current_player)
        session['player'] = game.current_player
        session['table'] = game.table
    return redirect('/index')

@app.route('/new')
def new_game():
    '''new game'''
    if 'table' in session:
        del session['table']
    if 'player' in session:
        del session['player']
    return redirect ('/index')


