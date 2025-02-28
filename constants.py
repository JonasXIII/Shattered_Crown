"""
Chronicles of the Shattered Crown - Game Constants

This file contains all global constants and configuration settings for the game.
"""
import logging

# Display Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False
TARGET_FPS = 60
GAME_TITLE = "Chronicles of the Shattered Crown"

# Debug Settings
DEBUG_MODE = True
SHOW_FPS = True
SHOW_GRID = True
LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO

# Game Settings
TILE_SIZE = 32  # Size of a tile in pixels
ACTION_POINT_MAX = 5
BASE_PLAYER_HEALTH = 100
BASE_ENEMY_HEALTH = 50
PLAYER_START_GOLD = 100

# Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
UI_BG_COLOR = (40, 40, 60)
UI_TEXT_COLOR = (220, 220, 220)
UI_HIGHLIGHT_COLOR = (100, 100, 240)
UI_BORDER_COLOR = (80, 80, 100)

# Asset Paths
ASSET_DIR = "assets/"
IMAGE_DIR = ASSET_DIR + "images/"
SOUND_DIR = ASSET_DIR + "sounds/"
MUSIC_DIR = ASSET_DIR + "music/"
FONT_DIR = ASSET_DIR + "fonts/"
DATA_DIR = "data/"

# Control Mappings
KEY_UP = "up"
KEY_DOWN = "down"
KEY_LEFT = "left"
KEY_RIGHT = "right"
KEY_INTERACT = "interact"
KEY_INVENTORY = "inventory"
KEY_ATTACK = "attack"
KEY_SKILL_1 = "skill_1"
KEY_SKILL_2 = "skill_2"
KEY_SKILL_3 = "skill_3"
KEY_CANCEL = "cancel"
KEY_CONFIRM = "confirm"


# Tile settings
TILE_SIZE = 32  # Pixel dimensions for grid tiles

# Color definitions
GROUND_COLOR = (100, 80, 60)  # Earth brown
WATER_COLOR = (30, 144, 255)   # Dodger blue
PATH_COLOR = (139, 69, 19)     # Sandy brown

# Debug settings
DEBUG_MODE = False  # Enable visual debugging aids