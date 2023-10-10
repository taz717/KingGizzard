# HackED2023LizardWizards - AI
## Moataz (Taz) Khallaf & Gordon Chi
### What is this?
This is a Python-programmed non-ml chess AI made as a smaller part of my main project in HackED2023.

### REVISED
This AI is now being used for a MacEwan CMPT 496 capstone project led by Taz Khallaf, Bob Blinde

Gordon Chi and Travis Mundy

### How to use?
- make sure you have Python installed
- run '''pip install python chess'''
- run '''python3 main.py''' in the correct directory
- follow instructions on the terminal from there

### Resources and Credits
#### Libraries used
- python_chess

#### Debugging aid
https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers \
https://www.chessprogramming.org/Hans_Berliner

#### Chess notation
https://www.chess.com/article/view/chess-notation

##### TLDR
- x: captures
- 0-0: kingside castle
- 0-0-0: queenside castle
- +: check
- #: checkmate
- !: good move
- ?: poor move

### Python naming conventions used
https://peps.python.org/pep-0008/

#### TLDR
- classes use CapWords
- functions use snake_case
- methods use snake_case
- constants use SNAKE_CAP_WORDS
- vars use camelCase

### Final update
The project was demo'd on Aug18, and the team could play about half of a chess match.
Everything worked according to plan until someone's hand entered the picture the AI took
to read the player's move and crashed the program because we forgot to put a safety feature
to prevent crashes.

Overall, it works, but the project will be retired until the team decides to meet again.

### Credits
Credits to members not officially recognized as the team go to:
 - Dr. Davis @MacEwan
 - Kareem Ali @HackathonMember 
 - Rj Forjie @HackathonMember
 - Ali Muneer @HackathonMember
 - Eric Peterson @HackathonMember
