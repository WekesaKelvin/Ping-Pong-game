# Ping-Pong Game

A classic Pong game built with Python and Pygame. The objective is to outscore your opponent by hitting the ball past their paddle.

## Table of Contents
1. [Installation](#installation)
2. [How to Run](#how-to-run)
3. [Game Modes](#game-modes)
4. [Sound Effects](#sound-effects)
5. [Game Controls](#game-controls)
6. [Gameplay Win Conditions](#gameplay-win-conditions)
7. [Settings Section](#settings-section)
8. [File Structure](#file-structure)

---

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

## How to Run
Create a folder in Desktop or any where you prefer and clone the repository in the terminal or command prompt inside that folder using this code:

```bash
git clone https://github.com/WekesaKelvin/Ping-Pong-game.git
```
After Cloning the repository Install pygame by running:

```bash
pip install pygame
```
Navigate into the repository folder:

```bash
cd Ping-Pong-game
```
Run the game by executing the following command in your terminal:

```bash
python ping_pong_game.py
```
## Game Modes
Single Player: Play against the computer, aiming to beat its AI at varying difficulty levels.

Multiplayer: Compete against another player in a race to 10 points to claim victory.

## Score Tracking
Players in single-player mode can track their highest scores against the computer.

## Difficulty Levels
Easy: Slower ball speed and larger paddles for a relaxed gameplay experience.

Medium: A balanced challenge with moderate ball speed and paddle size.

Hard: High-intensity gameplay with faster ball speeds and smaller paddles for seasoned players.

## Sound Effects
Dynamic sound effects enhance gameplay:
Ball hits the wall.
Ball is hit by a paddle.
Player wins or loses a match.

## Game Controls
- **Player (Right Paddle)**  
  - Move Up: Press the `UP Arrow` key
  - Move Down: Press the `DOWN Arrow` key

- **Opponent (Left Paddle)**  
  - Move Up: Press the `W` key
  - Move Down: Press the `S` key

## Gameplay Win Conditions

Single Player Mode: Aim for the highest score possible against the computer.

Multiplayer Mode: Achieve the highest points within **20 seconds**. If you reach the highest score before the timer ends, you win immediately.

**Settings Section**
- Customize the game settings to adjust difficulty:
  - **Ball Speed**: Increase or decrease the speed of the ball.
  - **Ball Size**: Adjust the size of the ball for a personalized challenge.
  - **Paddle Speed**: Control how fast the paddles move.
  - **Paddle Size**: Modify the paddle size for easier or more challenging gameplay.
  - **Match Type**: Select specific match configurations to suit your skill level.

## File Structure
Game.py - Main game code including game setup, event handling, animations, and main game loop.
