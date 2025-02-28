#!/usr/bin/env python3
"""
Chronicles of the Shattered Crown - Main Entry Point

This is the main entry point for the game that initializes all required
subsystems, manages the game loop, and handles program shutdown.
"""
import sys
import logging
import time
from typing import Optional

import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FULLSCREEN,
    TARGET_FPS,
    DEBUG_MODE,
    GAME_TITLE,
    LOG_LEVEL
)
from engine.game_state import StateManager, GameState
from engine.input_handler import InputHandler
from engine.resource_manager import ResourceManager


def setup_logging() -> None:
    """Configure the logging system for the game."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=LOG_LEVEL,
        format=log_format,
        handlers=[
            logging.FileHandler("game.log"),
            logging.StreamHandler()
        ]
    )


def initialize_pygame() -> pygame.Surface:
    """
    Initialize PyGame and create the game window.
    
    Returns:
        The main screen surface for rendering.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption(GAME_TITLE)
    
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    return screen


def main() -> None:
    """Main entry point for the game."""
    # Setup logging first so we can capture any initialization errors
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Starting Chronicles of the Shattered Crown")
    
    try:
        # Initialize pygame and create window
        screen = initialize_pygame()
        logger.info("PyGame initialized successfully")
        
        # Initialize core game systems
        resource_manager = ResourceManager.get_instance()
        logger.info("Resource Manager initialized")
        
        state_manager = StateManager()
        logger.info("State Manager initialized")
        
        input_handler = InputHandler()
        logger.info("Input Handler initialized")
        
        # Set initial game state
        state_manager.change_state(GameState.TITLE)
        logger.info("Set initial game state to TITLE")
        
        # Create a clock for managing frame rate
        clock = pygame.time.Clock()
        running = True
        
        # Variables for FPS calculation
        fps_counter = 0
        fps_timer = time.time()
        current_fps: Optional[float] = None
        
        # Main game loop
        logger.info("Entering main game loop")
        while running:
            # Calculate delta time in seconds
            delta_time = clock.tick(TARGET_FPS) / 1000.0
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                # Let the input handler process the event
                input_handler.process_event(event)
                
                # Let the current state handle the event
                consumed = state_manager.handle_event(event)
                if not consumed and event.type == pygame.KEYDOWN:
                    # Global key handlers for events not handled by current state
                    if event.key == pygame.K_ESCAPE:
                        if state_manager.get_current_state() == GameState.TITLE:
                            running = False
                        else:
                            # For other states, attempt to return to the previous state
                            # or open pause menu
                            state_manager.request_state_change(GameState.PAUSE)
            
            # Update game state
            input_handler.update()
            state_manager.update(delta_time)
            
            # Render current state
            screen.fill((0, 0, 0))  # Clear screen
            state_manager.render(screen)
            
            # Display debug information if enabled
            if DEBUG_MODE:
                # Calculate and display FPS
                fps_counter += 1
                if time.time() - fps_timer > 1.0:
                    current_fps = fps_counter / (time.time() - fps_timer)
                    fps_counter = 0
                    fps_timer = time.time()
                
                if current_fps is not None:
                    fps_text = f"FPS: {current_fps:.1f}"
                    font = resource_manager.get_font("debug", 16)
                    fps_surface = font.render(fps_text, True, (255, 255, 255))
                    screen.blit(fps_surface, (10, 10))
            
            # Flip the display
            pygame.display.flip()
        
        logger.info("Main game loop exited")
    
    except Exception as e:
        logger.exception(f"Unhandled exception in main loop: {e}")
        raise
    
    finally:
        # Clean shutdown
        logger.info("Performing clean shutdown")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()