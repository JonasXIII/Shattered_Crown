"""
Map System Module
Handles game map grid, pathfinding, collisions, and fog of war
"""

import logging
from typing import Dict, List, Tuple, Optional, Set
import utils.math_utils as math_utils
from entities.entity import Entity
from world.tile import Tile
from engine.camera import Camera

class Map:
    """
    Represents a game map grid with tiles, entities, and exploration state
    Implements core spatial and navigation functionality
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = []
        self.entities: Dict[Tuple[int, int], Entity] = {}
        self.fog_of_war: List[List[bool]] = []
        self.revealed_tiles: Set[Tuple[int, int]] = set()
        
        # Initialize empty grid
        for y in range(height):
            row = []
            fog_row = []
            for x in range(width):
                row.append(Tile('empty', blocking=False))
                fog_row.append(False)
            self.grid.append(row)
            self.fog_of_war.append(fog_row)
        
        logging.info(f"Created map {width}x{height}")

    # Tile Management ---------------------------------------------------------
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get tile at coordinates if within bounds"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def set_tile(self, x: int, y: int, tile: Tile) -> bool:
        """Set tile type at coordinates if valid"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile
            return True
        return False

    # Entity Management -------------------------------------------------------
    def place_entity(self, entity: Entity, x: int, y: int) -> bool:
        """Place entity at coordinates if position is valid and unoccupied"""
        if not self.is_blocked(x, y):
            self.remove_entity(entity)
            self.entities[(x, y)] = entity
            entity.set_position(x, y)
            return True
        return False

    def remove_entity(self, entity: Entity) -> bool:
        """Remove entity from map"""
        pos = entity.get_position()
        if pos in self.entities:
            del self.entities[pos]
            return True
        return False

    def get_entity_at(self, x: int, y: int) -> Optional[Entity]:
        """Get entity at coordinates if present"""
        return self.entities.get((x, y))

    # Collision Detection -----------------------------------------------------
    def is_blocked(self, x: int, y: int) -> bool:
        """Check if a position is blocked by terrain or entity"""
        tile = self.get_tile(x, y)
        if tile and tile.blocking:
            return True
        return (x, y) in self.entities

    # Pathfinding -------------------------------------------------------------
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find path between two points using A* algorithm
        Returns empty list if no path exists
        """
        def passable(x, y):
            return not self.is_blocked(x, y)
            
        return math_utils.a_star(
            start, 
            end, 
            passable,
            self.get_neighbors
        )

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring coordinates"""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors

    # Fog of War --------------------------------------------------------------
    def update_fog_of_war(self, viewer_pos: Tuple[int, int], radius: int = 5):
        """Update revealed tiles based on viewer position and line of sight"""
        self.revealed_tiles.add(viewer_pos)
        self.fog_of_war[viewer_pos[1]][viewer_pos[0]] = True
        
        # Reveal tiles in vision radius with line of sight
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                x = viewer_pos[0] + dx
                y = viewer_pos[1] + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if math_utils.has_line_of_sight(viewer_pos, (x, y), self.grid):
                        self.revealed_tiles.add((x, y))
                        self.fog_of_war[y][x] = True

    # Rendering ---------------------------------------------------------------
    def render(self, screen: pygame.Surface, camera: Camera):
        """Render visible portion of map through camera viewport"""
        for y in range(self.height):
            for x in range(self.width):
                # Get screen coordinates from world coordinates
                screen_pos = camera.world_to_screen((x * Tile.SIZE, y * Tile.SIZE))
                
                # Only draw tiles within camera view
                if camera.is_visible((x, y)):
                    # Apply fog of war shading
                    if (x, y) in self.revealed_tiles:
                        alpha = 128 if not self.fog_of_war[y][x] else 0
                    else:
                        alpha = 255
                        
                    # Draw tile and any entities
                    self.grid[y][x].render(screen, screen_pos, alpha)
                    if (x, y) in self.entities:
                        self.entities[(x, y)].render(screen, camera)

    # Save/Load ---------------------------------------------------------------
    def save_state(self) -> Dict:
        """Serialize map state for saving"""
        return {
            'width': self.width,
            'height': self.height,
            'grid': [[tile.serialize() for tile in row] for row in self.grid],
            'revealed_tiles': list(self.revealed_tiles)
        }

    def load_state(self, data: Dict):
        """Load map state from serialized data"""
        self.width = data['width']
        self.height = data['height']
        self.revealed_tiles = set(tuple(pos) for pos in data['revealed_tiles'])
        
        # Rebuild grid
        self.grid = []
        for y, row in enumerate(data['grid']):
            new_row = []
            for x, tile_data in enumerate(row):
                tile = Tile.deserialize(tile_data)
                new_row.append(tile)
                # Update fog of war based on revealed tiles
                self.fog_of_war[y][x] = (x, y) in self.revealed_tiles
            self.grid.append(new_row)

    # Utility Methods ---------------------------------------------------------
    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within map bounds"""
        return 0 <= x < self.width and 0 <= y < self.height