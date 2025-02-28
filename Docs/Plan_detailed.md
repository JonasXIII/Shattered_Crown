main.py
Create the main entry point for "Chronicles of the Shattered Crown". This file should:
1. Initialize PyGame with appropriate settings (resolution, display mode)
2. Create a game state manager instance
3. Implement the main game loop that:
   - Processes inputs via input_handler
   - Updates the current game state
   - Renders the current state
   - Maintains a consistent frame rate (target 60 FPS)
4. Handle transitions between game states (title screen, overworld, local area, combat, inventory, etc.)
5. Initialize the resource manager for loading assets
6. Set up error handling and logging
7. Implement clean shutdown procedures

constants.py
Define all game constants and configuration settings:
1. Display settings: SCREEN_WIDTH (1280), SCREEN_HEIGHT (720), FULLSCREEN (False)
2. Color definitions: (BLACK, WHITE, UI_BG_COLOR, UI_TEXT_COLOR, etc.)
3. Game settings: TILE_SIZE (32px), FONT_SIZES, ACTION_POINT_MAX (5)
4. Asset paths: directories for images, sounds, data files
5. Game balance constants: BASE_ENEMY_HEALTH, PLAYER_START_GOLD, etc.
6. Debug settings: DEBUG_MODE, SHOW_FPS, SHOW_GRID
7. Control mappings: KEY_UP, KEY_DOWN, etc.

Game Engine
engine/game_state.py
Implement the game state management system:
1. Define a GameState enum with states: TITLE, OVERWORLD, LOCAL_AREA, COMBAT, INVENTORY, DIALOG, SHOP, QUEST_LOG, GAME_OVER
2. Create a StateManager class that:
   - Maintains the current state
   - Handles state transitions with proper cleanup/initialization
   - Provides update() and render() methods that delegate to the current state
   - Manages a stack of states for hierarchical states (e.g., inventory while in overworld)
3. Define a base State abstract class with methods:
   - enter(): Called when state becomes active
   - exit(): Called when state is left
   - update(delta_time): Updates state logic
   - render(screen): Renders the state
   - handle_event(event): Processes input events

engine/camera.py
Create a camera system for managing the viewport:
1. Implement a Camera class that:
   - Tracks position coordinates in the world
   - Provides methods to center on an entity (usually the player)
   - Handles smooth scrolling with damping
   - Calculates screen coordinates from world coordinates
   - Implements screen shaking for effects (combat hits, explosions)
2. Add boundary checks to prevent showing areas outside the map
3. Include zoom functionality for overworld view
4. Implement functions to convert between screen and world coordinates

engine/input_handler.py
Create a flexible input processing system:
1. Define an InputHandler class that:
   - Processes PyGame events and translates them to game actions
   - Supports keyboard, mouse, and gamepad inputs
   - Maintains a dictionary mapping inputs to game actions
   - Provides methods to check if an action was just pressed, held, or released
2. Implement context-sensitive controls that change based on game state
3. Support input rebinding functionality
4. Include methods for UI interaction (clicking buttons, dragging items)
5. Implement a history of recent inputs for combo detection

engine/resource_manager.py
Create an asset management system:
1. Implement a singleton ResourceManager class that:
   - Loads and caches images, sounds, fonts, and data files
   - Supports loading sprites and sprite sheets
   - Provides methods to get assets by name or ID
   - Handles transparent pixel colors and scaling
2. Implement proper error handling for missing resources
3. Add support for animations with frame timing
4. Include hot-reloading of assets for development
5. Add methods for unloading unused resources to manage memory

World Components
world/map.py
Create the core map system:
1. Implement a Map class that:
   - Manages a 2D grid of Tile objects
   - Provides methods for pathfinding and distance calculations
   - Handles collision detection between entities and terrain
   - Renders visible portions of the map based on camera position
2. Add fog of war system with revealed and unexplored areas
3. Include methods to save/load map state
4. Implement tile-based line of sight calculations
5. Add methods to place and retrieve entities on the map
6. Support different map layers (ground, obstacles, decoration, entities)

world/tile.py
Define the tile system for the game grid:
1. Create a Tile class with properties:
   - Type (grass, water, mountain, road, etc.)
   - Blocking status (can entities move through it?)
   - Movement cost (how many AP to traverse)
   - Special effects (damage, healing, etc.)
   - Visual properties (base sprite, decorations)
