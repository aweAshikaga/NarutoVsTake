#! usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Player(object):
    """
    Base player class which contains all the stuff that Naruto and Take
    share.
    """
    def __init__(self):
        self.score = 0
    
    def addToScore(self, amount):
        """
        Adds the amount to the score.
        
        Args:
            amount (int): the number to add to the score
        
        Returns:
            the score as an integer
        """
        self.score = self.score + amount
        return self.score
    
    def setScore(self, newValue):
        """
        Sets the score to the new Value
        
        Args:
            newValue (int): the number to set the score to
        
        Returns:
            the score as an integer
        """
        self.score = newValue
        return self.score
    
    def getScore(self):
        """
        Returns the score
        
        Args:
            no arguments
            
        Returns:
            self.score (int): the score of the player
        """
        
        return self.score
