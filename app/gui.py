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
@app.route('/index/<int:dimensions>')
def index(dimensions=None):
    '''index'''
    table = session.get('table', None)
    player = session.get('player', None)
    if dimensions == None:
        dimensions = GaleGame.TABLE_MAX_WIDTH
        return new_game(dimensions)
    #set default player
    if not player:
        player = GaleGame.PLAYER_1
    game = GaleGame(table=table, cp=player, table_width=dimensions)
    session['table'] = game.table
    session['player'] = game.current_player
    session['dimensions'] = game.TABLE_MAX_WIDTH
    return render_template('index.html', table=game.table,
        player=game.current_player, dimensions=game.TABLE_MAX_WIDTH)

@app.route('/move', methods=['POST'])
def move():
    '''move'''
    if request.method == 'POST':
        move = request.form['move-button']
        player = session.get('player', None)
        table = session.get('table', None)
        dimensions = session.get('dimensions', None)
        game = GaleGame(table=table, cp=player, table_width=dimensions)
        if game.move(move):
            return render_template('index.html', table=game.table,
                player=game.current_player, dimensions=game.TABLE_MAX_WIDTH,
                win=game.current_player)
        session['player'] = game.current_player
        session['table'] = game.table
        session['dimensions'] = game.TABLE_MAX_WIDTH
    return redirect('/index/{}'.format(dimensions))

@app.route('/new/<int:dimensions>')
def new_game(dimensions):
    '''new game'''
    if 'table' in session:
        del session['table']
    if 'player' in session:
        del session['player']
    return redirect ('/index/{}'.format(dimensions))


