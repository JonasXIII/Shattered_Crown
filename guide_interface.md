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