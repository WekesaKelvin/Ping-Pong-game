# Ping-Pong-game
Pong Game
Overview
Pong is a simple arcade-style game where you control a paddle and try to bounce a ball past your opponent's paddle. The game ends when either the player or the opponent reaches 10 points.
Requirements
•	Python 3.x
•	Pygame library (Install using pip install pygame)
Game Controls
•	Player Paddle:
o	Use Up Arrow to move up.
o	Use Down Arrow to move down.
•	Opponent Paddle:
o	Use W to move up.
o	Use S to move down.
Game Rules
•	The game is played between two paddles (one controlled by the player and the other by the opponent).
•	The ball bounces off the top and bottom walls and can be hit by either paddle.
•	When the ball crosses the left or right side of the screen, the player or the opponent scores a point.
•	The first player to reach 10 points wins the game.
•	A win message is displayed at the center of the screen when a player reaches 10 points, and the game ends after 2 seconds.
How to Run
1.	Install Python 3.x and Pygame.
2.	Download the project files and open the terminal/command prompt in the project directory.
3.	Run the game with the following command:
bash
Copy code
python pong_game.py
Game Features
•	Real-time gameplay: The ball moves and bounces based on its speed, and the paddles respond to user input.
•	Scoring system: The game tracks and displays the score for both the player and the opponent.
•	Game Over: The game ends when a player reaches 10 points, and a win message is displayed for 2 seconds.
•	Paddle movement: Both paddles are constrained within the screen boundaries.
Technologies Used
•	Python: Programming language used to develop the game.
•	Pygame: Game development library used to handle graphics, sound, and user input.

