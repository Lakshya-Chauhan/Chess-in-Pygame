<h1 align="center">♟ Chess ♟</h1>

A Chess game made in **Python3** using `pygame` module.

The project mainly consists of the following Python Scripts:
- ```main.py```
- ```thechess.py```

These scripts are responsible for the game logics and GUI.
Further for the Audio and Images, we have:
- [Audio Folder](https://github.com/Legendary3995/Chess-in-Pygame/tree/main/audio)

     ```py
     audio = {
    'start'     :   mixer.Sound('audio/start.mp3'),
    'move'      :   mixer.Sound('audio/move.mp3'),
    'capture'   :   mixer.Sound('audio/capture.mp3'),
    'check'     :   mixer.Sound('audio/check.mp3'),
    'castle'    :   mixer.Sound('audio/castle.mp3'),
    'game_over' :   mixer.Sound('audio/game_over.mp3'),
    'draw'      :   mixer.Sound('audio/draw.mp3'),
    'checkmate' :   mixer.Sound('audio/checkmate.mp3')
    }
    ```
- [Images Folder](https://github.com/Legendary3995/Chess-in-Pygame/tree/main/images)
 <img src="https://user-images.githubusercontent.com/97667653/206763461-5d872993-9dfe-4d29-8f78-382949fbbc1b.png" height="100" width="600">


## `main.py`
`main.py` makes use of the game logics by importing `thechess.py`. It serves the following roles:
1. Displaying the game board.
2. Updation of the game board after each move.
3. Alternating between each player after each turn is played.
4. Displaying the end screen, which could be either:
    * a **Stalemate** (Draw) endscreen, or
    * a **Checkmate** endscreen, accompanied with the name of the winner.

<br>

## `thechess.py`
`thechess.py` is the main lifeline of this project, which includes all the logics of all the pieces i.e. it defines the legal moves of each chess piece.

#### `__init__()` method:
It initialises the object with attributes necessary for the game logic.

#### `occupied_pos()` method:
It stores all the squares that are occupied by the pieces.

#### `legal_moves()` method:
It stores all the legal move logics for each of the chess pieces:

0. King
1. Queen
2. Rook
3. Bishop
4. Knight
5. Pawn

## How to use the program?

Simply visit the following link to download the `.exe` file of the game:

> [Executable Game](https://Chess-Download.legendaryalpha.repl.co)
