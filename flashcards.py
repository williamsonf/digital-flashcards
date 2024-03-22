'''
Created on Mar 21, 2024

@author: Fred
'''
import os, csv, random

class FlashcardDeck():
    '''
    Attributes-
        card_cats
        
        cards
        
        deck
        
    Methods-
        build_deck
        
        draw
        
        deck_count
        
        discard
        
        curr_place
            int. our current index in the discard pile.
    '''


    def __init__(self, paths):
        '''
        Constructs the deck of flashcards from a set of csv files. The flashcards
        are categorized based on the csv file they are drawn from, allowing for
        separation between topics.
        
        Args-
            paths (list(str)): List of filepaths, formatted as strings, targeting
                csv files containing flash card labels and questions. First field
                is the 'front' of the card, second field is 'back', third field is
                an image which may be used in place of the front text.
                As so:
                    "What is the air speed velocity of an unladen swallow?","African or European swallow?","monty.png"
        '''
        self.card_cats = {} #We start by separating the cards into categories as we read them.
        for p in paths: #Categories are dictated by csv file - one csv file is one category
            category = os.path.splitext(p)[0].split('/')[-1]
            self.card_cats[category] = {}
            with open(p) as f:
                csv_reader = csv.reader(f)
                for line in csv_reader:
                    self.card_cats[category][line[0]] = line[1:]
        
        self.cards = {} #Then we construct one big pile, combining all categories.            
        for cat in self.card_cats.keys():
            for card in self.card_cats[cat].keys():
                self.cards[card] = self.card_cats[cat][card]
                
        self.deck = self.build_deck() #Lastly, we construct our deck
        if self.build_deck():
            pass
        else:
            print("Something went wrong while constructing the deck.")
            
        self.discard = []
        self.curr_place = 0
        self.is_flipped = False
            
    def build_deck(self):
        deck = []
        try:
            for card in self.cards.keys():
                deck.append(card)
            return deck
        except:
            return False
            
    def draw(self):
        '''
        Randomly draws a card from the deck.
        
        Places a tuple of the card in the discard pile.
        Also returns a tuple of the card, why not.
        '''
        if self.deck_count() <= 0:
            return ('No more cards! Something has gone wrong.', 'You should not be seeing this.')
        drawn = self.deck.pop(random.randrange(len(self.deck)))
        if self.cards[drawn][1] != "": #if the card has an image...
            front = random.choice([drawn, self.cards[drawn][1]])
        else:
            front = drawn
        back = self.cards[drawn][0]
        card = (front, back)
        self.discard.append(card)
        self.curr_place = len(self.discard)-1 #move us forward to the latest card in the discard pile
        self.is_flipped = False #make sure we're not flipped
        return (front, back)
    
    def deck_count(self):
        return len(self.deck)
                    
if __name__ == '__main__':
    #print(os.listdir(os.getcwd()))
    #print(os.listdir('test'))
    test = FlashcardDeck(['Classes/test flashcards - not an actual class/test1.csv'])
    #print(test.card_cats)
    #print(test.card_cats.keys())
    #print(test.cards)
    print(test.deck)
    print(test.deck_count())
    while test.deck_count() > 0:
        print(test.draw())
        print(test.deck)
        print(test.deck_count())
    print(test.draw())
    print(test.deck)
    print(test.deck_count())