Table of Contents
Installation
How to Run
Game Controls
Gameplay
File Structure
Contributors
Installation
Prerequisites
Python 3.6 or higher is required.

Pygame library is required. Install it by running:

bash
Copy code
pip install pygame
How to Run
Clone this repository:

bash
Copy code
git clone <repository_url>
cd <repository_folder>
Run the game by executing the following command in your terminal:

bash
Copy code
python pong_game.py
Game Controls
Player (Right Paddle)

Move Up: Press the UP Arrow Key
Move Down: Press the DOWN Arrow Key
Opponent (Left Paddle)

Move Up: Press the W Key
Move Down: Press the S Key
Gameplay
The objective of the game is to reach a score of 10 before your opponent. Each time the ball passes a paddle, the other player scores a point.

File Structure
pong_game.py - Main game code including game setup, event handling, animations, and main game loop.
Contributors
This project was developed collaboratively by five contributors:

Dennis 1 - Setup and Initialization
Bahati 2 - Game Elements and Ball Animation
Kelvin 3 - Paddle Animation and Ball Reset
Stella 4 - Input Handling and Score Display
Shaddy 5 - Main Game Loop and Game Over Condition
