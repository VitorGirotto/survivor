# Survivor

Survivor is an early-stage, top-down survival game in which the player must
stay alive while increasingly frequent waves of enemies close in. Movement is
controlled by the player, while attacks automatically target the nearest
enemy.

## Tech stack

- Python 3.11+
- [Pygame Community Edition](https://pyga.me/) for rendering, input, sprites,
  animation, collision detection, and the game loop
- [uv](https://docs.astral.sh/uv/) for dependency and virtual-environment
  management
- pytest for automated tests
- Ruff for linting and formatting
- PyInstaller configuration for producing a standalone executable

## Current functionality

- Main menu with Play and Exit buttons
- Player movement with WASD or the arrow keys
- Animated player movement and animated enemies
- Enemies that spawn at random screen edges and chase the player
- Enemy separation behavior that reduces overlap between nearby enemies
- A spawn rate that increases as the session progresses
- Automatic attacks aimed at the nearest enemy
- Projectile range, attack cooldowns, damage, and enemy health
- Contact damage to the player with a damage cooldown
- A score counter that increases when an enemy is defeated
- An elapsed survival timer
- Game-over behavior that returns the player to the menu when health reaches
  zero

## Installation and running

### Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

From the project root, install the locked dependencies:

```bash
uv sync
```

Start the game:

```bash
uv run python src/main.py
```

Use WASD or the arrow keys to move. Attacks are automatic. Use the menu's Exit
button or close the window to quit.

## Development checks

Run the automated test suite:

```bash
uv run pytest
```

Run the linter:

```bash
uv run ruff check .
```