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

    def __init__(self, table = [], cp = 'blue', table_width = 11):
        '''init
        :param list table: table data set
        :param str cp: Current player set
        :param int table_width: Table width
        '''
        #back to default 11x11 if issue with dimendions
        if table_width == None:
            table_width = self.TABLE_MAX_WIDTH
        if table_width % 2 == 0:
            table_width = self.TABLE_MAX_WIDTH
        self.TABLE_MAX_WIDTH = table_width
        #init start/end cells
        self.__init_start_cells()
        self.__init_end_cells()
        #set current player
        self.current_player = cp
        #table init with starting colors and empty spaces for links
        if table:
            self.table_data = table
        else:
            self.__init_table()

    def __init_start_cells(self):
        '''init start cells for players'''
        self.START = {
                self.PLAYER_1: [
                    (0, x) for x in range(self.TABLE_MAX_WIDTH - 1) if x % 2 > 0
                    ],
                self.PLAYER_2: [
                    (x, 0) for x in range(self.TABLE_MAX_WIDTH - 1) if x % 2 > 0
                    ],
                }

    def __init_end_cells(self):
        '''init end cells for players'''
        self.END = {
                self.PLAYER_1: [
                    (self.TABLE_MAX_WIDTH - 1, x)
                    for x in range(self.TABLE_MAX_WIDTH - 1) if x % 2 > 0
                    ],
                self.PLAYER_2: [
                    (x, self.TABLE_MAX_WIDTH - 1)
                    for x in range(self.TABLE_MAX_WIDTH - 1) if x % 2 > 0
                    ],
                }

    def __init_table(self):
        '''init table'''
        self.table_data = [
                ['' for i in range(self.TABLE_MAX_WIDTH)]
                for b in range(self.TABLE_MAX_WIDTH)
                ]
        pos = 0 #position
        player = self.PLAYER_2
        for i in range(self.TABLE_MAX_WIDTH):
            if player == self.PLAYER_1:
                player = self.PLAYER_2
            else:
                player = self.PLAYER_1
            for b in range(self.TABLE_MAX_WIDTH):
                pos = pos + 1
                #corners
                if i == 0 and b == 0:
                    self.table_data[i][b] = self.CORNER
                if i == self.TABLE_MAX_WIDTH - 1\
                        and b == self.TABLE_MAX_WIDTH - 1:
                            self.table_data[i][b] = self.CORNER
                if i == self.TABLE_MAX_WIDTH - 1 and b == 0:
                    self.table_data[i][b] = self.CORNER
                if i == 0 and b == self.TABLE_MAX_WIDTH - 1:
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
        :param string move_coord: Move coordinates ("x_y")
        :return bool: Returns True if game ended
        '''
        #move (protected on input as buttons do not show if already selected)
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
            if self.__check_nodes(s, s):
                #set all empty links to empty for display results
                for i in range(self.TABLE_MAX_WIDTH):
                    for b in range(self.TABLE_MAX_WIDTH):
                        if not self.table_data[i][b]:
                            self.table_data[i][b] = 'X'
                return True
        return False

    def __check_node(self, x, y, coor):
        '''check single node
        :param int x: Coordinate X
        :param int y: Coordinate Y
        :param list coord: Cooridinates to check
        :return bool: Returns True if path is to the end
        '''
        if self.table_data[x][y].lower() == self.current_player:
            if (x, y) in self.END[self.current_player]:
                return True
            else:
                if self.__check_nodes([x, y], coor):
                    return True
        return False

    def __check_nodes(self, coor, prev):
        '''check nodes from start to end
        :param list coord: Cooridinates to check
        :param list prev: previous cooridinates
        :return bool: Returns True if path is to the end
        '''
        x = coor[0]
        y = coor[1]
        #check all sides of current active cell
        if x + 1 < self.TABLE_MAX_WIDTH and x + 1 > prev[0]:
            if self.__check_node(x+1, y, prev):
                return True
        if x - 1 >= 0 and x - 1 < prev[0]:
            if self.__check_node(x-1, y, prev):
                return True
        if y + 1 < self.TABLE_MAX_WIDTH and y + 1 > prev[1]:
            if self.__check_node(x, y+1, prev):
                return True
        if y - 1 >= 0 and y-1 < prev[1]:
            if self.__check_node(x, y-1, prev):
                return True
        return False

