WIDTH = 800
HEIGHT = 400

FPS = 60

MUSIC_VOLUME = 0.5

GRAVITY = 0.8
JUMP_FORCE = -15

PLAYER_SCALE = 120

GROUND_Y = HEIGHT - 80

SPEED_START = 6
SPEED_INCREASE = 0.002
START_LIVES = 3
HIT_INVINCIBILITY_FRAMES = 30

# Level settings by stage selection
LEVEL_CONFIGS = {
    1: {
        "name": "Level 1",
        "speed_increase": 1.0,
        "spawn_rate": 60,
        "score_multiplier": 1.0,
    },
    2: {
        "name": "Level 2",
        "speed_increase": 1.3,
        "spawn_rate": 45,
        "score_multiplier": 1.2,
    },
    3: {
        "name": "Level 3",
        "speed_increase": 1.6,
        "spawn_rate": 30,
        "score_multiplier": 1.4,
    },
}
