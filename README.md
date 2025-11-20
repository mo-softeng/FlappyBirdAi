
# 🐦 FlappyBirdAi

FlappyBirdAi is an AI-powered version of the classic **Flappy Bird** game.  
Instead of a human controlling the bird, a population of neural-network agents learns to play the game through repeated simulation and evolution.

---

## 🚀 Features

- Fully playable Flappy Bird clone (visual game loop).
- Multiple AI birds trained in parallel each generation.
- Simple neuro-evolution setup (genetic algorithm / NEAT-style):
  - Networks scored by how long they survive and how far they travel.
  - Best performers are kept, mutated and recombined to form the next generation.
- Modular code split into game logic, AI logic, and config.

---

## 📂 Project Structure

- `main.py` – Entry point. Sets up the game window, runs the main loop, steps the population, and handles drawing / frame updates.
- `player.py` – Bird logic: position, velocity, jumping, collision checks.
- `components.py` – Game objects such as pipes, ground, background, and their update/draw logic.
- `brain.py` – Neural network “brain” used by each bird to decide when to jump.
- `node.py` – Defines individual neural network nodes.
- `connections.py` – Represents weighted connections between nodes.
- `species.py` – Groups similar networks into species for more stable evolution.
- `population.py` – Manages the full population of birds: selection, fitness, mutation, and generation updates.
- `config.py` – Central config for hyperparameters (population size, mutation rates, etc.).
- `LICENSE` – MIT license.
- `README.md` – This file.

---

## 🧰 Requirements

- Python 3.9+  
- `pygame`  
- (Optional) `numpy` if your implementation uses it

Install dependencies:

```bash
pip install pygame numpy