2. Add methods to check adjacency and connections
3. Include support for animated tiles (water, fire)
4. Implement interactive tile features (doors, chests, traps)

world/overworld.py
Create the overworld map system:
1. Implement an Overworld class that:
   - Generates a pixel-art style world map with different biomes
   - Manages locations (towns, dungeons, points of interest)
   - Handles player movement between locations
   - Triggers random encounters based on terrain type
2. Add support for fast travel between discovered locations
3. Include progressive revealing of the map as the player explores
4. Implement day/night cycle affecting encounters and visuals
5. Add weather effects that impact gameplay (rain slows movement, etc.)

world/local_area.py
Create the system for detailed gameplay areas:
1. Implement a LocalArea class that:
   - Generates grid-based maps (hex or square) for gameplay
   - Places enemies, treasures, and obstacles
   - Manages entry/exit points
   - Tracks cleared status and respawn timers
2. Add procedural generation for different area types:
   - Forests: Dense trees, clearings, hunting grounds
   - Dungeons: Rooms, corridors, traps
   - Ruins: Broken walls, hidden treasures
3. Include special interactive elements (shrines, puzzles)
4. Implement environment hazards (poison gas, spike traps)

world/town.py
Create the town system for player hubs:
1. Implement a Town class that:
   - Manages services (shops, healers, blacksmiths)
   - Tracks town reputation and quest board
   - Houses NPCs with dialog and quests
   - Provides safe resting areas
2. Add town improvement mechanics as player helps them
3. Implement town events and festivals based on progress
4. Include unique features for each town (special shop, guild)

Entity System
entities/entity.py
Create the base entity system:
1. Implement an Entity base class with:
   - Position and movement on the grid
   - Health and status effects
   - Rendering methods
   - Collision detection
   - Basic stats (strength, dexterity, intelligence)
2. Add support for entity tags and types
3. Implement a component system for extensibility
4. Include methods for serialization/deserialization
5. Add event hooks for damage, healing, death, etc.

entities/player.py
Implement the player character:
1. Create a Player class (extends Entity) with:
   - Inventory management
   - Equipment slots and effects
   - Experience and leveling system
   - Character class and abilities
   - Quest tracking
2. Add methods for interact with world objects
3. Implement skill cooldown tracking
4. Add reputation tracking with factions
5. Include save/load functionality for player state

entities/enemy.py
Create the enemy system:
1. Implement an Enemy class (extends Entity) with:
   - AI behavior patterns
   - Loot tables
   - Aggression and detection ranges
   - Special abilities
2. Create enemy types:
   - Bandits: Human enemies with weapons
   - Wolves: Pack tactics, surround player
   - Undead: Skeletal warriors with resurrection
   - Vampires: Life-stealing attacks
   - Bosses: Special enemies with unique mechanics
3. Add enemy spawning logic and level scaling
4. Implement enemy factions and rivalries

entities/npc.py
Create the NPC system:
1. Implement an NPC class (extends Entity) with:
   - Dialog trees and conversation
   - Shop inventory if merchant
   - Daily routines and schedules
   - Quest-giving functionality
2. Add companion system for NPCs that join the player
3. Implement relationship tracking with the player
4. Include special NPC types (blacksmith, healer, sage)

entities/character_class.py
Define the character class system:
1. Implement a CharacterClass base class with:
   - Base stats modifiers
   - Starting equipment
   - Available skills and progressions
2. Create specific classes:
   - Knight: Tanky with shield abilities
   - Ranger: Ranged attacks and traps
   - Mage: Spells with various effects
   - Rogue: Stealth and critical hits
3. Add multi-classing capabilities
4. Implement skill trees for each class
5. Include class-specific quests and items

Combat System
combat/combat_manager.py
Create the combat management system:
1. Implement a CombatManager class that:
   - Initializes combat encounters
   - Manages turn order and initiative
   - Tracks action points for all combatants
   - Handles victory/defeat conditions
   - Distributes experience and loot
2. Add combat grid management (highlighting valid moves)
3. Implement turn time limits (optional)
4. Include retreat and reinforcement mechanics
5. Add terrain impact on combat (cover, hazards)

combat/actions.py
Define the combat action system:
1. Create an Action base class with:
   - AP cost calculation
   - Target selection (single, area, all)
   - Execution logic
   - Animation triggers
