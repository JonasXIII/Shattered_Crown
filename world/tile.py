"""
Tile System Module
Defines tile types and properties for grid-based maps
"""

import pygame
from typing import Dict, Any, List, Optional, Tuple
from constants import TILE_SIZE, GROUND_COLOR, DEBUG_MODE

class Tile:
    """
    Represents a single grid tile with properties and visual representation
    Implements serialization and animation handling
    """
    
    SIZE = TILE_SIZE  # Defined in constants.py
    
    def __init__(
        self,
        tile_type: str = "empty",
        blocking: bool = False,
        movement_cost: int = 1,
        effects: Optional[Dict[str, Any]] = None,
        base_sprite: Optional[pygame.Surface] = None,
        animation_frames: Optional[List[pygame.Surface]] = None,
        frame_duration: int = 100
    ):
        self.tile_type = tile_type
        self.blocking = blocking
        self.movement_cost = movement_cost
        self.effects = effects or {}
        self.animation_frames = animation_frames or []
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.animated = len(self.animation_frames) > 0
        
        # Default sprite handling
        self.base_sprite = base_sprite if base_sprite else self._create_default_sprite()
        
        # Debug visualization
        if DEBUG_MODE and not base_sprite:
            self._add_debug_overlay()

    def _create_default_sprite(self) -> pygame.Surface:
        """Create fallback sprite with color from constants"""
        surf = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        surf.fill(GROUND_COLOR)
        return surf

    def _add_debug_overlay(self):
        """Add debug information to sprite"""
        if self.blocking:
            pygame.draw.rect(self.base_sprite, (255, 0, 0), (0, 0, self.SIZE, self.SIZE), 1)
        if self.movement_cost > 1:
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.movement_cost), True, (255, 255, 255))
            self.base_sprite.blit(text, (2, 2))

    def update(self, delta_time: float):
        """Update animation progress"""
        if self.animated:
            self.elapsed_time += delta_time
            if self.elapsed_time >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.elapsed_time = 0.0

    def render(self, surface: pygame.Surface, position: Tuple[int, int], alpha: int = 255):
        """Draw tile to target surface with optional transparency"""
        current_sprite = self.get_current_sprite()
        current_sprite.set_alpha(alpha)
        surface.blit(current_sprite, position)

    def get_current_sprite(self) -> pygame.Surface:
        """Get active sprite considering animation"""
        return self.animation_frames[self.current_frame] if self.animated else self.base_sprite

    def is_adjacent(self, other_pos: Tuple[int, int], origin: Tuple[int, int]) -> bool:
        """Check if two positions are adjacent (orthogonal)"""
        dx = abs(other_pos[0] - origin[0])
        dy = abs(other_pos[1] - origin[1])
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def serialize(self) -> Dict[str, Any]:
        """Convert tile data to save-friendly format"""
        return {
            "tile_type": self.tile_type,
            "blocking": self.blocking,
            "movement_cost": self.movement_cost,
            "effects": self.effects,
            "frame_duration": self.frame_duration
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Tile':
        """Reconstruct tile from serialized data"""
        return cls(
            tile_type=data["tile_type"],
            blocking=data["blocking"],
            movement_cost=data.get("movement_cost", 1),
            effects=data.get("effects", {}),
            frame_duration=data.get("frame_duration", 100)
        )