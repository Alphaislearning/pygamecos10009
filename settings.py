WIDTH = 800
HEIGHT = 400

FPS = 60

GRAVITY = 0.8
JUMP_FORCE = -15

PLAYER_SCALE = 120

GROUND_Y = HEIGHT - 80

SPEED_START = 6
SPEED_INCREASE = 0.002
START_LIVES = 3
HIT_INVINCIBILITY_FRAMES = 30

# Level settings
LEVEL_THRESHOLDS = {
    1: 0,      # Level 1: 0+ score
    2: 100,    # Level 2: 100+ score
    3: 300     # Level 3: 300+ score
}

# Difficulty multipliers by level
LEVEL_MULTIPLIERS = {
    1: {
        "speed_increase": 1.0,
        "spawn_rate": 60,  # Lower = faster
        "obstacle_colors": [(160, 50, 50)]
    },
    2: {
        "speed_increase": 1.3,
        "spawn_rate": 45,
        "obstacle_colors": [(200, 80, 80)]
    },
    3: {
        "speed_increase": 1.6,
        "spawn_rate": 30,
        "obstacle_colors": [(255, 100, 100)]
    }
}