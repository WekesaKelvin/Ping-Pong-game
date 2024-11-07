# Pong Game

A classic Pong game built with Python and Pygame. The objective is to outscore your opponent by hitting the ball past their paddle.

## Table of Contents
1. [Installation](#installation)
2. [How to Run](#how-to-run)
3. [Game Controls](#game-controls)
4. [Gameplay](#gameplay)
5. [File Structure](#file-structure)

---

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

Install Pygame by running:
```bash
pip install pygame
```
## How to Run
Clone this repository:

```bash
Copy code
git clone <repository_url>
```
Navigate into the repository folder:

```bash
Copy code
cd <repository_folder>
```
Run the game by executing the following command in your terminal:

```bash
Copy code
python pong_game.py
```
## Game Controls

- **Player (Right Paddle)**  
  - Move Up: Press the `UP Arrow` key
  - Move Down: Press the `DOWN Arrow` key

- **Opponent (Left Paddle)**  
  - Move Up: Press the `W` key
  - Move Down: Press the `S` key

## Gameplay
The objective of the game is to reach a score of 10 before your opponent. Each time the ball passes a paddle, the other player scores a point.

#@ File Structure
pong_game.py - Main game code including game setup, event handling, animations, and main game loop.
