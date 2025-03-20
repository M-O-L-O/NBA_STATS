### The Adjacentanor

### Returns a list of strings adjacent to the inputted string in order to match the inputs
import numpy as np

class Adjacentator():
    def __init__(self, string):
        self.similar_words = self.similar(string)
        if len(string.split()) > 1:
            self.abbreviations = self.abbreviate(string)
        else:
            self.abbreviations = []
        self.switched_letters = self.switchLetters(string)
        self.deleted_letters = self.deleteLetters(self, string)
        self.replaced_letters = self.replaceLetters(self, string)
        self.inserted_letters = self.insertLetters(self, string)
        
        return np.unique(self.similar_words, self.abbreviations, self.switched_letters, self.deleted_letters, self.replaced_letters, self.inserted_letters)
    
    def similar(string):
        pass
    
    def abbreviate(string):
        words = string.split()
        abbr = ''
        for word in words:
            abbr+= word[0]
            
        return abbr
    
    def switchLetters(self, string):
        pass
    
    def deleteLetters(self, string):
        pass
    
    def replaceLetters(self, string):
        pass
    
    def insertLetters(self, string):
        pass