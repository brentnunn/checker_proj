
from __future__ import absolute_import
import logging
import random
import checkerboard as cb
import checker as ch
from player import Player
from copy import deepcopy


logger = logging.getLogger(__name__)


class ComputerPlayer(Player):
    u""" Computer based Player for the game of Checkers """

    def __init__(self):
        Player.__init__(self)
        random.seed()
        logger.info(u'Initialized player {}'.format(self.__repr__()))
        logger.setLevel(logging.INFO)


    def list_jumps(self):
        u""" Return list of all available jumps """

        jumps_list = []
        for ch in self.checkers:
            jumps = ch.list_jumps()
            if jumps:
                jumps_list.extend(deepcopy(jumps))

        random.shuffle(jumps_list)

        logger.debug(u'list_jumps({})'.format(jumps_list))

        return jumps_list


    def list_moves(self):
        u""" Returns list of all available checker moves """

        moves_list = []
        for ch in self.checkers:
            moves = ch.list_moves()
            if moves:
                moves_list.extend(deepcopy(moves))

        random.shuffle(moves_list)

        logger.debug(u'list_moves({})'.format(moves_list))

        return moves_list


    def move_checker(self, move_squares):
        u""" Move checker at move_squares[0] to move_squares[1] """

        logger.debug(u'move_checker({})'.format(move_squares))

        self.checkerboard.get_checker(move_squares[0]).move(move_squares[1])


    def jump_checkers(self, jump_squares):
        u""" The checker at jump_squares[0] will jump to the other squares in the list.
            This will execute all jumps in the list. """

        logger.debug(u'jump_checkers({})'.format(jump_squares))

        self.checkerboard.get_checker(jump_squares[0]).jump_chain(jump_squares)


    def evaluate_board(self):
        u""" Evaluate the checkerboard, to determine next move """

        jumps_list = self.list_jumps()
        if jumps_list:
            return (u'jump', random.choice(jumps_list))

        moves_list = self.list_moves()
        if moves_list:
            return (u'move', random.choice(moves_list))

        return (u'surrender',)


    def play(self):
        u""" Determine action in game of checkers """

        if self.checkers == self.checkerboard.black_checkers:
            color = u'Black'
        else:
            color = u'White'

        evaluation = self.evaluate_board()
        if evaluation[0] == u'jump':
            self.jump_checkers(evaluation[1])
            #print("{} jump move completed".format(color))
            logger.info(u'play(): {} jump move completed'.format(color))
            return u"jump"

        elif evaluation[0] == u'move':
            self.move_checker(evaluation[1])
            #print("{} move completed".format(color))
            logger.info(u'play(): {} move completed'.format(color))
            return u"move"

        else:
            #print("{} surrenders".format(color))
            logger.info(u'play(): {} surrenders'.format(color))
            return u"surrender"

