# Chronicles of the Shattered Crown - Coding Style Guide

## Naming Conventions
- Classes: PascalCase (e.g., PlayerCharacter, CombatManager)
- Methods/Functions: snake_case (e.g., calculate_damage, get_player_position)
- Variables: snake_case (e.g., player_health, current_map)
- Constants: UPPER_SNAKE_CASE (e.g., MAX_HEALTH, SCREEN_WIDTH)
- Private methods/attributes: _prefixed_with_underscore (e.g., _internal_method)

## Common Variable Names
- player: The main player entity
- current_state: The active game state
- game_map: The current map instance
- screen: The PyGame display surface
- delta_time: Time since last frame update

## Interface Patterns
- All entity updates take delta_time as parameter
- Event handlers return True if they consumed the event
- Resource loading uses resource_id strings
- State transitions use explicit enter/exit methods

## Import Order
1. Standard library imports
2. Third-party library imports
3. Local application imports (sorted by path)

## File Structure
- Maximum line length: 79 characters
- Docstrings for all classes and public methods
- Type hints for function parameters and return values


