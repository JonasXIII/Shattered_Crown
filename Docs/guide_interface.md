# Chronicles of the Shattered Crown - Interface Specifications

## Events System
Events should follow this structure:
{
    "type": "EVENT_TYPE",
    "source": source_entity,
    "target": target_entity,
    "data": {additional data}
}

## Entity Base Class
All entities must implement:
- update(delta_time)
- render(surface, camera)
- get_position()
- set_position(x, y)

## Grid Coordinates
- Position is stored as (x, y) tuples
- Grid coordinates start at (0, 0) in top-left
- Movement directions: NORTH, SOUTH, EAST, WEST (or hex equivalents)

## Common Data Structures
- Inventory items: {"id": "item_id", "count": quantity, "quality": 0-100}
- Stats: {"strength": value, "dexterity": value, "intelligence": value}
- Combat actions: {"name": "action_name", "ap_cost": value, "target_type": "single/area"}

## Resource Manager Interface

### Resource Types
- Images: Load with `load_image(resource_id: str) -> pygame.Surface`
- Sounds: Load with `load_sound(resource_id: str) -> pygame.mixer.Sound`
- Fonts: Load with `load_font(resource_id: str, size: int) -> pygame.font.Font`
- Data: Load raw data with `load_data(resource_id: str) -> str`

### Animation Registration
Animations are registered using:
{
    "anim_id": "unique_animation_name",
    "frames": [Surface1, Surface2, ...],
    "durations": [frame_time_ms, ...]
}

## Map System Interface

### Core Methods
- `get_tile(x, y) -> Tile`: Get tile at coordinates
- `place_entity(entity, x, y) -> bool`: Add entity to map
- `find_path(start, end) -> path`: Calculate path using A*
- `update_fog_of_war(viewer_pos, radius)`: Update visibility

### Tile Properties
- `type`: Tile type identifier (string)
- `blocking`: Blocks movement (bool)
- `render(surface, pos, alpha)`: Draw tile with optional transparency

### Coordinate Systems
- World coordinates: Grid-based (x, y) pairs
- Screen coordinates: Pixel positions handled by Camera

## Tile System Interface

### Tile Properties
- `tile_type`: String identifier (e.g., "grass", "water")
- `blocking`: Blocks movement/vision when True
- `movement_cost`: AP required to enter tile
- `effects`: Dictionary of status effects applied on entry

### Core Methods
- `update(delta_time)`: Handle animation progression
- `render(surface, position)`: Draw tile at screen coordinates
- `serialize()/deserialize()`: Save/load tile configuration