2. Implement specific actions:
   - BasicAttack: Standard weapon attack
   - Move: Grid movement
   - UseItem: Consume inventory items
   - SpecialAbility: Class-specific skills
3. Add combo actions that chain multiple effects
4. Implement reactions to enemy actions (counters, guards)

combat/skills.py
Create the skill system:
1. Implement a Skill base class with:
   - AP cost and cooldown
   - Damage/healing calculation
   - Status effect application
   - Range and area of effect
2. Create class-specific skills:
   - Knight: Shield Bash, Taunt, Whirlwind
   - Ranger: Aimed Shot, Trap, Volley
   - Mage: Fireball, Heal, Freeze
   - Rogue: Backstab, Poison, Smoke Bomb
3. Implement skill upgrading and evolution
4. Add passive skills and traits

combat/effects.py
Create the status effect system:
1. Implement a StatusEffect base class with:
   - Duration tracking
   - Tick effect (damage over time, healing)
   - Stat modifications
   - Visual indicators
2. Create specific effects:
   - Burning: Damage over time
   - Poisoned: Damage over time, reduced healing
   - Frozen: Reduced AP, increased damage taken
   - Blessed: Increased damage, healing received
3. Add effect stacking rules
4. Implement immunity and resistance mechanics

Items and Economy
items/item.py
Create the base item system:
1. Implement an Item base class with:
   - Name, description, icon
   - Value and rarity
   - Use effects
   - Equipment stats (if applicable)
2. Add item categories (weapon, armor, consumable, quest)
3. Implement item stacking for consumables
4. Add item quality variations (damaged, normal, excellent)
5. Include item condition and durability (optional)

items/inventory.py
Implement the inventory management system:
1. Create an Inventory class with:
   - Grid-based or slot-based storage
   - Methods to add, remove, use items
   - Weight/capacity limitations
   - Sorting and filtering functionality
2. Add support for different containers (backpack, chest)
3. Implement currency system
4. Include UI hooks for rendering inventory

items/equipment.py
Create the equipment system:
1. Implement an Equipment class with:
   - Slots (head, chest, weapons, etc.)
   - Methods to equip/unequip items
   - Stat calculation based on equipped items
   - Set bonuses for matching equipment
2. Add weapon types with different attack patterns
3. Implement equipment restrictions by class
4. Include equipment upgrading and enchanting

items/crafting.py
Design the crafting system:
1. Implement a Crafting class with:
   - Recipe management
   - Material requirements checking
   - Crafting result generation
   - Crafting skill progression
2. Add disassembly of items for materials
3. Implement discovery of new recipes
4. Include crafting stations with specialties
5. Add quality variations based on skill

Quest System
quests/quest.py
Create the quest framework:
1. Implement a Quest class with:
   - Objectives (kill X enemies, collect Y items)
   - State tracking (not started, active, completed)
   - Rewards (gold, items, experience)
   - Associated NPCs and locations
2. Add branching quest paths based on choices
3. Implement time-limited quests
4. Include quest dependencies (prerequisites)
5. Add support for multi-stage quests

quests/quest_manager.py
Implement the quest tracking system:
1. Create a QuestManager class that:
   - Tracks all available and active quests
   - Updates quest progress based on game events
   - Triggers quest completion and rewards
   - Stores completed quest history
2. Add methods to generate random side quests
3. Implement quest markers on maps
4. Include quest difficulty scaling

quests/quest_board.py
Create the quest board interface:
1. Implement a QuestBoard class that:
   - Displays available quests in towns
   - Allows accepting new quests
   - Shows quest details and rewards
   - Filters quests by type or difficulty
2. Add reputation requirements for special quests
3. Implement quest rotation/refresh mechanics
4. Include time-limited special quests

UI System
ui/ui_manager.py
Create the UI management system:
1. Implement a UIManager class that:
   - Handles all UI elements and their states
   - Manages UI input and focus
   - Coordinates screen transitions
   - Controls UI element positioning and layout
2. Add support for UI themes and styling
3. Implement UI animation and transitions
4. Include responsive layout for different resolutions

ui/title_screen.py
Design the game's title screen:
1. Implement a TitleScreen class that:
   - Displays game logo and background
   - Provides menu options (New Game, Load Game, Options, Exit)
   - Handles menu navigation and selection
   - Shows credits and version information
