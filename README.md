# HackED2023LizardWizards - AI
## Moataz (Taz) Khallaf & Gordon Chi
### What is this?
This is a python programmed non ml chess ai made as a smaller part of my main project in HackED2023.

### REVISED
This AI is now being used for a MacEwan CMPT 496 capstone project lead by Taz Khallaf, Bob Blinde
Gordon Chi and Travis Mund

### How to use?
- make sure you have python installed
- run '''pip install python chess'''
- run '''python3 main.py''' in the correct directory
- follow instructions on terminal from there

### Resources and Credits
#### Libraries used
- python_chess
- random

#### Python naming convetions used
https://peps.python.org/pep-0008/

##### TLDR
- classes use CapWords
- functions use snake_case
- methods use snake_case
- constants use SNAKE_CAP_WORDS
- vars use camelCase

#### Debugging aid
https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers
https://www.chessprogramming.org/Hans_Berliner

### Updates
#### V1.00
- base model from HackED

#### v2.00
- fix issue where AI would crash when player was black
- TODO fix issue where crash occurs during 1 move mate as black player
- TODO start working on translater
- TODO issues where AI would creash at depth 7+
- TODO figure out issue where game is not detecting mate

#### v2.01
- add to state control to board to reset better
- add stalemate detection
- add player vs ai win detection
- fix checkmate crash
- TODO depth 7+ crash
