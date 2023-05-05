# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:01:15 2023

@author: mathi
"""

class Element():
    def __init__(self,coord):
        self.next = None
        self.coord = coord
        
    def setNext(self,element):
        self.next = element