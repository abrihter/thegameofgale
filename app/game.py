#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Bojan"
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Bojan"

from flask import render_template, request, redirect, url_for
from app import app

class GaleGame:
    '''gale game class'''
    TABLE_MAX_WIDTH = 11
    CORNER = 'X'
    PLAYER_1 = 'blue'
    PLAYER_2 = 'red'
    #start cells
    START = {
        'blue': [[0, 1], [0,3], [0,5], [0,7], [0,9]],
        'red' : [[1, 0], [3,0], [5,0], [7,0], [9,0]],
    }
    #end cells
    END = {
        'blue': ['10,1', '10,3', '10,5', '10,7', '10,9'],
        'red' : ['1,10', '3,10', '5,10', '7,10', '9,10'],
    }

    def __init__(self, table = [], cp = 'blue'):
        '''init
        :param list table: table data set
        :parma str cp: Current player set
        '''
        self.current_player = cp
        #table init with starting colors and empty spaces for links
        if table:
            self.table_data = table
        else:
            self.table_data = [
                ['' for i in range(self.TABLE_MAX_WIDTH)]
                    for b in range(self.TABLE_MAX_WIDTH)
            ]
            pos = 0 #position
            player = self.PLAYER_2
            for i in range(11):
                if player == self.PLAYER_1:
                    player = self.PLAYER_2
                else:
                    player = self.PLAYER_1
                for b in range(11):
                    pos = pos + 1
                    #corners
                    if i == 0 and b == 0:
                        self.table_data[i][b] = self.CORNER
                    if i == 10 and b == 10:
                        self.table_data[i][b] = self.CORNER
                    if i == 10 and b == 0:
                        self.table_data[i][b] = self.CORNER
                    if i == 0 and b == 10:
                        self.table_data[i][b] = self.CORNER
                    if self.table_data[i][b] == self.CORNER:
                        continue
                    #table generate
                    if pos % 2 == 0:
                        self.table_data[i][b] = player

    @property
    def table(self):
        '''table'''
        return self.table_data

    def move(self, move_coord):
        '''make move
        :param list move_coord: Move coordinates
        :return bool: Returns True if game ended
        '''
        #move (protected on input as buttons do not show)
        mv = move_coord.split('_')
        self.table[int(mv[0])][int(mv[1])] = self.current_player.upper()
        if self.check_end():
            return True
        #switch player
        if self.current_player == self.PLAYER_1:
            self.current_player = self.PLAYER_2
        else:
            self.current_player = self.PLAYER_1
        return False


    def check_end(self):
        '''check if game is finished
        :return bool: Return True if game ended
        '''
        for s in self.START[self.current_player]:
            if self._check_nodes(s, s):
                #set all empty links to empty for display results
                for i in range(self.TABLE_MAX_WIDTH):
                    for b in range(self.TABLE_MAX_WIDTH):
                        if not self.table_data[i][b]:
                            self.table_data[i][b] = 'X'
                return True
        return False

    def _check_nodes(self, coor, prev):
        '''check nodes from start to end
        :param list coord: Cooridinates to check
        :param list prev: previous cooridinates
        :return bool: Returns True if path is to the end
        '''
        x = coor[0]
        y = coor[1]
        #check all sides of current active cell
        if x + 1 < self.TABLE_MAX_WIDTH and x+1 > prev[0]:
            if self.table_data[x+1][y].lower() == self.current_player:
                if '{},{}'.format(x+1, y) in self.END[self.current_player]:
                    return True
                else:
                    if self._check_nodes([x+1, y], coor):
                        return True
        if x - 1 >= 0 and x-1 < prev[0]:
            if self.table_data[x-1][y].lower() == self.current_player:
                if '{},{}'.format(x-1, y) in self.END[self.current_player]:
                    return True
                else:
                    if self._check_nodes([x-1, y], coor):
                        return True
        if y + 1 < self.TABLE_MAX_WIDTH and y+1 > prev[1]:
            if self.table_data[x][y+1].lower() == self.current_player:
                if '{},{}'.format(x, y+1) in self.END[self.current_player]:
                    return True
                else:
                    if self._check_nodes([x, y+1], coor):
                        return True
        if y - 1 >= 0 and y-1 < prev[1]:
            if self.table_data[x][y-1].lower() == self.current_player:
                if '{},{}'.format(x, y-1) in self.END[self.current_player]:
                    return True
                else:
                    if self._check_nodes([x, y-1], coor):
                        return True
        return False

