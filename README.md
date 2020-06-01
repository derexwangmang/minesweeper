# Minesweeper
Python implementation of the classical single-player puzzle game, Minesweeper.

## Objective

A player attempts to clear the grid without denoating any mines with limited information. Each cell on the grid is either uncovered or covered. Uncovered cells will have a number referencing the number of adjacent mines while covered cells may be revealed through a player's left click. If the covered cell is actually a mine, the player loses. The player may place flags in positions where they believe there is a mine by right-clicking. The win condition is uncovering all cell without detonating a mine.

## Getting Started

### Prerequisites

* pygame

To install pygame, type or copy/paste the following into the command line:

```
python3 -m pip install -U pygame --user
```

To see if it worked, run the following command:

```
python3 -m pygame.examples.aliens
```

View instructions and further information [here](https://www.pygame.org/wiki/GettingStarted).

* numpy

To install numpy, type or copy/paste the following into the command line:

```
python -m pip install --user numpy
```

View instructions and further information [here](https://www.edureka.co/blog/install-numpy/#NumPyInstallationOnWindowsOperatingSystem)

### Installing

Download the files, including the images.

To run the game, navigate to the directory in which Minesweeper.py is stored in the command line:

```
cd \insert\path\here
```

Then start the game in the command line:

```
python Minesweeper.py
```

The following should now appear on the screen:

![Starting Screen](/screenshots/starting_screen.jpg?raw=true)
