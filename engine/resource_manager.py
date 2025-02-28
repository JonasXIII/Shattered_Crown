"""
Resource Manager Module
Handles asset loading, caching, and management
"""

import os
import pygame
import logging
from typing import Dict, Tuple, List, Any, Optional
from pathlib import Path
from constants import ASSET_PATHS  # Assuming defined in constants.py

# Type aliases
Surface = pygame.Surface
Sound = pygame.mixer.Sound
Font = pygame.font.Font

class ResourceManager:
    """
    Singleton class managing game resources with caching and error handling
    Implements resource loading and management patterns from interface specs
    """
    
    _instance: Optional['ResourceManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize caches
        self._image_cache: Dict[str, Surface] = {}
        self._sound_cache: Dict[str, Sound] = {}
        self._font_cache: Dict[Tuple[str, int], Font] = {}  # (path, size) as key
        self._data_cache: Dict[str, Any] = {}
        self._spritesheets: Dict[str, List[Surface]] = {}
        self._animations: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default assets
        self._missing_image = pygame.Surface((32, 32))
        self._missing_image.fill((255, 0, 255))  # Magenta error color
        
        self._initialized = True
        logging.info("Resource Manager initialized")

    # Image handling ----------------------------------------------------------
    def load_image(self, resource_id: str, scale: int = 1) -> Surface:
        """
        Load and cache an image resource with optional scaling
        Returns placeholder image if resource not found
        """
        if resource_id in self._image_cache:
            return self._image_cache[resource_id]
            
        path = self._get_resource_path('images', resource_id)
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale != 1:
                size = (image.get_width() * scale, 
                        image.get_height() * scale)
                image = pygame.transform.scale(image, size)
            self._image_cache[resource_id] = image
            return image
        except (FileNotFoundError, pygame.error) as e:
            logging.error(f"Image load failed: {resource_id} - {str(e)}")
            return self._missing_image

    def load_spritesheet(self, resource_id: str, 
                        frame_size: Tuple[int, int],
                        scale: int = 1) -> List[Surface]:
        """
        Load and parse a spritesheet into individual frames
        """
        cache_key = f"{resource_id}_{frame_size[0]}x{frame_size[1]}"
        if cache_key in self._spritesheets:
            return self._spritesheets[cache_key]
            
        sheet = self.load_image(resource_id, scale)
        if sheet == self._missing_image:
            return [self._missing_image]
            
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        cols = sheet_width // frame_size[0]
        rows = sheet_height // frame_size[1]
        
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(
                    x * frame_size[0],
                    y * frame_size[1],
                    frame_size[0],
                    frame_size[1]
                )
                frames.append(sheet.subsurface(rect))
                
        self._spritesheets[cache_key] = frames
        return frames

    # Audio handling ----------------------------------------------------------
    def load_sound(self, resource_id: str) -> Sound:
        """Load and cache a sound resource"""
        if resource_id in self._sound_cache:
            return self._sound_cache[resource_id]
            
        path = self._get_resource_path('sounds', resource_id)
        try:
            sound = pygame.mixer.Sound(path)
            self._sound_cache[resource_id] = sound
            return sound
        except (FileNotFoundError, pygame.error) as e:
            logging.error(f"Sound load failed: {resource_id} - {str(e)}")
            return pygame.mixer.Sound(b''))  # Silent placeholder

    # Font handling -----------------------------------------------------------
    def load_font(self, resource_id: str, size: int = 24) -> Font:
        """Load and cache a font resource with specific size"""
        cache_key = (resource_id, size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
            
        path = self._get_resource_path('fonts', resource_id)
        try:
            font = pygame.font.Font(path, size)
            self._font_cache[cache_key] = font
            return font
        except (FileNotFoundError, pygame.error) as e:
            logging.error(f"Font load failed: {resource_id} - {str(e)}")
            return pygame.font.SysFont('Arial', size)

    # Data file handling ------------------------------------------------------
    def load_data(self, resource_id: str) -> Any:
        """
        Load and cache game data files (JSON, etc.)
        Actual parsing should be handled by other systems
        """
        if resource_id in self._data_cache:
            return self._data_cache[resource_id]
            
        path = self._get_resource_path('data', resource_id)
        try:
            with open(path, 'r') as f:
                data = f.read()
                self._data_cache[resource_id] = data
                return data
        except IOError as e:
            logging.error(f"Data load failed: {resource_id} - {str(e)}")
            return None

    # Utility methods ---------------------------------------------------------
    def _get_resource_path(self, asset_type: str, resource_id: str) -> str:
        """
        Construct full path from constants.ASSET_PATHS
        Raises FileNotFoundError if path not configured
        """
        base_path = ASSET_PATHS.get(asset_type)
        if not base_path:
            raise FileNotFoundError(
                f"Asset type {asset_type} not configured in constants")
                
        return str(Path(base_path) / resource_id)

    def clear_cache(self, resource_type: str = None):
        """
        Clear specified cache or all caches
        Valid types: 'images', 'sounds', 'fonts', 'data', 'all'
        """
        if resource_type == 'images' or resource_type == 'all':
            self._image_cache.clear()
        if resource_type == 'sounds' or resource_type == 'all':
            self._sound_cache.clear()
        if resource_type == 'fonts' or resource_type == 'all':
            self._font_cache.clear()
        if resource_type == 'data' or resource_type == 'all':
            self._data_cache.clear()

    # Animation handling ------------------------------------------------------
    def register_animation(self, anim_id: str, frames: List[Surface], 
                          frame_durations: List[int]):
        """
        Register animation sequence with timing data
        Durations in milliseconds
        """
        self._animations[anim_id] = {
            'frames': frames,
            'durations': frame_durations,
            'total_frames': len(frames)
        }

    def get_animation(self, anim_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve registered animation data"""
        return self._animations.get(anim_id)

if __name__ == '__main__':
    # Test implementation
    pygame.init()
    rm = ResourceManager()
    test_image = rm.load_image('player/idle.png')
    print(f"Loaded image size: {test_image.get_size()}")