2. Add animated background elements
3. Implement save file selection for loading
4. Include option to view tutorial or introduction

ui/hud.py
Create the in-game heads-up display:
1. Implement a HUD class that:
   - Shows player health, AP, and status
   - Displays mini-map of current area
   - Indicates active quests and objectives
   - Shows current location and time
2. Add combat-specific HUD elements
3. Implement inventory quick-access
4. Include notification system for events

ui/inventory_screen.py
Design the inventory interface:
1. Implement an InventoryScreen class that:
   - Displays player inventory in a grid or list
   - Shows item details on selection
   - Allows using, equipping, dropping items
   - Provides sorting and filtering options
2. Add equipment comparison tooltips
3. Implement drag-and-drop functionality
4. Include character paper-doll display for equipment

ui/shop_screen.py
Create the merchant interface:
1. Implement a ShopScreen class that:
   - Displays merchant inventory and player inventory
   - Shows prices for buying and selling
   - Handles transactions and currency
   - Allows haggling based on reputation
2. Add special deals and discounts
3. Implement shop inventory refresh mechanics
4. Include selling price calculation based on item condition

ui/dialog_system.py
Design the NPC conversation system:
1. Implement a DialogSystem class that:
   - Displays NPC dialogs with portrait
   - Shows conversation options for player
   - Tracks dialog history
   - Triggers quest-related dialog
2. Add support for conditionally available dialog options
3. Implement reputation influence on dialog choices
4. Include animated portraits (optional)

Utility Files
utils/math_utils.py
Create mathematical utility functions:
1. Implement grid-specific functions:
   - Path finding (A* algorithm)
   - Line of sight calculations
   - Distance calculations (Manhattan, Euclidean, hex)
   - Collision detection helpers
2. Add general math utilities:
   - Vector operations
   - Angle calculations
   - Interpolation functions
3. Implement grid conversion functions (hex<->screen coordinates)
4. Add probability and distribution functions

utils/random_generator.py
Design procedural generation utilities:
1. Implement a RandomGenerator class with:
   - Seeded random number generation
   - Noise functions (Perlin, Simplex)
   - Weighted random selection
   - Probability tables
2. Add name generation for NPCs and locations
3. Implement loot table system with rarities
4. Include dungeon layout generation algorithms
5. Add biome and terrain generation functions

utils/save_system.py
Create the game saving/loading system:
1. Implement a SaveSystem class that:
   - Serializes game state to JSON or binary format
   - Loads saved games and restores state
   - Manages multiple save slots
   - Handles save corruption detection
2. Add save versioning for compatibility
3. Implement auto-save functionality
4. Include save metadata (play time, level, location)

Audio System
audio/sound_manager.py
Design the audio management system:
1. Implement a SoundManager class that:
   - Plays sound effects and background music
   - Handles volume control and muting
   - Manages audio channels for layering sounds
   - Supports fading between tracks
2. Add positional audio for sound effects
3. Implement adaptive music system based on game state
4. Include audio settings persistence
5. Add support for random ambient sounds

Data Files
data/items.json
Define the structure for item data:
1. Create a comprehensive JSON schema for items:
   - Weapons with damage, range, special properties
   - Armor with defense values and resistances
   - Consumables with effects and durations
   - Quest items with descriptions
2. Include rarities, value, and weight
3. Add crafting material categories
4. Define upgrade paths and enchantments

data/enemies.json
Define the structure for enemy data:
1. Create a JSON schema for enemies:
   - Base stats (health, damage, defense)
   - Attack patterns and special abilities
   - Loot tables and drop rates
   - Behavior types and AI patterns
2. Include faction relationships
3. Add spawn conditions and locations
4. Define difficulty scaling by player level

data/quests.json
Define the structure for quest data:
1. Create a JSON schema for quests:
   - Objectives and completion criteria
   - Rewards (gold, XP, items)
   - Related NPCs and dialog
   - Quest chain relationships
2. Include time-limited quest templates
3. Add faction-specific quests
4. Define branching quest structures

data/dialog.json
Define the structure for dialog data:
1. Create a JSON schema for NPC dialogs:
   - Conversation trees with responses
   - Conditional dialog based on player choices/state
   - Quest-related dialog triggers
   - NPC personality traits affecting speech
2. Include reputation-influenced dialog
3. Add special event dialog
4. Define shopkeeper bargaining dialog
