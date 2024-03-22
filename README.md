A simple digital flashcard "game" which supports both text and images. Created because I was unable to find a decent free flashcard program online.

Each subfolder is a Class or Topic, which then may contain any number of .csv files referred to within the code as "modules." These csv files contain the flashcards.
The table for the csv file is as such: "front text","back text","filename.png"
Images are optional, and should be replaced with empty quotes "" when an image is not to be used. 
Cards will randomly select between front text or a supplied image, and the user may select multiple modules within a class/topic for the cards to be drawn from.

# Setup
## Windows
Set up on Windows requires a small understanding of the command line, and little else.
1. Download and install the most recent stable release of [Python](https://www.python.org/downloads/).
2. Download the contents of this Github Repository to a folder.
3. In the Windows Command Prompt (search `cmd`), navigate to the folder containing these files.
4. Run the command `pip install -r requirements.txt` This will install the Python Arcade library to your system, which is necessary for this application to run.
5. You may then run the flashcards application with the command `python main.py`

Once you have completed setup, only Step 5 is necessary. The command must be run from the folder containing this application.

## Linux
TODO: Write this section of the readme

# Adding Your Own Flashcards
TODO: Write this section of the readme