# Asteroids

Arcade-style Asteroids built with `pygame`.

## Features

- Smooth delta-time game loop at 60 FPS target
- Lumpy polygon asteroids with splitting behavior
- Multiple weapon types: single, spread, burst
- Powerups: shield, speed boost, bomb refill
- Bomb system with fuse, blast radius, and shockwave effect
- Lives, respawn invulnerability, start screen, and game-over screen
- Score + persisted high score
- Modular architecture (`objects/` + `systems/`)

## Controls

- `W` / `S`: Thrust forward / reverse
- `A` / `D`: Rotate ship
- `SPACE`: Shoot
- `1` / `2` / `3`: Weapon select (single / spread / burst)
- `B`: Drop bomb
- `ENTER`: Start game from title screen
- `SPACE`: Restart after game over

## Requirements

- Python `3.13+`
- `pygame==2.6.1`

## Run

If you use `uv` (recommended):

```bash
uv run main.py
```

If you use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame==2.6.1
python main.py
```

## Project Structure

- `main.py`: top-level orchestration loop
- `objects/`: entities and geometric/collision primitives
- `systems/`: isolated gameplay systems (collision, spawn, render, background, state, session)
- `hud.py`: HUD and screen overlays
- `input_handler.py`: event to action mapping
- `constants.py`: central gameplay tuning values

## Notes

- Runtime data files like `highscore.json` and log JSONL outputs are ignored in git.
