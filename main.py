'''
Created on Mar 21, 2024

@author: Fred
'''
import arcade, arcade.gui, os
from flashcards import FlashcardDeck

#Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Digital Flashcards"
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20

#Global Vars
TARG_COURSE = None #the selected course, to be selected by the user
TARG_MODULE = [] #the selected modules, to be selected by the user
IS_RUNNING = False
DECK = None

def reset_globals():
    global TARG_COURSE
    TARG_COURSE = None
    global TARG_MODULE
    TARG_MODULE = []
    global IS_RUNNING
    IS_RUNNING = False
    global DECK
    DECK = None

class CourseButton(arcade.gui.UIFlatButton):
        def on_click(self, event: arcade.gui.UIOnClickEvent):
            global TARG_COURSE
            TARG_COURSE = self.text
            
class ModuleButton(arcade.gui.UIFlatButton):            
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        global TARG_MODULE
        if self.text[-8:] == " - ADDED":
            self.text = self.text.replace(" - ADDED",'')
        p = "Classes/" + TARG_COURSE + "/" + self.text + ".csv"
        if p in TARG_MODULE:
            TARG_MODULE.remove(p)
        else:
            TARG_MODULE.append(p)
            self.text += " - ADDED"
            
class StartButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        global IS_RUNNING
        if len(TARG_MODULE) > 0:
            IS_RUNNING = True
        else:
            if " - Pick some modules first!" not in self.text:
                self.text += " - Pick some modules first!"

class MainMenu(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)
        self.title = None
        self.course_list = None
        self.module_list = None
        self.started = None
        self.manager = None
        self.course_box = None
        self.module_box = None
        self.control_box = None
        self.course_box_anchor = None
        self.module_box_anchor = None
        self.control_box_anchor = None
        self.is_running = None
        self.setup()
                
    def setup(self):
        start_x = 0
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
        self.title = arcade.Text(
            "Select a Class",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE * 2,
            width = SCREEN_WIDTH,
            align = "center",
            bold = True
            )

        #Construct a list of all available courses
        self.course_list = [f.name for f in os.scandir(os.getcwd() + "/Classes") if f.is_dir()]
        self.module_list = []
        self.started = False

        #We create our GUI manager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.course_box = arcade.gui.UIBoxLayout()
        self.module_box = arcade.gui.UIBoxLayout()
        self.control_box = arcade.gui.UIBoxLayout(vertical=False)
        
        #populate course button list
        for course in self.course_list:
            button = CourseButton(text=course, width=SCREEN_WIDTH / 2)
            self.course_box.add(button.with_space_around(bottom=20))
        self.course_box_anchor = arcade.gui.UIAnchorWidget(anchor_x = "center_x", anchor_y = "center_y", child=self.course_box)
        self.module_box_anchor = arcade.gui.UIAnchorWidget(anchor_x = "center_x", anchor_y = "center_y", child=self.module_box)
        self.control_box_anchor = arcade.gui.UIAnchorWidget(anchor_x = "center_x", anchor_y =  "bottom", align_y = 100, child=self.control_box)
        
        self.manager.add(self.course_box_anchor)
        
        self.is_running = False
        
    def on_draw(self):
        pass
        
    def on_update(self, delta_time):
        self.clear()
        if TARG_COURSE: #If a course has been selected
            if len(self.module_list) <= 0: #If the module list has not already been constructed
                self.title.text = TARG_COURSE
                self.manager.remove(self.course_box_anchor)
                self.module_list = [f for f in os.listdir(os.getcwd() + "/Classes/" + TARG_COURSE) if f.endswith('.csv')]
                for module in self.module_list:
                    module = module.replace(".csv","")
                    button = ModuleButton(text = module, width = SCREEN_WIDTH / 2)
                    self.module_box.add(button.with_space_around(bottom=20))
                button = StartButton(text = "Start", width = SCREEN_WIDTH / 2)
                self.module_box.add(button.with_space_around(bottom=20))
                self.manager.add(self.module_box_anchor)
            elif IS_RUNNING and not self.started: #If the game has started but we haven't setup yet
                self.manager.remove(self.module_box_anchor)
                global DECK
                DECK = FlashcardDeck(TARG_MODULE) #create the deck!
                DECK.draw() #draw our first card
                #creating our control buttons
                for b in ['<', 'Flip', '>']:
                    button = self.ControlButton(text=b, width = DEFAULT_FONT_SIZE * 2)
                    self.control_box.add(button)
                self.manager.add(self.control_box_anchor)
                self.started = True
            elif IS_RUNNING and self.started: #if we're running and we've done setup
                if not DECK.is_flipped: #If the card hasn't been flipped yet
                    if DECK.discard[DECK.curr_place][0][-3:] not in ['png', 'jpg']: #If it's not an image
                        arcade.draw_text(text=DECK.discard[DECK.curr_place][0], start_x= SCREEN_WIDTH / 2, start_y= SCREEN_HEIGHT / 2, color= arcade.color.BLACK, font_size= DEFAULT_FONT_SIZE * 2, width= SCREEN_WIDTH, anchor_x= "center", anchor_y= "center", multiline= True)
                    else: #If it is an image
                        img = arcade.load_texture(os.getcwd() + "/Classes/" + TARG_COURSE + "/images/" + DECK.discard[DECK.curr_place][0])
                        img.draw_scaled(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, scale= min(SCREEN_WIDTH / img.width, SCREEN_HEIGHT / img.height))
                else: #If we're looking at the answer side
                    arcade.draw_text(text=DECK.discard[DECK.curr_place][1], start_x= SCREEN_WIDTH / 2, start_y= SCREEN_HEIGHT / 2, color= arcade.color.BLACK, font_size= DEFAULT_FONT_SIZE * 2, width= SCREEN_WIDTH, anchor_x= "center", anchor_y= "center", multiline= True)
        if not IS_RUNNING and not self.started: #We only want to draw the title if we're not looking at cards
            self.title.draw()
        self.manager.draw()
        if not IS_RUNNING and self.started: #If we've done setup but we're not running, reset
            self.setup()
        
    class ControlButton(arcade.gui.UIFlatButton):
        '''
        I don't know why I made this an inner class lmao oh well
        '''
        def on_click(self, event: arcade.gui.UIOnClickEvent):
            global DECK
            max_discard = len(DECK.discard) - 1
            if self.text == '<':
                if DECK.curr_place > 0: #If we're not at the beginning
                    DECK.curr_place -= 1 #move us back one
                    DECK.is_flipped = False
                    arcade.cleanup_texture_cache()
            elif self.text == '>':
                if DECK.curr_place == max_discard: #if we're at the last card in discard
                    if DECK.deck_count() > 0: #if there are cards left
                        DECK.draw() #draw a new card, this automatically updates our current place in the pile
                        arcade.cleanup_texture_cache()
                    else: #we want to start over
                        arcade.cleanup_texture_cache()
                        reset_globals()
                else: #if we're not at the last card in the discard pile
                    DECK.curr_place += 1 #move forward by 1
                    DECK.is_flipped = False
                    arcade.cleanup_texture_cache()
            elif self.text == 'Flip':
                if not DECK.is_flipped:
                    DECK.is_flipped = True
                else:
                    DECK.is_flipped = False
                arcade.cleanup_texture_cache()
            else:
                print("Something has gone horribly wrong. How did you hit a button that does not exist?")
                
if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()