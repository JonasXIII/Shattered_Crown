"""
Chronicles of the Shattered Crown - Camera System

This module implements a camera system for managing the viewport and 
handling coordinate transformations between world and screen space.
"""
import math
import random
from typing import Tuple, Optional
import logging
import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Camera:
    """
    Camera system that controls the viewport into the game world.
    
    The camera handles:
    - Tracking entity positions
    - Converting between world and screen coordinates
    - Camera effects like shaking and smooth movement
    - Zoom functionality
    """
    
    def __init__(
        self, 
        world_width: int, 
        world_height: int,
        viewport_width: int = SCREEN_WIDTH,
        viewport_height: int = SCREEN_HEIGHT
    ) -> None:
        """
        Initialize the camera with world boundaries.
        
        Args:
            world_width: The width of the world in pixels
            world_height: The height of the world in pixels
            viewport_width: The width of the viewport in pixels
            viewport_height: The height of the viewport in pixels
        """
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        
        # Camera position in world coordinates (top-left corner)
        self.x = 0
        self.y = 0
        
        # Target position for smooth movement
        self._target_x = 0
        self._target_y = 0
        
        # Camera effects
        self._shake_duration = 0
        self._shake_intensity = 0
        self._shake_offset_x = 0
        self._shake_offset_y = 0
        
        # Zoom level (1.0 = normal, 0.5 = zoomed out, 2.0 = zoomed in)
        self._zoom = 1.0
        self._target_zoom = 1.0
        
        self.logger = logging.getLogger("Camera")
    
    @property
    def center(self) -> Tuple[float, float]:
        """
        Get the center position of the camera in world coordinates.
        
        Returns:
            A tuple of (x, y) coordinates
        """
        return (
            self.x + (self.viewport_width / 2 / self._zoom),
            self.y + (self.viewport_height / 2 / self._zoom)
        )
    
    @property
    def zoom(self) -> float:
        """
        Get the current zoom level.
        
        Returns:
            Current zoom level (1.0 = normal)
        """
        return self._zoom
    
    def set_zoom(self, zoom: float, smooth: bool = True) -> None:
        """
        Set the camera zoom level.
        
        Args:
            zoom: The zoom level to set (1.0 = normal)
            smooth: Whether to transition smoothly to the new zoom
        """
        # Clamp zoom to reasonable values
        zoom = max(0.25, min(zoom, 4.0))
        
        if smooth:
            self._target_zoom = zoom
        else:
            self._zoom = zoom
            self._target_zoom = zoom
        
        self.logger.debug(f"Camera zoom set to {zoom}")
    
    def move_to(self, x: float, y: float, smooth: bool = True) -> None:
        """
        Move the camera to a specific position in world coordinates.
        
        Args:
            x: X coordinate in world space
            y: Y coordinate in world space
            smooth: Whether to move smoothly to the new position
        """
        if smooth:
            self._target_x = x - (self.viewport_width / 2 / self._zoom)
            self._target_y = y - (self.viewport_height / 2 / self._zoom)
        else:
            self.x = x - (self.viewport_width / 2 / self._zoom)
            self.y = y - (self.viewport_height / 2 / self._zoom)
            self._target_x = self.x
            self._target_y = self.y
        
        # Ensure the camera stays within the world bounds
        self._clamp_position()
    
    def center_on_entity(self, entity, smooth: bool = True) -> None:
        """
        Center the camera on an entity.
        
        Args:
            entity: The entity to center on (must have get_position method)
            smooth: Whether to move smoothly to the new position
        """
        x, y = entity.get_position()
        self.move_to(x, y, smooth)
    
    def shake(self, duration: float, intensity: float) -> None:
        """
        Start a camera shake effect.
        
        Args:
            duration: How long the shake should last in seconds
            intensity: How strong the shake should be (in pixels)
        """
        self._shake_duration = duration
        self._shake_intensity = intensity
        self.logger.debug(f"Camera shake started: {duration}s at {intensity} intensity")
    
    def update(self, delta_time: float) -> None:
        """
        Update the camera position and effects.
        
        Args:
            delta_time: Time elapsed since the last update in seconds
        """
        # Update smooth camera movement
        self._update_smooth_movement(delta_time)
        
        # Update camera shake
        self._update_shake(delta_time)
        
        # Ensure the camera stays within the world bounds
        self._clamp_position()
    
    def _update_smooth_movement(self, delta_time: float) -> None:
        """
        Update smooth camera movement towards target position.
        
        Args:
            delta_time: Time elapsed since the last update in seconds
        """
        # Smoothly move towards target position
        lerp_factor = 1.0 - math.pow(0.1, delta_time)
        
        self.x = self.x + (self._target_x - self.x) * lerp_factor
        self.y = self.y + (self._target_y - self.y) * lerp_factor
        
        # Smoothly transition zoom
        self._zoom = self._zoom + (self._target_zoom - self._zoom) * lerp_factor
    
    def _update_shake(self, delta_time: float) -> None:
        """
        Update camera shake effect.
        
        Args:
            delta_time: Time elapsed since the last update in seconds
        """
        if self._shake_duration > 0:
            self._shake_duration -= delta_time
            
            # Calculate shake offset
            intensity = self._shake_intensity
            if self._shake_duration < 0.5:
                # Fade out shake during the last 0.5 seconds
                intensity *= (self._shake_duration / 0.5)
            
            self._shake_offset_x = random.uniform(-intensity, intensity)
            self._shake_offset_y = random.uniform(-intensity, intensity)
            
            if self._shake_duration <= 0:
                # End shake
                self._shake_duration = 0
                self._shake_offset_x = 0
                self._shake_offset_y = 0
    
    def _clamp_position(self) -> None:
        """Ensure the camera stays within the world boundaries."""
        # Calculate the effective viewport dimensions based on zoom
        effective_viewport_width = self.viewport_width / self._zoom
        effective_viewport_height = self.viewport_height / self._zoom
        
        # Clamp target position
        self._target_x = max(0, min(self._target_x, self.world_width - effective_viewport_width))
        self._target_y = max(0, min(self._target_y, self.world_height - effective_viewport_height))
        
        # Clamp current position
        self.x = max(0, min(self.x, self.world_width - effective_viewport_width))
        self.y = max(0, min(self.y, self.world_height - effective_viewport_height))
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            world_x: X coordinate in world space
            world_y: Y coordinate in world space
            
        Returns:
            A tuple of (x, y) screen coordinates
        """
        # Apply camera offset, zoom, and shake
        screen_x = (world_x - self.x) * self._zoom + self._shake_offset_x
        screen_y = (world_y - self.y) * self._zoom + self._shake_offset_y
        
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.
        
        Args:
            screen_x: X coordinate in screen space
            screen_y: Y coordinate in screen space
            
        Returns:
            A tuple of (x, y) world coordinates
        """
        # Apply inverse camera offset and zoom
        world_x = (screen_x - self._shake_offset_x) / self._zoom + self.x
        world_y = (screen_y - self._shake_offset_y) / self._zoom + self.y
        
        return (world_x, world_y)
    
    def is_visible(self, world_x: float, world_y: float, width: float, height: float) -> bool:
        """
        Check if a rectangle in world space is visible in the camera view.
        
        Args:
            world_x: X coordinate of the rectangle in world space
            world_y: Y coordinate of the rectangle in world space
            width: Width of the rectangle in world space
            height: Height of the rectangle in world space
            
        Returns:
            True if the rectangle is at least partially visible
        """
        # Calculate the effective viewport boundaries
        view_left = self.x - (width * 0.5)  # Add a small buffer
        view_right = self.x + (self.viewport_width / self._zoom) + (width * 0.5)
        view_top = self.y - (height * 0.5)
        view_bottom = self.y + (self.viewport_height / self._zoom) + (height * 0.5)
        
        # Check if the rectangle is outside the view
        if (world_x + width < view_left or
            world_x > view_right or
            world_y + height < view_top or
            world_y > view_bottom):
            return False
        
        return True
    
    def world_to_grid(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """
        Convert world coordinates to grid coordinates.
        
        Args:
            world_x: X coordinate in world space
            world_y: Y coordinate in world space
            
        Returns:
            A tuple of (grid_x, grid_y) coordinates
        """
        grid_x = int(world_x / TILE_SIZE)
        grid_y = int(world_y / TILE_SIZE)
        return (grid_x, grid_y)
    
    def grid_to_world(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """
        Convert grid coordinates to world coordinates (center of the tile).
        
        Args:
            grid_x: X coordinate in grid space
            grid_y: Y coordinate in grid space
            
        Returns:
            A tuple of (world_x, world_y) coordinates (center of the tile)
        """
        world_x = grid_x * TILE_SIZE + (TILE_SIZE / 2)
        world_y = grid_y * TILE_SIZE + (TILE_SIZE / 2)
        return (world_x, world_y)
    
    def get_visible_grid_bounds(self) -> Tuple[int, int, int, int]:
        """
        Get the grid coordinates that are currently visible.
        
        Returns:
            A tuple of (min_x, min_y, max_x, max_y) grid coordinates
        """
        min_x = int(self.x / TILE_SIZE)
        min_y = int(self.y / TILE_SIZE)
        max_x = int((self.x + self.viewport_width / self._zoom) / TILE_SIZE) + 1
        max_y = int((self.y + self.viewport_height / self._zoom) / TILE_SIZE) + 1
        
        return (min_x, min_y, max_x, max_y)
    
    def reset(self) -> None:
        """Reset the camera to its default state."""
        self.x = 0
        self.y = 0
        self._target_x = 0
        self._target_y = 0
        self._zoom = 1.0
        self._target_zoom = 1.0
        self._shake_duration = 0
        self._shake_intensity = 0
        self._shake_offset_x = 0
        self._shake_offset_y = 0
        self.logger.debug("Camera reset to default state")