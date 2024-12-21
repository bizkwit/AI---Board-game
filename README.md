# AI-Board-Game

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)


## Overview

This project implements a two-player board game with an optional AI opponent.  The game involves placing cards on a board, aiming to create horizontal or vertical sequences of four or more matching colors or dots. The AI uses a Minimax algorithm with a heuristic evaluation function to make optimal moves.


## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Examples](#examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)


## Features

- Two-player gameplay (human vs. human or human vs. AI).
- AI opponent using the Minimax algorithm.
- Heuristic evaluation function for efficient AI decision-making.
- Card recycling mechanic for strategic gameplay in the late game.
- Win condition: Four or more consecutive matching colors or dots (horizontally or vertically).
- Game ends in a tie if no player achieves the win condition within a set number of moves.
- Option to trace Minimax algorithm execution for analysis.


## Technologies

- Python 3
- [![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)


## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bizkwit/AI---Board-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd AI---Board-game
   ```

### Usage

1. Run the `gameplay.py` script:
   ```bash
   python gameplay.py
   ```
2. Follow the on-screen prompts to choose game mode (human vs. human or human vs. AI), AI difficulty, and input method.
3. Play the game according to the instructions.  The game will indicate the current player's turn and provide instructions for card placement and recycling.



## Examples

**Valid Move Input (Regular Move):**  `0 5 H 1` (Place card configuration 5, horizontally, starting at column H, row 1)

**Valid Move Input (Recycling Move):** `F 2 F 3 3 A 2` (Recycle card at F2, F3 and place card 3 at A2)

The game provides prompts and error handling for invalid inputs.


## Roadmap

- [x] Implement core game logic.
- [x] Develop Minimax AI with heuristic evaluation.
- [x] Add card recycling mechanic.
- [x] Create user interface (CLI).
- [x] Implement win condition checking.
- [x] Add game over conditions.
- [x] Improve AI performance and decision making.
- [ ] Add a graphical user interface (GUI).
- [ ] Implement different AI difficulty levels.
- [ ] Add online multiplayer functionality.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgements

- This project was inspired by a desire to explore game AI and Minimax algorithms.
