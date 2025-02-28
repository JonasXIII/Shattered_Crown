"""
Chronicles of the Shattered Crown - Game State Management

This module defines the game state system, including the state manager
and base state class for creating different game states.
"""
from enum import Enum, auto
from typing import Dict, List, Optional, Any
import logging
import pygame


class GameState(Enum):
    """Enumeration of all possible game states."""
    TITLE = auto()
    OVERWORLD = auto()
    LOCAL_AREA = auto()
    COMBAT = auto()
    INVENTORY = auto()
    DIALOG = auto()
    SHOP = auto()
    QUEST_LOG = auto()
    PAUSE = auto()
    OPTIONS = auto()
    GAME_OVER = auto()
    CHARACTER_CREATION = auto()


class State:
    """
    Abstract base class for all game states.
    
    Each state represents a discrete mode of gameplay, such as the title screen,
    overworld map, or combat encounter.
    """
    
    def __init__(self, state_manager: 'StateManager') -> None:
        """
        Initialize the state.
        
        Args:
            state_manager: Reference to the state manager for state transitions
        """
        self.state_manager = state_manager
        self.logger = logging.getLogger(f"state.{self.__class__.__name__}")
    
    def enter(self, **kwargs: Any) -> None:
        """
        Called when this state becomes active.
        
        Args:
            **kwargs: Optional arguments passed from the previous state
        """
        self.logger.debug("Entering state")
    
    def exit(self) -> Dict[str, Any]:
        """
        Called when this state is being exited.
        
        Returns:
            A dictionary of data to pass to the next state
        """
        self.logger.debug("Exiting state")
        return {}
    
    def pause(self) -> None:
        """Called when this state is paused (e.g., when opening a menu)."""
        self.logger.debug("State paused")
    
    def resume(self) -> None:
        """Called when this state is resumed after being paused."""
        self.logger.debug("State resumed")
    
    def update(self, delta_time: float) -> None:
        """
        Update the state logic.
        
        Args:
            delta_time: Time elapsed since the last update in seconds
        """
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the state to the provided surface.
        
        Args:
            surface: The surface to render to (usually the screen)
        """
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Process an input event.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            True if the event was consumed, False otherwise
        """
        return False


class StateManager:
    """
    Manages game states and transitions between them.
    
    The StateManager maintains a stack of states, allowing for hierarchical state
    management (e.g., opening inventory while in the overworld).
    """
    
    def __init__(self) -> None:
        """Initialize the state manager."""
        self.states: Dict[GameState, State] = {}
        self.state_stack: List[GameState] = []
        self.active_state: Optional[State] = None
        self.pending_state_change: Optional[GameState] = None
        self.pending_state_args: Dict[str, Any] = {}
        self.logger = logging.getLogger("StateManager")
    
    def register_state(self, state_type: GameState, state_instance: State) -> None:
        """
        Register a state instance with the manager.
        
        Args:
            state_type: The enum value representing the state type
            state_instance: The instantiated state object
        """
        self.states[state_type] = state_instance
        self.logger.debug(f"Registered state: {state_type.name}")
    
    def get_current_state(self) -> Optional[GameState]:
        """
        Get the current active state type.
        
        Returns:
            The current GameState enum value, or None if no state is active
        """
        if not self.state_stack:
            return None
        return self.state_stack[-1]
    
    def request_state_change(self, new_state: GameState, **kwargs: Any) -> None:
        """
        Request a change to a new state.
        
        The state change will be applied on the next update cycle to avoid
        issues with changing state mid-update or mid-render.
        
        Args:
            new_state: The GameState to transition to
            **kwargs: Arguments to pass to the new state's enter method
        """
        self.pending_state_change = new_state
        self.pending_state_args = kwargs
        self.logger.debug(f"State change requested: {new_state.name}")
    
    def change_state(self, new_state: GameState, **kwargs: Any) -> None:
        """
        Immediately change to a new state.
        
        Args:
            new_state: The GameState to transition to
            **kwargs: Arguments to pass to the new state's enter method
        """
        # Exit the current state if there is one
        transition_data = {}
        if self.active_state:
            transition_data = self.active_state.exit()
            self.active_state = None
        
        # Clear the state stack and add the new state
        self.state_stack.clear()
        self.state_stack.append(new_state)
        
        # Activate the new state
        if new_state in self.states:
            self.active_state = self.states[new_state]
            # Combine transition data with explicitly provided kwargs
            # (kwargs take precedence)
            enter_args = {**transition_data, **kwargs}
            self.active_state.enter(**enter_args)
            self.logger.info(f"State changed to: {new_state.name}")
        else:
            self.logger.error(f"State {new_state.name} not registered")
    
    def push_state(self, new_state: GameState, **kwargs: Any) -> None:
        """
        Push a new state onto the stack without removing the current one.
        
        This pauses the current state and activates the new one.
        
        Args:
            new_state: The GameState to push onto the stack
            **kwargs: Arguments to pass to the new state's enter method
        """
        # Pause the current state if there is one
        if self.active_state:
            self.active_state.pause()
        
        # Push the new state onto the stack
        self.state_stack.append(new_state)
        
        # Activate the new state
        if new_state in self.states:
            self.active_state = self.states[new_state]
            self.active_state.enter(**kwargs)
            self.logger.info(f"State pushed: {new_state.name}")
        else:
            self.logger.error(f"State {new_state.name} not registered")
            # Revert the stack change if the state doesn't exist
            self.state_stack.pop()
    
    def pop_state(self) -> None:
        """
        Pop the current state off the stack and resume the previous one.
        
        If there is no previous state, this does nothing.
        """
        if not self.state_stack:
            self.logger.warning("Attempted to pop state with empty stack")
            return
        
        # Exit the current state
        if self.active_state:
            transition_data = self.active_state.exit()
            self.active_state = None
        
        # Remove the current state from the stack
        popped_state = self.state_stack.pop()
        self.logger.info(f"State popped: {popped_state.name}")
        
        # Resume the previous state if there is one
        if self.state_stack:
            prev_state = self.state_stack[-1]
            if prev_state in self.states:
                self.active_state = self.states[prev_state]
                self.active_state.resume()
                self.logger.info(f"Resumed state: {prev_state.name}")
            else:
                self.logger.error(f"State {prev_state.name} not registered")
    
    def update(self, delta_time: float) -> None:
        """
        Update the current active state.
        
        This also processes any pending state changes.
        
        Args:
            delta_time: Time elapsed since the last update in seconds
        """
        # Process any pending state changes
        if self.pending_state_change is not None:
            self.change_state(self.pending_state_change, **self.pending_state_args)
            self.pending_state_change = None
            self.pending_state_args = {}
        
        # Update the active state if there is one
        if self.active_state:
            self.active_state.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the current active state.
        
        Args:
            surface: The surface to render to (usually the screen)
        """
        if self.active_state:
            self.active_state.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Pass an event to the current active state for handling.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            True if the event was consumed, False otherwise
        """
        if self.active_state:
            return self.active_state.handle_event(event)
        return False